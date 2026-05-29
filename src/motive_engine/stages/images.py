"""Images stage: generate background plates via a local ComfyUI server.

Closes the loop between `motive make-image-prompt` (which emits text) and the
asset library `resolve_assets()` reads from. POSTs the workflow template to a
local ComfyUI HTTP API, polls `/history/<prompt_id>` until the prompt completes,
downloads the PNG via `/view`, and writes it atomically to
``assets/backgrounds/<world>/<background_prompt_key>.png``.

Idempotent by design: if the target file already exists, the function returns
a `GeneratedImage(skipped=True)` without touching the network. Pass `force=True`
to regenerate.

This stage is **backgrounds only** for v1. Figures with a named prompt key
(`figure_prompt_key != "none"`) still need to be supplied manually until the
v2 figure-template work lands.

See config/COMFYUI_README.md for setup steps.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import httpx
from rich.console import Console

from motive_engine.schemas import ComfyUIProfile, ContentSpec
from motive_engine.stages.visual_prompts import (
    DEFAULT_WORLDS_PATH,
    build_image_prompt,
)
from motive_engine.utils import load_yaml

DEFAULT_ASSETS_ROOT = Path("assets")
DEFAULT_COMFYUI_CONFIG_PATH = Path("config") / "comfyui.yaml"
DEFAULT_WORKFLOW_PATH = Path("config") / "comfyui_workflow.json"
DEFAULT_KIND: Literal["background"] = "background"

# Tokens substituted in the workflow JSON before parsing.
STRING_TOKENS = ("__POSITIVE__", "__NEGATIVE__", "__FILENAME_PREFIX__")
NUMERIC_TOKENS = ("__SEED__", "__WIDTH__", "__HEIGHT__")
ALL_TOKENS = STRING_TOKENS + NUMERIC_TOKENS

_console = Console(stderr=True)


# ---- types -----------------------------------------------------------------


@dataclass(frozen=True)
class GeneratedImage:
    """Result of a generate_image() call."""

    kind: Literal["background"]
    key: str
    world: str
    output_path: Path
    seed: int
    skipped: bool


class ComfyUIError(RuntimeError):
    """Anything went wrong talking to ComfyUI or rendering its response."""


class ComfyUITimeout(ComfyUIError):
    """The /history polling loop exceeded the profile's timeout."""


class ComfyUIUnreachable(ComfyUIError):
    """We could not reach the ComfyUI server (connect/DNS/refused)."""


# ---- public API ------------------------------------------------------------


def deterministic_seed(spec_id: str, kind: str, key: str) -> int:
    """Stable int32 seed derived from spec.id|kind|key.

    Same inputs always return the same seed, so regenerating an existing
    asset reproduces the original image (assuming the same model + workflow).
    """
    h = hashlib.sha256(f"{spec_id}|{kind}|{key}".encode()).hexdigest()
    return int(h[:15], 16) % (2**31)


def load_profile(config_path: Path, profile_name: str | None) -> ComfyUIProfile:
    """Load one named profile from config/comfyui.yaml."""
    if not config_path.is_file():
        raise FileNotFoundError(f"ComfyUI config not found: {config_path}")
    data = load_yaml(config_path)
    profiles = data.get("profiles") or {}
    name = profile_name or data.get("default_profile")
    if not name:
        raise ComfyUIError(
            f"No profile specified and no default_profile in {config_path}."
        )
    if name not in profiles:
        available = ", ".join(sorted(profiles)) or "(none)"
        raise ComfyUIError(
            f"Unknown ComfyUI profile {name!r}. Available: {available}."
        )
    return ComfyUIProfile.model_validate(profiles[name])


def render_workflow(
    template_text: str,
    *,
    positive: str,
    negative: str,
    seed: int,
    width: int,
    height: int,
    filename_prefix: str,
) -> dict[str, Any]:
    """Substitute the six tokens in `template_text` and parse the result.

    String-slot tokens are escaped via ``json.dumps(value)[1:-1]`` so quotes
    and backslashes in prompts don't break the surrounding JSON string.
    Numeric tokens are substituted as bare ``str(int)``.
    """
    substitutions: dict[str, str] = {
        "__POSITIVE__": _json_string_inner(positive),
        "__NEGATIVE__": _json_string_inner(negative),
        "__FILENAME_PREFIX__": _json_string_inner(filename_prefix),
        "__SEED__": str(int(seed)),
        "__WIDTH__": str(int(width)),
        "__HEIGHT__": str(int(height)),
    }

    missing = [t for t in ALL_TOKENS if t not in template_text]
    if missing:
        _console.print(
            f"[yellow]warn[/yellow] workflow template is missing tokens: "
            f"{', '.join(missing)} (values will not be applied)"
        )

    rendered = template_text
    for token, value in substitutions.items():
        rendered = rendered.replace(token, value)

    try:
        return json.loads(rendered)
    except json.JSONDecodeError as exc:
        raise ComfyUIError(
            f"Workflow template is not valid JSON after substitution: {exc}"
        ) from exc


def submit_and_wait(
    workflow: dict[str, Any],
    profile: ComfyUIProfile,
    client_id: str,
    *,
    poll_interval: float | None = None,
    timeout_seconds: float | None = None,
    http: httpx.Client | None = None,
) -> bytes:
    """POST workflow to /prompt, poll /history/<id>, GET /view. Return PNG bytes."""
    base = str(profile.base_url).rstrip("/")
    poll = poll_interval if poll_interval is not None else profile.poll_interval_seconds
    timeout = (
        timeout_seconds if timeout_seconds is not None else profile.timeout_seconds
    )

    owned_client = http is None
    client = http or httpx.Client(timeout=30.0)
    try:
        # 1. Submit prompt
        try:
            resp = client.post(
                f"{base}/prompt",
                json={"prompt": workflow, "client_id": client_id},
            )
        except httpx.ConnectError as exc:
            raise ComfyUIUnreachable(
                f"Can't reach ComfyUI at {base}. Is it running?"
            ) from exc
        except httpx.RequestError as exc:
            raise ComfyUIUnreachable(f"ComfyUI request error: {exc}") from exc

        if resp.status_code >= 400:
            raise ComfyUIError(
                f"ComfyUI /prompt returned HTTP {resp.status_code}: {resp.text}"
            )

        body = resp.json()
        node_errors = body.get("node_errors") or {}
        if node_errors:
            # Surface the first node's first error verbatim — usually
            # "model not found" or similar.
            first_node, first_err = next(iter(node_errors.items()))
            msg = _first_error_message(first_err)
            raise ComfyUIError(
                f"ComfyUI rejected workflow: node {first_node}: {msg}"
            )

        prompt_id = body.get("prompt_id")
        if not prompt_id:
            raise ComfyUIError(
                f"ComfyUI /prompt response had no prompt_id. Body: {body!r}"
            )

        # 2. Poll history
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() > deadline:
                raise ComfyUITimeout(
                    f"ComfyUI timed out after {timeout:.0f}s waiting for "
                    f"prompt {prompt_id}."
                )
            try:
                hist = client.get(f"{base}/history/{prompt_id}")
            except httpx.RequestError as exc:
                raise ComfyUIUnreachable(
                    f"ComfyUI request error while polling: {exc}"
                ) from exc
            hist_body = hist.json() if hist.status_code == 200 else {}
            entry = hist_body.get(prompt_id) if isinstance(hist_body, dict) else None
            if entry and _is_completed(entry):
                image_ref = _first_image_ref(entry)
                if image_ref is None:
                    raise ComfyUIError(
                        f"ComfyUI prompt {prompt_id} completed but produced no image."
                    )
                # 3. Download
                view = client.get(
                    f"{base}/view",
                    params={
                        "filename": image_ref["filename"],
                        "subfolder": image_ref.get("subfolder", ""),
                        "type": image_ref.get("type", "output"),
                    },
                )
                if view.status_code != 200:
                    raise ComfyUIError(
                        f"Could not fetch output image: HTTP {view.status_code}"
                    )
                return view.content
            time.sleep(poll)
    finally:
        if owned_client:
            client.close()


def generate_image(
    spec: ContentSpec,
    *,
    kind: Literal["background"] = DEFAULT_KIND,
    assets_root: Path = DEFAULT_ASSETS_ROOT,
    worlds_path: Path = DEFAULT_WORLDS_PATH,
    config_path: Path = DEFAULT_COMFYUI_CONFIG_PATH,
    workflow_path: Path = DEFAULT_WORKFLOW_PATH,
    profile_name: str | None = None,
    force: bool = False,
    random_seed: bool = False,
    http: httpx.Client | None = None,
) -> GeneratedImage:
    """Generate the background image for a spec via ComfyUI.

    Writes ``assets_root/backgrounds/<world>/<background_prompt_key>.png``
    atomically. Returns the result, including ``skipped=True`` if the target
    file already existed and ``force`` was not set.
    """
    if kind != "background":  # pragma: no cover — narrowed by Literal
        raise NotImplementedError("Only kind='background' is supported in v1.")

    world = spec.visual.world
    key = spec.visual.background_prompt_key
    target_dir = assets_root / "backgrounds" / world
    target = target_dir / f"{key}.png"

    if target.is_file() and not force:
        return GeneratedImage(
            kind=kind,
            key=key,
            world=world,
            output_path=target,
            seed=0,
            skipped=True,
        )

    if not workflow_path.is_file():
        raise FileNotFoundError(
            f"Workflow template not found: {workflow_path}"
        )

    profile = load_profile(config_path, profile_name)

    prompts = build_image_prompt(spec, worlds_path=worlds_path)
    seed = random.randint(0, 2**31 - 1) if random_seed else deterministic_seed(
        spec.id, kind, key
    )
    # ComfyUI uses / as a subfolder separator on the server side.
    filename_prefix = f"motive/{spec.id}/{kind}"

    template_text = workflow_path.read_text(encoding="utf-8")
    workflow = render_workflow(
        template_text,
        positive=prompts.positive,
        negative=prompts.negative,
        seed=seed,
        width=profile.width,
        height=profile.height,
        filename_prefix=filename_prefix,
    )

    png_bytes = submit_and_wait(
        workflow,
        profile,
        client_id=str(uuid.uuid4()),
        http=http,
    )

    target_dir.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_bytes(png_bytes)
    os.replace(tmp, target)

    return GeneratedImage(
        kind=kind,
        key=key,
        world=world,
        output_path=target,
        seed=seed,
        skipped=False,
    )


# ---- internals -------------------------------------------------------------


def _json_string_inner(value: str) -> str:
    """Escape `value` for placement inside a JSON string slot."""
    return json.dumps(value)[1:-1]


def _is_completed(entry: dict[str, Any]) -> bool:
    """Treat a /history entry as done when status.completed is True
    OR when status_str signals terminal state."""
    status = entry.get("status") or {}
    if status.get("completed") is True:
        return True
    if status.get("status_str") in ("success", "error"):
        return True
    # Some ComfyUI versions don't populate status; if outputs exist, treat as done.
    return bool(entry.get("outputs"))


def _first_image_ref(entry: dict[str, Any]) -> dict[str, Any] | None:
    """Find the first node output that produced an image."""
    outputs = entry.get("outputs") or {}
    for node_output in outputs.values():
        images = node_output.get("images") or []
        if images:
            return images[0]
    return None


def _first_error_message(node_err: Any) -> str:
    """Pull a human-readable string out of ComfyUI's per-node error structure."""
    if isinstance(node_err, dict):
        errors = node_err.get("errors") or []
        if errors:
            first = errors[0]
            if isinstance(first, dict):
                return str(first.get("message") or first)
            return str(first)
        if "message" in node_err:
            return str(node_err["message"])
    return str(node_err)

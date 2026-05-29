"""Tests for the images (ComfyUI) stage.

Mirrors tests/test_visual_prompts.py: load real example specs against the
real visual_worlds.yaml, but replace ComfyUI HTTP calls with a FakeClient
that records requests and returns canned responses. No real network.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import httpx
import pytest
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.schemas import ComfyUIProfile, ContentSpec
from motive_engine.stages.images import (
    ALL_TOKENS,
    ComfyUIError,
    ComfyUITimeout,
    ComfyUIUnreachable,
    GeneratedImage,
    deterministic_seed,
    generate_image,
    render_workflow,
    submit_and_wait,
)
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"
WORLDS = ROOT / "config" / "visual_worlds.yaml"

PNG_BYTES = b"\x89PNG\r\n\x1a\nFAKE"


# ---- fixtures --------------------------------------------------------------


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


def _profile(workflow_path: Path) -> ComfyUIProfile:
    return ComfyUIProfile(
        description="test profile",
        base_url="http://127.0.0.1:8188",
        workflow_path=workflow_path,
        width=1080,
        height=1920,
        timeout_seconds=10.0,
        poll_interval_seconds=0.001,
    )


def _minimal_workflow_template() -> str:
    """A minimum ComfyUI-API-shaped workflow with all six tokens.

    Numeric tokens (__SEED__, __WIDTH__, __HEIGHT__) are placed in numeric
    JSON slots (no surrounding quotes); string tokens stay quoted.
    """
    return (
        "{"
        '"3": {"class_type": "KSampler", "inputs": {"seed": __SEED__}},'
        '"5": {"class_type": "EmptyLatentImage", "inputs": {"width": __WIDTH__, "height": __HEIGHT__}},'
        '"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "__POSITIVE__"}},'
        '"7": {"class_type": "CLIPTextEncode", "inputs": {"text": "__NEGATIVE__"}},'
        '"9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "__FILENAME_PREFIX__"}}'
        "}"
    )


def _config_pointing_at(workflow_path: Path, config_dir: Path) -> Path:
    """Write a comfyui.yaml with one profile and return its path."""
    cfg = {
        "default_profile": "test_local",
        "profiles": {
            "test_local": {
                "description": "test profile",
                "base_url": "http://127.0.0.1:8188",
                "workflow_path": str(workflow_path),
                "width": 1080,
                "height": 1920,
                "timeout_seconds": 10.0,
                "poll_interval_seconds": 0.001,
            }
        },
    }
    p = config_dir / "comfyui.yaml"
    p.write_text(json.dumps(cfg), encoding="utf-8")
    return p


# ---- FakeClient: stand-in for httpx.Client --------------------------------


class FakeClient:
    """Records HTTP calls and returns scripted responses.

    Pass a list of (predicate, response_factory) entries. Each request
    iterates through entries and uses the first whose predicate matches.
    """

    def __init__(self, script: list[tuple] | None = None) -> None:
        self.script = script or []
        self.requests: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    def post(self, url: str, json: dict | None = None, **kwargs: Any) -> Any:
        self.requests.append(("POST", url, {"json": json, **kwargs}))
        return self._respond("POST", url, json or {})

    def get(self, url: str, params: dict | None = None, **kwargs: Any) -> Any:
        self.requests.append(("GET", url, {"params": params, **kwargs}))
        return self._respond("GET", url, params or {})

    def close(self) -> None:
        self.closed = True

    def _respond(self, method: str, url: str, data: dict) -> Any:
        for predicate, factory in self.script:
            if predicate(method, url):
                return factory()
        raise AssertionError(f"FakeClient: no scripted response for {method} {url}")


class FakeResponse:
    def __init__(
        self,
        *,
        status_code: int = 200,
        body: dict | None = None,
        content: bytes | None = None,
        text: str = "",
    ) -> None:
        self.status_code = status_code
        self._body = body
        self.content = content or b""
        self.text = text

    def json(self) -> Any:
        if self._body is None:
            raise ValueError("no json body")
        return self._body


# ---- deterministic_seed ---------------------------------------------------


def test_deterministic_seed_is_stable_and_in_range() -> None:
    a = deterministic_seed("marcus_self_command_001", "background", "ruined_courtyard_dawn")
    b = deterministic_seed("marcus_self_command_001", "background", "ruined_courtyard_dawn")
    c = deterministic_seed("marcus_self_command_001", "background", "other_key")
    assert a == b
    assert a != c
    assert 0 <= a < 2**31


# ---- render_workflow ------------------------------------------------------


def test_render_workflow_substitutes_all_tokens() -> None:
    out = render_workflow(
        _minimal_workflow_template(),
        positive="a Roman courtyard",
        negative="text, logo",
        seed=123,
        width=1080,
        height=1920,
        filename_prefix="motive/marcus/background",
    )
    assert out["3"]["inputs"]["seed"] == 123
    assert out["5"]["inputs"]["width"] == 1080
    assert out["5"]["inputs"]["height"] == 1920
    assert out["6"]["inputs"]["text"] == "a Roman courtyard"
    assert out["7"]["inputs"]["text"] == "text, logo"
    assert out["9"]["inputs"]["filename_prefix"] == "motive/marcus/background"


def test_render_workflow_escapes_quotes_in_prompt() -> None:
    """Prompt containing a double quote must not break the JSON parse."""
    out = render_workflow(
        _minimal_workflow_template(),
        positive='a so-called "ruined" courtyard',
        negative="",
        seed=1,
        width=1,
        height=1,
        filename_prefix="x",
    )
    assert out["6"]["inputs"]["text"] == 'a so-called "ruined" courtyard'


def test_render_workflow_warns_on_missing_token(capsys: Any) -> None:
    # Template missing __WIDTH__ and __HEIGHT__ should still parse OK,
    # but a warning is emitted.
    template = json.dumps({"3": {"class_type": "K", "inputs": {"seed": "__SEED__"}}})
    render_workflow(
        template,
        positive="p",
        negative="n",
        seed=1,
        width=1,
        height=1,
        filename_prefix="x",
    )
    err = capsys.readouterr().err
    # At minimum one missing token must be reported.
    assert any(tok in err for tok in ALL_TOKENS if tok not in template)


def test_render_workflow_invalid_json_raises() -> None:
    # Inject a quote so substitution produces invalid JSON.
    template = '{"6": {"text": "__POSITIVE__"'  # missing closing braces
    with pytest.raises(ComfyUIError, match="not valid JSON"):
        render_workflow(
            template,
            positive="hi",
            negative="bye",
            seed=1,
            width=1,
            height=1,
            filename_prefix="x",
        )


# ---- submit_and_wait ------------------------------------------------------


def test_submit_and_wait_polls_then_downloads(tmp_path: Path) -> None:
    workflow_path = tmp_path / "wf.json"
    profile = _profile(workflow_path)

    # First /history call: prompt not done yet. Second: completed with image.
    poll_calls = {"n": 0}

    def history_response() -> FakeResponse:
        poll_calls["n"] += 1
        if poll_calls["n"] == 1:
            return FakeResponse(body={})  # queued, empty
        return FakeResponse(
            body={
                "abc": {
                    "status": {"completed": True, "status_str": "success"},
                    "outputs": {
                        "9": {
                            "images": [
                                {
                                    "filename": "motive_marcus.png",
                                    "subfolder": "",
                                    "type": "output",
                                }
                            ]
                        }
                    },
                }
            }
        )

    fake = FakeClient(
        script=[
            (lambda m, u: m == "POST" and u.endswith("/prompt"),
             lambda: FakeResponse(body={"prompt_id": "abc", "node_errors": {}})),
            (lambda m, u: m == "GET" and "/history/abc" in u, history_response),
            (lambda m, u: m == "GET" and u.endswith("/view"),
             lambda: FakeResponse(content=PNG_BYTES)),
        ]
    )

    bytes_out = submit_and_wait(
        {"workflow": "stub"}, profile, client_id="test-client", http=fake
    )

    assert bytes_out == PNG_BYTES
    methods = [r[0] for r in fake.requests]
    assert methods.count("POST") == 1
    assert methods.count("GET") == 3  # 2x history (empty then done) + 1x view


def test_submit_and_wait_node_error_raises(tmp_path: Path) -> None:
    profile = _profile(tmp_path / "wf.json")
    fake = FakeClient(
        script=[
            (
                lambda m, u: m == "POST" and u.endswith("/prompt"),
                lambda: FakeResponse(
                    body={
                        "prompt_id": "abc",
                        "node_errors": {
                            "4": {
                                "errors": [{"message": "model not found: REPLACE.safetensors"}]
                            }
                        },
                    }
                ),
            )
        ]
    )
    with pytest.raises(ComfyUIError, match="model not found"):
        submit_and_wait({}, profile, client_id="x", http=fake)


def test_submit_and_wait_connection_refused_raises(tmp_path: Path) -> None:
    profile = _profile(tmp_path / "wf.json")

    class RefusedClient(FakeClient):
        def post(self, url: str, json: dict | None = None, **kwargs: Any) -> Any:
            raise httpx.ConnectError("connection refused")

    with pytest.raises(ComfyUIUnreachable, match="Can't reach ComfyUI"):
        submit_and_wait({}, profile, client_id="x", http=RefusedClient())


def test_submit_and_wait_times_out(tmp_path: Path) -> None:
    profile_dict = _profile(tmp_path / "wf.json").model_dump()
    profile_dict["timeout_seconds"] = 0.05  # tight timeout for fast test
    profile = ComfyUIProfile.model_validate(profile_dict)
    fake = FakeClient(
        script=[
            (lambda m, u: m == "POST" and u.endswith("/prompt"),
             lambda: FakeResponse(body={"prompt_id": "abc"})),
            (lambda m, u: m == "GET" and "/history/abc" in u,
             lambda: FakeResponse(body={})),  # never completes
        ]
    )
    with pytest.raises(ComfyUITimeout):
        submit_and_wait({}, profile, client_id="x", http=fake)


# ---- generate_image (end-to-end with mocked HTTP) -------------------------


def _write_workflow_and_config(tmp_path: Path) -> tuple[Path, Path]:
    workflow_path = tmp_path / "wf.json"
    workflow_path.write_text(_minimal_workflow_template(), encoding="utf-8")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = _config_pointing_at(workflow_path, config_dir)
    return workflow_path, config_path


def _success_client() -> FakeClient:
    return FakeClient(
        script=[
            (lambda m, u: m == "POST" and u.endswith("/prompt"),
             lambda: FakeResponse(body={"prompt_id": "abc", "node_errors": {}})),
            (lambda m, u: m == "GET" and "/history/abc" in u,
             lambda: FakeResponse(
                 body={
                     "abc": {
                         "status": {"completed": True},
                         "outputs": {
                             "9": {
                                 "images": [
                                     {
                                         "filename": "out.png",
                                         "subfolder": "",
                                         "type": "output",
                                     }
                                 ]
                             }
                         },
                     }
                 }
             )),
            (lambda m, u: m == "GET" and u.endswith("/view"),
             lambda: FakeResponse(content=PNG_BYTES)),
        ]
    )


def test_generate_image_writes_to_assets(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"
    spec = _spec("marcus_self_command.yaml")

    result = generate_image(
        spec,
        assets_root=assets_root,
        worlds_path=WORLDS,
        config_path=config_path,
        workflow_path=workflow_path,
        http=_success_client(),
    )

    expected = assets_root / "backgrounds" / "stoic_rome" / "ruined_courtyard_dawn.png"
    assert result.skipped is False
    assert result.output_path == expected
    assert expected.read_bytes() == PNG_BYTES
    assert result.seed == deterministic_seed(
        spec.id, "background", spec.visual.background_prompt_key
    )


def test_generate_image_skipped_when_exists_without_force(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"
    spec = _spec("marcus_self_command.yaml")

    target = assets_root / "backgrounds" / "stoic_rome" / "ruined_courtyard_dawn.png"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"existing image")

    # No HTTP client passed — if we tried to call out, FakeClient would assert.
    # Pass an empty FakeClient to prove the network is untouched.
    fake = FakeClient(script=[])
    result = generate_image(
        spec,
        assets_root=assets_root,
        worlds_path=WORLDS,
        config_path=config_path,
        workflow_path=workflow_path,
        http=fake,
    )
    assert result.skipped is True
    assert target.read_bytes() == b"existing image"
    assert fake.requests == []


def test_generate_image_force_overwrites(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"
    spec = _spec("marcus_self_command.yaml")

    target = assets_root / "backgrounds" / "stoic_rome" / "ruined_courtyard_dawn.png"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"existing image")

    result = generate_image(
        spec,
        assets_root=assets_root,
        worlds_path=WORLDS,
        config_path=config_path,
        workflow_path=workflow_path,
        force=True,
        http=_success_client(),
    )
    assert result.skipped is False
    assert target.read_bytes() == PNG_BYTES


def test_generate_image_atomic_on_failure(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"
    spec = _spec("marcus_self_command.yaml")

    # /view returns 500 -> ComfyUIError, no PNG written
    fake = FakeClient(
        script=[
            (lambda m, u: m == "POST" and u.endswith("/prompt"),
             lambda: FakeResponse(body={"prompt_id": "abc"})),
            (lambda m, u: m == "GET" and "/history/abc" in u,
             lambda: FakeResponse(
                 body={
                     "abc": {
                         "status": {"completed": True},
                         "outputs": {"9": {"images": [{"filename": "x.png", "subfolder": "", "type": "output"}]}},
                     }
                 }
             )),
            (lambda m, u: m == "GET" and u.endswith("/view"),
             lambda: FakeResponse(status_code=500)),
        ]
    )
    with pytest.raises(ComfyUIError, match="Could not fetch"):
        generate_image(
            spec,
            assets_root=assets_root,
            worlds_path=WORLDS,
            config_path=config_path,
            workflow_path=workflow_path,
            http=fake,
        )

    target_dir = assets_root / "backgrounds" / "stoic_rome"
    target = target_dir / "ruined_courtyard_dawn.png"
    tmp = target.with_suffix(".png.tmp")
    assert not target.exists()
    assert not tmp.exists()


def test_generate_image_missing_workflow_raises(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = _config_pointing_at(tmp_path / "wf.json", config_dir)
    assets_root = tmp_path / "assets"
    spec = _spec("marcus_self_command.yaml")
    with pytest.raises(FileNotFoundError, match="Workflow template"):
        generate_image(
            spec,
            assets_root=assets_root,
            worlds_path=WORLDS,
            config_path=config_path,
            workflow_path=tmp_path / "wf.json",  # doesn't exist
            http=FakeClient(),
        )


# ---- CLI ------------------------------------------------------------------


def _patch_httpx_with(client_factory: Any) -> Any:
    """Patch httpx.Client used by submit_and_wait to return our fake."""
    return patch("motive_engine.stages.images.httpx.Client", client_factory)


def test_cli_make_images_ok(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"

    runner = CliRunner()
    with _patch_httpx_with(lambda **kwargs: _success_client()):
        result = runner.invoke(
            app,
            [
                "make-images",
                str(EXAMPLES / "marcus_self_command.yaml"),
                "--assets-dir", str(assets_root),
                "--config", str(config_path),
                "--workflow", str(workflow_path),
            ],
        )
    assert result.exit_code == 0, result.output
    assert "OK" in result.output
    assert "seed=" in result.output


def test_cli_make_images_skip_message(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"
    target = assets_root / "backgrounds" / "stoic_rome" / "ruined_courtyard_dawn.png"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"existing")

    runner = CliRunner()
    with _patch_httpx_with(lambda **kwargs: FakeClient()):
        result = runner.invoke(
            app,
            [
                "make-images",
                str(EXAMPLES / "marcus_self_command.yaml"),
                "--assets-dir", str(assets_root),
                "--config", str(config_path),
                "--workflow", str(workflow_path),
            ],
        )
    assert result.exit_code == 0, result.output
    assert "skip" in result.output.lower()


def test_cli_make_images_unreachable(tmp_path: Path) -> None:
    workflow_path, config_path = _write_workflow_and_config(tmp_path)
    assets_root = tmp_path / "assets"

    class RefusedClient(FakeClient):
        def post(self, url: str, json: dict | None = None, **kwargs: Any) -> Any:
            raise httpx.ConnectError("no")

    runner = CliRunner()
    with _patch_httpx_with(lambda **kwargs: RefusedClient()):
        result = runner.invoke(
            app,
            [
                "make-images",
                str(EXAMPLES / "marcus_self_command.yaml"),
                "--assets-dir", str(assets_root),
                "--config", str(config_path),
                "--workflow", str(workflow_path),
            ],
        )
    assert result.exit_code == 1
    assert "unreachable" in result.output.lower()


def test_cli_make_images_invalid_spec(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("id: x\nseries: y\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(app, ["make-images", str(bad)])
    assert result.exit_code == 1
    assert "invalid" in result.output.lower()

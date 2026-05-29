"""Cross-config lint: verify a ContentSpec's references all resolve.

`motive validate-spec` checks the YAML against the schema (single-file).
`motive lint` additionally checks that every config-driven field
(series, world, background/figure prompt keys, voice and music profiles)
points to a real entry in the corresponding YAML file. Without this, a
typo like `world: stoic_rume` passes validate-spec and silently breaks
the visual-prompts stage later.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from motive_engine.schemas import ContentSpec
from motive_engine.stages.captions import CAPTION_STYLES
from motive_engine.utils import load_yaml

DEFAULT_WORLDS_PATH = Path("config") / "visual_worlds.yaml"
DEFAULT_VOICES_PATH = Path("config") / "voices.yaml"
DEFAULT_SERIES_PATH = Path("config") / "series.yaml"
DEFAULT_BRAND_PATH = Path("config") / "brand.yaml"


@dataclass(frozen=True)
class LintIssue:
    """One lint finding."""

    field: str
    message: str
    severity: str = "error"  # "error" | "warning"


def lint_spec(
    spec: ContentSpec,
    *,
    worlds_path: Path = DEFAULT_WORLDS_PATH,
    voices_path: Path = DEFAULT_VOICES_PATH,
    series_path: Path = DEFAULT_SERIES_PATH,
    brand_path: Path = DEFAULT_BRAND_PATH,
) -> list[LintIssue]:
    """Check every config-driven reference in `spec`. Returns a list of issues."""
    issues: list[LintIssue] = []
    issues.extend(_check_series(spec, series_path))
    issues.extend(_check_visual(spec, worlds_path))
    issues.extend(_check_caption_style(spec))
    issues.extend(_check_audio(spec, voices_path, brand_path))
    return issues


def _check_caption_style(spec: ContentSpec) -> list[LintIssue]:
    name = spec.visual.caption_style
    if name not in CAPTION_STYLES:
        return [
            LintIssue(
                "visual.caption_style",
                _unknown_msg(name, CAPTION_STYLES, "caption style"),
            )
        ]
    return []


# ---- checks ---------------------------------------------------------------


def _check_series(spec: ContentSpec, series_path: Path) -> list[LintIssue]:
    catalog = _load_catalog(series_path, "series")
    if catalog is None:
        return [LintIssue("series", f"could not load {series_path}")]
    if spec.series not in catalog:
        return [LintIssue("series", _unknown_msg(spec.series, catalog, "series"))]
    return []


def _check_visual(spec: ContentSpec, worlds_path: Path) -> list[LintIssue]:
    data = _load_or_none(worlds_path)
    if data is None:
        return [LintIssue("visual.world", f"could not load {worlds_path}")]
    worlds = data.get("worlds") or {}

    world_id = spec.visual.world
    if world_id not in worlds:
        return [LintIssue("visual.world", _unknown_msg(world_id, worlds, "world"))]

    world = worlds[world_id]
    issues: list[LintIssue] = []

    bg_catalog = world.get("background_prompts") or {}
    bg_key = spec.visual.background_prompt_key
    if bg_key not in bg_catalog:
        issues.append(
            LintIssue(
                "visual.background_prompt_key",
                _unknown_msg(bg_key, bg_catalog, f"background prompt in '{world_id}'"),
            )
        )

    fig_catalog = world.get("figure_prompts") or {}
    fig_key = spec.visual.figure_prompt_key
    if fig_key != "none" and fig_key not in fig_catalog:
        issues.append(
            LintIssue(
                "visual.figure_prompt_key",
                _unknown_msg(fig_key, fig_catalog, f"figure prompt in '{world_id}'"),
            )
        )

    return issues


def _check_audio(
    spec: ContentSpec, voices_path: Path, brand_path: Path
) -> list[LintIssue]:
    issues: list[LintIssue] = []

    voices = _load_catalog(voices_path, "voices")
    if voices is None:
        issues.append(
            LintIssue("audio.voice_profile", f"could not load {voices_path}")
        )
    elif spec.audio.voice_profile not in voices:
        issues.append(
            LintIssue(
                "audio.voice_profile",
                _unknown_msg(spec.audio.voice_profile, voices, "voice profile"),
            )
        )
    else:
        declared = spec.audio.tts_provider
        resolved = voices[spec.audio.voice_profile].get("tts_provider")
        if declared and resolved and declared != resolved:
            issues.append(
                LintIssue(
                    "audio.tts_provider",
                    f"spec declares '{declared}' but voice profile "
                    f"'{spec.audio.voice_profile}' uses '{resolved}'",
                    severity="warning",
                )
            )

    music = _load_catalog(brand_path, "music_profiles")
    if music is None:
        issues.append(
            LintIssue("audio.music_profile", f"could not load {brand_path}")
        )
    elif spec.audio.music_profile not in music:
        issues.append(
            LintIssue(
                "audio.music_profile",
                _unknown_msg(spec.audio.music_profile, music, "music profile"),
            )
        )

    return issues


# ---- helpers --------------------------------------------------------------


def _load_or_none(path: Path) -> dict[str, Any] | None:
    try:
        data = load_yaml(path)
    except (FileNotFoundError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _load_catalog(path: Path, top_key: str) -> dict[str, Any] | None:
    data = _load_or_none(path)
    if data is None:
        return None
    inner = data.get(top_key)
    return inner if isinstance(inner, dict) else None


def _unknown_msg(value: str, catalog: dict[str, Any], what: str) -> str:
    available = ", ".join(sorted(catalog)) or "<none>"
    return f"unknown {what} '{value}' (available: {available})"

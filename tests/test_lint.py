"""Tests for the cross-config lint stage."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.lint import lint_spec
from motive_engine.schemas import ContentSpec
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"
CONFIG = ROOT / "config"

CONFIG_PATHS = {
    "worlds_path": CONFIG / "visual_worlds.yaml",
    "voices_path": CONFIG / "voices.yaml",
    "series_path": CONFIG / "series.yaml",
    "brand_path": CONFIG / "brand.yaml",
}


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


def _with(spec: ContentSpec, **updates) -> ContentSpec:
    """Return a copy of `spec` with top-level fields overridden."""
    return spec.model_copy(update=updates)


def _with_visual(spec: ContentSpec, **updates) -> ContentSpec:
    """Return a copy with visual sub-fields overridden."""
    return spec.model_copy(update={"visual": spec.visual.model_copy(update=updates)})


def _with_audio(spec: ContentSpec, **updates) -> ContentSpec:
    """Return a copy with audio sub-fields overridden."""
    return spec.model_copy(update={"audio": spec.audio.model_copy(update=updates)})


# ---- happy path -----------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "marcus_self_command.yaml",
        "epictetus_freedom.yaml",
        "field_notes_resilience.yaml",
    ],
)
def test_example_specs_lint_clean(name: str) -> None:
    issues = lint_spec(_spec(name), **CONFIG_PATHS)
    errors = [i for i in issues if i.severity == "error"]
    assert errors == [], errors


# ---- each unknown field flagged ------------------------------------------


def test_unknown_series_flagged() -> None:
    spec = _with(_spec("marcus_self_command.yaml"), series="no_such_series")
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "series" for i in issues)


def test_unknown_world_flagged() -> None:
    spec = _with_visual(_spec("marcus_self_command.yaml"), world="no_such_world")
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "visual.world" for i in issues)


def test_unknown_background_key_flagged() -> None:
    spec = _with_visual(
        _spec("marcus_self_command.yaml"), background_prompt_key="no_such_bg"
    )
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "visual.background_prompt_key" for i in issues)


def test_unknown_figure_key_flagged() -> None:
    spec = _with_visual(
        _spec("marcus_self_command.yaml"), figure_prompt_key="no_such_fig"
    )
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "visual.figure_prompt_key" for i in issues)


def test_figure_key_none_always_passes() -> None:
    spec = _with_visual(_spec("marcus_self_command.yaml"), figure_prompt_key="none")
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert not any(i.field == "visual.figure_prompt_key" for i in issues)


def test_unknown_voice_profile_flagged() -> None:
    spec = _with_audio(
        _spec("marcus_self_command.yaml"), voice_profile="no_such_voice"
    )
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "audio.voice_profile" for i in issues)


def test_unknown_music_profile_flagged() -> None:
    spec = _with_audio(
        _spec("marcus_self_command.yaml"), music_profile="no_such_music"
    )
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "audio.music_profile" for i in issues)


def test_unknown_caption_style_flagged() -> None:
    spec = _with_visual(
        _spec("marcus_self_command.yaml"), caption_style="no_such_style"
    )
    issues = lint_spec(spec, **CONFIG_PATHS)
    assert any(i.field == "visual.caption_style" for i in issues)


def test_tts_provider_mismatch_is_warning() -> None:
    spec = _with_audio(_spec("marcus_self_command.yaml"), tts_provider="openai")
    issues = lint_spec(spec, **CONFIG_PATHS)
    tts = [i for i in issues if i.field == "audio.tts_provider"]
    assert tts and tts[0].severity == "warning"


def test_multiple_issues_reported_at_once() -> None:
    base = _spec("marcus_self_command.yaml")
    spec = _with(base, series="no_such_series")
    spec = _with_visual(spec, world="no_such_world")
    spec = _with_audio(spec, voice_profile="no_such_voice")
    fields = {i.field for i in lint_spec(spec, **CONFIG_PATHS)}
    assert "series" in fields
    assert "visual.world" in fields
    assert "audio.voice_profile" in fields


# ---- missing config files ------------------------------------------------


def test_missing_voices_file_flagged(tmp_path: Path) -> None:
    issues = lint_spec(
        _spec("marcus_self_command.yaml"),
        **{**CONFIG_PATHS, "voices_path": tmp_path / "nope.yaml"},
    )
    assert any(i.field == "audio.voice_profile" and "could not load" in i.message for i in issues)


# ---- CLI ------------------------------------------------------------------


def test_cli_lint_clean() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["lint", str(EXAMPLES / "marcus_self_command.yaml")])
    assert result.exit_code == 0, result.output
    assert "OK" in result.output


def test_cli_lint_with_errors(tmp_path: Path) -> None:
    bad = tmp_path / "bad_spec.yaml"
    original = (EXAMPLES / "marcus_self_command.yaml").read_text(encoding="utf-8")
    bad.write_text(
        original.replace(
            "voice_profile: classical_male",
            "voice_profile: no_such_voice",
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(app, ["lint", str(bad)])
    assert result.exit_code == 1
    assert "Lint failed" in result.output
    assert "no_such_voice" in result.output

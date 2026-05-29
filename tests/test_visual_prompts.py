"""Tests for the visual-prompts stage."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.schemas import ContentSpec
from motive_engine.stages import build_image_prompt
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"
WORLDS = ROOT / "config" / "visual_worlds.yaml"


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


# ---- happy path: each example produces a non-empty prompt -----------------


@pytest.mark.parametrize(
    "name",
    [
        "marcus_self_command.yaml",
        "epictetus_freedom.yaml",
        "field_notes_resilience.yaml",
    ],
)
def test_each_example_produces_a_prompt(name: str) -> None:
    result = build_image_prompt(_spec(name), worlds_path=WORLDS)
    assert result.positive.strip()
    assert result.negative.strip()


# ---- substitution actually happens ----------------------------------------


def test_marcus_prompt_substitutes_figure_and_background() -> None:
    result = build_image_prompt(_spec("marcus_self_command.yaml"), worlds_path=WORLDS)
    assert "Marcus Aurelius" in result.positive
    assert "marble bust" in result.positive
    assert "ruined Roman courtyard" in result.positive


def test_field_notes_prompt_omits_figure_section() -> None:
    """field_notes templates have no {figure} placeholder; verify it's clean."""
    result = build_image_prompt(_spec("field_notes_resilience.yaml"), worlds_path=WORLDS)
    assert "No human figure" in result.positive
    assert "burned" in result.positive.lower() or "ridge" in result.positive.lower()


def test_theme_is_substituted() -> None:
    result = build_image_prompt(_spec("marcus_self_command.yaml"), worlds_path=WORLDS)
    assert "self-command" in result.positive


# ---- error paths ----------------------------------------------------------


def test_unknown_world_raises() -> None:
    spec = _spec("marcus_self_command.yaml")
    spec.visual.__dict__["world"] = "no_such_world"  # bypass forbid for the test
    with pytest.raises(KeyError, match="Unknown visual world"):
        build_image_prompt(spec, worlds_path=WORLDS)


def test_unknown_background_key_raises() -> None:
    spec = _spec("marcus_self_command.yaml")
    spec.visual.__dict__["background_prompt_key"] = "no_such_background"
    with pytest.raises(KeyError, match="no_such_background"):
        build_image_prompt(spec, worlds_path=WORLDS)


def test_missing_worlds_file_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    with pytest.raises(FileNotFoundError):
        build_image_prompt(spec, worlds_path=tmp_path / "nope.yaml")


# ---- CLI integration ------------------------------------------------------


def test_cli_make_image_prompt_ok() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["make-image-prompt", str(EXAMPLES / "marcus_self_command.yaml")],
    )
    assert result.exit_code == 0, result.output
    assert "Image prompt" in result.output
    assert "Negative prompt" in result.output
    assert "Marcus Aurelius" in result.output


def test_cli_make_image_prompt_invalid_spec(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("id: x\nseries: y\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(app, ["make-image-prompt", str(bad)])
    assert result.exit_code == 1
    assert "invalid" in result.output.lower()

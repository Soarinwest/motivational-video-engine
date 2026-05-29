"""Schema and CLI tests for ContentSpec."""

from pathlib import Path

import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.schemas import ContentSpec
from motive_engine.utils import load_yaml

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "specs"


def _minimal_dict(**overrides) -> dict:
    """Smallest valid spec, with top-level overrides applied."""
    base = {
        "id": "test-001",
        "series": "test_series",
        "author": "Marcus Aurelius",
        "theme": "self-command",
        "duration_seconds": 30,
        "message": "Govern yourself before anything else.",
        "hook": "There is one thing you control.",
        "voiceover": "Govern yourself. The day asks one thing.",
        "final_line": "Begin with that.",
        "visual": {
            "world": "stoic_rome",
            "background_prompt_key": "ruined_courtyard_dawn",
            "figure_prompt_key": "marcus_bust_storm_light",
            "motion_profile": "slow_zoom",
            "overlays": [],
            "caption_style": "serif_quiet",
        },
        "audio": {
            "tts_provider": "kokoro",
            "voice_profile": "low_steady_male",
            "music_profile": "ambient_low",
        },
        "render": {
            "resolution": "1080x1920",
            "fps": 30,
        },
    }
    base.update(overrides)
    return base


# ---- example fixtures on disk ---------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "marcus_self_command.yaml",
        "epictetus_freedom.yaml",
        "field_notes_resilience.yaml",
    ],
)
def test_example_spec_validates(name: str) -> None:
    data = load_yaml(EXAMPLES / name)
    spec = ContentSpec.model_validate(data)
    assert spec.id
    assert spec.voiceover.strip()


# ---- defaults --------------------------------------------------------------


def test_minimal_spec_validates() -> None:
    spec = ContentSpec.model_validate(_minimal_dict())
    assert spec.render.format == "mp4"
    assert spec.visual.overlays == []


def test_author_can_be_null_for_field_notes() -> None:
    spec = ContentSpec.model_validate(_minimal_dict(author=None))
    assert spec.author is None


# ---- field validation -----------------------------------------------------


def test_duration_too_short_rejected() -> None:
    with pytest.raises(ValidationError) as exc:
        ContentSpec.model_validate(_minimal_dict(duration_seconds=5))
    assert "duration_seconds" in str(exc.value)


def test_duration_too_long_rejected() -> None:
    with pytest.raises(ValidationError) as exc:
        ContentSpec.model_validate(_minimal_dict(duration_seconds=120))
    assert "duration_seconds" in str(exc.value)


def test_invalid_fps_rejected() -> None:
    d = _minimal_dict()
    d["render"]["fps"] = 15
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(d)


def test_empty_voiceover_rejected() -> None:
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(_minimal_dict(voiceover=""))


def test_invalid_resolution_rejected() -> None:
    d = _minimal_dict()
    d["render"]["resolution"] = "1080-by-1920"
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(d)


def test_extra_field_forbidden() -> None:
    d = _minimal_dict()
    d["unknown_field"] = "oops"
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(d)


# ---- CLI integration -------------------------------------------------------


def test_cli_validate_spec_ok(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["validate-spec", str(EXAMPLES / "marcus_self_command.yaml")])
    assert result.exit_code == 0, result.output
    assert "OK" in result.output


def test_cli_validate_spec_missing_file(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["validate-spec", str(tmp_path / "nope.yaml")])
    assert result.exit_code == 2
    assert "not found" in result.output.lower()


def test_cli_validate_spec_invalid(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("id: x\nseries: y\n", encoding="utf-8")  # missing required fields
    runner = CliRunner()
    result = runner.invoke(app, ["validate-spec", str(bad)])
    assert result.exit_code == 1
    assert "invalid" in result.output.lower()


def test_cli_validate_spec_malformed_yaml(tmp_path: Path) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("[1, 2,\n", encoding="utf-8")  # unclosed flow sequence
    runner = CliRunner()
    result = runner.invoke(app, ["validate-spec", str(bad)])
    assert result.exit_code == 2
    assert "yaml parse" in result.output.lower()


def test_extra_field_in_nested_visual_rejected() -> None:
    d = _minimal_dict()
    d["visual"]["unknown_overlay_field"] = True
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(d)


def test_id_pattern_rejects_path_traversal() -> None:
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(_minimal_dict(id="../etc/passwd"))


def test_id_pattern_rejects_slashes() -> None:
    with pytest.raises(ValidationError):
        ContentSpec.model_validate(_minimal_dict(id="foo/bar"))


def test_id_pattern_accepts_letters_digits_underscore_hyphen() -> None:
    spec = ContentSpec.model_validate(_minimal_dict(id="abc_123-XYZ"))
    assert spec.id == "abc_123-XYZ"

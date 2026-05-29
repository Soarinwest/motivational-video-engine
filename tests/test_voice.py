"""Tests for the voice stage."""

import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.schemas import ContentSpec
from motive_engine.stages import voice as voice_stage
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"
VOICES = ROOT / "config" / "voices.yaml"


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


def _fake_synth(text: str, voice_id: str, speed: float) -> Iterable[tuple[str, str, Any]]:
    """Stand-in for Kokoro's pipeline. One fake chunk per sentence."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if not sentences:
        sentences = [text]
    for s in sentences:
        # 1 second of near-silence at 24kHz.
        yield (s, "<phonemes>", np.full(24000, 0.001, dtype=np.float32))


def _fake_factory(_lang_code: str) -> voice_stage.Synthesizer:
    return _fake_synth


# ---- voice profile loading ------------------------------------------------


def test_load_voice_profile_known() -> None:
    p = voice_stage.load_voice_profile("low_steady_male", voices_path=VOICES)
    assert p.voice_id == "am_michael"
    assert p.tts_provider == "kokoro"


def test_load_voice_profile_unknown_raises() -> None:
    with pytest.raises(KeyError, match="Unknown voice profile"):
        voice_stage.load_voice_profile("no_such_voice", voices_path=VOICES)


def test_load_voice_profile_invalid_speed_raises(tmp_path: Path) -> None:
    bad = tmp_path / "voices.yaml"
    bad.write_text(
        "voices:\n"
        "  bad:\n"
        "    description: x\n"
        "    tts_provider: kokoro\n"
        "    voice_id: x\n"
        "    lang_code: a\n"
        "    speed: -1.0\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        voice_stage.load_voice_profile("bad", voices_path=bad)


# ---- render_voice ---------------------------------------------------------


def test_render_voice_writes_wavs_and_index(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    profile = voice_stage.load_voice_profile(spec.audio.voice_profile, voices_path=VOICES)
    track = voice_stage.render_voice(
        spec, profile, output_root=tmp_path, synthesizer=_fake_synth
    )

    voice_dir = tmp_path / spec.id / "voice"
    assert voice_dir.is_dir()
    assert len(track.lines) >= 1
    for line in track.lines:
        assert (voice_dir / line.filename).is_file()
    assert (voice_dir / "index.json").is_file()

    saved = json.loads((voice_dir / "index.json").read_text(encoding="utf-8"))
    assert saved["spec_id"] == spec.id
    assert saved["voice_id"] == profile.voice_id
    assert saved["lang_code"] == profile.lang_code


def test_render_voice_cleans_stale_files(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    voice_dir = tmp_path / spec.id / "voice"
    voice_dir.mkdir(parents=True)
    (voice_dir / "line-099.wav").write_bytes(b"stale")
    (voice_dir / "index.json").write_text("{}", encoding="utf-8")

    profile = voice_stage.load_voice_profile(spec.audio.voice_profile, voices_path=VOICES)
    voice_stage.render_voice(spec, profile, output_root=tmp_path, synthesizer=_fake_synth)

    assert not (voice_dir / "line-099.wav").exists()


def test_render_voice_empty_synthesizer_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    profile = voice_stage.load_voice_profile(spec.audio.voice_profile, voices_path=VOICES)

    def empty(text: str, voice_id: str, speed: float) -> Iterable[tuple[str, str, Any]]:
        return iter(())

    with pytest.raises(RuntimeError, match="no audio"):
        voice_stage.render_voice(spec, profile, output_root=tmp_path, synthesizer=empty)


# ---- CLI integration ------------------------------------------------------


def test_cli_make_voice_ok(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "motive_engine.stages.voice.make_kokoro_synthesizer", _fake_factory
    )
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["make-voice", str(EXAMPLES / "marcus_self_command.yaml"), "-o", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    assert (tmp_path / "marcus_self_command_001" / "voice" / "line-001.wav").exists()
    assert (tmp_path / "marcus_self_command_001" / "voice" / "index.json").exists()


def test_cli_make_voice_unknown_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "motive_engine.stages.voice.make_kokoro_synthesizer", _fake_factory
    )
    bad_spec = tmp_path / "bad_spec.yaml"
    original = (EXAMPLES / "marcus_self_command.yaml").read_text(encoding="utf-8")
    bad_spec.write_text(
        original.replace(
            "voice_profile: classical_male",
            "voice_profile: no_such_voice",
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(app, ["make-voice", str(bad_spec), "-o", str(tmp_path)])
    assert result.exit_code == 1
    assert "voice profile" in result.output.lower()

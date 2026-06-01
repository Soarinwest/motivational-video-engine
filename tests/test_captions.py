"""Tests for the captions stage."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from motive_engine.cli import app
from motive_engine.schemas import ContentSpec
from motive_engine.stages.captions import (
    CAPTION_STYLES,
    build_caption_track,
    get_caption_style,
    render_ass,
    write_captions,
    _format_ass_time,
)
from motive_engine.stages.voice import VoiceLine, VoiceTrack
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


def _fake_voice_track(spec_id: str) -> VoiceTrack:
    return VoiceTrack(
        spec_id=spec_id,
        voice_profile="classical_male",
        voice_id="bm_george",
        lang_code="b",
        speed=0.88,
        lines=[
            VoiceLine(index=1, filename="line-001.wav", graphemes="First line of text.", duration_seconds=2.5),
            VoiceLine(index=2, filename="line-002.wav", graphemes="Second line follows.", duration_seconds=3.0),
            VoiceLine(index=3, filename="line-003.wav", graphemes="And a third.", duration_seconds=1.8),
        ],
    )


def _write_voice_index(voice_dir: Path, track: VoiceTrack) -> None:
    voice_dir.mkdir(parents=True, exist_ok=True)
    (voice_dir / "index.json").write_text(track.model_dump_json(indent=2), encoding="utf-8")


# ---- style registry -------------------------------------------------------


def test_default_styles_present() -> None:
    assert "serif_quiet" in CAPTION_STYLES
    assert "sans_quiet" in CAPTION_STYLES


def test_get_caption_style_known() -> None:
    style = get_caption_style("serif_quiet")
    assert style.font == "Georgia"
    assert style.alignment == 8  # top-center


def test_get_caption_style_unknown_raises() -> None:
    with pytest.raises(KeyError, match="Unknown caption style"):
        get_caption_style("no_such_style")


# ---- time formatting ------------------------------------------------------


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (0.0, "0:00:00.00"),
        (5.23, "0:00:05.23"),
        (61.5, "0:01:01.50"),
        (3661.0, "1:01:01.00"),
    ],
)
def test_ass_time_format(seconds: float, expected: str) -> None:
    assert _format_ass_time(seconds) == expected


# ---- build_caption_track --------------------------------------------------


def test_caption_track_accumulates_timing() -> None:
    spec = _spec("marcus_self_command.yaml")
    voice_track = _fake_voice_track(spec.id)
    captions = build_caption_track(spec, voice_track)

    assert len(captions.lines) == 3
    assert captions.lines[0].start_seconds == 0.0
    assert captions.lines[0].end_seconds == pytest.approx(2.5)
    assert captions.lines[1].start_seconds == pytest.approx(2.5)
    assert captions.lines[1].end_seconds == pytest.approx(5.5)
    assert captions.lines[2].start_seconds == pytest.approx(5.5)
    assert captions.lines[2].end_seconds == pytest.approx(7.3)


def test_caption_track_skips_empty_lines_but_advances_cursor() -> None:
    spec = _spec("marcus_self_command.yaml")
    voice_track = VoiceTrack(
        spec_id=spec.id,
        voice_profile="classical_male",
        voice_id="bm_george",
        lang_code="b",
        speed=0.88,
        lines=[
            VoiceLine(index=1, filename="line-001.wav", graphemes="Real text.", duration_seconds=2.0),
            VoiceLine(index=2, filename="line-002.wav", graphemes="   ", duration_seconds=1.0),  # empty after strip
            VoiceLine(index=3, filename="line-003.wav", graphemes="More text.", duration_seconds=2.0),
        ],
    )
    captions = build_caption_track(spec, voice_track)

    assert len(captions.lines) == 2  # the whitespace one was skipped
    # But cursor advanced through the empty line — the second real caption starts at 3.0
    assert captions.lines[1].start_seconds == pytest.approx(3.0)


# ---- render_ass -----------------------------------------------------------


def test_render_ass_includes_headers_and_styles_and_events() -> None:
    spec = _spec("marcus_self_command.yaml")
    voice_track = _fake_voice_track(spec.id)
    captions = build_caption_track(spec, voice_track)
    style = get_caption_style(spec.visual.caption_style)
    ass = render_ass(captions, style)

    assert "[Script Info]" in ass
    assert "[V4+ Styles]" in ass
    assert "[Events]" in ass
    assert "Georgia" in ass  # serif_quiet
    assert "PlayResX: 1080" in ass
    assert "PlayResY: 1920" in ass
    # Three Dialogue: lines
    assert ass.count("\nDialogue:") == 3


def test_render_ass_escapes_newlines_in_text() -> None:
    spec = _spec("marcus_self_command.yaml")
    # Build a CaptionTrack directly with an embedded \n in the chunk text
    # (build_caption_track now splits on whitespace and so does not produce
    # \n-containing chunks, but render_ass's escape behavior must still work
    # if upstream code ever hands it such a chunk).
    from motive_engine.stages.captions import CaptionLine, CaptionTrack
    track = CaptionTrack(
        spec_id=spec.id,
        style=spec.visual.caption_style,
        resolution=spec.render.resolution,
        lines=[CaptionLine(index=1, start_seconds=0.0, end_seconds=3.0, text="line one\nline two")],
    )
    ass = render_ass(track, get_caption_style(spec.visual.caption_style))
    assert "line one\\Nline two" in ass


def test_build_caption_track_chunks_long_lines_to_max_ten_words() -> None:
    """A single voice line over 10 words is split into multiple caption blocks."""
    spec = _spec("marcus_self_command.yaml")
    voice_track = VoiceTrack(
        spec_id=spec.id,
        voice_profile="classical_male",
        voice_id="bm_george",
        lang_code="b",
        speed=0.88,
        lines=[
            VoiceLine(
                index=1,
                filename="line-001.wav",
                # 14 words; should chunk into 10 + 4
                graphemes="one two three four five six seven eight nine ten eleven twelve thirteen fourteen",
                duration_seconds=14.0,
            ),
        ],
    )
    captions = build_caption_track(spec, voice_track)
    assert len(captions.lines) == 2
    assert len(captions.lines[0].text.split()) == 10
    assert len(captions.lines[1].text.split()) == 4
    # Duration distributed proportionally (10/14 and 4/14 of 14.0s)
    assert abs(captions.lines[0].end_seconds - captions.lines[0].start_seconds - 10.0) < 0.01
    assert abs(captions.lines[1].end_seconds - captions.lines[1].start_seconds - 4.0) < 0.01


# ---- write_captions end-to-end -------------------------------------------


def test_write_captions_creates_ass_file(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    _write_voice_index(tmp_path / spec.id / "voice", _fake_voice_track(spec.id))

    output_path, track = write_captions(spec, output_root=tmp_path)

    assert output_path == tmp_path / spec.id / "captions.ass"
    assert output_path.is_file()
    assert len(track.lines) == 3
    content = output_path.read_text(encoding="utf-8")
    assert "[Events]" in content


def test_write_captions_missing_voice_dir_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    # No voice/index.json written.
    with pytest.raises(FileNotFoundError, match="make-voice"):
        write_captions(spec, output_root=tmp_path)


# ---- CLI integration ------------------------------------------------------


def test_cli_make_captions_ok(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    _write_voice_index(tmp_path / spec.id / "voice", _fake_voice_track(spec.id))

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["make-captions", str(EXAMPLES / "marcus_self_command.yaml"), "-o", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    assert (tmp_path / spec.id / "captions.ass").is_file()


def test_cli_make_captions_missing_voice(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["make-captions", str(EXAMPLES / "marcus_self_command.yaml"), "-o", str(tmp_path)],
    )
    assert result.exit_code == 2
    assert "voice" in result.output.lower()

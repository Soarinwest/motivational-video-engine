"""Tests for the review stage's pure helpers.

The Streamlit UI itself isn't unit-tested — it's exercised by `motive review`.
"""

from pathlib import Path

import pytest

from motive_engine.stages.review import (
    approve_draft,
    list_drafts,
    load_draft,
    reject_draft,
)
from motive_engine.stages.voice import VoiceLine, VoiceTrack

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"


def _make_draft_dir(
    outputs_root: Path,
    draft_id: str,
    *,
    with_video: bool = True,
    with_spec: bool = True,
    with_voice_index: bool = True,
) -> Path:
    """Build a draft directory under outputs_root/drafts/<id>/."""
    draft_dir = outputs_root / "drafts" / draft_id
    draft_dir.mkdir(parents=True, exist_ok=True)
    if with_video:
        (draft_dir / f"{draft_id}.mp4").write_bytes(b"\x00\x00\x00 ftypisom")  # tiny MP4-ish bytes
    if with_spec:
        # Copy a real example spec so ContentSpec.model_validate succeeds.
        spec_src = EXAMPLES / "marcus_self_command.yaml"
        (draft_dir / "spec.yaml").write_text(
            spec_src.read_text(encoding="utf-8"), encoding="utf-8"
        )
    if with_voice_index:
        track = VoiceTrack(
            spec_id=draft_id,
            voice_profile="classical_male",
            voice_id="bm_george",
            lang_code="b",
            speed=0.88,
            lines=[
                VoiceLine(
                    index=1, filename="line-001.wav",
                    graphemes="A line.", duration_seconds=2.0,
                ),
            ],
        )
        (draft_dir / "voice").mkdir(exist_ok=True)
        (draft_dir / "voice" / "index.json").write_text(
            track.model_dump_json(indent=2), encoding="utf-8"
        )
    return draft_dir


# ---- list_drafts ----------------------------------------------------------


def test_list_drafts_empty_when_no_outputs(tmp_path: Path) -> None:
    assert list_drafts(tmp_path) == []


def test_list_drafts_empty_when_drafts_dir_empty(tmp_path: Path) -> None:
    (tmp_path / "drafts").mkdir()
    assert list_drafts(tmp_path) == []


def test_list_drafts_skips_dirs_without_video(tmp_path: Path) -> None:
    _make_draft_dir(tmp_path, "ready_one", with_video=True)
    _make_draft_dir(tmp_path, "halfway", with_video=False)
    drafts = list_drafts(tmp_path)
    assert [d.id for d in drafts] == ["ready_one"]


def test_list_drafts_returns_multiple_sorted(tmp_path: Path) -> None:
    _make_draft_dir(tmp_path, "draft_c")
    _make_draft_dir(tmp_path, "draft_a")
    _make_draft_dir(tmp_path, "draft_b")
    drafts = list_drafts(tmp_path)
    assert [d.id for d in drafts] == ["draft_a", "draft_b", "draft_c"]


# ---- load_draft -----------------------------------------------------------


def test_load_draft_with_spec_and_voice(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "marcus_self_command_001")
    draft = load_draft(draft_dir)
    assert draft.id == "marcus_self_command_001"
    assert draft.spec is not None
    assert draft.spec.author == "Marcus Aurelius"
    assert draft.voice_track is not None
    assert draft.voice_track.voice_id == "bm_george"


def test_load_draft_without_spec_returns_none(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "no_spec_001", with_spec=False)
    draft = load_draft(draft_dir)
    assert draft.spec is None


def test_load_draft_with_invalid_spec_returns_none(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "bad_spec_001", with_spec=False)
    (draft_dir / "spec.yaml").write_text(
        "id: ???\nseries: not-enough-fields\n", encoding="utf-8"
    )
    draft = load_draft(draft_dir)
    assert draft.spec is None  # bad spec is tolerated; UI shows a warning


def test_load_draft_without_voice_index_returns_none(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "no_voice_001", with_voice_index=False)
    draft = load_draft(draft_dir)
    assert draft.voice_track is None


# ---- approve_draft --------------------------------------------------------


def test_approve_moves_dir_to_approved(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "to_approve_001")
    draft = load_draft(draft_dir)

    target = approve_draft(draft, outputs_root=tmp_path)

    assert target == tmp_path / "approved" / "to_approve_001"
    assert target.is_dir()
    assert (target / "to_approve_001.mp4").is_file()
    assert (target / "spec.yaml").is_file()
    assert not draft_dir.exists()  # original moved away


def test_approve_refuses_to_overwrite_existing(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "collide_001")
    draft = load_draft(draft_dir)

    (tmp_path / "approved" / "collide_001").mkdir(parents=True)

    with pytest.raises(FileExistsError, match="already exists"):
        approve_draft(draft, outputs_root=tmp_path)
    assert draft_dir.exists()  # original untouched


# ---- reject_draft ---------------------------------------------------------


def test_reject_moves_dir_and_writes_reason(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "to_reject_001")
    draft = load_draft(draft_dir)

    target = reject_draft(draft, reason="caption timing felt off", outputs_root=tmp_path)

    assert target == tmp_path / "rejected" / "to_reject_001"
    assert (target / "rejection_reason.txt").read_text(encoding="utf-8") == (
        "caption timing felt off"
    )
    assert not draft_dir.exists()


def test_reject_with_empty_reason_raises(tmp_path: Path) -> None:
    draft_dir = _make_draft_dir(tmp_path, "no_reason_001")
    draft = load_draft(draft_dir)

    with pytest.raises(ValueError, match="reason must not be empty"):
        reject_draft(draft, reason="   ", outputs_root=tmp_path)
    assert draft_dir.exists()

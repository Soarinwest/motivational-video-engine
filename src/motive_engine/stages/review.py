"""Review stage: discover drafts, move them on operator decision.

Pure helpers. The Streamlit UI lives in motive_engine.review_app.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from motive_engine.schemas import ContentSpec
from motive_engine.stages.voice import VoiceTrack
from motive_engine.utils import load_yaml

DEFAULT_OUTPUTS_ROOT = Path("outputs")


@dataclass(frozen=True)
class Draft:
    """A draft visible in the review queue."""

    id: str
    path: Path                    # the per-draft directory
    video_path: Path              # <path>/<id>.mp4
    spec: ContentSpec | None      # loaded from <path>/spec.yaml if present
    voice_track: VoiceTrack | None  # loaded from <path>/voice/index.json if present


# ---- public API ------------------------------------------------------------


def list_drafts(outputs_root: Path = DEFAULT_OUTPUTS_ROOT) -> list[Draft]:
    """Return all drafts in <outputs_root>/drafts/ that have a <id>.mp4."""
    drafts_dir = outputs_root / "drafts"
    if not drafts_dir.is_dir():
        return []

    drafts: list[Draft] = []
    for entry in sorted(drafts_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not (entry / f"{entry.name}.mp4").is_file():
            continue
        drafts.append(load_draft(entry))
    return drafts


def load_draft(draft_dir: Path) -> Draft:
    """Construct a Draft from the contents of a draft directory."""
    spec_path = draft_dir / "spec.yaml"
    voice_idx = draft_dir / "voice" / "index.json"

    spec: ContentSpec | None = None
    if spec_path.is_file():
        try:
            spec = ContentSpec.model_validate(load_yaml(spec_path))
        except Exception:
            spec = None

    voice: VoiceTrack | None = None
    if voice_idx.is_file():
        try:
            voice = VoiceTrack.model_validate_json(
                voice_idx.read_text(encoding="utf-8")
            )
        except Exception:
            voice = None

    return Draft(
        id=draft_dir.name,
        path=draft_dir,
        video_path=draft_dir / f"{draft_dir.name}.mp4",
        spec=spec,
        voice_track=voice,
    )


def approve_draft(
    draft: Draft,
    outputs_root: Path = DEFAULT_OUTPUTS_ROOT,
) -> Path:
    """Move draft dir to <outputs_root>/approved/<id>/. Returns the new path."""
    return _move_draft(draft, outputs_root / "approved")


def reject_draft(
    draft: Draft,
    reason: str,
    outputs_root: Path = DEFAULT_OUTPUTS_ROOT,
) -> Path:
    """Move draft dir to <outputs_root>/rejected/<id>/ and write rejection_reason.txt."""
    if not reason.strip():
        raise ValueError("rejection reason must not be empty")
    target = _move_draft(draft, outputs_root / "rejected")
    (target / "rejection_reason.txt").write_text(reason, encoding="utf-8")
    return target


# ---- internals -------------------------------------------------------------


def _move_draft(draft: Draft, target_root: Path) -> Path:
    target_root.mkdir(parents=True, exist_ok=True)
    target = target_root / draft.id
    if target.exists():
        raise FileExistsError(
            f"Cannot move {draft.path} to {target}: target already exists. "
            f"Resolve the conflict by hand before re-running."
        )
    shutil.move(str(draft.path), str(target))
    return target

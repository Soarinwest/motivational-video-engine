"""Streamlit review app for motive-engine drafts.

Run via `motive review` (the CLI launcher spawns Streamlit pointed at this
file). Reads the outputs root from the MOTIVE_OUTPUTS_ROOT env var; defaults
to ./outputs if unset.
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from motive_engine.stages.review import (
    DEFAULT_OUTPUTS_ROOT,
    Draft,
    approve_draft,
    list_drafts,
    reject_draft,
)


def _outputs_root() -> Path:
    return Path(os.environ.get("MOTIVE_OUTPUTS_ROOT") or DEFAULT_OUTPUTS_ROOT)


def _render_meta(draft: Draft) -> None:
    spec = draft.spec
    if spec is None:
        st.warning("No spec.yaml in this draft — context unavailable.")
        return

    st.markdown(f"**Series:** {spec.series}")
    st.markdown(f"**Theme:** {spec.theme}")
    st.markdown(f"**Author:** {spec.author or '—'}")
    st.markdown(f"**World:** {spec.visual.world}")
    st.markdown(f"**Voice:** {spec.audio.voice_profile}")
    st.markdown(f"**Target duration:** {spec.duration_seconds}s")
    st.markdown("---")
    st.markdown("**Hook**")
    st.write(spec.hook)
    st.markdown("**Final line**")
    st.write(spec.final_line)
    st.markdown("---")
    st.markdown("**Voiceover**")
    st.text(spec.voiceover)

    if draft.voice_track:
        actual = sum(line.duration_seconds for line in draft.voice_track.lines)
        st.caption(
            f"Rendered duration: {actual:.1f}s "
            f"({len(draft.voice_track.lines)} line(s), voice "
            f"{draft.voice_track.voice_id} @ speed {draft.voice_track.speed})"
        )


def main() -> None:
    st.set_page_config(page_title="motive-engine review", layout="wide")

    outputs_root = _outputs_root()
    st.title("motive-engine — review queue")
    st.caption(f"Watching: {outputs_root / 'drafts'}")

    drafts = list_drafts(outputs_root)

    if not drafts:
        st.info(
            "No drafts ready for review.\n\n"
            "Produce one by running `motive render <spec>` after "
            "`motive make-voice` and `motive make-captions`."
        )
        return

    st.sidebar.markdown(f"**{len(drafts)}** draft(s) pending")
    selected_id = st.sidebar.radio(
        "Drafts",
        [d.id for d in drafts],
        label_visibility="collapsed",
    )
    draft = next(d for d in drafts if d.id == selected_id)

    st.header(draft.id)

    col_video, col_meta = st.columns([3, 2])
    with col_video:
        st.video(str(draft.video_path))
    with col_meta:
        _render_meta(draft)

    st.markdown("---")

    col_approve, col_reject, col_revise = st.columns(3)

    with col_approve:
        if st.button(
            "Approve", type="primary", use_container_width=True,
            key=f"approve_{draft.id}",
        ):
            try:
                target = approve_draft(draft, outputs_root)
                st.success(f"Approved → {target}")
                st.rerun()
            except FileExistsError as e:
                st.error(str(e))

    with col_reject:
        reason = st.text_input(
            "Rejection reason",
            key=f"reject_reason_{draft.id}",
            label_visibility="collapsed",
            placeholder="reason (required)",
        )
        if st.button(
            "Reject", use_container_width=True, key=f"reject_{draft.id}"
        ):
            if not reason.strip():
                st.error("Provide a reason before rejecting.")
            else:
                try:
                    target = reject_draft(draft, reason=reason, outputs_root=outputs_root)
                    st.success(f"Rejected → {target}")
                    st.rerun()
                except FileExistsError as e:
                    st.error(str(e))

    with col_revise:
        st.button(
            "Revise (leave in queue)",
            use_container_width=True,
            disabled=True,
            key=f"revise_{draft.id}",
        )
        st.caption("Re-run `make-voice` / `make-captions` / `render` to revise.")


main()

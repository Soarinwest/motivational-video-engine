"""Render stage: composite background + figure + motion + voice (+ captions)
into a vertical MP4.

The MVP focuses on the spine. Music mixing and visual overlays are deferred
to later polish milestones; they're declared in specs but ignored here.

Caption burn-in is a second pass via FFmpeg's subtitle filter (libass), using
the binary `imageio_ffmpeg` provides. If captions.ass doesn't exist yet, the
render proceeds without captions and warns the caller via the returned summary.

Asset lookup convention:
    assets/backgrounds/<world>/<background_prompt_key>.{png,jpg,jpeg,webp}
    assets/figures/<world>/<figure_prompt_key>.{png,jpg,jpeg,webp}
A spec with `figure_prompt_key: none` skips the figure layer entirely.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from motive_engine.schemas import ContentSpec
from motive_engine.utils import load_yaml

ASSET_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
DEFAULT_ASSETS_ROOT = Path("assets")
DEFAULT_BRAND_PATH = Path("config") / "brand.yaml"
KNOWN_MOTION_PROFILES = (
    "static",
    "slow_zoom",
    "slow_pan",
    "medium_zoom",
    "medium_pan",
    "figure_pan",
)
DEFAULT_MUSIC_GAIN_DB = -18.0


@dataclass(frozen=True)
class AssetPaths:
    """Resolved asset locations for a spec."""

    background: Path
    figure: Path | None


@dataclass(frozen=True)
class RenderSummary:
    """What was rendered."""

    output_path: Path
    duration_seconds: float
    captions_burned: bool


# ---- public API ------------------------------------------------------------


def resolve_assets(
    spec: ContentSpec,
    assets_root: Path = DEFAULT_ASSETS_ROOT,
) -> AssetPaths:
    """Find background + (optional) figure assets for the spec's world+keys.

    If spec.visual.background_override_path is set, it takes precedence over
    the world/background_prompt_key lookup. Override paths are interpreted
    relative to the repository root (the parent of `assets_root`).
    """
    override = spec.visual.background_override_path
    if override:
        bg = (assets_root.parent / override).resolve()
        if not bg.is_file():
            raise FileNotFoundError(
                f"background_override_path is set but the file is missing: {bg}\n"
                f"  spec id: {spec.id}\n"
                f"  override: {override!r}"
            )
    else:
        bg_stem = assets_root / "backgrounds" / spec.visual.world / spec.visual.background_prompt_key
        bg = _find_asset(bg_stem)
        if bg is None:
            raise FileNotFoundError(
                f"No background asset for world '{spec.visual.world}' / key "
                f"'{spec.visual.background_prompt_key}'.\n"
                f"  Expected: {bg_stem}.{{png,jpg,jpeg,webp}}\n"
                f"  Generate one with: motive make-image-prompt <spec>"
            )

    figure: Path | None = None
    if spec.visual.figure_prompt_key != "none":
        fig_stem = assets_root / "figures" / spec.visual.world / spec.visual.figure_prompt_key
        figure = _find_asset(fig_stem)
        if figure is None:
            raise FileNotFoundError(
                f"No figure asset for world '{spec.visual.world}' / key "
                f"'{spec.visual.figure_prompt_key}'.\n"
                f"  Expected: {fig_stem}.{{png,jpg,jpeg,webp}}"
            )

    return AssetPaths(background=bg, figure=figure)


def parse_resolution(res: str) -> tuple[int, int]:
    """Parse 'WIDTHxHEIGHT' into a (width, height) int tuple."""
    parts = res.split("x")
    if len(parts) != 2:
        raise ValueError(f"resolution must be 'WIDTHxHEIGHT', got {res!r}")
    return int(parts[0]), int(parts[1])


def render_video(
    spec: ContentSpec,
    voice_dir: Path,
    captions_path: Path | None,
    assets_root: Path,
    output_path: Path,
    brand_path: Path = DEFAULT_BRAND_PATH,
) -> RenderSummary:
    """Composite the full video and write to output_path. Returns a summary."""
    # MoviePy is heavy; import inside the function so tests of pure helpers
    # don't pay the cost.
    from moviepy import (  # type: ignore[import-untyped]
        AudioFileClip,
        CompositeAudioClip,
        CompositeVideoClip,
        ImageClip,
        concatenate_audioclips,
    )

    assets = resolve_assets(spec, assets_root)
    width, height = parse_resolution(spec.render.resolution)

    voice_wavs = sorted(voice_dir.glob("line-*.wav"))
    if not voice_wavs:
        raise FileNotFoundError(
            f"No line-*.wav in {voice_dir}. Run `motive make-voice` first."
        )
    voice_clips = [AudioFileClip(str(p)) for p in voice_wavs]
    voice_audio = concatenate_audioclips(voice_clips)
    duration = float(voice_audio.duration)

    # Music bed (optional)
    music = _load_music_track(
        spec.audio.music_profile, assets_root, brand_path, duration
    )
    audio = CompositeAudioClip([voice_audio, music]) if music else voice_audio

    # Background layer with smooth pan/zoom via PIL affine (sub-pixel correct).
    bg = _make_motion_clip(
        assets.background,
        spec.visual.motion_profile,
        duration,
        (width, height),
        fps=spec.render.fps,
    )

    layers = [bg]

    # Figure layer (optional, alpha-gated).
    #
    # The AI prompt template already places the figure into the background
    # scene (via "{figure}" in image_prompt_template), so an OPAQUE figure
    # asset composited on top would produce a double-figure artifact. We
    # only composite the figure layer when the asset has an alpha channel —
    # i.e., it's a transparent cutout. Opaque "figure" images (typically
    # copies of older scene assets) are skipped here; the AI-generated
    # background is treated as the final scene.
    if assets.figure is not None and _has_alpha_channel(assets.figure):
        fig = ImageClip(str(assets.figure), duration=duration)
        # Figure occupies the middle ~70% of frame height, horizontally centered.
        fig = fig.resized(height=int(height * 0.70))
        fig = fig.with_position(("center", int(height * 0.18)))
        layers.append(fig)

    composite = (
        CompositeVideoClip(layers, size=(width, height))
        .with_duration(duration)
        .with_audio(audio)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    captions_burned = False

    if captions_path is not None and captions_path.is_file():
        # Two-pass: render visuals + audio to temp, then burn captions.
        # mkstemp returns an open fd we must close before MoviePy writes to the path
        # (Windows refuses to open a file that already has an open handle).
        import os
        tmp_fd, tmp_path_str = tempfile.mkstemp(suffix=".mp4")
        os.close(tmp_fd)
        tmp_path = Path(tmp_path_str)
        try:
            composite.write_videofile(
                str(tmp_path),
                fps=spec.render.fps,
                codec="libx264",
                audio_codec="aac",
                logger=None,
            )
            _burn_captions(tmp_path, captions_path, output_path)
            captions_burned = True
        finally:
            tmp_path.unlink(missing_ok=True)
    else:
        composite.write_videofile(
            str(output_path),
            fps=spec.render.fps,
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )

    return RenderSummary(
        output_path=output_path,
        duration_seconds=duration,
        captions_burned=captions_burned,
    )


def write_render(
    spec: ContentSpec,
    output_root: Path,
    assets_root: Path = DEFAULT_ASSETS_ROOT,
) -> RenderSummary:
    """End-to-end render of one spec. Returns a RenderSummary."""
    spec_dir = output_root / spec.id
    voice_dir = spec_dir / "voice"
    captions_path = spec_dir / "captions.ass"
    output_path = spec_dir / f"{spec.id}.mp4"

    return render_video(
        spec=spec,
        voice_dir=voice_dir,
        captions_path=captions_path if captions_path.is_file() else None,
        assets_root=assets_root,
        output_path=output_path,
    )


# ---- internals -------------------------------------------------------------


def _find_asset(stem: Path) -> Path | None:
    """Return the first existing file at <stem>.<ext> for known extensions."""
    for ext in ASSET_EXTENSIONS:
        candidate = stem.with_suffix(ext)
        if candidate.is_file():
            return candidate
    return None


def _has_alpha_channel(image_path: Path) -> bool:
    """True if the image has a usable alpha channel (transparent cutout).

    Used to decide whether a figure asset can be safely composited over an
    AI-generated background that already contains the figure. Opaque figure
    assets are skipped (they would double-stack the figure on the scene).
    """
    from PIL import Image

    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA"):
            return True
        if img.mode == "P" and "transparency" in img.info:
            return True
    return False


# Motion-profile parameters: (start_zoom, end_zoom, start_ax, end_ax, start_ay, end_ay).
# Interpreted by _make_motion_clip. Zoom is a multiplier on the source; the visible
# window in source coords is (src_w / zoom, src_h / zoom). The anchor (ax, ay) gives
# the window's center as fractions of source width / height.
_MOTION_PARAMS: dict[str, tuple[float, float, float, float, float, float]] = {
    "static":       (1.00, 1.00, 0.50, 0.50, 0.50, 0.50),
    "slow_zoom":    (1.00, 1.08, 0.50, 0.50, 0.50, 0.50),
    "slow_pan":     (1.10, 1.10, 0.45, 0.55, 0.50, 0.50),
    "medium_zoom":  (1.00, 1.18, 0.50, 0.50, 0.50, 0.50),
    "medium_pan":   (1.18, 1.18, 0.42, 0.58, 0.50, 0.50),
    # figure_pan: gentle zoom toward the figure's face zone (~35% from top) with
    # a small horizontal drift. Used when there's a foreground figure layer.
    "figure_pan":   (1.00, 1.12, 0.48, 0.52, 0.35, 0.35),
}


def _make_motion_clip(
    image_path: Path,
    profile: str,
    duration: float,
    frame_size: tuple[int, int],
    *,
    fps: int = 30,
) -> Any:
    """Build a VideoClip that pans/zooms a still image smoothly to (frame_w, frame_h).

    Bypasses MoviePy's per-frame `clip.resized(callable)` which rounds output
    size to integer pixels and produces visible stepping when the per-frame
    scale change is sub-pixel. Instead, loads the source once via PIL and uses
    PIL's AFFINE transform per frame with BILINEAR interpolation — sub-pixel
    correct, no stepping.
    """
    import numpy as np
    from moviepy import VideoClip  # type: ignore[import-untyped]
    from PIL import Image

    if profile not in _MOTION_PARAMS:
        raise ValueError(
            f"Unknown motion profile: {profile!r}. "
            f"Known: {', '.join(KNOWN_MOTION_PROFILES)}."
        )

    frame_w, frame_h = frame_size
    start_zoom, end_zoom, start_ax, end_ax, start_ay, end_ay = _MOTION_PARAMS[profile]

    # Load and cover-resize the source ONCE up front. After this, src has the
    # frame's aspect ratio and is at least frame_size big.
    src = Image.open(image_path).convert("RGB")
    src_w, src_h = src.size
    src_aspect = src_w / src_h
    target_aspect = frame_w / frame_h
    if src_aspect > target_aspect:
        new_h = frame_h
        new_w = int(round(src_w * frame_h / src_h))
    else:
        new_w = frame_w
        new_h = int(round(src_h * frame_w / src_w))
    if (new_w, new_h) != (src_w, src_h):
        src = src.resize((new_w, new_h), Image.LANCZOS)
        src_w, src_h = src.size

    def make_frame(t: float) -> "np.ndarray":
        progress = max(0.0, min(1.0, t / duration)) if duration > 0 else 0.0
        zoom = start_zoom + (end_zoom - start_zoom) * progress
        ax = start_ax + (end_ax - start_ax) * progress
        ay = start_ay + (end_ay - start_ay) * progress

        # Visible window in source coords. Clamp anchor so the window stays
        # within bounds even when the user picks an aggressive value.
        win_w = src_w / zoom
        win_h = src_h / zoom
        ax_min = (win_w / 2) / src_w
        ay_min = (win_h / 2) / src_h
        ax = max(ax_min, min(1.0 - ax_min, ax))
        ay = max(ay_min, min(1.0 - ay_min, ay))

        cx = ax * src_w
        cy = ay * src_h
        x1 = cx - win_w / 2
        y1 = cy - win_h / 2

        # PIL AFFINE: target (u, v) -> source (a*u + b*v + c, d*u + e*v + f).
        # Map target (0..frame_w, 0..frame_h) onto source (x1..x1+win_w, y1..y1+win_h).
        result = src.transform(
            (frame_w, frame_h),
            Image.AFFINE,
            (win_w / frame_w, 0, x1, 0, win_h / frame_h, y1),
            Image.BILINEAR,
        )
        return np.array(result)

    clip = VideoClip(make_frame, duration=duration)
    return clip.with_fps(fps)


def _load_music_track(
    profile_name: str,
    assets_root: Path,
    brand_path: Path,
    duration: float,
) -> Any | None:
    """Resolve a music_profile to an AudioClip looped/trimmed to `duration`.

    Returns None if the profile has no `folder` (e.g. `silence`), if brand.yaml
    is missing, or if the resolved folder is empty. Music is mixed at the
    profile's `gain_db` (default -18 dB) below the voice track.
    """
    if not brand_path.is_file():
        return None
    brand = load_yaml(brand_path)
    profile = (brand.get("music_profiles") or {}).get(profile_name)
    if not profile:
        return None
    folder = profile.get("folder")
    if not folder:
        return None
    music_dir = assets_root / "music" / folder
    candidates = sorted(music_dir.glob("*.mp3"))
    if not candidates:
        return None

    from moviepy import AudioFileClip, concatenate_audioclips

    clip = AudioFileClip(str(candidates[0]))
    # Loop if shorter than the voice, then trim to exact duration.
    if clip.duration < duration:
        n_loops = int(duration // clip.duration) + 1
        clip = concatenate_audioclips([clip] * n_loops)
    clip = clip.subclipped(0, duration)

    gain_db = float(profile.get("gain_db", DEFAULT_MUSIC_GAIN_DB))
    factor = 10 ** (gain_db / 20)
    clip = clip.with_volume_scaled(factor)

    # Soft 1s fade-in/out so music doesn't pop in or cut off abruptly.
    from moviepy.audio.fx import AudioFadeIn, AudioFadeOut

    fade = min(1.0, duration / 4)
    return clip.with_effects([AudioFadeIn(fade), AudioFadeOut(fade)])


def _burn_captions(video_in: Path, ass_path: Path, video_out: Path) -> None:
    """Run FFmpeg to burn ASS captions into a video. Reencodes video, copies audio."""
    try:
        import imageio_ffmpeg  # type: ignore[import-untyped]

        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg_bin = shutil.which("ffmpeg") or "ffmpeg"

    # FFmpeg subtitle filter parsing on Windows: backslashes break the filter
    # syntax, and the drive-letter colon must be escaped.
    ass_arg = str(ass_path).replace("\\", "/").replace(":", r"\:")

    subprocess.run(
        [
            ffmpeg_bin,
            "-y",
            "-i",
            str(video_in),
            "-vf",
            f"subtitles={ass_arg}",
            "-c:a",
            "copy",
            str(video_out),
        ],
        check=True,
        capture_output=True,
    )

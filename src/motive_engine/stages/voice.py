"""Voice stage: render a ContentSpec's voiceover via Kokoro, write WAVs.

The stage takes an injected synthesizer (callable) so tests can swap in a
fake without loading Kokoro. The production factory `make_kokoro_synthesizer`
lazily imports kokoro and returns a closure over a KPipeline.
"""

from __future__ import annotations

import wave
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from motive_engine.schemas import ContentSpec
from motive_engine.schemas.voice_profile import VoiceProfile
from motive_engine.utils import load_yaml

DEFAULT_VOICES_PATH = Path("config") / "voices.yaml"
SAMPLE_RATE = 24_000  # Kokoro outputs 24 kHz mono.

# (text, voice_id, speed) -> iterable of (graphemes, phonemes, audio).
# `audio` is typically a torch tensor; numpy arrays also accepted.
Synthesizer = Callable[[str, str, float], Iterable[tuple[str, str, Any]]]


class VoiceLine(BaseModel):
    """One audio chunk produced by the synthesizer."""

    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=1)
    filename: str = Field(min_length=1)
    graphemes: str
    duration_seconds: float = Field(gt=0)


class VoiceTrack(BaseModel):
    """Voice stage output artifact (serialized as index.json beside the WAVs)."""

    model_config = ConfigDict(extra="forbid")

    spec_id: str
    voice_profile: str
    voice_id: str
    lang_code: str
    speed: float
    sample_rate: int = Field(default=SAMPLE_RATE)
    lines: list[VoiceLine]


# ---- public API ------------------------------------------------------------


def load_voice_profile(
    name: str,
    voices_path: Path = DEFAULT_VOICES_PATH,
) -> VoiceProfile:
    """Look up and validate a voice profile by name in voices.yaml."""
    data = load_yaml(voices_path)
    try:
        voices = data["voices"]
    except (KeyError, TypeError) as e:
        raise ValueError(
            f"{voices_path} is missing a top-level 'voices:' mapping"
        ) from e
    if name not in voices:
        available = ", ".join(sorted(voices)) or "<none>"
        raise KeyError(
            f"Unknown voice profile '{name}' (available: {available})"
        )
    return VoiceProfile.model_validate(voices[name])


def make_kokoro_synthesizer(lang_code: str) -> Synthesizer:
    """Build a synthesizer backed by Kokoro for a specific language code."""
    from kokoro import KPipeline  # type: ignore[import-untyped]

    pipeline = KPipeline(lang_code=lang_code)

    def synth(text: str, voice_id: str, speed: float) -> Iterable[tuple[str, str, Any]]:
        return pipeline(text, voice=voice_id, speed=speed)

    return synth


def render_voice(
    spec: ContentSpec,
    profile: VoiceProfile,
    output_root: Path,
    synthesizer: Synthesizer,
) -> VoiceTrack:
    """Render spec.voiceover via the synthesizer; write per-chunk WAVs + index.json."""
    voice_dir = output_root / spec.id / "voice"
    _clean_voice_dir(voice_dir)
    voice_dir.mkdir(parents=True, exist_ok=True)

    lines: list[VoiceLine] = []
    counter = 0
    for graphemes, _phonemes, audio in synthesizer(
        spec.voiceover, profile.voice_id, profile.speed
    ):
        samples = _to_numpy(audio)
        if len(samples) == 0:
            continue
        counter += 1
        filename = f"line-{counter:03d}.wav"
        _save_wav(voice_dir / filename, samples)
        lines.append(
            VoiceLine(
                index=counter,
                filename=filename,
                graphemes=str(graphemes),
                duration_seconds=len(samples) / SAMPLE_RATE,
            )
        )

    if not lines:
        raise RuntimeError(f"Synthesizer produced no audio for spec {spec.id!r}")

    track = VoiceTrack(
        spec_id=spec.id,
        voice_profile=spec.audio.voice_profile,
        voice_id=profile.voice_id,
        lang_code=profile.lang_code,
        speed=profile.speed,
        lines=lines,
    )
    (voice_dir / "index.json").write_text(
        track.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return track


# ---- internals -------------------------------------------------------------


def _clean_voice_dir(voice_dir: Path) -> None:
    """Remove stale .wav and index.json from a previous run."""
    if not voice_dir.is_dir():
        return
    for f in voice_dir.iterdir():
        if f.is_file() and (f.suffix == ".wav" or f.name == "index.json"):
            f.unlink()


def _to_numpy(audio: Any) -> np.ndarray:
    """Kokoro yields torch tensors on CPU; accept tensor or ndarray."""
    if hasattr(audio, "cpu"):
        return audio.cpu().numpy()
    return np.asarray(audio)


def _save_wav(path: Path, audio: np.ndarray) -> None:
    """Write a mono 16-bit WAV using the stdlib — no soundfile dependency."""
    samples = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(samples.tobytes())

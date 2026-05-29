"""Audition Kokoro voices for the project's voice profiles.

Render the project creed in several candidate voices at hand-picked speeds
and save the WAVs to outputs/voice_auditions/. Listen, then promote the
winners into config/voices.yaml.

Run directly:

    .\\.venv\\Scripts\\python.exe tests\\audition_kokoro_voices.py

Not a pytest test — filename intentionally does not start with test_, so
pytest will not collect it.

First run downloads Kokoro model weights (~325 MB) from Hugging Face.
If that fails with an SSL error, Norton HTTPS Scanning is likely
intercepting the download — same root cause as the earlier pip install
issue.
"""

from __future__ import annotations

import sys
import wave
from pathlib import Path
from typing import Any, TypedDict

import numpy as np

try:
    from kokoro import KPipeline  # type: ignore[import-untyped]
except ImportError as e:
    sys.exit(f"kokoro is not installed in this Python: {e}")


class VoiceTest(TypedDict):
    label: str
    speed: float


OUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "voice_auditions"
SAMPLE_RATE = 24_000


AUDITION_TEXT = """
Hard truth. Clean heart.

No one is coming to organize your life for you.
That is not despair.
That is responsibility.

Start with what is in front of you.
Your room. Your body. Your word. Your work.

Order is not aesthetic.
It is evidence.
"""


# Voice candidates, with curated labels and speeds.
# Voice ID pattern: <lang><gender>_<name>. lang: a=American, b=British.
VOICE_TESTS: dict[str, VoiceTest] = {
    "am_michael": {"label": "Main modern hard-truth voice",         "speed": 0.92},
    "am_adam":    {"label": "Firmer, darker hard-truth voice",      "speed": 0.92},
    "bm_george":  {"label": "Classical Stoic / ancient wisdom",     "speed": 0.88},
    "bm_lewis":   {"label": "Literary, reflective, field-notes",    "speed": 0.88},
    "af_heart":   {"label": "Warm contrast voice",                  "speed": 0.92},
    "af_nicole":  {"label": "Soft reflective contrast voice",       "speed": 0.92},
}


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


def synthesize(pipeline: KPipeline, voice: str, text: str, speed: float) -> Path:
    """Generate one voice sample (concatenating all chunks) and save as WAV."""
    chunks = [_to_numpy(audio) for _, _, audio in pipeline(text, voice=voice, speed=speed)]
    if not chunks:
        raise RuntimeError(f"no audio generated for voice {voice!r}")
    full = np.concatenate(chunks)
    out_path = OUT_DIR / f"{voice}.wav"
    _save_wav(out_path, full)
    return out_path


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUT_DIR}")
    print(f"Sample text: {len(AUDITION_TEXT.split())} words\n")

    # One pipeline per language code; voices route by their first letter.
    needed_langs = sorted({v[0] for v in VOICE_TESTS})
    print(f"Loading Kokoro pipelines: {needed_langs}")
    print("(First run downloads model weights from Hugging Face — ~325 MB)\n")

    pipelines: dict[str, KPipeline] = {}
    for lang in needed_langs:
        try:
            pipelines[lang] = KPipeline(lang_code=lang)
        except Exception as e:
            print(f"Failed to load pipeline for lang_code={lang!r}:\n  {e}")
            print(
                "\nIf this is an SSL/cert error, Norton HTTPS Scanning may be "
                "intercepting Hugging Face downloads. Same root cause as the "
                "earlier pip install issue."
            )
            return 2

    failures: list[tuple[str, str]] = []
    for voice, settings in VOICE_TESTS.items():
        label = settings["label"]
        speed = settings["speed"]
        lang = voice[0]
        print(f"  rendering {voice:11s} @ speed {speed} — {label}")
        try:
            out_path = synthesize(pipelines[lang], voice, AUDITION_TEXT, speed)
            print(f"      saved {out_path.name}")
        except Exception as e:
            failures.append((voice, str(e)))
            print(f"      FAILED: {e}")

    print()
    if failures:
        print(f"{len(failures)} voice(s) failed:")
        for v, msg in failures:
            print(f"  {v}: {msg}")
        print()
    print(f"Listen in: {OUT_DIR}")
    print("Promote the winners into config/voices.yaml under voices.<name>.voice_id")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

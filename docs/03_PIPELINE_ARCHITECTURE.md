# 03 — Pipeline Architecture

## Shape

A linear pipeline of independent stages. Each stage reads typed input from disk, does one thing, and writes typed output to disk. No stage calls the next stage directly.

```
spec(YAML) -> visual-prompts -> images (local ComfyUI) -> voice -> captions -> render -> review -> (manual) publish
```

## The core design principle

```
You define the world.
AI makes assets inside the world.
Python assembles the film.
You approve the result.
```

The engine is **not** "AI makes everything and you hope it looks good." AI is used only for **still visual assets**, inside a defined world (see [02_VISUAL_WORLDS.md](02_VISUAL_WORLDS.md)). All composition, animation, voice, captions, and final assembly happen locally in Python. The operator approves before anything ships.

## Why stages on disk

- **Resumable.** Re-run any stage from the previous stage's artifact.
- **Inspectable.** Open any intermediate file and read it.
- **Testable.** Each stage is a pure-ish function of its input artifact.
- **Swappable.** Implementations change; the artifact contract holds.

## Stage contracts

Each stage has:

- A **Pydantic model** for input/output where structured data crosses the boundary.
- A **CLI command** under `motive <stage>`.
- A **per-draft directory** on disk (`outputs/drafts/<id>/`) where artifacts live.

| Stage           | Input                  | Output            | Artifact                                       | Status                       |
| --------------- | ---------------------- | ----------------- | ---------------------------------------------- | ---------------------------- |
| spec            | operator's YAML        | `ContentSpec`     | validated in-memory                            | **shipped (M1)** — PyYAML    |
| visual-prompts  | `ContentSpec` + world  | image prompts     | printed positive + negative prompts            | **shipped (M2)**             |
| images          | `ContentSpec` + prompts | PNG backgrounds  | `assets/backgrounds/<world>/<key>.png`         | **shipped (M2.5)** — local ComfyUI HTTP |
| voice           | `ContentSpec`          | `VoiceTrack`      | `outputs/drafts/<id>/voice/*.wav`              | **shipped (M3)** — Kokoro TTS |
| captions        | `ContentSpec` + voice  | ASS / SRT         | `outputs/drafts/<id>/captions.ass`             | **shipped (M4)**             |
| render          | all above              | MP4               | `outputs/drafts/<id>/<id>.mp4`                 | **shipped (M5)** — MoviePy / FFmpeg |
| review          | draft                  | move decision     | promote to `outputs/approved/` or `outputs/rejected/` | **shipped (M6)** — Streamlit UI |
| publish         | approved render        | (out-of-process)  | manual upload by the operator                  | OUT OF SCOPE                 |

See [06_MVP_ROADMAP.md](06_MVP_ROADMAP.md) for milestone detail.

## Editorial gate

There is no automated ethics check in the MVP. Scripts are hand-authored in YAML and are the operator's responsibility. [01_CONTENT_PHILOSOPHY.md](01_CONTENT_PHILOSOPHY.md) is the gate — the operator reads and applies it. An automated gate may be added later if it earns its way in.

## The human approval gate

`review` is the only stage that requires a human to act. The CLI surfaces `<id>.mp4` and the operator chooses **approve**, **revise**, or **reject**. Approved drafts move to `outputs/approved/`. Rejected drafts move to `outputs/rejected/`. There is no automatic path from `render` to `publish`.

## Directory layout (runtime)

```
outputs/
  drafts/
    <id>/
      prompts.json
      voice/
        line-001.wav
      captions.ass
      <id>.mp4
  approved/
  rejected/
```

`outputs/` is local-only and should be gitignored.

## Code layout (current and intended)

```
src/motive_engine/
  __init__.py
  cli.py                  # Typer app — one subcommand per stage
  schemas/
    __init__.py
    content_spec.py       # ContentSpec, VisualSpec, AudioSpec, RenderSpec
  utils/
    __init__.py
    yaml_loader.py
  # planned next:
  # stages/
  #   visual_prompts.py
  #   voice.py
  #   captions.py
  #   render.py
  #   review.py
```

This document is the source of truth for stage boundaries. If an implementation needs to break a boundary, update this document first.

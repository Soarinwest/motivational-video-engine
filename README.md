# motive-engine

> Hard truth. Clean heart.

A local-first **cinematic quote-film engine**. Short-form motivational videos with a clear aesthetic and a clear ethical line. Discipline without resentment. Human approval before anything ships.

## Status

**M1 — Spec validation.** YAML content specs can be authored and validated. Rendering, voice, and review are planned but not yet implemented. See [docs/06_MVP_ROADMAP.md](docs/06_MVP_ROADMAP.md).

## Core design principle

```
You define the world.
AI makes assets inside the world.
Python assembles the film.
You approve the result.
```

AI generates only **still visual assets**. All composition, animation, voice, captions, and final assembly happen locally. No third-party AI video generator.

## Prerequisites

- **Python 3.11+**
- **FFmpeg** on `PATH` — required later by MoviePy (not needed for M1)

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Validate a spec

```powershell
motive validate-spec examples/specs/marcus_self_command.yaml
```

Three example specs ship in [examples/specs/](examples/specs/). Run validate-spec on each.

## Test

```powershell
pytest
```

## Pipeline

```
spec(YAML) -> visual-prompts -> [external: AI image gen] -> voice -> captions -> render -> review -> (manual) publish
```

See [docs/03_PIPELINE_ARCHITECTURE.md](docs/03_PIPELINE_ARCHITECTURE.md) for stage contracts.

## Stack

- **Typer** + **rich** — CLI
- **Pydantic v2** — typed schemas
- **PyYAML** — content specs + config
- **SQLModel** on **SQLite** — later, run state
- **Kokoro TTS** — later, local voiceover
- **MoviePy** (FFmpeg) — later, vertical short-form render
- **Streamlit** — later, local review UI
- **pytest** — tests

## Principles

- **Local-first.** Runs on your machine. No mandatory cloud.
- **Typed contracts.** Stage boundaries are Pydantic models.
- **Resumable.** Any stage can be re-run from prior artifacts.
- **Human in the loop.** Nothing publishes automatically.

## Read next

- [Project vision](docs/00_PROJECT_VISION.md)
- [Content philosophy](docs/01_CONTENT_PHILOSOPHY.md)
- [Visual worlds](docs/02_VISUAL_WORLDS.md)
- [Pipeline architecture](docs/03_PIPELINE_ARCHITECTURE.md)
- [MVP roadmap](docs/06_MVP_ROADMAP.md)

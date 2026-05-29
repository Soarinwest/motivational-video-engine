# Content Library Index

The content library is the source-of-truth corpus for everything the motive-engine produces. It is the humanities side of the project: texts, ideas, themes, traditions, ethical guardrails, and the scaffolding that connects all of them to the video pipeline.

## Why sources are separated from eras, traditions, themes, and series

A canonical source entry lives in one place — under `sources/`. Eras, traditions, themes, series, arcs, and per-video scripts are *references* to those sources, not copies. This lets one quote belong to many categories without ever being duplicated. Update the canonical entry and every cross-reference is up to date by definition.

The structure is:

- `sources/` — canonical quote/paraphrase entries live here, keyed by stable IDs
- `eras/` — when was it written
- `traditions/` — what intellectual school does it belong to
- `themes/` — what motivational idea does it support
- `series/` — recurring video series (a content lens: who it speaks to, what tone)
- `arcs/` — multi-video arcs grouped under a region/era (a publishing-order lens)
- `scripts/` — individual ~30-second video scripts, nested by region and arc
- `choreography/` — season-level publishing plans

## The four classification axes

Every source is classified along four independent axes:

1. **Era written** — the historical period the text was authored (e.g. `ancient_rome`)
2. **World depicted** — the historical period or setting the text portrays (often, but not always, the same as era written)
3. **Intellectual tradition** — the school of thought (`stoicism`, `existentialism`, `christian_wisdom`, etc.)
4. **Motivational theme** — the directly usable idea (`self_command`, `duty`, `courage`, `mortality`)

Axes 1 and 2 are separated because, for example, Shakespeare wrote in early modern England (era written) but *Julius Caesar* depicts ancient Rome (world depicted). The visual world we draw assets from is the depicted one.

## How this supports video generation

The pipeline reads canonical source entries and pairs them with assets:

```
source text
  -> quote / paraphrase (sources/)
    -> core idea
      -> interpretation
        -> script angle (sources/ video.script_angle)
          -> per-video script (scripts/<region>/<arc>/NNN.yaml)
            -> arc grouping (arcs/)
              -> season choreography (choreography/)
                -> render and review
```

Each video draft is the product of one source entry, one script, one arc, one visual world, and one voice profile.

## Core principle

**Hard truth. Clean heart.**

Masculine discipline without resentment. The output should sharpen the viewer, not flatter them — and never punch down. See [03_CONTENT_ETHICS.md](03_CONTENT_ETHICS.md) for the explicit boundaries.

## Separation of voices

Within any source entry, these fields are kept distinct:

- **Direct quote** — exact translated text, used only when rights are clear
- **Paraphrase** — restatement in modern English, safe for any source
- **Core idea** — the underlying claim, abstracted away from any specific wording
- **Interpretation** — the project's own commentary; the only place editorial voice speaks
- **Script angle** — direction for one video script
- **Per-video script** (in `scripts/`) — the actual ~30-second draft text

Mixing these is the easiest way to get rights and ethics wrong. Keep them separate.

## Where to go next

- [01_SCHEMA.md](01_SCHEMA.md) — canonical source-entry schema, field by field
- [02_TAXONOMY.md](02_TAXONOMY.md) — full taxonomy across eras and traditions
- [03_CONTENT_ETHICS.md](03_CONTENT_ETHICS.md) — what the project will and will not produce
- [04_RIGHTS_AND_SOURCE_NOTES.md](04_RIGHTS_AND_SOURCE_NOTES.md) — copyright, licensing, attribution
- [05_VISUAL_WORLD_MAP.md](05_VISUAL_WORLD_MAP.md) — how content maps to the visual worlds in `assets/backgrounds/`
- [06_SERIES_MAP.md](06_SERIES_MAP.md) — the recurring video series under `series/`
- [07_ARCS_AND_PRODUCTION.md](07_ARCS_AND_PRODUCTION.md) — arcs, per-video scripts, and choreography
- [08_PLANNED_ARCS.md](08_PLANNED_ARCS.md) — master content roadmap: every planned arc across every region, with status
- [templates/](templates/) — copy-paste starting points for new entries

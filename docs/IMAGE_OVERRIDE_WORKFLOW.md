# Pointing a script at a specific image file

The default render path resolves the background by the world+bg_key registry — `assets/backgrounds/<world>/<bg_key>.png`. That works when the bg is registered as a `background_prompt` in [config/visual_worlds.yaml](../config/visual_worlds.yaml).

When you want to render a script with **a specific image file** — without registering a new prompt key, without moving files around — set `image_path:` on the script.

## How to override

Edit the script YAML, e.g. [content_library/scripts/ancient_greece/odyssey/018_homer_bind_me_tighter.yaml](../content_library/scripts/ancient_greece/odyssey/018_homer_bind_me_tighter.yaml):

```yaml
voice: bm_lewis
music: island_enchantment
visual_world: odyssey
visual_motif: "view from inside a vast sea cave..."
caption_style: sparse_centered_captions

# This line wins over the world/bg_key lookup
image_path: "assets/figures/feminine/sirens/sirens_over_black_rocks.png"
```

The path is **repo-relative** (starts at the repo root). It can point at anything:
- A file in `assets/backgrounds/<some-world>/...`
- A file in `assets/figures/<archetype>/...`
- A file in any new folder you create
- A one-off image you dropped into the repo

## Re-rendering a single spec

After editing the script:

```pwsh
# 1. Regenerate the spec from the script YAML
.venv\Scripts\python.exe scripts\generate_ancient_greece_drafts.py

# 2. (Optional) lint the spec to catch typos
.venv\Scripts\python.exe -m motive_engine.cli lint outputs\specs\ancient_greece\odyssey\homer_bind_me_tighter_001.yaml

# 3. Re-make captions (fast, no voice re-gen)
.venv\Scripts\python.exe -m motive_engine.cli make-captions outputs\specs\ancient_greece\odyssey\homer_bind_me_tighter_001.yaml

# 4. Re-render the MP4
.venv\Scripts\python.exe -m motive_engine.cli render outputs\specs\ancient_greece\odyssey\homer_bind_me_tighter_001.yaml
```

You only need to re-run `make-voice` if you changed the script text. The captions and render steps pick up the new image automatically.

## When to use the override vs the registry

| Use case | Recommended |
|---|---|
| You're authoring a new arc, want shared visual vocabulary | Register prompts in `visual_worlds.yaml`, use `bg_key` |
| You want to swap one script to a different existing PNG | `image_path:` override |
| You want a figure asset (Sirens, Athena) to *be* the hero image | `image_path:` override pointing at the figure file |
| You replaced or moved a PNG and don't want to chase down every bg_key | `image_path:` override |
| You're doing a one-off creative pass on a single script | `image_path:` override |

The override does not register a prompt in `visual_worlds.yaml`. If you want the bg to be discoverable by the prompt-generation tools (`motive make-image-prompt`), register it as a `background_prompt` and use the `bg_key` flow instead.

## How it works (one paragraph)

The script YAML's `image_path:` is passed through the transformer into the spec YAML as `visual.background_override_path`. The render stage ([src/motive_engine/stages/render.py](../src/motive_engine/stages/render.py)) checks `background_override_path` *first* — when present, it resolves to that exact file and skips the world/key registry lookup. The lint stage ([src/motive_engine/lint.py](../src/motive_engine/lint.py)) also skips the bg_key registration check when the override is set. The figure layer is unaffected — figures still resolve via `assets/figures/<world>/<figure_prompt_key>.*`.

## Two examples already wired up

- [011_antigone_unwritten_laws.yaml](../content_library/scripts/ancient_greece/women_law_tragedy/011_antigone_unwritten_laws.yaml) — original bg `temple_above_sea.png` was removed; the override points at `ancient_greece_temple_cliff_storm_001.png` instead. No structural change to the ancient_greece world's prompt registry.
- [018_homer_bind_me_tighter.yaml](../content_library/scripts/ancient_greece/odyssey/018_homer_bind_me_tighter.yaml) — points at the Sirens figure asset, since the figure image actually depicts the scene the script narrates.

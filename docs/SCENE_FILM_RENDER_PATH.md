# Scene-Film: A Second Render Path for Narrative Beats

**Status:** Planning doc. Implementation deferred until quote-film matures.
**Source:** Mirrored from the per-user plan at `~/.claude/plans/lets-write-it-up-jazzy-wilkes.md`.

## Context

motive-engine currently ships one render path: the **quote-film**. A single still background is generated via local ComfyUI (SDXL Juggernaut workflow at [../config/comfyui_workflow.json](../config/comfyui_workflow.json)), then [../src/motive_engine/stages/render.py](../src/motive_engine/stages/render.py) pans/zooms it with PIL AFFINE while Kokoro narrates a ~30s monologue and an ASS caption track is burned in. The output is one pull-quote, one image, one voice. As of the last commit-ready state in this session: ~50 specs across 11 arcs, all rendered as quote-films.

This is the right format for philosophy and aphorism (Stoic practice, Marcus's notebook, Antigone's defiance). It is the wrong format for **narrative** — story beats where the meaning lives in *what happens between two characters in three seconds*. The Iliad's farewell at the Scaean Gates, Penelope at the loom unweaving by lamplight, Cincinnatus walking back to his plow — these are scenes, not quotes. Trying to render them as one static image flattens them.

The goal: a **second** render path — "scene-film" — that uses ComfyUI's *video* models to produce 30-60s narrative beats from the same source library. Quote-film stays as-is; scene-film is parallel infrastructure that any spec can opt into.

This doc is parked for revisit. The right time to come back is after the existing quote-film system has matured further (figure pipeline shipped, Season 02 fully reviewed, the difference between "quote-film is enough" and "this entry deserves a scene" legible from inside the project).

## Goals

- A new render path that turns one entry from `content_library/sources/*/work.md` into a multi-beat narrative video (30-60s).
- Shared input layer: the same arc YAMLs, source entries, and (optionally) the same `speaker`/`addressee`/`scene_context` fields drive both paths.
- Local-first: all ComfyUI work, all voice synthesis, all assembly stays on the user's machine. No cloud video APIs.
- Coexists with quote-film; no breaking changes to the existing pipeline or any rendered draft.

## Non-goals

- Replacing quote-film. It remains the default for aphoristic material.
- Lip-sync, facial animation, or "talking-head" AI video. Out of scope; current models are not good enough and the brand voice would suffer.
- Auto-generating dialogue. The dialogue is human-written, just as scripts are now.
- Real-time generation. A 30s scene will take 10-30 minutes of local generation; that is acceptable.

## The architectural shift

```
quote-film (current):   spec.yaml → 1 image (ComfyUI SDXL) → 1 Kokoro voice
                                  → ASS captions → MoviePy assemble → 30s MP4

scene-film (new):       scene.yaml → N beat clips (ComfyUI video model)
                                   → multi-voice Kokoro (one per character)
                                   → ASS captions, dialogue style
                                   → FFmpeg concat + audio mix → 30-60s MP4
```

Same input layer (sources, arcs). Different output layer (beats vs single image, multi-voice vs monologue, video model vs SDXL).

## Pipeline shape

A parallel pipeline under a new namespace:

```
src/motive_engine/scenes/                  # new module, mirrors stages/
  schemas.py            # SceneSpec, Beat, Character (Pydantic)
  scene_prompts.py      # SceneSpec → per-beat ComfyUI video workflow inputs
  make_beats.py         # POSTs to local ComfyUI video workflow per beat
  make_scene_voices.py  # multi-character Kokoro voice gen, one wav per beat
  make_scene_captions.py # ASS with dialogue formatting + speaker tags
  assemble_scene.py     # FFmpeg concat beats + mix voices + music + captions
```

CLI grows a subcommand group: `motive scene <command> <scene.yaml>` mirroring `motive validate-spec / make-images / make-voice / render` for the new path. The existing Typer entry point at [../src/motive_engine/cli.py](../src/motive_engine/cli.py) gets a `scene` sub-app rather than additional top-level commands.

## SceneSpec sketch

```yaml
scene_id: iliad_hector_farewell_scene
arc_id: ancient_greece_iliad
quote_source_id: homer_iliad_hector_farewell   # links back to source entry
duration_target_seconds: 35

characters:
  - id: narrator
    voice: bm_george              # Kokoro voice slug, config/voices.yaml
  - id: hector
    voice: bm_lewis
  - id: andromache
    voice: af_sarah               # to be added to config/voices.yaml

music_profile: somber_cinematic
caption_style: scene_dialogue     # new style, speaker prefix + lower-third

beats:
  - id: 1
    duration_seconds: 4
    visual_prompt: "Bronze-age city gate at dusk, Greek camp in distance, warrior approaching"
    camera: "slow push toward the gate"
    speaker: narrator
    line: "Book Six of the Iliad. Hector at the Scaean Gates."
  - id: 2
    duration_seconds: 5
    visual_prompt: "..."
    camera: "static"
    speaker: andromache
    line: "If you fall, my comfort is to die."
  # ...
```

A SceneSpec validates against a Pydantic schema parallel to ContentSpec in [../src/motive_engine/schemas.py](../src/motive_engine/schemas.py) — same patterns, new shape.

## What carries over from quote-film (reuse, do not reimplement)

- **Source library**: `content_library/sources/*/work.md`. SceneSpec references `quote_source_id` exactly as ContentSpec does — no duplication.
- **Arc YAMLs**: `content_library/arcs/*.yaml`. A single arc may now list both `scripts:` (quote-films) and `scenes:` (scene-films).
- **Voice tech**: Kokoro via [../src/motive_engine/stages/voice.py](../src/motive_engine/stages/voice.py). Multi-voice = multiple calls with different `voice_profile` lookups from [../config/voices.yaml](../config/voices.yaml). New female voice slugs (e.g., for Andromache, Helen, Penelope) get added to that config.
- **Caption format**: ASS V4+ from [../src/motive_engine/stages/captions.py](../src/motive_engine/stages/captions.py). New `scene_dialogue` style added alongside `serif_quiet`.
- **Music mixing**: same `music_profile` slugs from [../config/brand.yaml](../config/brand.yaml), same `_load_music_track` helper from render.py.
- **Review gate**: same human-approval rule, same `outputs/drafts/<id>/<id>.mp4` convention.
- **FFmpeg via imageio_ffmpeg**: no system install. Already proven.

## What's actually new

1. **ComfyUI video workflow JSON** (new file: `config/comfyui_video_workflow.json`). Mirrors the structure of the existing image workflow at [../config/comfyui_workflow.json](../config/comfyui_workflow.json) — a JSON template with token slots (`__POSITIVE__`, `__NEGATIVE__`, `__SEED__`, `__DURATION_FRAMES__`, `__FILENAME_PREFIX__`) that the new `make_beats.py` substitutes per beat.
2. **Per-beat asset directory layout**:
   ```
   outputs/drafts/<scene_id>/beats/beat_001.mp4, beat_002.mp4, ...
                            /voice/beat_001.wav, ...
                            /captions.ass
                            /<scene_id>.mp4    # final concat
   ```
3. **Multi-voice Kokoro pacing**: each beat has at most one speaker line; voices align to beat duration with leading/trailing silence padding.
4. **FFmpeg concat with audio mix**: stitches beat clips end-to-end, overlays per-beat voice tracks at the beat's offset, mixes music underneath, then burns captions in a final pass — same two-pass pattern render.py already uses for libass.

## Critical technical risks (call out now, don't discover late)

1. **Character continuity across cuts**. All current open-weights video models drift on character identity between independent clips. The same warrior looks different in beat 3 vs beat 6. Three mitigations, in increasing effort:
   - *Cinematic discipline*: wide shots, silhouettes, no on-face cuts, longer beats (5-7s instead of 3-4s). Prove the pipeline with single-figure scenes first.
   - *Reference-image conditioning*: most video models accept a still as the first frame. Use a fixed reference image (or one of the new alpha figures from `assets/figures/<archetype>/`) as the anchor for every clip featuring that character.
   - *Character LoRAs*: train a tiny LoRA per recurring character on 20-50 reference images. Highest-fidelity but requires a training pass and per-arc LoRA management.
2. **Render time**. RTX 3080 10GB realistic options: LTX-Video (fastest, ~30s per 5s clip), Wan 2.1 quantized (best quality, ~2-3 min per clip), CogVideoX-5B (middle). A 30s scene = 6-10 beats = 5-30 minutes of pure ComfyUI generation per render attempt.
3. **Voice acting in Kokoro**. Excellent for narration, decent for restrained dialogue, weak for emotion. The brand register favors restraint anyway — design scenes around narration carrying meaning with sparse dialogue, not the other way around.
4. **Brand drift risk**. Multi-clip scenes with characters tilt easily toward "AI cinema slop." The countermove is structural: fewer cuts than instinct says, longer beats than instinct says, wider compositions than instinct says, no attempt at facial expression nuance. The series's tone is sparse and weighty, not theatrical.
5. **ComfyUI video models are large downloads**. 10-30 GB for the model + VAE per choice. Plan for that the first time the path is exercised.

## Recommended first pilot

Smallest meaningful slice that proves the pipeline shape:

- **Source**: `homer_odyssey_penelope_patience` (already in [../content_library/sources/homer/odyssey.md](../content_library/sources/homer/odyssey.md))
- **Scene**: Penelope at the loom — single figure, one room, day-to-night transition with the unweaving
- **Beats**: 4-5 beats, 30s total
- **Voices**: narrator only (no dialogue) — leans on Kokoro's strongest mode
- **Continuity strategy**: reference-image conditioning using an existing Penelope figure asset
- **Model**: LTX-Video (fast iteration cycle for pipeline debugging)

This avoids the multi-character continuity problem entirely on the first pass, while still exercising every other piece (SceneSpec → beat workflow → multi-clip voice timing → FFmpeg concat).

Successor pilots, in order of complexity:
1. **Cincinnatus at the plow** — one figure, two locations (field + path home), single distant supporting figure
2. **Marcus alone by the lamp** — one figure, interior, brief narrator + brief Marcus voiceover (introduces multi-voice without character continuity demands across cuts)
3. **Hector's farewell** — three characters, on-screen interaction (only after character-LoRA strategy is decided)

## Open decisions for the user to make at revisit time

1. **Which ComfyUI video model for the pilot?** LTX-Video (fastest, lowest quality bar), Wan 2.1 quantized (best quality, slowest), CogVideoX-5B (middle).
2. **Where does the new module live?** `src/motive_engine/scenes/` (parallel to `stages/`) or `src/motive_engine/stages/scene_*.py` (folded into existing stages namespace)?
3. **Same arcs or new "scene-only" arcs?** Recommend: same arcs. The arc YAML grows a `scenes:` list alongside the existing `scripts:` list. One source entry can feed both a quote-film and a scene-film.
4. **Continuity strategy on day one** — single-figure pilot only (no character continuity work yet), or invest in IP-Adapter / first-frame reference conditioning from the start?
5. **Review gate placement** — review per-beat (catch continuity drift early, costlier feedback loop) or whole-scene only (faster iteration but late discovery of failures)?
6. **New caption style** — does dialogue need a different style than `serif_quiet`? Probably yes: speaker prefix ("HECTOR:") + lower-third positioning + smaller font. Sketch: `scene_dialogue` style added to [../src/motive_engine/stages/captions.py](../src/motive_engine/stages/captions.py).
7. **Female voices in `config/voices.yaml`**. Penelope, Andromache, Helen, Calypso, Circe, Thetis, Hera, Athena all need female Kokoro voice slugs. Pick 2-3 (e.g., a "literary female" + "severe female" + "tender female") rather than per-character voices.

## Files that will be created when implementation begins

```
src/motive_engine/scenes/__init__.py
src/motive_engine/scenes/schemas.py
src/motive_engine/scenes/scene_prompts.py
src/motive_engine/scenes/make_beats.py
src/motive_engine/scenes/make_scene_voices.py
src/motive_engine/scenes/make_scene_captions.py
src/motive_engine/scenes/assemble_scene.py
config/comfyui_video_workflow.json
content_library/scenes/<region>/<arc>/<NNN>_<slug>.yaml   # new content type
tests/test_scene_schemas.py
tests/test_scene_prompts.py
tests/test_assemble_scene.py
```

## Files that will be modified (small surface)

- [../src/motive_engine/cli.py](../src/motive_engine/cli.py) — add `scene` sub-app
- [../config/voices.yaml](../config/voices.yaml) — add 2-3 female voice profiles
- [../src/motive_engine/stages/captions.py](../src/motive_engine/stages/captions.py) — add `scene_dialogue` style preset
- [../content_library/01_SCHEMA.md](../content_library/01_SCHEMA.md) — document the SceneSpec shape alongside ContentSpec
- Arc YAMLs that get a `scenes:` list (e.g., `ancient_greece_odyssey.yaml` once Penelope pilot ships)

## Verification when implementation lands

End-to-end test on the Penelope pilot:

1. `motive scene validate-spec content_library/scenes/ancient_greece/odyssey/001_penelope_loom.yaml` — pass
2. `motive scene make-beats <spec>` — produces N beat MP4s under `outputs/drafts/<scene_id>/beats/`. Manually eyeball each; reject if continuity drifts.
3. `motive scene make-voice <spec>` — produces N voice WAVs aligned to beat durations
4. `motive scene make-captions <spec>` — produces a single ASS with per-beat dialogue blocks and the `scene_dialogue` style
5. `motive scene assemble <spec>` — produces `outputs/drafts/<scene_id>/<scene_id>.mp4` (30s, captions burned in, music mixed)
6. `pytest -q` — all existing tests still pass (no regressions to quote-film); new tests pass for SceneSpec validation, beat-prompt expansion, and concat assembly

Acceptance bar: a watchable 30s Penelope-at-the-loom MP4 with one narrator voice, four beats that hold visual continuity well enough to read as one continuous scene, and the same Kokoro+ASS+music stack the quote-film pipeline already proves.

## Why this plan, not implementation now

Quote-film still has structural work to finish first:
- Figure compositing pipeline is unexercised (every shipped spec uses `figure_prompt_key: "none"`)
- Three arcs in Season 02 are content-complete but the figures-vs-backgrounds principle hasn't actually been wired into renders yet
- Seasons 03 (Late Antiquity), 04 (Norse), 05 (Renaissance) are entirely empty
- Translation verification on existing quote-films is still pending across most entries

Adding a second render path before quote-film is mature would dilute focus. The right time to come back is once the figure pipeline ships and Season 02 is fully reviewed and approved for publishing. That's when the difference between "quote-film is enough" and "this entry deserves a scene" becomes legible from inside the project.

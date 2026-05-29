# Source Entry Schema

Every entry in the content library follows this schema. Entries live inside `sources/<author>/<work>.md` files as YAML blocks separated by `---` lines.

## Canonical example

```yaml
id: marcus_meditations_self_command_001

source:
  author: Marcus Aurelius
  work: Meditations
  section: Book 2
  translator: null
  source_url: null
  rights_status: public_domain_translation_needed
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - self_command
    - duty
    - mortality
  tone:
    - severe
    - restrained
    - direct

content:
  direct_quote: ""
  paraphrase: "You do not rule the world. You rule the part of yourself that responds to it."
  core_idea: "Freedom begins with control over judgment and action."
  interpretation: "The first kingdom is the mind."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_rome_self_command
  visual_worlds:
    - stoic_rome
  visual_motif: "weathered marble bust in ruined courtyard at dawn"
  voice_profile: bm_george
  music_profile: stoic_low_strings
  caption_style: marble_serif_centered
  script_angle: "A man is not free if every appetite commands him."
  final_line: "Rule there first."

review:
  human_review_required: true
  notes: ""
```

## Field meanings

### Top-level

- **id** — unique stable identifier. Format: `{author_or_work}_{topic_or_theme}_{NNN}`. Examples: `marcus_meditations_self_command_001`, `plato_apology_unexamined_life`, `roosevelt_arena_courage_001`. The ID is the join key referenced by eras, traditions, themes, series, arcs, and per-video scripts. **Once published, do not change it.**

### `source`

- **author** — historical author. Use canonical English spelling.
- **work** — title of the work the passage comes from.
- **section** — book, chapter, line, verse, or scene reference.
- **translator** — translator name, or `null` if not yet identified.
- **source_url** — link to the public-domain edition used, when available.
- **rights_status** — controlled vocabulary; see [04_RIGHTS_AND_SOURCE_NOTES.md](04_RIGHTS_AND_SOURCE_NOTES.md).
- **translation_check_needed** — `true` until the exact wording has been verified against the cited edition. Drafts with this set to `true` should not be published.
- **notes** — free text on edition, accuracy, or sourcing concerns.

### `classification`

- **era_written** — slug matching a file under `eras/`. When the source was authored.
- **world_depicted** — slug for the historical setting portrayed. Often equal to `era_written`. For Shakespeare's *Julius Caesar*, `era_written` is `renaissance_early_modern` but `world_depicted` is `ancient_rome`.
- **region** — high-level region/era slug used for grouping arcs and per-video scripts (e.g. `ancient_greece`, `ancient_rome`, `medieval_world`). Matches the first folder under `scripts/<region>/`.
- **traditions** — list of slugs matching files under `traditions/`. A source can sit in more than one.
- **themes** — list of slugs matching files under `themes/`. A source usually carries several.
- **tone** — short tag list describing emotional register. Free vocabulary, but stay consistent. Common: severe, restrained, direct, elegiac, defiant, mournful, ironic.

### `content`

This is the cluster where rights and editorial voice are kept apart. **Always fill at least one of `direct_quote`, `paraphrase`, `core_idea`.**

- **direct_quote** — exact translated text. Use only when `rights_status` is `public_domain_original`, `public_domain_translation`, or `cc0`. Leave empty otherwise.
- **paraphrase** — your own restatement in modern English. Always safe to use. Preferred for copyrighted material and for video voiceover (more accessible to a modern ear).
- **core_idea** — the underlying claim, abstracted away from any specific wording. One sentence.
- **interpretation** — the project's editorial commentary. The only field where the project's own voice speaks. Keep it short and severe — one or two sentences.

### `video`

- **series** — list of slugs matching files under `series/`. Which recurring video series this entry can feed.
- **arcs** — list of arc slugs matching files under `arcs/`. Which multi-video arcs the entry belongs to.
- **visual_worlds** — list of slugs matching folders under `assets/backgrounds/`. Which visual worlds fit the entry.
- **visual_motif** — short free-text description of the specific composition within a visual world (e.g. `"athenian agora at dusk"`, `"shoreline at dawn, ship silhouette"`).
- **voice_profile** — Kokoro TTS voice identifier (e.g. `bm_george`, `bm_lewis`, `am_michael`).
- **music_profile** — slug for a music bed (e.g. `ancient_low_drone`, `low_strings`, `somber_cinematic`).
- **caption_style** — slug for caption typography and layout (e.g. `marble_serif_centered`, `parchment_lower_third`).
- **script_angle** — single sentence giving direction for one video script. Not the full script — the full draft lives in `scripts/<region>/<arc>/<NNN>.yaml`.
- **final_line** — the closing line of the eventual video. Often the most quotable part. Optional but recommended.

### `review`

- **human_review_required** — defaults to `true`. The project's hard rule: a human reviews and approves before publishing.
- **notes** — review-stage notes (translation to verify, ethics flag to check, etc.).

## Important rules

- **`direct_quote` is the dangerous field.** If you cannot prove the translation is in the public domain, leave it empty and use `paraphrase` instead. See [04_RIGHTS_AND_SOURCE_NOTES.md](04_RIGHTS_AND_SOURCE_NOTES.md).
- **`paraphrase` is the workhorse field.** Most video voiceovers will use it.
- **`interpretation` is the project's added value.** Without it the channel is quote-recycling. With it the channel has a point of view.
- **`script_angle` is direction, not script.** The actual ~30-second draft lives in `scripts/<region>/<arc>/<NNN>.yaml`. See [07_ARCS_AND_PRODUCTION.md](07_ARCS_AND_PRODUCTION.md).
- **`translation_check_needed: true` blocks publishing.** A draft with this flag must not be rendered to final until the wording is verified against the cited edition.

## Multiple entries per file

A single work (e.g. `meditations.md`) holds many entries. Separate them with `---`:

```yaml
id: marcus_meditations_self_command_001
...
---
id: marcus_meditations_duty_002
...
```

The file is the work. Each YAML block is one entry. The ID is the join key.

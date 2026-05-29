# 02 — Visual Worlds

The engine builds video by *composing within a world*. A world is a defined aesthetic vocabulary — palette, mood, motifs, lighting — that every asset, overlay, and motion in a video respects.

Four worlds ship for the MVP. New worlds are added as new entries in [config/visual_worlds.yaml](../config/visual_worlds.yaml) with no code changes.

## The four worlds

### 1. stoic_rome
Marble busts, ruined courtyards, columns, storm light, ash, dawn. Severe, disciplined, ancient. Default for the `stoic_practice` series.

### 2. ancient_greece
Greek temples above the sea, agora in shadow, classical figures, sun-bleached stone. Default for `socratic_questions`.

### 3. literary_dark
Candlelit desks, old books and manuscript pages, rain on windows. Interior, quiet, weighty. Default for the `literary_dark` series.

### 4. field_notes
Forests, mountains, weather, recovering land. No human figure. Observational. Default for `field_notes`.

## Why named worlds, not free-form prompts

Two reasons:

1. **Throughline.** A series should *feel like itself* across many videos. The world is the visual constant; the spec varies what happens inside it.
2. **Operator control.** AI generates *assets inside* a defined world, not the world itself. The aesthetic is yours, not the model's.

See [05_PROMPT_LIBRARY.md](05_PROMPT_LIBRARY.md) for how a world definition turns into an image-generator prompt.

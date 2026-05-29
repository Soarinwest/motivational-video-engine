# 05 — Prompt Library

Reusable text prompts the engine emits for external tools. These are templates — the engine fills in the variables. The operator runs them in their image generator of choice (ComfyUI, Krea, Midjourney, local SD).

This file is the *human-readable canon* for what the engine emits. The machine-readable per-world variants live in [config/visual_worlds.yaml](../config/visual_worlds.yaml) and are expanded during the M2 milestone.

## Visual asset prompt — base template

```
Create a cinematic vertical image for a motivational philosophy video.

Visual world: {world}             # stoic_rome / ancient_greece / literary_dark / field_notes
Author or figure: {author}        # Marcus Aurelius / Epictetus / Socrates / Dostoevsky / none
Theme: {theme}                    # self-command / responsibility / endurance / restraint / ...

Style:
  serious, cinematic, painterly realism, historical atmosphere,
  dramatic natural light, textured, restrained, not cartoonish,
  not fantasy armor, not modern influencer aesthetic

Composition:
  vertical 9:16, strong central silhouette or symbolic subject,
  large negative space for captions, atmospheric depth,
  subtle background detail

Avoid:
  modern clothing, neon, sci-fi, cheesy fantasy, smiling influencer,
  text in image, extra fingers, distorted face, fake logos, glossy AI look

Prompt:
{full visual description, derived from the world's image_prompt_template
 with background_prompt_key and figure_prompt_key from the content spec}
```

## Example — stoic_rome, Marcus Aurelius, self-command

```
Create a cinematic vertical 9:16 image for a Stoic discipline video about self-command.

A weathered marble bust of Marcus Aurelius stands in the foreground of a ruined
Roman courtyard at dawn. Storm clouds break above distant columns. Fine ash
drifts through cold golden light. The scene feels severe, disciplined, ancient,
and quiet. The bust is not speaking. It is symbolic, still, and dignified.
Leave dark negative space in the upper third for captions.

Style: painterly realism, cinematic lighting, textured marble, restrained
colors, historical atmosphere, serious and masculine, not cartoonish,
not glossy, not fantasy.

Avoid: modern objects, text, logos, exaggerated muscles, fantasy armor,
neon lighting, smiling face, influencer aesthetic.
```

## Negative prompt — universal

```
text, watermark, logo, signature, extra fingers, distorted face, deformed,
disfigured, anime, cartoon, fantasy armor, neon, modern clothing, modern
objects, smartphone, sunglasses, influencer pose, glossy AI render
```

## Aesthetic non-negotiables

- **No text in the image.** Captions are composited by the engine.
- **No modern objects.** Including clothing, phones, glasses.
- **No fantasy / sci-fi cues.** No armor, glowing runes, neon.
- **No smiling presenter / influencer poses.** This is not influencer content.
- **Strong vertical 9:16 with negative space.** Captions need room.

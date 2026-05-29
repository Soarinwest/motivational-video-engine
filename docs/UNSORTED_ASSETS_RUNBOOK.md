# Sorting `assets/backgrounds/_unsorted/` — runbook

When you drop new Midjourney/AI-generated images into
`assets/backgrounds/_unsorted/`, follow this process to label and place them.
Designed to be re-runnable: by Claude in a future session, by you, or as a
checklist driving a future `motive sort-unsorted` CLI command.

## TL;DR

For each file in `_unsorted/`:
1. **Identify subject + period** — read the Midjourney prompt embedded in the
   filename (or open the image if the filename is uninformative). Most
   filenames look like `soarin_west_<prompt-text>_<uuid>.png`.
2. **Choose a world slug** from the table below by matching subject + mood.
3. **Choose a descriptive key** in `snake_case` matching the world's existing
   prompt vocabulary (see `config/visual_worlds.yaml`).
4. **Rename** to `{world}_{descriptor}_{NNN}.png` (e.g.
   `mythic_polyphemus_cave_001.png`).
5. **Move** to `assets/backgrounds/{world}/`.
6. **Update** [assets/CATALOG.md](../assets/CATALOG.md) counts.
7. **(Optional)** add the descriptor as a new entry in the world's
   `background_prompts` dict in [config/visual_worlds.yaml](../config/visual_worlds.yaml)
   so a future `make-images --force` regenerates it via ComfyUI.

## World-selection table

The 14 worlds defined in `config/visual_worlds.yaml`. Pick the closest match
by subject + mood. When uncertain, move to `_unsorted/_review_<name>.png`
for a human call.

| World | Subject matter | Visual cues |
|---|---|---|
| `stoic_rome` | Roman ruins, marble busts, fluted columns, drifting ash | Severe, classical, weathered marble; storm light; ash; cold gold dawn |
| `ancient_greece` | Greek temples, Mediterranean coast, agora, olive groves, bronze-age ships | Sun-bleached marble, deep blue Aegean, knotted olive trees |
| `literary_dark` | 19th-c interiors, candlelit desks, snow streets, rain windows | Chiaroscuro, candle/lamp, deep shadow, gothic mood |
| `field_notes` | Forest recovery, ponds at dawn, ecological detail | Patient, observational, natural light, no human figure |
| `modern_discipline` | Workshops, sparse rooms, plowed fields, honest labor | Working hands, daylight, no Roman/Greek markers |
| `quiet_strength` | Lone figures on ridges, sea cliffs, snow trails | Restrained, individual subject in landscape, endurance |
| `existential` | Dry Mediterranean roads, mountain ascents, stairway descents | Severe, philosophical, sparse |
| `mythic` | Homer/Beowulf — Bronze-age warriors, ancient shorelines, sea caves, ships, Odysseus material | Bronze, dark sea, weathered, epic but grounded |
| `chivalric` | Medieval castles, stone chapels, forges, great halls, knightly objects | Stone, hearth, storm light, restrained |
| `hudson_river_school` | Historical American luminist landscapes (Church, Cole, Bierstadt et al.) | Painterly, romantic, American wilderness, named-artist scans |
| `anti_doom_scroll` | Phone face-down, windows over screens, attention reclaimed | Contemporary domestic, restrained, choosing-presence |
| `public_duty` | Empty podiums, post-rain arenas, civic dignity | Civic architecture, no crowd, post-event mood |
| `abstract_brand` | Marble texture, ash and light, parchment, caption-ready backgrounds | No specific subject, useful as quote-only intro/outro plates |
| `war` | Battlefields, returning soldiers, homefront, refugees | Cost-of-war framing; somber, never spectacle |

## Filename convention

```
{world}_{descriptor}_{NNN}.{ext}
```

- `world`: matches the destination folder (e.g. `mythic`, `chivalric`)
- `descriptor`: short snake_case key naming the specific scene. Should
  resemble existing entries in the world's `background_prompts` dict.
- `NNN`: zero-padded 3-digit sequence to distinguish variants. Use `_001`
  unless a file with that name already exists; increment as needed.
- `ext`: `.png`, `.jpg`, `.jpeg`, or `.webp` (the pipeline accepts all four).

**Examples that match this convention:**
```
mythic_polyphemus_cave_001.png
chivalric_castle_road_duty_002.png
ancient_greece_temple_above_sea_001.png
stoic_rome_marcus_bust_dawn_001.png
```

## When to flag a file for human review

Drop the file into `assets/backgrounds/_unsorted/_review_<descriptor>_NNN.{ext}`
when:

- You can't confidently pick a world from the table
- Subject leans **out-of-brand**: influencer-aesthetic, glossy AI render,
  modern-clothing/phones/cars in an ancient scene, smiling face, fantasy
  armor, anime/cartoon — anything in the negative-prompt list in
  [config/visual_worlds.yaml](../config/visual_worlds.yaml)
- Subject is a **figure** (an isolated character on transparent background)
  rather than a scene — figures go under `assets/figures/<gender>/<archetype>/`,
  not `assets/backgrounds/`
- Filename has no descriptive prompt and the image is generic

Currently held in `_review_`: `_review_amalfi_coastal_village_001.png` (too
travel-Instagram for the restrained aesthetic).

## After sorting

1. **Update [assets/CATALOG.md](../assets/CATALOG.md)** counts per world so the
   inventory stays accurate.
2. **(Optional but recommended)** Add new descriptors to
   [config/visual_worlds.yaml](../config/visual_worlds.yaml)'s
   `background_prompts` dict for the relevant world. This lets a future
   `motive make-images` regenerate the asset via ComfyUI using the same key
   if you ever want a fresh version.
3. **Verify nothing broke**: `pytest -q` should still be green.

## Example: how the May 29 batch was sorted

14 new files landed in `_unsorted/` on May 28-29 from a Midjourney run
focused on the Homer/Odyssey arc. Filenames carried the prompt verbatim.
Categorization decisions:

| Source filename (prompt fragment) | Destination |
|---|---|
| `A_dark_ancient_shoreline_at_the_edge_of_the_underwo...` | `mythic/mythic_underworld_shoreline_001.png` |
| `A_great_ancient_bow_resting_on_a_stone_table_inside...` | `mythic/mythic_odysseus_bow_on_table_001.png` |
| `A_medieval_blacksmith_forge_before_dawn_glowing_coa...` | `chivalric/chivalric_blacksmith_forge_dawn_001.png` |
| `A_mysterious_island_clearing_at_twilight_ancient_st...` | `mythic/mythic_island_clearing_twilight_001.png` |
| `A_narrow_muddy_road_leading_toward_a_distant_mediev...` | `chivalric/chivalric_castle_road_duty_002.png` (variant of `_001`) |
| `A_single_weathered_wooden_oar_half-buried_in_wet_sa...` | `mythic/mythic_oar_in_sand_001.png` |
| `A_small_medieval_stone_chapel_on_a_hill_under_storm...` | `chivalric/chivalric_stone_chapel_storm_001.png` |
| `A_vast_shadowed_sea_cave_with_a_rough_stone_entranc...` | `mythic/mythic_sea_cave_entrance_001.png` |
| `An_ancient_Greek_ship_struggling_through_a_violent_...` | `mythic/mythic_greek_ship_storm_001.png` |
| `An_empty_medieval_great_hall_after_a_feast_long_woo...` | `chivalric/chivalric_great_hall_after_feast_001.png` |
| `Odysseus_and_his_men_trapped_inside_the_cave_of_the...` | `mythic/mythic_polyphemus_cave_001.png` |
| `Odysseus_standing_alone_on_a_rocky_shoreline_at_daw...` | `mythic/mythic_odysseus_shoreline_dawn_002.png` |
| `Penelope_seated_at_a_loom_in_a_dim_ancient_Greek_ch...` | `mythic/mythic_penelope_at_loom_001.png` (scene with figure baked in — kept as background) |
| `The_island_of_Ithaca_at_dawn_rugged_cliffs_olive_tr...` | `mythic/mythic_ithaca_dawn_cliffs_001.png` |

10 of 14 → `mythic` (Odyssey arc), 4 of 14 → `chivalric`. None flagged for review.

## Prompt template for Claude to follow

To re-run this process in a future session, paste this prompt:

> "Look at `assets/backgrounds/_unsorted/`. For each file:
> 1. Read the Midjourney prompt from the filename (or open the image if
>    needed). 
> 2. Pick a world from `config/visual_worlds.yaml`'s defined worlds,
>    using [docs/UNSORTED_ASSETS_RUNBOOK.md](docs/UNSORTED_ASSETS_RUNBOOK.md)'s
>    world-selection table.
> 3. Choose a snake_case descriptor matching the world's existing
>    prompt vocabulary, with a `_NNN` suffix.
> 4. Move and rename per the convention `{world}_{descriptor}_{NNN}.png`.
> 5. Update [assets/CATALOG.md](assets/CATALOG.md) counts.
> 6. Flag anything out-of-brand or ambiguous as
>    `_review_<descriptor>_NNN.png` and leave it in `_unsorted/`."

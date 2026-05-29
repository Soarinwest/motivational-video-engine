# Asset Catalogue

Snapshot of what is in `assets/` and what is missing. Pair this with [figures/visual_asset_prompt_library.md](figures/visual_asset_prompt_library.md) for prompt templates and curation rules.

## Backgrounds — 112 assets across 11/14 worlds

Organized by visual world. Targets are from the prompt-library asset-pack table.

For sorting new drops into `_unsorted/`, see [docs/UNSORTED_ASSETS_RUNBOOK.md](../docs/UNSORTED_ASSETS_RUNBOOK.md).

| World | Have | Target | Gap |
|---|---:|---:|---|
| [stoic_rome/](backgrounds/stoic_rome/) | 11 | 5-10 | Over target — well-stocked |
| [ancient_greece/](backgrounds/ancient_greece/) | 14 | 5-10 | Over target — well-stocked |
| [literary_dark/](backgrounds/literary_dark/) | 7 | 5-10 | OK |
| [field_notes/](backgrounds/field_notes/) | 7 | 5-10 | OK |
| [modern_discipline/](backgrounds/modern_discipline/) | 3 | 5-10 | Need 2-7 more |
| [quiet_strength/](backgrounds/quiet_strength/) | 4 | 3-5 | OK |
| [existential/](backgrounds/existential/) | 1 | 3-5 | Need 2-4 more |
| [mythic/](backgrounds/mythic/) | 33 | 3-5 | Over target — Iliad + Odyssey arcs richly stocked |
| [chivalric/](backgrounds/chivalric/) | 6 | 3-5 | Over target |
| [hudson_river_school/](backgrounds/hudson_river_school/) | 15 | — | **New world** — historical paintings; documented below |
| [anti_doom_scroll/](backgrounds/anti_doom_scroll/) | 0 | 3-5 | **Empty** |
| [public_duty/](backgrounds/public_duty/) | 0 | 3-5 | **Empty** |
| [abstract_brand/](backgrounds/abstract_brand/) | 0 | 5-10 | **Empty** |
| [war/](backgrounds/war/) | 0 | TBD | **New world** — no prompts in library yet |
| [_unsorted/](backgrounds/_unsorted/) | 1 | — | `_review_amalfi_coastal_village_001.png` held for curation decision |

### Mythic — Iliad + Odyssey-ready (33 files)

All mythic backgrounds named to content (simple-key convention matches the rest of the project). Drives `ancient_greece_iliad` and `ancient_greece_odyssey` arcs.

**Iliad-side (13 files):**

| File | Source | Used by script |
|---|---|---|
| `battlefield_aftermath.png` | ChatGPT | (alt for Iliad battle scripts) |
| `greek_camp_at_troy.png` | ChatGPT | (broad camp shot) |
| `greek_ship_storm.png` | Midjourney | 013 patroclus_rage |
| `hector_city_gates.png` | **ComfyUI / Juggernaut** | 011 hector_farewell |
| `hero_overlooking_camp.png` | ChatGPT | (alt — Achilles surveying) |
| `old_king_in_palace.png` | ChatGPT | (alt for Priam) |
| `priam_in_tent.png` | **ComfyUI / Juggernaut** | 012 priam_mercy |
| `troy_walls_storm.png` | ChatGPT | (alt for siege scripts) |
| `war_camp_fire_meadow.png` | Midjourney | 007 homer_check_quarrel |
| `war_tent_at_sunset.png` | ChatGPT | (alt for Achilles tent) |
| `warrior_at_city_gates.png` | ChatGPT | (alt for Hector) |
| `warrior_grieving_campfire.png` | ChatGPT | (alt — Patroclus grief) |
| `ship_in_lightning_storm.png` | ChatGPT | (alt — drama at sea, Patroclus rage) |

**Odyssey-side (17 files):**

| File | Source | Used by script |
|---|---|---|
| `boat_on_shore_sunset.png` | Midjourney | (unassigned) |
| `bow_in_great_hall.png` | Midjourney | (Odysseus's bow / return; unassigned) |
| `calypso_island_twilight.png` | Midjourney | 015 calypso_refuse |
| `crossing_river_of_dead.png` | ChatGPT | (alt for Tiresias underworld) |
| `eumaeus_cottage_twilight.png` | ChatGPT | (swineherd's hut; unassigned) |
| `ithaca_dawn_cliffs.png` | Midjourney | (Ithaca arrival; unassigned) |
| `oar_on_beach_sunset.png` | ChatGPT | (the literal oar — Tiresias prophecy) |
| `odysseus_facing_sunset.png` | ChatGPT | (alt — Odysseus contemplation) |
| `odysseus_olive_bed.png` | ChatGPT | (the olive bed, Book XXIII — homecoming) |
| `odysseus_shoreline.png` | Midjourney | (alt) |
| `odysseus_shoreline_dawn.png` | Midjourney | (alt) |
| `penelope_at_loom.png` | ChatGPT | **016 penelope_patience** (replaces penelope_by_window) |
| `penelope_by_window.png` | Midjourney | (alt — woman at window) |
| `polyphemus_cave.png` | Midjourney | 014 polyphemus_cunning |
| `polyphemus_cave_men_interior.png` | ChatGPT | (alt cave shot) |
| `polyphemus_cave_torchbearer.png` | ChatGPT | (alt cave shot) |
| `polyphemus_cave_with_torch.png` | ChatGPT | (alt cave shot) |
| `sea_cave_entrance.png` | Midjourney | (Scylla candidate; unassigned) |
| `underworld_shoreline.png` | Midjourney | 017 tiresias_underworld |

**Beowulf / generic (3 files):**

| File | Source | Used by script |
|---|---|---|
| `beowulf_warrior_cave.png` | Midjourney | (unassigned) |

### Ancient Greece — Iliad + Odyssey-relevant additions (3 new files)

| File | Source | Use case |
|---|---|---|
| `ithaca_homecoming_path.png` | ChatGPT | path through olives toward temple — Odyssey homecoming approach |
| `woman_at_balcony_sea.png` | ChatGPT | Helen/Andromache at the window |
| `woman_on_city_walls.png` | ChatGPT | Andromache vigil on the walls of Troy |

### Hudson River School — 15 paintings

Historical paintings, named `{artist_lastname}_{title_snake_case}.{ext}`.

| File | Artist | Title |
|---|---|---|
| `bierstadt_in_the_sierras.png` | Albert Bierstadt | In the Sierras (1868) |
| `bierstadt_the_rocky_mountains_landers_peak.jpg` | Albert Bierstadt | The Rocky Mountains, Lander's Peak |
| `church_heart_of_the_andes.jpg` | Frederic Edwin Church | Heart of the Andes |
| `cole_the_oxbow.jpg` | Thomas Cole | The Oxbow |
| `cropsey_the_valley_of_wyoming.jpg` | Jasper Francis Cropsey | The Valley of Wyoming |
| `durand_in_the_woods.jpg` | Asher B. Durand | In the Woods |
| `durand_the_beeches.jpg` | Asher B. Durand | The Beeches |
| `gifford_a_gorge_in_the_mountains.jpg` | Sanford Robinson Gifford | A Gorge in the Mountains |
| `heade_approaching_thunder_storm.jpg` | Martin Johnson Heade | Approaching Thunder Storm |
| `heade_newburyport_meadows.jpg` | Martin Johnson Heade | Newburyport Meadows |
| `kensett_eatons_neck_long_island.jpg` | John Frederick Kensett | Eaton's Neck, Long Island |
| `kensett_lake_george.jpg` | John Frederick Kensett | Lake George |
| `lane_stage_fort_across_gloucester_harbor.jpg` | Fitz Henry Lane | Stage Fort across Gloucester Harbor |
| `moran_colburns_butte_south_utah.jpg` | Thomas Moran | Colburn's Butte, South Utah |
| `whittredge_the_trout_pool.jpg` | Worthington Whittredge | The Trout Pool |

## Figures — restructured by archetype

Each archetype has its own folder under `masculine/` or `feminine/`. Source type (generated vs. real reference photo) is encoded in the filename suffix, e.g. `marcus_aurelius_generated_bust_001.png` vs. `aristotle_real_001.png`.

### Masculine — 12 archetypes, 12 assets

| Archetype | Files | Notes |
|---|---:|---|
| [marcus_aurelius/](figures/masculine/marcus_aurelius/) | 1 generated | Bust three-quarter |
| [socrates/](figures/masculine/socrates/) | 1 generated | — |
| [epictetus/](figures/masculine/epictetus/) | 1 generated | — |
| [odysseus/](figures/masculine/odysseus/) | 1 generated | Weathered traveler |
| [shakespeare_king/](figures/masculine/shakespeare_king/) | 1 generated | Tragic king silhouette |
| [aristotle/](figures/masculine/aristotle/) | 1 real | Classical bust |
| [chrysippos/](figures/masculine/chrysippos/) | 1 real | Stoic philosopher bust |
| [demosthenes/](figures/masculine/demosthenes/) | 1 real | Orator bust |
| [epikouros/](figures/masculine/epikouros/) | 1 real | Epicurus bust (distinct from Epictetus) |
| [hesiod/](figures/masculine/hesiod/) | 1 real | — |
| [hippokrates/](figures/masculine/hippokrates/) | 1 real | — |
| [hypnos_thanatos/](figures/masculine/hypnos_thanatos/) | 1 real | Greek vase scene |

### Feminine — 11 archetypes, 17 assets

| Archetype | Files | Notes |
|---|---:|---|
| [aphrodite/](figures/feminine/aphrodite/) | 3 generated | — |
| [athena/](figures/feminine/athena/) | 1 generated | — |
| [greek_muse/](figures/feminine/greek_muse/) | 1 generated | — |
| [melpomene/](figures/feminine/melpomene/) | 1 real | Muse of tragedy |
| [greek_heroine/](figures/feminine/greek_heroine/) | 1 generated | Tragic figure |
| [roman_matron/](figures/feminine/roman_matron/) | 1 generated | — |
| [mother/](figures/feminine/mother/) | 1 generated | Ruined courtyard |
| [modern_woman/](figures/feminine/modern_woman/) | 4 generated | Rooftop + red slip + 2 lace bodysuit. **Review against "Hard truth. Clean heart." rule** — the bodysuit shots may read influencer-aesthetic. |
| [mediterranean_woman/](figures/feminine/mediterranean_woman/) | 1 generated | Generic Mediterranean shore |
| [war_widow/](figures/feminine/war_widow/) | 2 generated | Candlelit room + cold shoreline |
| [refugees/](figures/feminine/refugees/) | 1 generated | Women and children, muddy road |

## Overlays — partially stocked

| Pack | Files | Notes |
|---|---:|---|
| [fog/](overlays/fog/) | 4 mp4 | Best stocked |
| [dust/](overlays/dust/) | 2 mp4 | — |
| [snow/](overlays/snow/) | 1 mp4 | Thin |
| [ash/](overlays/ash/) | 0 | **Empty** — referenced in stoic_rome prompts |
| [rain/](overlays/rain/) | 0 | **Empty** — referenced in literary_dark prompts |
| [film_grain/](overlays/film_grain/) | 0 | **Empty** — suggested in prompt library |

## Fonts — 3 families, all SIL OFL (free for commercial use)

| Family | Files | Default pairing | Use for |
|---|---|---|---|
| [Cinzel/](fonts/Cinzel/) | 1 variable + 6 static weights | `marble_serif_centered` caption style | Roman inscriptions; pair with `stoic_rome`, `ancient_greece`, `hudson_river_school`, `chivalric`, `public_duty` |
| [EB_Garamond/](fonts/EB_Garamond/) | 2 variable + 12 static weights | `parchment_lower_third` caption style | Classical Renaissance serif; pair with `literary_dark`, `field_notes`, Shakespeare/Plato/Aristotle contexts |
| [Inter/](fonts/Inter/) | 2 variable + 54 static weights (3 optical sizes × 9 weights × upright/italic) | `clean_white_caps_centered`, `hard_cut_captions`, `sharp_white_text` | Modern geometric sans; pair with `modern_discipline`, `anti_doom_scroll`, `quiet_strength` |

Each family ships a variable font at the root and a `static/` subfolder with individual weight cuts. License files (`OFL.txt`) are present in each — preserve them.

## Music — 12 in mood folders, 2 in `_review/`

Files are renamed to `{slug}_{descriptor}_{NNN}.mp3` to match the project naming convention. Source IDs preserved in this table for licensing traceability.

| Music profile slug | Files | Used by |
|---|---:|---|
| [ancient_low_drone/](music/ancient_low_drone/) | 4 | Plato, Marcus Aurelius, philosophical/meditative scripts |
| [low_strings/](music/low_strings/) | 1 | Epictetus, Aristotle, restrained-but-melodic scripts |
| [soft_lyre_ambient/](music/soft_lyre_ambient/) | 2 | Aristotle (habit), Odyssey (return home), nature/contemplative |
| [somber_cinematic/](music/somber_cinematic/) | 5 | Homer war material, Antigone, Dostoevsky, dark literary |
| [_review/](music/_review/) | 2 | Tracks held for keep/cut decision (see notes) |

### Mood folder contents

| Slug | File | Original source filename |
|---|---|---|
| `ancient_low_drone` | `ancient_low_drone_classical_001.mp3` | bfcmusic-classical-music-479078 |
| `ancient_low_drone` | `ancient_low_drone_meditation_002.mp3` | mixkit-meditation-441 |
| `ancient_low_drone` | `ancient_low_drone_vastness_003.mp3` | mixkit-vastness-184 |
| `ancient_low_drone` | `ancient_low_drone_calm_dreamscape_004.mp3` | morgan-ambient-calm-ambient-dreamscape-529861 |
| `low_strings` | `low_strings_violin_cello_loop_001.mp3` | farran_ez-string-violin-cello-loop-456150 |
| `soft_lyre_ambient` | `soft_lyre_ambient_mellow_piano_guitar_001.mp3` | sharvarion-mellow-ambient-piano-pad-guitar-strings-138801 |
| `soft_lyre_ambient` | `soft_lyre_ambient_sleepy_002.mp3` | mixkit-sleepy-cat-135 |
| `somber_cinematic` | `somber_cinematic_dark_ambient_001.mp3` | freemusicforvideo-dark-ambient-soundscape-dreamscape-524032 |
| `somber_cinematic` | `somber_cinematic_dark_crime_piano_002.mp3` | universfield-dark-crime-piano-506186 |
| `somber_cinematic` | `somber_cinematic_dark_crime_piano_drama_003.mp3` | universfield-dark-crime-piano-drama-498841 |
| `somber_cinematic` | `somber_cinematic_dark_mystery_piano_004.mp3` | universfield-dark-mystery-piano-161660 |
| `somber_cinematic` | `somber_cinematic_unforgiven_005.mp3` | mixkit-unforgiven-890 |
| `_review` | `_review_hip_hop_offbrand_001.mp3` | mixkit-hip-hop-02-738 — does not fit "Hard truth. Clean heart." aesthetic |
| `_review` | `_review_sun_and_his_daughter_unclear_002.mp3` | mixkit-sun-and-his-daughter-580 — mood unclear from filename; needs human listen |

### Music_profile slug coverage vs. script YAMLs

The 10 ancient-Greece script YAMLs reference these `music_profile` slugs:

| Slug | Used in scripts | Have files? |
|---|---|---|
| `ancient_low_drone` | 001 plato_examined_life, 004 plato_inner_order | Yes (4) |
| `low_strings` | 002 epictetus_control, 005 aristotle_choice, 007 homer_check_your_anger, 010 antigone_i_deny_nothing | Yes (1) — light |
| `soft_lyre_ambient` | 003 aristotle_habit, 008 homer_return_home | Yes (2) |
| `somber_cinematic` | 006 homer_anger, 009 homer_bear_the_wreck | Yes (5) |

All four slugs in use have at least one matching file. `low_strings/` is thin at 1 file — worth sourcing 2-3 more before the war/tragedy scripts go into production.

### Licensing notes

Most tracks are from Mixkit, Pixabay (universfield, morgan, freemusicforvideo, sharvarion), and similar royalty-free sources. **Save the source URL and license text for each file before publishing any video that uses it.** A sidecar `LICENSES.md` per mood folder is the right next step — TBD.

## Other

- [logo/](logo/) — 1 logo

## Priority gaps (ranked)

1. **War world** is a new direction with zero coverage and no prompt-library entry. Author 3-5 prompts (battlefields, legions, sieges, weary returning soldiers) and generate first batch.
2. **Two empty worlds with library prompts ready:** anti_doom_scroll, public_duty. Generate 3-5 each. Chivalric just got its first asset.
3. **Abstract_brand backgrounds** are needed for quote-only intro/outro frames. Library has 3 prompts ready to use.
4. **Ash + rain overlays** — cheaper to source from Pexels/Vecteezy than to generate.
5. **`low_strings/` music thin** — only 1 track but referenced by 4 of the 10 ancient-Greece scripts. Source 2-3 more.
6. **License sidecars for music** — record source URL + license text for each track before any video using them publishes.
7. **Curation pass on feminine/modern_woman/** — 3 of 4 files lean sensual/influencer; decide which fit the brand voice.
8. **Resolve `_unsorted/_review_amalfi_coastal_village_001.png`** — keep (route to ancient_greece) or cut.
9. **Resolve `music/_review/` tracks** — hip-hop is off-brand for the project; sun-and-his-daughter needs a human listen.
10. **Decide permanent home for `modern_discipline_farmer_oxen_plowing_003.png`** — defaulted to modern_discipline. Could re-home to literary_dark (Tolstoy/Levin) or a new agrarian world if that direction grows.

## Conventions used here

- Background filenames (originals): `{world}_{subject}_{detail}_{NNN}.png`
- Hudson River School filenames: `{artist_lastname}_{title_snake_case}.{ext}`
- Figure filenames: `{archetype}_{source}_{detail}_{NNN}.{ext}` where `source` is `generated` or `real`
- Per-world / per-archetype folders are flat. No deeper nesting.
- `_unsorted/` is a holding pen for assets that need a human curation decision before mapping. Files prefixed `_review_` need an explicit keep/cut call.

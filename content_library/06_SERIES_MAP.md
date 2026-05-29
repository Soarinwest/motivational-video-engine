# Series Map

The recurring video series the project produces. Each series is a **content lens**: who it speaks to, in what voice, with what aesthetic. A source entry can belong to several series via its `video.series` field.

Series files live in [`series/`](series/). Each file is the canonical page for one series: angle, audience, default visual worlds, default voice, and the source IDs that feed it.

For arcs (multi-video sequences inside a region/era) and per-video scripts, see [07_ARCS_AND_PRODUCTION.md](07_ARCS_AND_PRODUCTION.md).

## Active series

| Slug | One-line | Default visual worlds | Audience |
|---|---|---|---|
| `stoic_discipline` | Roman and Greek stoicism on self-command, duty, mortality. | stoic_rome, quiet_strength | men 18-45 looking for serious frame |
| `hard_truths_for_men` | Direct truths about responsibility and self-government, drawn from across the corpus. | stoic_rome, modern_discipline, quiet_strength | men, broad age range |
| `literature_for_the_living` | Lessons from tragedy and the novel — Shakespeare, Dostoevsky, Tolstoy, Sophocles. | literary_dark | readers, humanities-curious |
| `field_notes_for_the_human_animal` | Ecological and naturalist wisdom on attention, resilience, place. | field_notes, hudson_river_school | nature-leaning, contemplative |
| `war_and_consequence` | War, grief, and the cost — not glorification. Homer, Sophocles, 20th-century war writers. | war, mythic, literary_dark | mixed; serious frame required |
| `women_left_alive` | Women in war and aftermath — survivors, widows, refugees, mothers. Honors them as historical subjects. | war, literary_dark | mixed; treat carefully |
| `quiet_strength` | Endurance without applause. Lone figures, private discipline. | quiet_strength, mythic | introverts, contemplatives |
| `the_useful_man` | Competence, labor, and responsibility. Workshop and field. | modern_discipline | men, working-age |
| `anti_doom_scroll` | Attention and presence over digital panic. Choose the window over the screen. | anti_doom_scroll, abstract_brand | broad, screen-fatigued |
| `sensual_autonomy` | Adult sexuality as belonging to the subject, not the consumer. Restraint and dignity. | literary_dark, abstract_brand | adult, mixed |

## How series, arcs, and visual worlds differ

- A **series** is a *content lens* — what kind of message, for whom, in what voice. Long-running and recurring. Lives in `series/`.
- An **arc** is a *publishing-order lens* — a sequenced multi-video story inside a region/era. Finite. Lives in `arcs/`.
- A **visual world** is an *aesthetic lens* — what the frame looks like. Lives in `assets/backgrounds/<world>/`.

The same source entry can be tagged into multiple series, multiple arcs, and multiple worlds. The render stage picks one of each per draft.

## Defining a new series

Copy [`templates/series_entry_template.md`](templates/series_entry_template.md) into `series/<new_slug>.md`. Fill in:

- **Slug** — short snake_case, matches filename
- **One-line** — what the series is, in one sentence
- **Audience** — who it speaks to
- **Default visual worlds** — which `assets/backgrounds/<world>/` folders feed it by default
- **Default voice profile** — Kokoro voice slug (TBD as the voice stage lands)
- **Tone constraints** — anything specific beyond the project default
- **Source IDs** — list of canonical source IDs that feed the series. Cross-references only; the source entries themselves stay under `sources/`.

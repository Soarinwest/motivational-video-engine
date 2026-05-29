# Arcs, Per-Video Scripts, and Choreography

The production half of the content library. Where [`sources/`](sources/), [`themes/`](themes/), and [`series/`](series/) capture canonical material and recurring framing, the directories described here capture **what gets made, in what order, this season.**

## The three production folders

### `arcs/`

A multi-video sequence inside one region/era, with its own publishing logic. An arc is finite: it has a beginning, a middle, an end. A typical arc holds 3-7 video scripts.

Example: [`arcs/ancient_greece_self_command.yaml`](arcs/ancient_greece_self_command.yaml) — examine, command, habit, order, choice.

An arc YAML lists:
- `arc_id`, `region`, `title`, `purpose`
- The visual world and default motifs that bind the arc together aesthetically
- Themes the arc carries
- Source files and source IDs that feed it
- The ordered list of scripts under it

### `scripts/<region>/<arc>/<NNN>_<slug>.yaml`

One YAML per video draft. The actual ~30-second script text lives in the `script:` field as a literal block. Each script references its `arc_id`, its `region`, and its `quote_source_id` — the canonical source entry under `sources/` it draws from. The script does not duplicate the quote metadata; that lives in the source entry.

Example: [`scripts/ancient_greece/self_command/001_plato_examined_life.yaml`](scripts/ancient_greece/self_command/001_plato_examined_life.yaml).

A script YAML carries:
- IDs and cross-references (`script_id`, `arc_id`, `region`, `quote_source_id`)
- Production hints (`voice`, `music`, `visual_world`, `visual_motif`, `caption_style`)
- The `script:` field — the literal voiceover text
- A `rights` block capturing the translator and source URL used in the draft
- A `review` block — at minimum `human_review_required: true`

### `choreography/`

Season-level publishing plans. A choreography YAML names the arcs to publish, in what order, with what default aesthetic, and the review rules to apply before any draft can ship.

Example: [`choreography/season_01_ancient_greece.yaml`](choreography/season_01_ancient_greece.yaml).

A choreography YAML carries:
- `season_id`, `title`, `region`, `creative_principle`
- Default palette and caption style for the season
- Ordered sub-arcs with their scripts
- Publishing-order rationale
- Review rules that gate publishing

## How they relate

```
sources/<author>/<work>.md       # canonical quote/paraphrase entries (YAML blocks)
   ^
   | quote_source_id
   |
scripts/<region>/<arc>/<NNN>.yaml  # per-video drafts (one YAML each)
   ^
   | listed in
   |
arcs/<region>_<arc>.yaml         # ordered list of scripts for one arc
   ^
   | listed in
   |
choreography/season_NN_<region>.yaml  # ordered list of arcs for one season
```

A single source entry can be drawn on by many scripts in many arcs. A single arc can appear in only one season at a time (it can be re-aired later by referencing it from a new choreography).

## How `arcs/` and `series/` differ

This catches people:

- A **series** ([`series/`](series/)) is a recurring *content lens* — `stoic_discipline`, `hard_truths_for_men`, `women_left_alive`. Indefinite. A source can belong to many series.
- An **arc** ([`arcs/`](arcs/)) is a *publishing-order lens* — finite, themed sequence inside a region. `ancient_greece_self_command`, `ancient_greece_iliad`, `ancient_greece_odyssey`.

A single source entry typically belongs to one or two arcs and several series. A single video script typically belongs to one arc but advertises in `series` on its source entry which series will adopt it once it goes live.

## The publishing pipeline (intent)

```
choreography/season_NN.yaml
  -> for each sub-arc, in order
       arcs/<arc>.yaml
         -> for each script, in order
              scripts/<region>/<arc>/<NNN>.yaml
                -> read quote_source_id
                   -> sources/<author>/<work>.md  (verify rights, fetch quote)
                -> render with voice + music + visual world
                -> human review (review.human_review_required is the gate)
                -> approve / reject / revise
                -> if approved: publish
```

No script renders to final until its `review.human_review_required` gate is cleared by a human. No script publishes until the source entry's `source.translation_check_needed` is `false`. These two flags are the project's hard guards.

## Naming conventions

- **Arc IDs**: `<region>_<arc_slug>` — e.g. `ancient_greece_self_command`. Files: `arcs/<arc_id>.yaml`.
- **Script IDs**: `<NNN>_<slug>` — e.g. `001_plato_examined_life`. The `NNN` is a season-wide running number; do not reset per arc. Files: `scripts/<region>/<arc_slug>/<NNN>_<slug>.yaml`.
- **Source IDs**: `<author_or_work>_<topic>_<NNN>` — e.g. `plato_apology_unexamined_life`. The NNN may be elided for unique-by-topic IDs. Defined in [01_SCHEMA.md](01_SCHEMA.md).
- **Season IDs**: `season_NN_<region>` — e.g. `season_01_ancient_greece`. Files: `choreography/<season_id>.yaml`.

## Where to start writing

To launch a new arc:

1. Pick the region and identify the source files needed under [`sources/`](sources/). Add new source folders if necessary.
2. Populate quote entries in the source files using the schema in [01_SCHEMA.md](01_SCHEMA.md).
3. Write the arc YAML in `arcs/`.
4. Write each script YAML under `scripts/<region>/<arc>/`.
5. Add the arc to a choreography YAML in `choreography/`.
6. Verify translation rights before any draft renders to final.

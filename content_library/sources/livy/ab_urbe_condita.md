# Ab Urbe Condita — Livy

**Source ID prefix:** `livy_auc_`
**Canonical file** for entries from Livy's *Ab Urbe Condita* (*From the Founding of the City*).

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema. Use the optional `speaker`/`addressee`/`scene_context`/`plot_function`/`modern_use_angle` fields for narrative-rich entries.

## Source metadata defaults

- **Author:** Livy (Titus Livius)
- **Work:** Ab Urbe Condita
- **Era written:** `ancient_rome`
- **World depicted:** `ancient_rome`
- **Traditions:** `roman_republican_virtue`
- **Default themes:** `public_responsibility`, `honor_service`, `restraint`, `duty`
- **Default rights status:** `public_domain_translation` (Canon Roberts / Spillan / Foster Loeb early volumes — all public domain)
- **Default visual worlds:** `stoic_rome`
- **Default series:** `stoic_practice`, `hard_truths_for_men`
- **Translator notes:** Canon Roberts (Everyman 1905) is the primary public-domain English translation. B. O. Foster's Loeb volumes (1919 onward) are mostly public domain in the US. Verify against the cited edition.
- **Source URLs:** Project Gutenberg, Perseus Tufts.

## Entries

```yaml
id: livy_auc_cincinnatus_power_to_plow

source:
  author: Livy
  work: Ab Urbe Condita
  section: "Book III.26-29 (the dictatorship of Cincinnatus)"
  translator: Canon Roberts
  source_url: "https://www.gutenberg.org/ebooks/19725"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Livy is the canonical source for the Cincinnatus story. The 'returned to his plow' detail is in III.29 — after sixteen days as dictator, he resigns and goes home."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
    - stoicism
  themes:
    - public_responsibility
    - restraint
    - honor_service
    - duty
  tone:
    - severe
    - restrained
    - direct

speaker:
  name: Livy (narrator)
  role: Roman historian, writing under Augustus, idealizing the early Republic

addressee:
  name: the reader
  role: a Roman citizen who has lived through civil war and is meant to remember what republican virtue looked like

scene_context: >
  Rome is in crisis. A consul and an army are surrounded by the Aequi.
  The Senate calls Cincinnatus from his small farm across the Tiber and
  makes him dictator with absolute power. He raises an army, lifts the
  siege, and defeats the enemy in sixteen days. Then he lays down the
  dictatorship and returns to his plow.

plot_function: >
  Livy's set piece for what Roman virtue is supposed to look like. Power
  taken reluctantly, used decisively, and returned willingly the moment
  the emergency ends. The story is told to remind Augustan Rome of what
  it has stopped being.

content:
  direct_quote: "He resigned his dictatorship on the sixteenth day, after holding it for six months, and went back to his farm."
  paraphrase: "He held supreme power for sixteen days, won the war, and went back to plowing."
  core_idea: "The man fit to hold power is the one who can put it down."
  interpretation: "Cincinnatus is dangerous to imitate because the test is not the seizing. It is the release. Most men can be trusted to take a sword. Almost no one can be trusted to set it down on the table while the room is still afraid."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_power_empire_corruption
  visual_worlds:
    - stoic_rome
  visual_motif: "small Roman field at sunrise, plow, messengers approaching with cloaks and standards"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "The man fit to hold power is the one who can put it down."
  final_line: "He went back to the plow."
  modern_use_angle: >
    The test of character is not whether a man takes the office. It is
    whether he can leave it. Most career trajectories are designed to
    make leaving impossible.

review:
  human_review_required: true
  notes: "Verify Canon Roberts III.26-29. The Cincinnatus story is partly legend; flag the historical-fact distinction in the script if relevant."
```

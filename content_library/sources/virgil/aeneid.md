# Aeneid — Virgil

**Source ID prefix:** `virgil_aeneid_`
**Canonical file** for entries from Virgil's *Aeneid*.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema.

## Source metadata defaults

- **Author:** Virgil (Publius Vergilius Maro)
- **Work:** Aeneid
- **Era written:** `ancient_rome` (29-19 BCE, under Augustus)
- **World depicted:** `ancient_rome` (and legendary Troy / Mediterranean)
- **Traditions:** `roman_republican_virtue`, `greek_tragedy`
- **Default themes:** `duty`, `mortality`, `fate`, `grief`, `homefront_rebuilding`, `honor_service`
- **Default rights status:** `public_domain_translation` (Dryden 1697 — public domain; Conington 1866 — public domain)
- **Default visual worlds:** `stoic_rome`
- **Default series:** `literary_dark`, `hard_truths_for_men`
- **Translator notes:** John Dryden (1697) is the great English verse translation. John Conington (1866) prose version is more literal. Both public domain. Verify against the cited edition.
- **Source URLs:** Project Gutenberg, Perseus Tufts.

## Entries

```yaml
id: virgil_aeneid_burden_of_destiny

source:
  author: Virgil
  work: Aeneid
  section: "Book II.707-711 (Aeneas tells his father he will carry him out of burning Troy)"
  translator: John Conington
  source_url: "https://www.gutenberg.org/ebooks/22456"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Troy is burning. Aeneas's father Anchises refuses to leave the city — he is old, the war is lost, let him die there. Aeneas lifts him onto his shoulders and carries him out, with his small son Iulus walking beside. The image becomes the defining icon of Roman pietas."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
    - greek_tragedy
  themes:
    - duty
    - grief
    - honor_service
    - homefront_rebuilding
    - mortality
  tone:
    - severe
    - elegiac
    - mournful
    - tender

speaker:
  name: Aeneas
  role: Trojan prince, son of Anchises, future founder of the Roman people

addressee:
  name: his father Anchises
  role: an old man refusing to leave the city he has loved

scene_context: >
  The last night of Troy. The city burns behind them. Anchises tells
  his son to leave him — he is old, the city is finished, there is
  no point. Aeneas refuses. He lifts the old man onto his shoulders
  and walks out of the burning city, son Iulus at his side, household
  gods in his hands. The picture is the founding image of *pietas*.

plot_function: >
  Establishes Aeneas's character and the moral weight of the entire
  Aeneid. The new city of Rome is founded by a man who carried his
  father out of the old one. Duty is not abstract — it is a weight
  on the shoulders.

content:
  direct_quote: "Come then, dear father, mount upon my neck. I will bear you up on my own shoulders, nor will this burden weigh me down."
  paraphrase: "Climb onto my back, father. I will carry you. This is not a burden I will feel as one."
  core_idea: "Duty has a shape. It is usually the shape of a man carrying someone he cannot leave behind."
  interpretation: "Aeneas does not argue. He does not explain. He picks up the man who carried him, and walks. Virgil's image is the answer to every philosophical debate about duty: when the city falls, who do you carry, and how far do you carry them?"

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "Aeneas carrying his elderly father through burning Troy, child following close behind, flames on bronze armor, smoke and ash"
  voice_profile: bm_lewis
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Duty is not an abstraction. It is the weight of the person you cannot leave behind."
  final_line: "He picked up the man who carried him, and walked."
  modern_use_angle: >
    The duty that matters is rarely the one a man chooses freely. It
    is the one that arrives on the worst night and has the shape of
    someone he loves. Aeneas does not deliberate. The picture is the
    point.

review:
  human_review_required: true
  notes: "Verify Conington Book II.707-711. The 'ergo age, care pater' Latin is canonical."
```

---

```yaml
id: virgil_aeneid_founding_through_loss

source:
  author: Virgil
  work: Aeneid
  section: "Book I.33 (the cost of founding Rome)"
  translator: John Dryden
  source_url: "https://www.gutenberg.org/ebooks/228"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "The closing line of the Aeneid's prologue. After listing the many years, the many wars, the many losses Aeneas faces, Virgil sums it up: 'tantae molis erat Romanam condere gentem' — so great a labor it was to found the Roman race."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
  themes:
    - duty
    - grief
    - homefront_rebuilding
    - mortality
    - fate
  tone:
    - severe
    - elegiac
    - weighty
    - foundational

speaker:
  name: Virgil (narrator)
  role: Roman epic poet, summing up Aeneas's labor in a single line

addressee:
  name: the Roman reader
  role: a citizen of the city founded on the labor he is about to read

scene_context: >
  The first thirty-three lines of the Aeneid lay out what the poem
  will cover: exile from Troy, the long Mediterranean wandering, war
  in Italy, the suffering of Aeneas's people, the eventual founding.
  Virgil closes the prologue with one line that frames all of it as
  cost paid.

plot_function: >
  Sets the tone for the entire Aeneid. The poem is not a triumphalist
  founding myth. It is the story of what founding actually costs —
  and who pays it (often: people other than the founder).

content:
  direct_quote: "Such time, such toil, required the Roman name, such length of labour for so vast a frame."
  paraphrase: "So much time, so much labor, so much loss — and only then a city."
  core_idea: "Nothing worth founding gets founded cheaply. The labor is the substance, not the obstacle."
  interpretation: "Virgil refuses to romanticize the work. He names it labor. The founding is real because the cost is real — exile, war, loss, the dead left behind. The line is meant to settle a reader who came expecting glory: this will not be that."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "Aeneas standing on a dark Italian shoreline at dawn, Trojan ships behind him, sword lowered, distant hills of future Rome through mist"
  voice_profile: bm_lewis
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Nothing worth founding gets founded cheaply. The labor is the substance, not the obstacle."
  final_line: "So great a labor."
  modern_use_angle: >
    The man who imagines he can found anything — a company, a family,
    a habit — without paying its cost has misread the genre. Virgil's
    line is the corrective: name the labor, do not romanticize the
    founding, do not skip the years it actually takes.

review:
  human_review_required: true
  notes: "Verify Dryden Book I prologue closing. Latin: 'tantae molis erat Romanam condere gentem'."
```

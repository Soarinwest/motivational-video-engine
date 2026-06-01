# Parallel Lives — Plutarch

**Source ID prefix:** `plutarch_lives_`
**Canonical file** for entries from Plutarch's *Parallel Lives*.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema.

## Source metadata defaults

- **Author:** Plutarch
- **Work:** Parallel Lives (Vitae Parallelae)
- **Era written:** `ancient_rome` (Plutarch wrote in Greek under Roman empire, ~110 CE)
- **World depicted:** `ancient_rome` (mostly — also Greek subjects in the paired lives)
- **Traditions:** `roman_republican_virtue`, `stoicism`, `greek_tragedy`
- **Default themes:** `ambition`, `duty`, `honor_service`, `mortality`
- **Default rights status:** `public_domain_translation` (Dryden / Clough 1683-1864 — public domain; Perrin Loeb 1914-26 — mostly PD in US)
- **Default visual worlds:** `stoic_rome`
- **Default series:** `literary_dark`, `hard_truths_for_men`
- **Translator notes:** John Dryden / Arthur Hugh Clough revised edition (1864) is the standard public-domain translation. Bernadotte Perrin Loeb is the precise scholarly text — Loeb volumes from 1914-1926 are public domain in the US.
- **Source URLs:** Project Gutenberg, Perseus Tufts.

## Entries

```yaml
id: plutarch_lives_caesar_crossing_rubicon

source:
  author: Plutarch
  work: Parallel Lives — Life of Caesar
  section: "Caesar 32 (crossing the Rubicon)"
  translator: John Dryden / Arthur Hugh Clough
  source_url: "https://www.gutenberg.org/ebooks/674"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Plutarch's Caesar 32 records Caesar's hesitation at the river and the famous line. Caesar's army crossing the Rubicon was the act of treason that began the civil war."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
  themes:
    - ambition
    - power_corruption
    - mortality
  tone:
    - severe
    - cinematic
    - cold

speaker:
  name: Julius Caesar
  role: Roman general and proconsul of Gaul

addressee:
  name: his army (and himself)
  role: the legionaries waiting on the north bank — and Caesar's own decision

scene_context: >
  The Rubicon is a small river. Crossing it with an army is treason —
  the Senate forbids any general to bring troops into Italy proper. On
  the north bank Caesar pauses. Plutarch records him saying the
  decision is made — and then he crosses, with his army, and the
  Republic is over.

plot_function: >
  The hinge of Roman history. Before this moment, the Republic could
  still be reformed. After it, the only question is which general wins
  the civil war and becomes the first emperor.

content:
  direct_quote: "The die is cast."
  paraphrase: "It is decided. There is no undoing this."
  core_idea: "Ambition's most expensive feature is its irreversibility — the line you cannot uncross."
  interpretation: "Caesar pauses at the river. He knows what the crossing costs — not just to him, but to a thousand years of Roman constitutional order. He crosses anyway. The line is true: the die was cast. The price was paid by everyone else."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - ancient_rome_power_empire_corruption
  visual_worlds:
    - stoic_rome
  visual_motif: "horseback at the edge of a narrow river at night, legionaries waiting in silence, red standards lowered"
  voice_profile: bm_george
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Ambition's true price is the line you cannot uncross."
  final_line: "He crossed."
  modern_use_angle: >
    Most decisions a man regrets were obvious before he made them.
    Caesar saw the river, knew the price, paid it for everyone. That
    is the model and the warning at once.

review:
  human_review_required: true
  notes: "Verify Dryden/Clough Caesar 32. 'Alea iacta est' — Suetonius gives the Latin; Plutarch the Greek."
```

---

```yaml
id: plutarch_lives_brutus_republic_over_blood

source:
  author: Plutarch
  work: Parallel Lives — Life of Brutus
  section: "Brutus 10-12 (Brutus joins the conspiracy)"
  translator: John Dryden / Arthur Hugh Clough
  source_url: "https://www.gutenberg.org/ebooks/674"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Plutarch's Brutus 10-12 covers the recruitment of Brutus into the conspiracy. The tension: Caesar treats Brutus as a son. Brutus chooses the Republic anyway."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
    - greek_tragedy
  themes:
    - duty
    - honor_service
    - ambition
    - public_responsibility
  tone:
    - severe
    - mournful
    - weighty

speaker:
  name: Brutus (Marcus Junius Brutus)
  role: Roman senator, descendant of the Brutus who expelled the kings

addressee:
  name: his own conscience
  role: the inner argument between personal loyalty to Caesar and inherited duty to the Republic

scene_context: >
  Caesar has made himself dictator for life. Brutus is one of his
  closest friends — Caesar has called him 'son.' The conspirators
  recruit Brutus by reminding him that his ancestor expelled the Roman
  kings five centuries earlier. The question Plutarch poses: will
  Brutus put personal love above the Republic, or the Republic above
  personal love?

plot_function: >
  Sets up the assassination on the Ides of March. The conspiracy needs
  Brutus's name to give it legitimacy — without him it is murder;
  with him it is republicanism. He pays for that name with his life,
  and the Republic dies anyway.

content:
  direct_quote: ""
  paraphrase: "He chose the Republic over the man who loved him. The Republic still died. He still had to choose."
  core_idea: "Some duties cost you the people closest to you, and the duty does not save what it was meant to save."
  interpretation: "Brutus is the tragedy of republican virtue acting too late. The Republic he kills Caesar to save is already dead. Plutarch lets the contradiction stand: Brutus is honorable, the act is honorable, and the result is the end of the thing he loved."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - ancient_rome_power_empire_corruption
  visual_worlds:
    - stoic_rome
  visual_motif: "shadowed Roman chamber, dagger on a marble table, busts of ancestors lining the walls"
  voice_profile: bm_lewis
  music_profile: somber_cinematic
  caption_style: sparse_centered_captions
  script_angle: "Some honorable acts arrive too late to save what they were meant to save."
  final_line: "And the Republic still died."
  modern_use_angle: >
    The duty that costs you the most is the one that does not solve
    the problem. Brutus's example is harder than it looks — it is not
    'do the right thing.' It is 'do the right thing knowing it will
    not work.'

review:
  human_review_required: true
  notes: "Verify Dryden/Clough Brutus 10-12. Treat the assassination ethically — it is not a model to imitate but a tragedy to read."
```

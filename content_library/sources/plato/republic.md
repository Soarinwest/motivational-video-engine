# Republic — Plato

**Source ID prefix:** `plato_republic_`
**Canonical file** for entries from Plato's *Republic*.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema.

## Source metadata defaults

- **Author:** Plato
- **Work:** Republic
- **Era written:** `ancient_greece`
- **World depicted:** `ancient_greece`
- **Region:** `ancient_greece`
- **Traditions:** `platonism`
- **Default themes:** `self_command`, `duty`, `honor_service`, `restraint`
- **Default rights status:** `public_domain_translation` (Jowett translation via Project Gutenberg)
- **Default visual worlds:** `ancient_greece`, `abstract_brand`
- **Default series:** `stoic_discipline`, `literature_for_the_living`, `hard_truths_for_men`
- **Translator notes:** Jowett translation is public domain. Verify book/section references against the chosen Gutenberg edition.
- **Source URLs:** https://www.gutenberg.org/ebooks/1497

## Entries

```yaml
id: plato_republic_justice_soul

source:
  author: Plato
  work: Republic
  section: "Book IV"
  translator: Benjamin Jowett
  source_url: "https://www.gutenberg.org/ebooks/1497"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Verify exact wording against chosen Jowett edition; the paraphrastic line 'justice is the excellence of the soul' is a common rendering of the Book IV discussion."

classification:
  era_written: ancient_greece
  world_depicted: ancient_greece
  region: ancient_greece
  traditions:
    - platonism
  themes:
    - duty
    - honor_service
    - self_command
    - restraint
  tone:
    - severe
    - restrained

content:
  direct_quote: "Justice is the excellence of the soul."
  paraphrase: "A just soul is a soul in working order."
  core_idea: "Justice is first a condition of the inner person, not only of the city."
  interpretation: "Disorder inside a person becomes disorder around a person. The first city is the soul."

video:
  series:
    - stoic_discipline
    - literature_for_the_living
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
    - abstract_brand
  visual_motif: "temple columns aligned in shadow"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "Justice is not first about courts. It is about whether the soul is in working order."
  final_line: "Order yourself first."

review:
  human_review_required: true
  notes: "Confirm phrasing against Jowett Book IV."
```

---

```yaml
id: plato_republic_justice_happiness

source:
  author: Plato
  work: Republic
  section: "Book IV"
  translator: Benjamin Jowett
  source_url: "https://www.gutenberg.org/ebooks/1497"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_greece
  world_depicted: ancient_greece
  region: ancient_greece
  traditions:
    - platonism
  themes:
    - duty
    - restraint
    - self_command
  tone:
    - restrained
    - direct

content:
  direct_quote: "Justice and happiness are necessarily connected."
  paraphrase: "There is no clean happiness in a disordered life."
  core_idea: "Flourishing follows order; it cannot be detached from how one lives."
  interpretation: "You cannot bribe yourself out of an unjust life. The damage shows up in your peace."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
    - quiet_strength
  visual_motif: "empty courtyard, single olive tree"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "There is no shortcut around your own conduct."
  final_line: "The two come together or not at all."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: plato_republic_good_soul_rules

source:
  author: Plato
  work: Republic
  section: "Book I (paraphrased from the discussion of the excellence of the soul)"
  translator: Benjamin Jowett
  source_url: "https://www.gutenberg.org/ebooks/1497"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Often quoted as 'the good soul is a good ruler.' Verify the exact wording against Jowett before using as direct_quote; otherwise treat as paraphrase."

classification:
  era_written: ancient_greece
  world_depicted: ancient_greece
  region: ancient_greece
  traditions:
    - platonism
  themes:
    - self_command
    - honor_service
    - duty
  tone:
    - severe
    - restrained

content:
  direct_quote: ""
  paraphrase: "A soul in good order is the only soul fit to command anything."
  core_idea: "Authority over others depends on authority over oneself."
  interpretation: "Whatever you cannot govern in yourself, you will eventually inflict on someone else."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
    - the_useful_man
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
    - stoic_rome
  visual_motif: "stone bench at dawn, empty"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "Govern yourself before you accept command over anyone else."
  final_line: "There is no other order of operations."

review:
  human_review_required: true
  notes: "Treat as paraphrase unless an exact Jowett rendering is confirmed."
```

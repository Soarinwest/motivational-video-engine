# Agricola — Tacitus

**Source ID prefix:** `tacitus_agricola_`
**Canonical file** for entries from Tacitus's *Agricola* (*De vita et moribus Iulii Agricolae*).

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema.

## Source metadata defaults

- **Author:** Tacitus
- **Work:** Agricola
- **Era written:** `ancient_rome`
- **World depicted:** `ancient_rome`
- **Traditions:** `roman_republican_virtue`
- **Default themes:** `tyranny`, `public_responsibility`, `restraint`, `honor_service`
- **Default rights status:** `public_domain_translation` (Maurice Hutton Loeb 1914 — public domain)
- **Default visual worlds:** `stoic_rome`
- **Default series:** `literary_dark`, `hard_truths_for_men`
- **Translator notes:** Maurice Hutton (Loeb Classical Library, 1914) is the primary public-domain English translation. Alfred John Church and William Brodribb (1877) is older but standard. Verify against the cited edition.
- **Source URLs:** Project Gutenberg, Wikisource.

## Entries

```yaml
id: tacitus_agricola_desert_and_peace

source:
  author: Tacitus
  work: Agricola
  section: "Chapter 30 (Calgacus's speech before the battle of Mons Graupius)"
  translator: Alfred John Church and William Brodribb
  source_url: "https://www.gutenberg.org/ebooks/7524"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Calgacus is a Caledonian (proto-Scottish) chieftain. The speech is Tacitus's literary composition — a Roman historian putting the empire's critique into the mouth of its enemy. The line 'they make a desert and call it peace' is one of the most quoted in Roman literature."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - roman_republican_virtue
  themes:
    - tyranny
    - power_corruption
    - public_responsibility
    - mortality
  tone:
    - severe
    - cold
    - observant
    - cinematic

speaker:
  name: Calgacus
  role: Caledonian chieftain, as imagined and composed by Tacitus

addressee:
  name: his warriors before battle
  role: the last free Britons about to fight Agricola's Roman legions at Mons Graupius

scene_context: >
  Tacitus's father-in-law Agricola has spent years subduing Britain.
  Calgacus is the leader of the last unconquered tribes. On the eve of
  the battle that will end Caledonian freedom, Tacitus gives him a
  speech — a Roman historian putting Rome's harshest self-critique into
  the mouth of its enemy.

plot_function: >
  The moral center of the Agricola. Tacitus admires his father-in-law's
  competence and his honor, and refuses to flatter the empire he served.
  Calgacus's speech is how Tacitus tells the truth about Roman conquest
  without abandoning loyalty to his own.

content:
  direct_quote: "To plunder, butcher, steal, these things they misname empire; they make a desert and call it peace."
  paraphrase: "They rob, they kill, they take. They give the result a kinder name. They call it peace."
  core_idea: "The empire's vocabulary lies about what the empire does."
  interpretation: "Tacitus is not endorsing the speech as policy. He is showing what the conquered see — and admitting, as a Roman, that they are not wrong. 'Peace' that is a desert is not peace. The naming is the lie."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - ancient_rome_power_empire_corruption
  visual_worlds:
    - stoic_rome
  visual_motif: "ruined arches at dusk, distant Roman soldiers marching across a barren landscape, smoke on horizon"
  voice_profile: bm_george
  music_profile: low_strings
  caption_style: marble_serif_centered
  script_angle: "The empire's vocabulary always lies about what the empire does."
  final_line: "They call it peace."
  modern_use_angle: >
    Power renames its costs to make them disappear from the ledger.
    'Collateral damage,' 'restructuring,' 'realignment' — any time the
    word does not match the thing it describes, look for the desert.

review:
  human_review_required: true
  notes: "Verify Church/Brodribb Chapter 30. The Latin is 'ubi solitudinem faciunt, pacem appellant'. Translate with care for register — Calgacus is not modern; the speech is severe and cold."
```

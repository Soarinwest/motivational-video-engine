# Apology — Plato

**Source ID prefix:** `plato_apology_`
**Canonical file** for entries from Plato's *Apology* (Socrates' defense speech).

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema. Copy [../../templates/quote_yaml_template.yaml](../../templates/quote_yaml_template.yaml) to add an entry.

## Source metadata defaults

- **Author:** Plato (depicting Socrates)
- **Work:** Apology
- **Era written:** `ancient_greece`
- **World depicted:** `ancient_greece`
- **Region:** `ancient_greece`
- **Traditions:** `platonism`
- **Default themes:** `self_command`, `courage`, `duty`, `honor_service`
- **Default rights status:** `public_domain_translation` (Jowett translation via MIT Classics / Project Gutenberg)
- **Default visual worlds:** `ancient_greece`, `quiet_strength`
- **Default series:** `stoic_discipline`, `literature_for_the_living`, `hard_truths_for_men`
- **Translator notes:** Benjamin Jowett translation is public domain. Verify section numbers (Stephanus pagination) before publishing any direct quote.
- **Source URLs:** https://classics.mit.edu/Plato/apology.html

## Entries

```yaml
id: plato_apology_unexamined_life

source:
  author: Plato (Socrates)
  work: Apology
  section: "38a"
  translator: Benjamin Jowett
  source_url: "https://classics.mit.edu/Plato/apology.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Verify exact wording and Stephanus section against chosen Jowett edition."

classification:
  era_written: ancient_greece
  world_depicted: ancient_greece
  region: ancient_greece
  traditions:
    - platonism
  themes:
    - self_command
    - duty
    - honor_service
  tone:
    - severe
    - restrained
    - direct

content:
  direct_quote: "The life which is unexamined is not worth living."
  paraphrase: "An unexamined life is not a life worth defending."
  core_idea: "Examination of one's own life is a condition of a worthy human life."
  interpretation: "Socrates is not asking for perfection. He is denying that drift is freedom."

video:
  series:
    - stoic_discipline
    - literature_for_the_living
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
    - quiet_strength
  visual_motif: "Athenian agora at dusk, lone philosopher silhouette"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "If you have not examined the life, you have only borrowed it."
  final_line: "Examine it before life does."

review:
  human_review_required: true
  notes: "Confirm wording against the selected Jowett edition."
```

---

```yaml
id: plato_apology_daily_virtue

source:
  author: Plato (Socrates)
  work: Apology
  section: "38a (preceding the unexamined-life line)"
  translator: Benjamin Jowett
  source_url: "https://classics.mit.edu/Plato/apology.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Verify wording against chosen Jowett edition."

classification:
  era_written: ancient_greece
  world_depicted: ancient_greece
  region: ancient_greece
  traditions:
    - platonism
  themes:
    - self_command
    - duty
    - honor_service
  tone:
    - severe
    - restrained

content:
  direct_quote: "The greatest good of man is daily to converse about virtue."
  paraphrase: "The best thing a person can do, each day, is talk seriously about how to live well."
  core_idea: "Virtue is a daily practice of attention, not an event."
  interpretation: "Discipline begins in conversation with yourself. The hard questions, asked again and again."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
  visual_motif: "stone bench under olive trees at first light"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "Virtue is the conversation you refuse to stop having with yourself."
  final_line: "Ask it again tomorrow."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: plato_apology_speaker_truth

source:
  author: Plato (Socrates)
  work: Apology
  section: "18a (opening)"
  translator: Benjamin Jowett
  source_url: "https://classics.mit.edu/Plato/apology.html"
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
    - honor_service
    - duty
    - courage
  tone:
    - severe
    - direct

content:
  direct_quote: "Let the judge decide justly and the speaker speak truly."
  paraphrase: "The judge's task is justice. The speaker's task is the truth. Neither replaces the other."
  core_idea: "Each role in a serious dispute has its own discipline; truth-telling is the speaker's discipline."
  interpretation: "Your job is not to win. Your job is to be accurate. The room's job is to weigh you."

video:
  series:
    - hard_truths_for_men
    - literature_for_the_living
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - ancient_greece
    - public_duty
  visual_motif: "empty Athenian courtroom, columns in early shadow"
  voice_profile: bm_george
  music_profile: low_strings
  caption_style: marble_serif_centered
  script_angle: "Speak the thing you would defend even if it costs you the verdict."
  final_line: "Truly is the only word you control."

review:
  human_review_required: true
  notes: ""
```

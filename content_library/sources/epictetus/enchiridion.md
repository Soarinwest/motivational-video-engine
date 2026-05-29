# Enchiridion - Epictetus

**Source ID prefix:** `epictetus_enchiridion_`
**Canonical file** for entries from *Enchiridion*, Epictetus.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema. Copy [../../templates/quote_yaml_template.yaml](../../templates/quote_yaml_template.yaml) to add an entry.

## Source metadata defaults

- **Author:** Epictetus
- **Work:** Enchiridion
- **Era written:** `ancient_rome`
- **World depicted:** `ancient_rome`
- **Region:** `ancient_greece`
- **Traditions:** `stoicism`
- **Default themes:** `self_command`, `restraint`, `duty`
- **Default rights status:** `public_domain_translation` (Elizabeth Carter, 1758)
- **Default visual worlds:** `stoic_rome`, `ancient_greece`, `quiet_strength`
- **Default series:** `stoic_discipline`, `hard_truths_for_men`
- **Translator notes:** Elizabeth Carter translation (1758) is firmly public domain. Verify chapter numbers against your chosen edition.
- **Source URLs:** https://classics.mit.edu/Epictetus/epicench.html

Note on `region`: although Epictetus wrote in the Roman period (`era_written: ancient_rome`), he is grouped with the Ancient Greece publishing arc because his work is in Greek, descends directly from Socratic philosophy, and the project's first arc treats Greek-language stoicism as foundational. The Roman-language stoics (Seneca, Marcus) belong to the Ancient Rome arc.

## Entries

```yaml
id: epictetus_enchiridion_control_first_rule

source:
  author: Epictetus
  work: Enchiridion
  section: "Chapter 1"
  translator: Elizabeth Carter
  source_url: "https://classics.mit.edu/Epictetus/epicench.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Verify wording against the Carter text."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_greece
  traditions:
    - stoicism
  themes:
    - self_command
    - restraint
    - duty
  tone:
    - severe
    - restrained
    - direct

content:
  direct_quote: "Some things are in our control and others not."
  paraphrase: "Some things are yours to govern. Most are not."
  core_idea: "Freedom begins with knowing the line between what you command and what you do not."
  interpretation: "Most of your suffering comes from arguing with what was never yours to command."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - stoic_rome
    - ancient_greece
  visual_motif: "stone road, hand opening and closing over dust"
  voice_profile: am_michael
  music_profile: low_strings
  caption_style: clean_white_caps_centered
  script_angle: "Your first task is not to control the world. It is to stop surrendering command of yourself."
  final_line: "Begin with the line."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: epictetus_enchiridion_own_actions

source:
  author: Epictetus
  work: Enchiridion
  section: "Chapter 1"
  translator: Elizabeth Carter
  source_url: "https://classics.mit.edu/Epictetus/epicench.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_greece
  traditions:
    - stoicism
  themes:
    - self_command
    - duty
  tone:
    - direct
    - restrained

content:
  direct_quote: "Things in our control are opinion, pursuit, desire, aversion, and, in a word, whatever are our own actions."
  paraphrase: "Yours: your opinion, your aim, your desire, your refusal, your next action."
  core_idea: "What is yours is small and total. You have full authority inside it."
  interpretation: "The list is short. The authority over it is complete. Spend your strength here."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - stoic_rome
    - quiet_strength
  visual_motif: "open hand at dawn, sparse stone room"
  voice_profile: am_michael
  music_profile: low_strings
  caption_style: clean_white_caps_centered
  script_angle: "Govern the small list. Stop arguing with the long one."
  final_line: "Those are yours."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: epictetus_enchiridion_not_own_actions

source:
  author: Epictetus
  work: Enchiridion
  section: "Chapter 1"
  translator: Elizabeth Carter
  source_url: "https://classics.mit.edu/Epictetus/epicench.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_greece
  traditions:
    - stoicism
  themes:
    - restraint
    - self_command
  tone:
    - severe
    - restrained

content:
  direct_quote: "Things not in our control are body, property, reputation, command, and, in one word, whatever are not our own actions."
  paraphrase: "Not yours: your body's condition, your property, your reputation, your office, every outcome you do not personally produce."
  core_idea: "Most of what you grasp for was never yours."
  interpretation: "The grip you exert on what you do not own is the grip that costs you the most."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - stoic_rome
  visual_motif: "empty office, polished but vacant"
  voice_profile: am_michael
  music_profile: low_strings
  caption_style: clean_white_caps_centered
  script_angle: "You spend your life defending what you do not actually own."
  final_line: "Loosen the grip."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: epictetus_enchiridion_appearance_not_thing

source:
  author: Epictetus
  work: Enchiridion
  section: "Chapter 1"
  translator: Elizabeth Carter
  source_url: "https://classics.mit.edu/Epictetus/epicench.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_greece
  traditions:
    - stoicism
  themes:
    - self_command
    - restraint
  tone:
    - direct

content:
  direct_quote: "You are but an appearance, and not absolutely the thing you appear to be."
  paraphrase: "What presses on me is an impression. The impression is not the thing itself."
  core_idea: "Judgment intervenes between event and reaction. That gap is freedom."
  interpretation: "The headline, the slight, the surge of fear: these are appearances. You decide what they become."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
    - anti_doom_scroll
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - stoic_rome
    - anti_doom_scroll
  visual_motif: "a phone face-down beside a window at first light"
  voice_profile: am_michael
  music_profile: low_strings
  caption_style: clean_white_caps_centered
  script_angle: "The thing that hits you is not yet a verdict. You decide what it becomes."
  final_line: "Pause. Look again."

review:
  human_review_required: true
  notes: ""
```

---

```yaml
id: epictetus_enchiridion_nothing_to_you

source:
  author: Epictetus
  work: Enchiridion
  section: "Chapter 1"
  translator: Elizabeth Carter
  source_url: "https://classics.mit.edu/Epictetus/epicench.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: ""

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_greece
  traditions:
    - stoicism
  themes:
    - restraint
    - self_command
  tone:
    - severe
    - direct

content:
  direct_quote: "If it concerns anything not in our control, be prepared to say that it is nothing to you."
  paraphrase: "If it is not yours to govern, be ready to say: this is nothing to me."
  core_idea: "Detachment from what is not yours is not coldness; it is accuracy."
  interpretation: "Most of what hijacks your day is a problem that does not belong to you. Hand it back."

video:
  series:
    - stoic_discipline
    - hard_truths_for_men
    - anti_doom_scroll
  arcs:
    - ancient_greece_self_command
  visual_worlds:
    - stoic_rome
    - quiet_strength
  visual_motif: "hand releasing a stone over still water"
  voice_profile: am_michael
  music_profile: low_strings
  caption_style: clean_white_caps_centered
  script_angle: "Most of what owns your day is not actually yours."
  final_line: "It is nothing to you."

review:
  human_review_required: true
  notes: ""
```

# Hávamál — Anonymous (Poetic Edda)

**Source ID prefix:** `havamal_`
**Canonical file** for entries from the Hávamál, the "Sayings of the High One" — a gnomic-wisdom poem in the Poetic Edda, attributed traditionally to the voice of Odin.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema.

## Source metadata defaults

- **Author:** Anonymous (Old Norse, before the 13th-c. compilation of the Codex Regius)
- **Work:** Hávamál
- **Collection:** Poetic Edda
- **Era written:** `medieval_world`
- **World depicted:** Norse legendary
- **Region:** `medieval_world`
- **Traditions:** `norse_wisdom`
- **Default themes:** `mortality`, `reputation`, `wisdom`, `restraint`, `sacrifice`
- **Default rights status:** `public_domain_translation_needed` (Bray 1908, Bellows 1923, Thorpe 1866 — public domain in the US; verify wording per stanza)
- **Default visual worlds:** `northern_fate`
- **Default series:** `literary_dark`, `hard_truths_for_men`
- **Translator notes:** Olive Bray (1908), Henry Adams Bellows (1923), Benjamin Thorpe (1866) are public domain. The stanza numbers shift between translations — verify against the cited edition before publishing.
- **Source URLs:** Wikisource, Project Gutenberg, Heimskringla.no.

## Entries

```yaml
id: havamal_reputation_after_death

source:
  author: Anonymous (Hávamál)
  work: Hávamál (Poetic Edda)
  section: "Stanza 76 or 77 (numbering varies by translation)"
  translator: Olive Bray
  source_url: "https://en.wikisource.org/wiki/The_Elder_or_Poetic_Edda"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "The 'cattle die, kinsmen die' formula appears in two adjacent stanzas in most editions. Verify the exact line breaks."

classification:
  era_written: medieval_world
  world_depicted: medieval_world
  region: medieval_world
  traditions:
    - norse_wisdom
  themes:
    - mortality
    - reputation
    - honor_service
    - legacy
    - duty
  tone:
    - severe
    - restrained
    - elegiac
    - direct

speaker:
  name: Odin (gnomic wisdom voice of the Hávamál)
  role: traditional wisdom speaker

addressee:
  name: the listener
  role: any person receiving counsel about death and reputation

scene_context: >
  The Hávamál gives practical and moral wisdom in terse sayings. This passage
  turns from the mortality of possessions, kin, and the self toward the one
  thing that may remain after death: earned reputation.

plot_function: >
  Establishes the Northern Fate arc's central claim: death is certain, but
  conduct still matters because memory outlives the body.

content:
  direct_quote: "Cattle die, and kinsmen die; thyself too soon must die; but one thing never, I ween, will die — fair fame of one who has earned."
  paraphrase: "Cattle die. Kinsmen die. You will die. The only thing that may not die is the reputation of a person who earned one."
  core_idea: "The body and its possessions all pass. What may remain is the moral weight of one's deeds in others' memory."
  interpretation: "The quote is not about vanity or empty fame. It says that a person cannot keep wealth, family, comfort, or even life itself. What remains is the shape of their deeds in the memory of others."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - medieval_world_northern_fate_courage_under_doom
  visual_worlds:
    - northern_fate
  visual_motif: "old Norse wisdom figure beside a burial mound at dusk, ravens circling, dead grass in wind"
  voice_profile: bm_george
  music_profile: low_war_drone
  caption_style: marble_serif_centered
  script_angle: "Stop living as if comfort is permanent. Build a life that would still mean something if your conveniences were removed."
  final_line: "Live so that death does not erase you."
  modern_use_angle: >
    Most contemporary life optimizes for accumulation. Hávamál says the
    accumulation does not survive you. The reputation might.

review:
  human_review_required: true
  notes: "Verify Bray Hávamál stanza 76/77."
```

---

```yaml
id: havamal_wisdom_and_silence

source:
  author: Anonymous (Hávamál)
  work: Hávamál (Poetic Edda)
  section: "Wisdom/speech stanzas (numbering varies; near stanzas 27-28 in Bellows)"
  translator: Olive Bray
  source_url: "https://en.wikisource.org/wiki/The_Elder_or_Poetic_Edda"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "The 'unwise man thinks he knows all' formula is one of several wisdom-warnings; the exact stanza varies between editions."

classification:
  era_written: medieval_world
  world_depicted: medieval_world
  region: medieval_world
  traditions:
    - norse_wisdom
  themes:
    - wisdom
    - restraint
    - self_command
    - humility
  tone:
    - austere
    - direct
    - restrained

speaker:
  name: Odin (gnomic wisdom voice of the Hávamál)
  role: traditional wisdom speaker warning against foolish speech

addressee:
  name: the listener
  role: any person being warned against overconfidence and careless speech

scene_context: >
  The Hávamál repeatedly warns against foolishness, overconfidence,
  drunkenness, careless speech, and entering social situations without
  judgment. The wisdom is practical, social, and survival-oriented.

plot_function: >
  Moves the arc from death and reputation into restraint. Reputation is not
  only won by bold action; it is also protected by silence, caution, and
  measured speech.

content:
  direct_quote: "The unwise man thinks that he knows all."
  paraphrase: "The unwise man imagines he already understands."
  core_idea: "Untested certainty is the foolish man's posture. Real wisdom appears under pressure, especially when speech has consequences."
  interpretation: "A person can feel wise when nothing has tested them. The Hávamál says: do not confuse the absence of contradiction with the presence of judgment."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - medieval_world_northern_fate_courage_under_doom
  visual_worlds:
    - northern_fate
  visual_motif: "solitary Norse man seated in silence inside a dim timber hall, firelight low"
  voice_profile: am_michael
  music_profile: cold_ambient
  caption_style: marble_serif_centered
  script_angle: "Do not confuse certainty with wisdom. Say less when you do not know."
  final_line: "Let reality examine you first."
  modern_use_angle: >
    Social media rewards loud certainty. The Hávamál rewards the man who
    waits until reality has spoken first.

review:
  human_review_required: true
  notes: "Verify exact wisdom-stanza wording across Bray / Bellows / Thorpe."
```

---

```yaml
id: havamal_odin_wisdom_cost

source:
  author: Anonymous (Hávamál — Runatal)
  work: Hávamál (Poetic Edda) — Runatal section
  section: "Stanzas 138-139 (Runatal)"
  translator: Olive Bray
  source_url: "https://en.wikisource.org/wiki/The_Elder_or_Poetic_Edda"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "The Runatal stanzas describe Odin's self-sacrifice on Yggdrasil. The 'myself to myself' line is canonical across translations; the line breaks vary."

classification:
  era_written: medieval_world
  world_depicted: medieval_world
  region: medieval_world
  traditions:
    - norse_myth
    - norse_wisdom
  themes:
    - wisdom
    - sacrifice
    - mortality
    - duty
  tone:
    - mythic
    - severe
    - sacred
    - dark

speaker:
  name: Odin
  role: god seeking wisdom through ordeal and self-sacrifice

addressee:
  name: the listener
  role: recipient of Odin's account of sacrifice and runic wisdom

scene_context: >
  Odin describes hanging on the world-tree, wounded by a spear, sacrificing
  himself to himself for nine nights to gain the runes. The passage is the
  canonical statement that wisdom is bought through ordeal.

plot_function: >
  Deepens the arc from practical wisdom (Hávamál's daily counsel) to
  sacrificial wisdom (the Runatal's ordeal). True insight is not cheap or
  comfortable.

content:
  direct_quote: "I know that I hung on a wind-rocked tree nine whole nights, with a spear wounded, and to Odin offered, myself to myself."
  paraphrase: "I hung on the wind-rocked tree nine nights, wounded by the spear, offered myself to myself."
  core_idea: "Real wisdom is paid for in ordeal. The body and the ego are the currency."
  interpretation: "The quote presents wisdom as something purchased through ordeal. It rejects the idea that deep knowledge comes without loss, pain, discipline, or transformation."

video:
  series:
    - literary_dark
    - hard_truths_for_men
  arcs:
    - medieval_world_northern_fate_courage_under_doom
  visual_worlds:
    - northern_fate
  visual_motif: "Odin hanging in silhouette from a vast wind-torn ash tree at twilight, ravens on branches"
  voice_profile: bm_george
  music_profile: dark_strings
  caption_style: marble_serif_centered
  script_angle: "If your knowledge costs you nothing, it may be worth the same."
  final_line: "If your knowledge costs you nothing, it may be worth the same."
  modern_use_angle: >
    Modern self-improvement promises insight from a book and a weekend
    retreat. The Runatal says: that price will produce a matching depth.

review:
  human_review_required: true
  notes: "Verify Bray Runatal 138-139. The full stanza names the spear and the nine nights — keep the full image."
```

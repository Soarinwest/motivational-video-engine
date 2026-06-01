# Meditations - Marcus Aurelius

**Source ID prefix:** `marcus_meditations_`
**Canonical file** for entries from *Meditations*, Marcus Aurelius.

See [../../01_SCHEMA.md](../../01_SCHEMA.md) for the entry schema. Copy [../../templates/quote_yaml_template.yaml](../../templates/quote_yaml_template.yaml) to add an entry.

## Source metadata defaults

- **Author:** Marcus Aurelius
- **Work:** Meditations
- **Era written:** `ancient_rome`
- **World depicted:** `ancient_rome`
- **Traditions:** `stoicism`
- **Default themes:** `self_command`, `duty`, `mortality`, `restraint`
- **Default rights status:** `public_domain_translation` (George Long 1862 is public domain)
- **Default visual worlds:** `stoic_rome`, `quiet_strength`
- **Default series:** `stoic_practice`, `hard_truths_for_men`
- **Translator notes:** George Long (1862) and Meric Casaubon (1634) translations are public domain. Verify wording against the chosen edition before publishing.
- **Source URLs:** MIT Classics (Long); Project Gutenberg.

## Entries

```yaml
id: marcus_meditations_morning_preparation

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book II.1"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long 1862 wording. Verify against the MIT Classics or Project Gutenberg edition before render."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - self_command
    - restraint
    - duty
  tone:
    - severe
    - direct
    - restrained

content:
  direct_quote: "Begin the morning by saying to thyself, I shall meet with the busybody, the ungrateful, arrogant, deceitful, envious, unsocial. All these things happen to them by reason of their ignorance of what is good and evil."
  paraphrase: "Tell yourself, before you leave the house, who you will meet today. None of it should surprise you."
  core_idea: "Rehearse the day's difficulty before it arrives, so it cannot ambush your character."
  interpretation: "The Stoic morning is not a mood. It is a brief, honest preview of what other people will be like — and a decision, in advance, not to be deformed by it."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_stoic_discipline
  visual_worlds:
    - stoic_rome
    - quiet_strength
  visual_motif: "Roman forum at first light, empty colonnade"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "Rehearse the day's friction in advance. It cannot ambush a man who already saw it coming."
  final_line: "None of it should surprise you."

review:
  human_review_required: true
  notes: "Confirm Long wording for Book II.1 opening lines."
```

---

```yaml
id: marcus_meditations_as_if_last_act

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book II.5"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long 1862. The 'as a Roman and a man' phrasing is Long-specific; Casaubon and Hays differ."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - duty
    - self_command
    - restraint
  tone:
    - severe
    - direct
    - restrained

content:
  direct_quote: "Every moment think steadily, as a Roman and a man, to do what thou hast in hand with perfect and simple dignity, and feeling of affection, and freedom, and justice; and to give thyself relief from all other thoughts."
  paraphrase: "Do the task in front of you with plain dignity, affection, freedom, and justice. Put down every other thought."
  core_idea: "Single-pointed attention to the present act is the whole of practice."
  interpretation: "Most failure is not lack of effort. It is the part of the mind that is somewhere else while the hands work."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_stoic_discipline
  visual_worlds:
    - stoic_rome
    - quiet_strength
  visual_motif: "sun on a worn marble step, single figure entering frame"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "The man who lays down every other thought owns the moment in front of him."
  final_line: "Put the rest down."

review:
  human_review_required: true
  notes: "Confirm Long II.5 wording; consider alternate translation if needed."
```

---

```yaml
id: marcus_meditations_depart_this_moment

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book II.11"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long 1862. Pull only the regulate-every-act clause; the surrounding paragraph wanders."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - mortality
    - self_command
    - duty
  tone:
    - severe
    - restrained
    - direct

content:
  direct_quote: "Since it is possible that thou mayest depart from life this very moment, regulate every act and thought accordingly."
  paraphrase: "You could leave life at any moment. Let that fact shape the next thing you do."
  core_idea: "Death's nearness is not morbid; it is the ground that makes every act serious."
  interpretation: "Memento mori is not a tattoo. It is the question asked over every action: if this were the last, would I still be doing it this way?"

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_stoic_discipline
  visual_worlds:
    - stoic_rome
    - quiet_strength
  visual_motif: "Roman road in mist, single figure walking forward"
  voice_profile: bm_george
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Death is not a future event. It is the standard against which the next act is measured."
  final_line: "Regulate the next act accordingly."

review:
  human_review_required: true
  notes: "Confirm Long II.11. Verify the 'this very moment' phrasing."
```

---

```yaml
id: marcus_meditations_waste_no_time_arguing

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book X.16"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long 1862, Book X.16."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - duty
    - self_command
    - restraint
  tone:
    - severe
    - direct
    - dry

content:
  direct_quote: "No longer talk at all about the kind of man that a good man ought to be, but be such."
  paraphrase: "Stop discussing what a good man would do. Be one."
  core_idea: "The argument about virtue is not the practice of virtue."
  interpretation: "Every hour spent characterizing the right kind of man is an hour not spent being one. Marcus closes the conversation and turns to the act."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_duty_and_self_mastery
  visual_worlds:
    - stoic_rome
  visual_motif: "Roman camp at dawn, soldiers and red standards in mist behind a calm severe man"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "The man who keeps talking about virtue is not yet practicing it."
  final_line: "Be one."

review:
  human_review_required: true
  notes: "Confirm Long X.16 wording."
```

---

```yaml
id: marcus_meditations_inner_citadel

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book IV.3 (the retreat into yourself)"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long IV.3 — the canonical 'inner citadel' passage. Marcus argues that the best retreat is not a house in the country but the interior of one's own mind."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - self_command
    - restraint
    - duty
  tone:
    - severe
    - restrained
    - reflective

speaker:
  name: Marcus Aurelius (private notebook)
  role: emperor writing to himself on campaign

addressee:
  name: himself
  role: a man under the daily pressure of empire, seeking interior shelter

scene_context: >
  Marcus is on the Danube frontier. He has no quiet country house to
  escape to. His relief from the noise of empire has to come from
  somewhere closer than that. He writes himself the instruction —
  the retreat is interior, and it is always available.

plot_function: >
  Sets the architecture of Stoic practice as Marcus lives it. The
  inner citadel is not a private fantasy. It is a sovereignty the
  emperor builds where no army can reach it.

content:
  direct_quote: "Men seek retreats for themselves, houses in the country, sea-shores, and mountains... But it is in thy power whenever thou shalt choose to retire into thyself."
  paraphrase: "Other men go to the country to escape. You can go to the same place without leaving the room."
  core_idea: "The only retreat that always stays available is the interior of the mind that learned to keep one."
  interpretation: "Marcus does not despise the country house. He notes that it is rarely available when you need it most. The retreat that matters is the one you can step into in the middle of a meeting, on the back of a horse, on the eve of a battle. It is built, not found."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "Marcus seated in meditation inside a dark stone chamber, faint golden light outlining his face, shadows of battle on the wall"
  voice_profile: bm_george
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "The retreat that matters is the one you do not have to travel to. It is built, not found."
  final_line: "Step in."
  modern_use_angle: >
    Most men wait for circumstances — a cabin, a weekend, an
    eventually — before they can be still. Marcus writes the
    Meditations on campaign. The retreat he names is the only one
    available to a man who never gets the weekend.

review:
  human_review_required: true
  notes: "Verify Long IV.3 wording."
```

---

```yaml
id: marcus_meditations_ten_thousand_years

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book IV.17"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long IV.17. The instruction is direct: do not behave as if you have unlimited time. Death is here. Live now."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - mortality
    - self_command
    - duty
  tone:
    - severe
    - direct
    - restrained

speaker:
  name: Marcus Aurelius (private notebook)
  role: emperor writing to himself

addressee:
  name: himself
  role: a man who, like everyone, postpones

scene_context: >
  Marcus catches himself acting as if he has indefinite time. He
  writes the corrective in a single sentence. Death hangs over every
  man at every moment. Treat the present accordingly.

plot_function: >
  One of the recurring corrections Marcus gives himself across the
  Meditations. The book is in part a record of these small course
  adjustments — the daily refusals to act as if time were free.

content:
  direct_quote: "Do not act as if thou wert going to live ten thousand years. Death hangs over thee. While thou livest, while it is in thy power, be good."
  paraphrase: "Stop behaving as if you have ten thousand years. You don't. While you still have the choice, be good."
  core_idea: "Mortality is not a future event to dread. It is a constraint that gives the present its weight."
  interpretation: "Marcus is not threatening himself. He is naming the constraint. The instruction 'be good' is not abstract — it is what becomes possible when you stop pretending the years are unlimited."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "Marcus alone beside a funeral pyre at dusk, smoke into a storm gray sky, distant Roman campfires"
  voice_profile: bm_george
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Mortality is not a future event. It is the constraint that lets the present have weight."
  final_line: "While it is in thy power, be good."
  modern_use_angle: >
    Time-management language ('next quarter, eventually') quietly
    assumes you get the years. Marcus's correction is plain — you do
    not. The instruction that follows ('be good') is the only thing
    worth doing under that constraint.

review:
  human_review_required: true
  notes: "Verify Long IV.17 wording."
```

---

```yaml
id: marcus_meditations_universe_is_change

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book VII.18 (change as the nature of things)"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long VII.18. The clearest statement of the Stoic position on change. Marcus poses a rhetorical question and answers it himself."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - fate
    - mortality
    - restraint
    - self_command
  tone:
    - severe
    - philosophical
    - reflective

speaker:
  name: Marcus Aurelius (private notebook)
  role: emperor reasoning out loud about change

addressee:
  name: himself
  role: a man who, like all men, prefers stability to flux

scene_context: >
  Marcus addresses the part of himself — and the part of any reader —
  that resents change. He poses the question directly and refuses
  the resentment: change is what existence is. The wish for
  stability is the wish for nothing.

plot_function: >
  Establishes the cosmic frame for the rest of the Meditations.
  Empire, body, friends, the self — all are in flux. The Stoic
  response is not to mourn the flux but to stop fighting its
  fundamental nature.

content:
  direct_quote: "Is any one afraid of change? Why, what can take place without change? What then is more pleasing or more suitable to the universal nature?"
  paraphrase: "Are you afraid of change? Look around. Nothing can happen without it. You are afraid of the only thing that ever lets anything be."
  core_idea: "Resentment of change is resentment of existence itself."
  interpretation: "Marcus is not consoling himself. He is naming the category error. The man who refuses change is refusing the substrate of all events — including the ones that brought him to this moment, including the ones he loves."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "the Roman Forum in ruins at twilight, broken columns, cracked marble statues, grass through stone"
  voice_profile: bm_george
  music_profile: ancient_low_drone
  caption_style: marble_serif_centered
  script_angle: "Resentment of change is resentment of existence itself."
  final_line: "It is the only thing that ever lets anything be."
  modern_use_angle: >
    Most grief at change is grief at being made of time. Marcus's
    correction is uncomfortable: the same change you mourn is the
    one that produced everything you have ever loved.

review:
  human_review_required: true
  notes: "Verify Long VII.18 wording."
```

---

```yaml
id: marcus_meditations_soon_forgotten

source:
  author: Marcus Aurelius
  work: Meditations
  section: "Book VII.21 (forgetfulness)"
  translator: George Long
  source_url: "https://classics.mit.edu/Antoninus/meditations.html"
  rights_status: public_domain_translation
  translation_check_needed: true
  notes: "Long VII.21. Short and clean. Marcus reminds himself that he will forget the world, and the world will forget him, and the time between is the only field of action."

classification:
  era_written: ancient_rome
  world_depicted: ancient_rome
  region: ancient_rome
  traditions:
    - stoicism
  themes:
    - mortality
    - legacy
    - restraint
    - self_command
  tone:
    - severe
    - elegiac
    - restrained

speaker:
  name: Marcus Aurelius (private notebook)
  role: emperor, the most famous man in the world, writing to himself about being forgotten

addressee:
  name: himself
  role: a man who, like everyone, secretly hopes to be remembered

scene_context: >
  Marcus is the most powerful man alive. Statues will be erected of
  him; histories will be written about him. He sits down in his tent
  and writes himself the line that should disturb any man in his
  position: forget the project of being remembered. It does not
  survive you.

plot_function: >
  A recurring theme in the Meditations: the small, severe corrections
  Marcus applies to his own desire for legacy. He outlives the
  desire by naming it.

content:
  direct_quote: "Near is thy forgetfulness of all things; and near the forgetfulness of thee by all."
  paraphrase: "You will soon forget everything. Everything will soon forget you."
  core_idea: "Legacy is the wrong target. The right target is the present act, undertaken because it is right, not because it will be remembered."
  interpretation: "Marcus removes the consolation he could most easily reach for. He will not be remembered, not in the way the desire for legacy imagines. The work of the present act has to be its own reason."

video:
  series:
    - stoic_practice
    - hard_truths_for_men
  arcs:
    - ancient_rome_death_fate_inner_citadel
  visual_worlds:
    - stoic_rome
  visual_motif: "close view of a Roman bronze eagle standard planted in dark earth after battle, torn red banner moving in cold wind, no bodies visible"
  voice_profile: bm_george
  music_profile: somber_cinematic
  caption_style: marble_serif_centered
  script_angle: "Legacy is the wrong target. The present act has to be its own reason."
  final_line: "Everything will soon forget you."
  modern_use_angle: >
    Most ambitious work is quietly underwritten by the fantasy of
    being remembered. Marcus removes the underwriter. What is left
    has to stand on the work itself.

review:
  human_review_required: true
  notes: "Verify Long VII.21 wording."
```



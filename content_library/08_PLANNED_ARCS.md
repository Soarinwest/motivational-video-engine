# Planned Arcs — Master Content Roadmap

The full set of arcs the project plans to publish, across every region and
tradition in [02_TAXONOMY.md](02_TAXONOMY.md). One row per arc. Status is the
production state, not the editorial confidence.

This is the *content* roadmap. For the *engineering* roadmap (M1-M6 pipeline
milestones), see [../docs/06_MVP_ROADMAP.md](../docs/06_MVP_ROADMAP.md).

## The five-season meta-vision

Greece teaches the inner foundation. Rome tests whether that foundation can
survive power, duty, time, and death. The next three seasons inherit and
extend that question through Christian conscience, Norse fate, and modern
reason.

| # | Season | Teaches |
|---|---|---|
| 01 | **Ancient Greece** — Self-command and consequence | examine yourself, command yourself, form virtue, beware rage, endure fate |
| 02 | **Ancient Rome** — Duty, discipline, empire, mortality | do your duty, master luxury, face death, serve something larger than comfort, carry responsibility without complaint |
| 03 | **Early Christianity / Late Antiquity** — Conscience, suffering, humility, eternity | (planned) |
| 04 | **Norse / Germanic / Anglo-Saxon** — Fate, courage, loyalty, doom | (planned) |
| 05 | **Renaissance / Enlightenment** — Reason, ambition, statecraft, liberty | (planned) |

The progression of voices, distilled to one line each:

> Socrates: Examine yourself.
> Epictetus: Control yourself.
> Aristotle: Train yourself.
> Homer: Beware rage.
> Antigone: Own consequence.
> Marcus Aurelius: Do your duty.
> Seneca: Stop wasting life.
> Cicero: Serve what is right.
> Tacitus: Beware power without virtue.
> Virgil: Carry the cost of destiny.

## Status legend

| Status | Meaning |
|---|---|
| ✅ **shipped** | Arc YAML exists, scripts written, drafts rendered, ready to publish |
| 🔄 **in production** | Arc YAML exists, some scripts written, drafts in progress |
| 📝 **drafted** | Arc YAML written, no scripts yet |
| 💡 **planned** | Listed here but no YAML yet — the next batch of work |
| 🌫 **idea** | Identified as candidate but not committed |

## Season 01 — Ancient Greece

The foundation season. Self-command first, Homer second, women+law+tragedy to close.
See [choreography/season_01_ancient_greece.yaml](choreography/season_01_ancient_greece.yaml).

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| [ancient_greece_self_command](arcs/ancient_greece_self_command.yaml) | ✅ shipped | 5 | Plato, Aristotle, Epictetus — examine, command, habit, order, choice |
| [ancient_greece_iliad](arcs/ancient_greece_iliad.yaml) | ✅ shipped | 5 | Anger, quarrel, Hector's farewell, Priam's mercy, Patroclus's grief |
| [ancient_greece_odyssey](arcs/ancient_greece_odyssey.yaml) | ✅ shipped | 6 | Return home, Polyphemus, Calypso, Tiresias, Penelope, bear the wreck |
| [ancient_greece_women_law_tragedy](arcs/ancient_greece_women_law_tragedy.yaml) | ✅ shipped | 3 | Antigone — deny nothing, unwritten laws, grief after war |
| [ancient_greece_socratic_questions](arcs/ancient_greece_socratic_questions.yaml) | 📝 drafted | 0 | Apology, the gadfly, dying for an idea, the examined city, the cave |
| [ancient_greece_greek_tragedy](arcs/ancient_greece_greek_tragedy.yaml) | 📝 drafted | 0 | Oedipus, Trojan Women (Euripides), Agamemnon homecoming (Aeschylus), beyond Antigone |
| [ancient_greece_heroic_myth](arcs/ancient_greece_heroic_myth.yaml) | 📝 drafted | 0 | Heracles, Theseus, Jason, Perseus, Bellerophon, Sisyphus — labor and atonement |
| [ancient_greece_olympian_myth](arcs/ancient_greece_olympian_myth.yaml) | 📝 drafted | 0 | Prometheus, Icarus, Persephone, Orpheus, Narcissus, Phaethon |
| [ancient_greece_pre_socratics](arcs/ancient_greece_pre_socratics.yaml) | 📝 drafted | 0 | Heraclitus, Parmenides, Pythagoras, Anaximander — koan-length fragments |
| ancient_greece_aesop_fables | 🌫 idea | 0 | Short fables as quick parables; ~15-second format |
| ancient_greece_hesiod | 🌫 idea | 0 | Works and Days — early Greek agrarian discipline |

## Season 02 — Ancient Rome

Reorganized into three top-level arcs that group the existing feeder work and the planned expansion. The progression: discipline → power → mortality.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| [ancient_rome_duty_and_self_mastery](arcs/ancient_rome_duty_and_self_mastery.yaml) | 🔄 in production | 6 (+4 planned) | **Umbrella arc.** Marcus, Seneca, Cicero, Epictetus bridge. Absorbs the six scripts from stoic_discipline + seneca_on_time and adds Cicero on duty, Seneca on the shortness of life, Seneca on imagined suffering. |
| [ancient_rome_power_empire_corruption](arcs/ancient_rome_power_empire_corruption.yaml) | 📝 drafted | 0 (5 planned) | Cincinnatus, Caesar at the Rubicon, Brutus, Tacitus, Sallust. Backgrounds in place for all 5. Sources need to be written. |
| [ancient_rome_death_fate_inner_citadel](arcs/ancient_rome_death_fate_inner_citadel.yaml) | 📝 drafted | 1 (+6 planned) | Marcus on impermanence, Seneca on death-always-present, Lucretius, Virgil. Backgrounds in place. Most sources need to be written. |
| [ancient_rome_stoic_discipline](arcs/ancient_rome_stoic_discipline.yaml) | 🔄 in production | 3 | **Feeder sub-arc** for `duty_and_self_mastery`. Marcus *Meditations* II.1, II.5, II.11. Specs lint clean; awaiting render. |
| [ancient_rome_seneca_on_time](arcs/ancient_rome_seneca_on_time.yaml) | 🔄 in production | 3 | **Feeder sub-arc** for `duty_and_self_mastery`. Seneca Letters I, II, XII. Specs lint clean; awaiting render. |
| ancient_rome_women_under_empire | 🌫 idea | 0 | Cornelia, Agrippina — Roman women's voices, frame carefully |

## Season 03 — Early Christianity / Late Antiquity (planned)

Conscience, suffering, humility, eternity. The bridge from pagan Stoicism to Christian interiority.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| late_antiquity_augustine_confessions | 💡 planned | 0 | The restless heart, the divided will, conversion |
| late_antiquity_boethius_consolation | 💡 planned | 0 | Fortune's wheel, philosophy in prison |
| late_antiquity_desert_fathers | 🌫 idea | 0 | Anchorite discipline, attention as prayer |

## Season 04 — Norse / Germanic / Anglo-Saxon (planned)

Fate, courage, loyalty, doom. The cold-iron register.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| norse_havamal_wisdom | 💡 planned | 0 | Sayings of the High One — guest right, restraint, mortality |
| norse_voluspa_fate | 💡 planned | 0 | The seeress's prophecy — cycles, ragnarok, return |
| anglo_saxon_beowulf | 💡 planned | 0 | The lone defender, the long defeat, the mound at the end |
| anglo_saxon_seafarer_wanderer | 🌫 idea | 0 | The exile poems — solitude, weather, the mead-hall remembered |

## Season 05 — Renaissance / Enlightenment (planned)

Reason, ambition, statecraft, liberty.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| renaissance_machiavelli_prince | 💡 planned | 0 | Statecraft without sentiment, virtù vs fortuna |
| renaissance_shakespeare_history | 💡 planned | 0 | The crowns and the cost — Henry IV/V, Richard II |
| enlightenment_kant_moral_law | 🌫 idea | 0 | Duty as the moral law within |
| enlightenment_locke_consent | 🌫 idea | 0 | Liberty, property, the limits of legitimate power |

## Other planned seasons (post-five)

### Season 06 — Literary Dark

19th-century novel + Shakespeare tragedy. The literary cost-of-things arc.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| literary_dark_dostoevsky | 💡 planned | 0 | Notes from Underground, Brothers Karamazov — self-deception, faith |
| literary_dark_tolstoy | 💡 planned | 0 | The Death of Ivan Ilyich — late-life reckoning |
| literary_dark_shakespeare_tragedy | 💡 planned | 0 | Macbeth (ambition), King Lear (grief), Hamlet (mortality) |
| literary_dark_camus_existential | 🌫 idea | 0 | Myth of Sisyphus, The Stranger — endurance without illusion |

### Season 07 — Field Notes

Ecological and naturalist material. Patience, recovery, place.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| field_notes_thoreau_walden | 💡 planned | 0 | Solitude, deliberate living, the wood pile |
| field_notes_aldo_leopold | 💡 planned | 0 | Sand County Almanac — the land ethic |
| field_notes_recovery_after_disturbance | 🔄 in production | 1 | Burned ridge piece already rendered; expand to 4-5 |

### Season 08 — Modern Discipline

The contemporary working-life arc.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| modern_discipline_useful_man | 💡 planned | 0 | Roosevelt's *Strenuous Life*, the man in the arena |
| modern_discipline_agrarian_dignity | 🌫 idea | 0 | Farmer with oxen image waits for content — Tolstoy's Levin or Berry |
| anti_doom_scroll_attention | 💡 planned | 0 | Choosing the window, putting the phone face-down |

### Season 09 — Cross-Civilizational

Eastern philosophy + war-strategy traditions.

| Arc | Status | Scripts | Notes |
|---|---|---:|---|
| eastern_taoism_restraint | 💡 planned | 0 | Tao Te Ching — wu wei, the value of softness |
| eastern_confucian_duty | 💡 planned | 0 | Analects — civic order, filial piety reframed |
| eastern_musashi_strategy | 💡 planned | 0 | Book of Five Rings — the long discipline of the warrior |

## Asset principle (new)

Going forward, the rule is:

- **Figures** = the named subject as an alpha-channel cutout. Composited onto a background by the render stage.
- **Backgrounds** = the world setting. People may appear as far-off distant figures, but the named subject is never the foreground of a background asset.

The 15 Rome backgrounds with named subjects (Marcus at lamp, Seneca at desk, Caesar at the Rubicon, etc.) were generated before this principle settled and are kept as "subject-in-scene" assets — usable, but future bgs should be subject-free. New Rome backgrounds 16–20 (Senate steps, legion road, ruined forum, bronze eagle, oil lamp & scroll) follow the new principle.

## How to add a new arc

1. Pick a row above marked 💡 planned, 📝 drafted, or 🌫 idea.
2. Identify which source entries under [sources/](sources/) feed it. Add new
   entries to the relevant `.md` file if needed (see [01_SCHEMA.md](01_SCHEMA.md)).
3. Copy [templates/era_entry_template.md](templates/era_entry_template.md) and
   write the arc YAML at `arcs/<region>_<arc>.yaml`. Use the existing
   [ancient_greece_iliad.yaml](arcs/ancient_greece_iliad.yaml) as a working
   reference.
4. Write the script YAMLs under
   `scripts/<region>/<arc>/NNN_<slug>.yaml`. ~65-85 words per ~30-second
   video. Voice/music/visual_world/visual_motif/caption_style per the
   conventions in [07_ARCS_AND_PRODUCTION.md](07_ARCS_AND_PRODUCTION.md).
5. Update the choreography file under [choreography/](choreography/) if the
   arc joins an existing season, or create a new season YAML.
6. Update this file: change the arc's status row from 💡/🌫 to 📝/🔄/✅.

## Priority for the next quarter

Right now the project has 26 scripts written (19 ancient_greece + 6 ancient_rome + 1 field_notes), 35 stoic_rome bgs, 105 backgrounds total, and a fresh batch of ~30 named figures in figures/masculine|feminine/ ready to be wired into specs once the figure pipeline is exercised.

Realistic next work:

1. **Render the 6 existing Rome specs** (stoic_discipline + seneca_on_time) — voice + captions + render. All backgrounds in place.
2. **Write source entries for the new Rome arcs** — Cicero *De Officiis*, Seneca *De Brevitate Vitae*, Lucretius *De Rerum Natura* III, Virgil *Aeneid* II + VI, Tacitus *Agricola*, Sallust *Catiline*, plus Marcus Meditations passages for waste-no-time, inner-citadel, universe-is-change, soon-forgotten. Most start as empty files like meditations.md/letters.md did.
3. **Write the 4 new "Duty and Self-Mastery" scripts** + **5 "Power, Empire, Corruption" scripts** + **6 "Death, Fate, Inner Citadel" scripts** = 15 new Rome scripts.
4. **Wire the new figures into the render pipeline.** The figure compositing path exists but is gated by alpha — verify which of the 30 new figures are alpha-channeled and update specs to reference them via `figure_prompt_key`.
5. **Generate the 2 missing Antigone backgrounds** (`antigone_throne_dawn`, `antigone_sisters_doorway`) so 011/012 can re-render cleanly. Old bindings were renamed to Andromache/Helen and moved to iliad/.
6. **Greek tragedy arc** (Oedipus + Euripides) — fills out Season 01.

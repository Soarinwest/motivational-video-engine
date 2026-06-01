"""One-shot back-fill: add new schema fields to every script YAML.

Adds top-level fields to each script:
  - quote_type: direct_quote | excerpt | paraphrase | narrative_scene
  - music_asset: { local_path, rights_status, attribution_required }
  - quote_integrity: { exact_translation_verified, public_domain_translation,
                        wording_modified_for_script }
  - speaker: { name, role }
  - addressee: { name, role }
  - scene_context: >

Pulls speaker/addressee/scene_context from the matching source entry if it
already has them; falls back to a hand-curated lookup table for older
entries; leaves empty placeholders otherwise.

Idempotent: skips scripts that already contain a top-level `quote_type:` line.

Run:  .venv/Scripts/python.exe scripts/backfill_script_schema.py
"""

from __future__ import annotations

from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
ASSETS_MUSIC = REPO / "assets" / "music"

# ---- Music routing ---------------------------------------------------------

# Script music key -> brand.yaml music_profile key
MUSIC_KEY_TO_PROFILE: dict[str, str] = {
    "ancient_low_drone": "ambient_low",
    "low_strings": "ambient_strings_low",
    "soft_lyre_ambient": "soft_lyre_ambient",
    "somber_cinematic": "somber_cinematic",
    "bardic_invocation": "bardic_invocation",
    "bronze_war_camp": "bronze_war_camp",
    "dark_rage": "dark_rage",
    "grief_lament": "grief_lament",
    "underworld_grief": "underworld_grief",
    "aegean_voyage": "aegean_voyage",
    "island_enchantment": "island_enchantment",
    "cave_tension": "cave_tension",
    "underworld_descent": "underworld_descent",
    "homecoming_recognition": "homecoming_recognition",
    "heroic_honor": "heroic_honor",
    "norse_skald_chant": "norse_skald_chant",
    "norse_hall_of_slain": "norse_hall_of_slain",
    "norse_seeress": "norse_seeress",
    "norse_shieldmaiden": "norse_shieldmaiden",
}

# brand.yaml music_profile key -> assets/music/ folder
MUSIC_PROFILE_TO_FOLDER: dict[str, str] = {
    "ambient_low": "ancient_low_drone",
    "ambient_strings_low": "low_strings",
    "soft_lyre_ambient": "soft_lyre_ambient",
    "somber_cinematic": "somber_cinematic",
    "bardic_invocation": "bardic_invocation",
    "bronze_war_camp": "bronze_war_camp",
    "dark_rage": "dark_rage",
    "grief_lament": "grief_lament",
    "underworld_grief": "underworld_grief",
    "aegean_voyage": "aegean_voyage",
    "island_enchantment": "island_enchantment",
    "cave_tension": "cave_tension",
    "underworld_descent": "underworld_descent",
    "homecoming_recognition": "homecoming_recognition",
    "heroic_honor": "heroic_honor",
    "norse_skald_chant": "norse_skald_chant",
    "norse_hall_of_slain": "norse_hall_of_slain",
    "norse_seeress": "norse_seeress",
    "norse_shieldmaiden": "norse_shieldmaiden",
}


def first_track_in(folder: str) -> str:
    """Return relative repo path of the first .mp3 in assets/music/<folder>/."""
    p = ASSETS_MUSIC / folder
    if not p.exists():
        return ""
    files = sorted(p.glob("*.mp3"))
    return f"music/{folder}/{files[0].name}" if files else ""


# ---- Narrative-scene flagging (from the audit) -----------------------------

NARRATIVE_SCENE_IDS: set[str] = {
    "011_homer_hector_farewell",
    "012_homer_priam_mercy",
    "013_homer_patroclus_rage",
    "015_homer_andromache_the_news",
    "015_homer_calypso_refuse",
    "016_homer_penelope_patience",
    "017_homer_tiresias_underworld",
    "001_cincinnatus_power_to_plow",
    "003_brutus_republic_over_blood",
}

# ---- Speaker / addressee fallbacks for source entries lacking these --------
# Keyed by quote_source_id. Tuple: (spk_name, spk_role, adr_name, adr_role, scene_context)

FALLBACKS: dict[str, tuple[str, str, str, str, str]] = {
    # Iliad (older entries without speaker/addressee in source)
    "homer_iliad_check_anger": (
        "Nestor", "elder Greek king and counselor",
        "Agamemnon", "commander of the Achaean army",
        "Nestor intervenes during the quarrel between Agamemnon and Achilles in Book I.",
    ),
    "homer_iliad_end_quarrel": (
        "Nestor", "elder Greek king and counselor",
        "Agamemnon and Achilles", "the quarreling leaders",
        "Nestor pleads with both men to end the quarrel before it ruins the Greek army.",
    ),
    "homer_iliad_order_not_me": (
        "Achilles", "greatest Greek warrior, dishonored by Agamemnon",
        "Agamemnon", "commander of the Achaean army",
        "Achilles refuses Agamemnon's authority after the seizure of Briseis.",
    ),
    "homer_iliad_hector_farewell": (
        "Hector", "Trojan prince and defender of Troy",
        "Andromache", "his wife",
        "Hector embraces Andromache and their infant son at the Scaean Gates before returning to the war that will kill him.",
    ),
    "homer_iliad_priam_mercy": (
        "Priam", "king of Troy, father of Hector",
        "Achilles", "the warrior who killed his son",
        "Priam crosses the battlefield at night to beg Achilles for the body of Hector.",
    ),
    "homer_iliad_patroclus_rage": (
        "Homeric narrator", "epic narrator",
        "the reader", "a reader watching grief turn what pride could not move",
        "Achilles refuses to fight for Agamemnon but rises the moment Patroclus is killed.",
    ),
    "homer_iliad_achilles_two_fates": (
        "Achilles", "greatest Greek warrior",
        "the embassy (Odysseus, Phoenix, Ajax)", "envoys sent by Agamemnon to bring Achilles back to the war",
        "Achilles tells the embassy his mother's prophecy: stay and die famous, or go home and live obscure.",
    ),
    "homer_iliad_andromache_the_news": (
        "Homeric narrator", "epic narrator",
        "the reader", "a reader watching the moment domestic warmth ends",
        "Andromache is at her loom warming Hector's bath when the wail comes up from the walls.",
    ),
    "homer_iliad_helen_self_blame": (
        "Helen", "Helen of Troy, cause of the war",
        "Priam", "king of Troy",
        "On the walls of Troy, Helen identifies the Greek champions for Priam and begins by blaming herself.",
    ),
    # Odyssey
    "homer_odyssey_tell_muse": (
        "Homeric narrator", "epic narrator invoking the Muse",
        "Muse", "goddess invoked as the source of song",
        "The opening invocation of the Odyssey.",
    ),
    "homer_odyssey_suffered_much": (
        "Homeric narrator", "epic narrator",
        "Muse", "goddess invoked as the source of song",
        "Part of the opening invocation — Odysseus's burden was the leader's return with what was left.",
    ),
    "homer_odyssey_want_home": (
        "Odysseus", "the returning hero",
        "Calypso", "the immortal who has held him on her island",
        "On Calypso's island, Odysseus refuses immortality. He wants only to go home.",
    ),
    "homer_odyssey_bear_it": (
        "Odysseus", "the returning hero, setting out",
        "Calypso", "the immortal letting him go",
        "Odysseus accepts that the sea may wreck him; he will bear it and go on.",
    ),
    "homer_odyssey_polyphemus_cunning": (
        "Odysseus", "trapped in the Cyclops's cave",
        "Polyphemus", "the Cyclops",
        "Odysseus gives the false name 'Noman' to escape the cave; later shouts his real name and pays for it.",
    ),
    "homer_odyssey_calypso_refuse": (
        "Odysseus", "the returning hero",
        "Calypso", "the immortal who has offered him eternal life",
        "Calypso offers Odysseus eternal life on her island. He refuses, choosing mortality and home.",
    ),
    "homer_odyssey_penelope_patience": (
        "Homeric narrator", "epic narrator",
        "the reader", "a reader watching active patience hold a house",
        "Penelope weaves Laertes's burial shroud by day and unweaves it by night to delay the suitors.",
    ),
    "homer_odyssey_tiresias_underworld": (
        "Tiresias", "the blind prophet in the land of the dead",
        "Odysseus", "the living man who has crossed to consult him",
        "Odysseus descends to the underworld in Book XI to ask the way home.",
    ),
    # Plato / Aristotle / Epictetus (Greek philosophy)
    "plato_apology_unexamined_life": (
        "Socrates", "philosopher on trial in Athens, 399 BCE",
        "the Athenian jury", "the men who will sentence him",
        "Socrates refuses to accept exile over death. The unexamined life, he says, is not worth living.",
    ),
    "plato_republic_justice_soul": (
        "Socrates (in Plato's Republic)", "philosopher arguing for the inner-order conception of justice",
        "Glaucon and Adeimantus", "interlocutors in the Republic dialogue",
        "Book IV: justice is the proper order of the parts of the soul, not just compliance with external law.",
    ),
    "plato_republic_justice_happiness": (
        "Socrates (in Plato's Republic)", "philosopher",
        "Glaucon", "interlocutor in the Republic dialogue",
        "Book IV-IX argument: the just soul is the happy soul; injustice is a form of internal disorder that cannot be healthy.",
    ),
    "plato_republic_good_soul_rules": (
        "Socrates (in Plato's Republic)", "philosopher",
        "Glaucon", "interlocutor",
        "Republic IV: the soul has parts; the just person is the one whose reason rules the appetites and the spirited part follows reason.",
    ),
    "epictetus_enchiridion_control": (
        "Epictetus", "Stoic philosopher, former slave",
        "his student / reader", "a man seeking what is in his power",
        "Opening of the Enchiridion: the first lesson of Stoic practice is the discipline of distinguishing what is and is not under one's control.",
    ),
    "aristotle_ethics_perfected_by_habit": (
        "Aristotle", "philosopher, on the genesis of moral virtue",
        "his student / reader", "anyone seeking to form good character",
        "Nicomachean Ethics II: moral virtues are not given by nature; they are formed by practice.",
    ),
    "aristotle_ethics_moral_virtue_habit": (
        "Aristotle", "philosopher",
        "his student / reader", "anyone seeking moral education",
        "Nicomachean Ethics II.1: moral virtue is the result of habit; ethical character is built by repeated action.",
    ),
    "aristotle_ethics_first_exercising": (
        "Aristotle", "philosopher",
        "his student / reader", "anyone in moral training",
        "Nicomachean Ethics II.4: practice precedes virtue; a man becomes just by doing just things first, however imperfectly.",
    ),
    "aristotle_ethics_not_by_nature": (
        "Aristotle", "philosopher",
        "his student / reader", "anyone forming character",
        "Nicomachean Ethics II.1: virtue does not arise in us by nature but by habituation; nature gives the capacity, practice fills it.",
    ),
    # Sophocles Antigone
    "sophocles_antigone_i_deny_not": (
        "Antigone", "Theban princess defying Creon's decree",
        "Creon", "king of Thebes, her uncle",
        "Creon confronts Antigone about the burial of Polynices. She refuses to dissemble.",
    ),
    "sophocles_antigone_unwritten_laws": (
        "Antigone", "Theban princess defying Creon's decree",
        "Creon", "king of Thebes",
        "Antigone tells the king his edict cannot override the older, unwritten laws of the gods.",
    ),
    "sophocles_antigone_grief_sisters": (
        "Antigone", "Theban princess",
        "Ismene", "her sister",
        "Before the burial, Antigone tells Ismene plainly: she has already seen every kind of grief.",
    ),
    # Marcus (older entries)
    "marcus_meditations_morning_preparation": (
        "Marcus Aurelius", "emperor writing to himself on campaign",
        "himself", "a man preparing to meet other people at their worst",
        "Marcus rehearses the day's difficulty before it arrives — Meditations II.1.",
    ),
    "marcus_meditations_as_if_last_act": (
        "Marcus Aurelius", "emperor writing to himself",
        "himself", "a man preparing to act with full attention",
        "Marcus instructs himself: act now with simple dignity, put down every other thought — Meditations II.5.",
    ),
    "marcus_meditations_depart_this_moment": (
        "Marcus Aurelius", "emperor writing to himself",
        "himself", "a man under death's nearness",
        "Marcus writes the single sentence the rest of Book II is built around — Meditations II.11.",
    ),
    # Seneca (older entries)
    "seneca_letters_hold_every_hour": (
        "Seneca", "Stoic teacher writing to Lucilius",
        "Lucilius", "the recipient of the Moral Letters",
        "Letter I — Seneca's first instruction: hold the hour, get today's work done now.",
    ),
    "seneca_letters_remain_in_one_place": (
        "Seneca", "Stoic teacher writing to Lucilius",
        "Lucilius", "the recipient of the Moral Letters",
        "Letter II — the first sign of a settled mind is the ability to stay in one place.",
    ),
    "seneca_letters_each_day_a_life": (
        "Seneca", "Stoic teacher writing to Lucilius",
        "Lucilius", "the recipient of the Moral Letters",
        "Letter XII — close every day as if it were the end of life; postpone nothing.",
    ),
}


# ---- Source-entry lookup ---------------------------------------------------

def find_source_entry(source_id: str) -> dict:
    """Find the source entry by id in content_library/sources/**/*.md."""
    sources_dir = REPO / "content_library" / "sources"
    for md in sources_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        # YAML blocks are fenced as ```yaml ... ```
        parts = text.split("```yaml")
        for blk in parts[1:]:
            yaml_text = blk.split("```", 1)[0]
            try:
                entry = yaml.safe_load(yaml_text)
            except Exception:
                continue
            if isinstance(entry, dict) and entry.get("id") == source_id:
                return entry
    return {}


# ---- Field computation -----------------------------------------------------

def compute_fields(script: dict) -> dict:
    sid = script.get("script_id", "")
    source_id = script.get("quote_source_id", "")
    music_key = script.get("music", "")

    src = find_source_entry(source_id)

    # quote_type
    if sid in NARRATIVE_SCENE_IDS:
        quote_type = "narrative_scene"
    elif (src.get("content") or {}).get("direct_quote", "").strip():
        quote_type = "direct_quote"
    else:
        quote_type = "narrative_scene"

    # music_asset
    profile = MUSIC_KEY_TO_PROFILE.get(music_key, "")
    folder = MUSIC_PROFILE_TO_FOLDER.get(profile, "")
    local_path = first_track_in(folder)

    # quote_integrity
    src_source = src.get("source") or {}
    src_content = src.get("content") or {}
    has_direct = bool(src_content.get("direct_quote", "").strip())
    translation_verified = not src_source.get("translation_check_needed", True)
    pd_translation = src_source.get("rights_status", "") == "public_domain_translation"

    # speaker / addressee / scene_context
    src_speaker = src.get("speaker") or {}
    src_addressee = src.get("addressee") or {}
    src_scene = (src.get("scene_context") or "").strip()

    if src_speaker.get("name") and src_addressee.get("name"):
        spk_name = src_speaker.get("name", "")
        spk_role = src_speaker.get("role", "")
        adr_name = src_addressee.get("name", "")
        adr_role = src_addressee.get("role", "")
        scene = src_scene
    elif source_id in FALLBACKS:
        spk_name, spk_role, adr_name, adr_role, scene = FALLBACKS[source_id]
    else:
        spk_name = spk_role = adr_name = adr_role = scene = ""

    return {
        "quote_type": quote_type,
        "music_asset": {
            "local_path": local_path,
            "rights_status": "open_license_attribution_required",
            "attribution_required": True,
        },
        "quote_integrity": {
            "exact_translation_verified": translation_verified,
            "public_domain_translation": pd_translation,
            "wording_modified_for_script": False,
        },
        "speaker": {"name": spk_name, "role": spk_role},
        "addressee": {"name": adr_name, "role": adr_role},
        "scene_context": scene,
    }


# ---- YAML block serialization ----------------------------------------------

def _wrap_paragraph(text: str, width: int = 78, indent: str = "  ") -> list[str]:
    """Wrap a paragraph to YAML folded-scalar lines at <= width cols."""
    words = text.split()
    lines: list[str] = []
    cur = indent
    for w in words:
        if len(cur) + len(w) + 1 > width and cur.strip():
            lines.append(cur.rstrip())
            cur = indent
        cur += w + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def fields_to_yaml(fields: dict) -> str:
    L: list[str] = []
    L.append(f"quote_type: {fields['quote_type']}")
    L.append("")
    L.append("music_asset:")
    ma = fields["music_asset"]
    L.append(f'  local_path: "{ma["local_path"]}"')
    L.append(f"  rights_status: {ma['rights_status']}")
    L.append(f"  attribution_required: {str(ma['attribution_required']).lower()}")
    L.append("")
    L.append("quote_integrity:")
    qi = fields["quote_integrity"]
    L.append(f"  exact_translation_verified: {str(qi['exact_translation_verified']).lower()}")
    L.append(f"  public_domain_translation: {str(qi['public_domain_translation']).lower()}")
    L.append(f"  wording_modified_for_script: {str(qi['wording_modified_for_script']).lower()}")
    L.append("")
    L.append("speaker:")
    sp = fields["speaker"]
    L.append(f'  name: "{sp["name"]}"')
    L.append(f'  role: "{sp["role"]}"')
    L.append("")
    L.append("addressee:")
    ad = fields["addressee"]
    L.append(f'  name: "{ad["name"]}"')
    L.append(f'  role: "{ad["role"]}"')
    L.append("")
    sc = fields["scene_context"]
    if sc:
        L.append("scene_context: >")
        L.extend(_wrap_paragraph(sc))
    else:
        L.append('scene_context: ""')
    return "\n".join(L)


# ---- File-level update -----------------------------------------------------

def update_script_file(script_path: Path) -> str:
    text = script_path.read_text(encoding="utf-8")
    if "\nquote_type:" in text or text.startswith("quote_type:"):
        return "skip"

    script = yaml.safe_load(text)
    if not isinstance(script, dict):
        return "skip"

    fields = compute_fields(script)
    block = fields_to_yaml(fields)

    lines = text.split("\n")
    new_lines: list[str] = []
    inserted = False
    for ln in lines:
        new_lines.append(ln)
        if not inserted and ln.startswith("caption_style:"):
            new_lines.append("")
            new_lines.append(block)
            inserted = True

    if not inserted:
        return "no-anchor"

    script_path.write_text("\n".join(new_lines), encoding="utf-8")
    return "ok"


def main() -> None:
    scripts_dir = REPO / "content_library" / "scripts"
    counts: dict[str, int] = {"ok": 0, "skip": 0, "no-anchor": 0}
    for f in sorted(scripts_dir.rglob("*.yaml")):
        status = update_script_file(f)
        counts[status] = counts.get(status, 0) + 1
        if status != "skip":
            print(f"{status:10s} {f.relative_to(REPO)}")
    print(f"\nOK: {counts['ok']}, Skipped (already has fields): {counts['skip']}, No anchor: {counts['no-anchor']}")


if __name__ == "__main__":
    main()

"""One-off transformer: content_library script YAMLs -> ContentSpec YAMLs.

For each of the 10 ancient_greece scripts under content_library/scripts/,
this generates a ContentSpec under outputs/specs/ and copies the chosen
background asset to the pipeline-expected path
(assets/backgrounds/<world>/<bg_key>.<ext>).

After running this, render each spec with `motive render` (or the bash
loop at the bottom of this file).

Why a script and not a long-term tool: the field mapping is opinionated
(splitting a single script: block into hook/voiceover/final_line,
picking which existing asset substitutes for a missing one). Codifying
these decisions in a permanent transformer would lock in arbitrary
choices. Better to handle this as a one-shot per arc until the
patterns settle.
"""

from __future__ import annotations

import shutil
from pathlib import Path
import yaml

# Voice slug used in content_library -> voice_profile in config/voices.yaml.
VOICE_MAP = {
    "bm_george": "classical_male",
    "am_michael": "low_steady_male",
    "bm_lewis": "literary_male",
    "narrator_blend": "narrator_blend",
}

# Music slug used in content_library -> music_profile in config/brand.yaml.
MUSIC_MAP = {
    # legacy ambient motifs
    "ancient_low_drone": "ambient_low",
    "low_strings": "ambient_strings_low",
    "soft_lyre_ambient": "soft_lyre_ambient",
    "somber_cinematic": "somber_cinematic",
    # Iliad
    "bardic_invocation": "bardic_invocation",
    "bronze_war_camp": "bronze_war_camp",
    "dark_rage": "dark_rage",
    "grief_lament": "grief_lament",
    "underworld_grief": "underworld_grief",
    # Odyssey
    "aegean_voyage": "aegean_voyage",
    "island_enchantment": "island_enchantment",
    "cave_tension": "cave_tension",
    "underworld_descent": "underworld_descent",
    "homecoming_recognition": "homecoming_recognition",
    # Cross-arc
    "heroic_honor": "heroic_honor",
    # Norse (Season 04 staging)
    "norse_skald_chant": "norse_skald_chant",
    "norse_hall_of_slain": "norse_hall_of_slain",
    "norse_seeress": "norse_seeress",
    "norse_shieldmaiden": "norse_shieldmaiden",
}

# Per-script overrides. The asset choices are best-fit substitutes from
# the current inventory; revisit when world-specific assets are generated.
SCRIPTS = [
    {
        "script_id": "001_plato_examined_life",
        "arc": "self_command",
        "spec_id": "plato_examined_life_001",
        "author": "Plato (Socrates)",
        "theme": "self-command",
        "series": "socratic_questions",
        "world": "ancient_greece",
        "bg_key": "plato_examined_life",
        "bg_source": "ancient_greece/ancient_greece_socrates_agora_dusk_001.png",
        "motion": "slow_zoom",
    },
    {
        "script_id": "002_epictetus_control",
        "arc": "self_command",
        "spec_id": "epictetus_control_001",
        "author": "Epictetus",
        "theme": "self-command",
        "series": "stoic_practice",
        "world": "ancient_greece",
        "bg_key": "epictetus_control_vineyard",
        "bg_source": "ancient_greece/ancient_greece_mediterranean_vineyard_002.png",
        "motion": "slow_zoom",
    },
    {
        "script_id": "003_aristotle_habit",
        "arc": "self_command",
        "spec_id": "aristotle_habit_001",
        "author": "Aristotle",
        "theme": "habit",
        "series": "socratic_questions",
        "world": "ancient_greece",
        "bg_key": "aristotle_habit_coast",
        "bg_source": "ancient_greece/ancient_greece_mediterranean_coast_003.png",
        "motion": "slow_pan",
    },
    {
        "script_id": "004_plato_inner_order",
        "arc": "self_command",
        "spec_id": "plato_inner_order_001",
        "author": "Plato",
        "theme": "self-command",
        "series": "socratic_questions",
        "world": "ancient_greece",
        "bg_key": "plato_inner_order_temple",
        "bg_source": "ancient_greece/ancient_greece_temple_cliff_storm_001.png",
        "motion": "slow_zoom",
    },
    {
        "script_id": "005_aristotle_choice",
        "arc": "self_command",
        "spec_id": "aristotle_choice_001",
        "author": "Aristotle",
        "theme": "habit",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "aristotle_choice_marble",
        "bg_source": "stoic_rome/stoic_rome_marcus_bust_dawn_001.png",
        "motion": "slow_zoom",
    },
    # --- Iliad arc ---
    {
        "script_id": "006_homer_anger",
        "arc": "iliad",
        "spec_id": "homer_anger_001",
        "author": "Homer",
        "theme": "war",
        "series": "literary_dark",
        "world": "literary_dark",
        "bg_key": "homer_anger_storm",
        "bg_source": "hudson_river_school/heade_approaching_thunder_storm.jpg",
        "motion": "medium_zoom",
    },
    {
        "script_id": "007_homer_check_your_anger",
        "arc": "iliad",
        "spec_id": "homer_check_quarrel_001",
        "author": "Homer",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "war_camp_fire_meadow",
        "bg_source": None,  # already in place
        "motion": "medium_pan",
    },
    {
        "script_id": "011_homer_hector_farewell",
        "arc": "iliad",
        "spec_id": "homer_hector_farewell_001",
        "author": "Homer",
        "theme": "duty",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "hector_city_gates",
        "bg_source": None,  # already in place
        "motion": "figure_pan",
    },
    {
        "script_id": "012_homer_priam_mercy",
        "arc": "iliad",
        "spec_id": "homer_priam_mercy_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "priam_in_tent",
        "bg_source": None,  # already in place
        "motion": "medium_zoom",
    },
    {
        "script_id": "013_homer_patroclus_rage",
        "arc": "iliad",
        "spec_id": "homer_patroclus_rage_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "greek_ship_storm",
        "bg_source": None,
        "motion": "medium_zoom",
    },
    # --- Odyssey arc ---
    {
        "script_id": "008_homer_return_home",
        "arc": "odyssey",
        "spec_id": "homer_return_home_001",
        "author": "Homer",
        "theme": "endurance",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "ithaca_dawn_cliffs",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "009_homer_bear_the_wreck",
        "arc": "odyssey",
        "spec_id": "homer_bear_wreck_001",
        "author": "Homer",
        "theme": "endurance",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "oar_on_beach_sunset",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "014_homer_polyphemus_cunning",
        "arc": "odyssey",
        "spec_id": "homer_polyphemus_cunning_001",
        "author": "Homer",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "polyphemus_cave",
        "bg_source": None,
        "motion": "medium_zoom",
    },
    {
        "script_id": "015_homer_calypso_refuse",
        "arc": "odyssey",
        "spec_id": "homer_calypso_refuse_001",
        "author": "Homer",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "calypso_island_twilight",
        "bg_source": None,
        "motion": "medium_zoom",
    },
    {
        "script_id": "016_homer_penelope_patience",
        "arc": "odyssey",
        "spec_id": "homer_penelope_patience_001",
        "author": "Homer",
        "theme": "patience",
        "series": "women_left_alive",
        "world": "odyssey",
        "bg_key": "penelope_at_loom",
        "bg_source": None,
        "motion": "figure_pan",
    },
    {
        "script_id": "017_homer_tiresias_underworld",
        "arc": "odyssey",
        "spec_id": "homer_tiresias_underworld_001",
        "author": "Homer",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "underworld_shoreline",
        "bg_source": None,
        "motion": "medium_zoom",
    },
    # --- Women, Law, Tragedy ---
    {
        "script_id": "010_antigone_i_deny_nothing",
        "arc": "women_law_tragedy",
        "spec_id": "antigone_i_deny_nothing_001",
        "author": "Sophocles (Antigone)",
        "theme": "moral-responsibility",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "antigone_ruined_courtyard",
        "bg_source": "stoic_rome/stoic_rome_ruined_courtyard_dawn_001.png",
        "motion": "medium_zoom",
    },
    {
        "script_id": "011_antigone_unwritten_laws",
        "arc": "women_law_tragedy",
        "spec_id": "antigone_unwritten_laws_001",
        "author": "Sophocles (Antigone)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_greece",
        "bg_key": "temple_above_sea",
        "bg_source": None,  # Greek temple — fits "unwritten laws of Heaven"
        "motion": "slow_zoom",
    },
    {
        "script_id": "012_antigone_grief_after_war",
        "arc": "women_law_tragedy",
        "spec_id": "antigone_grief_after_war_001",
        "author": "Sophocles (Antigone)",
        "theme": "grief",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "ruined_forum_after_empire",
        "bg_source": None,  # ruins after collapse — fits Antigone's catalogued grief
        "motion": "slow_pan",
    },
    # --- Iliad arc additions (more Achilles + Andromache + Helen) ---
    {
        "script_id": "014_homer_achilles_two_fates",
        "arc": "iliad",
        "spec_id": "homer_achilles_two_fates_001",
        "author": "Homer",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "achilles_overlooking_camp",
        "bg_source": None,  # already in place
        "motion": "slow_zoom",
    },
    {
        "script_id": "015_homer_andromache_the_news",
        "arc": "iliad",
        "spec_id": "homer_andromache_the_news_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "andromache_on_city_walls",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "016_homer_helen_self_blame",
        "arc": "iliad",
        "spec_id": "homer_helen_self_blame_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "helen_of_troy_at_balcony_sea",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "017_homer_anger_opening",
        "arc": "iliad",
        "spec_id": "homer_anger_opening_001",
        "author": "Homer",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "troy_walls_storm",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "018_homer_patroclus_has_fallen",
        "arc": "iliad",
        "spec_id": "homer_patroclus_has_fallen_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "warrior_grieving_campfire",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "019_homer_gnawing_heart",
        "arc": "iliad",
        "spec_id": "homer_gnawing_heart_001",
        "author": "Homer",
        "theme": "grief",
        "series": "literary_dark",
        "world": "iliad",
        "bg_key": "war_tent_at_sunset",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "018_homer_bind_me_tighter",
        "arc": "odyssey",
        "spec_id": "homer_bind_me_tighter_001",
        "author": "Homer",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "sea_cave_entrance",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "019_homer_bed_test",
        "arc": "odyssey",
        "spec_id": "homer_bed_test_001",
        "author": "Homer",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "odyssey",
        "bg_key": "odysseus_olive_bed",
        "bg_source": None,
        "motion": "slow_zoom",
    },
]

REPO = Path(__file__).resolve().parent.parent
ASSETS_ROOT = REPO / "assets"
SCRIPTS_ROOT = REPO / "content_library" / "scripts" / "ancient_greece"
SPECS_OUT = REPO / "outputs" / "specs" / "ancient_greece"


def load_script(arc: str, script_id: str) -> dict:
    return yaml.safe_load((SCRIPTS_ROOT / arc / f"{script_id}.yaml").read_text(encoding="utf-8"))


def build_spec(meta: dict) -> dict:
    script = load_script(meta["arc"], meta["script_id"])
    raw_text = script["script"].strip()
    lines = [line for line in raw_text.splitlines() if line.strip()]
    hook = lines[0]
    final_line = lines[-1]
    voiceover = raw_text
    message = lines[0]

    voice = VOICE_MAP.get(script.get("voice", ""), "classical_male")
    music = MUSIC_MAP.get(script.get("music", ""), "ambient_low")

    duration = int(script.get("duration_target_seconds", 30))
    duration = max(10, min(90, duration))  # ContentSpec range

    return {
        "id": meta["spec_id"],
        "series": meta["series"],
        "author": meta["author"],
        "theme": meta["theme"],
        "duration_seconds": duration,
        "message": message,
        "hook": hook,
        "voiceover": voiceover,
        "final_line": final_line,
        "visual": {
            "world": meta["world"],
            "background_prompt_key": meta["bg_key"],
            "background_override_path": script.get("image_path") or None,
            "figure_prompt_key": "none",
            "motion_profile": meta.get("motion", "slow_zoom"),
            "overlays": [],
            "caption_style": "serif_quiet",
        },
        "audio": {
            "tts_provider": "kokoro",
            "voice_profile": voice,
            "music_profile": music,
        },
        "render": {
            "resolution": "1080x1920",
            "fps": 30,
            "format": "mp4",
        },
    }


def prep_asset(meta: dict) -> Path | None:
    """Copy the source background asset into the world's folder under the
    spec's bg_key. If meta['bg_source'] is None, no copy is performed — the
    target file is assumed to exist already (either it was renamed in place
    or will be generated via ComfyUI). Returns the target Path, or None if
    bg_source is None and no file exists at the expected target yet.
    """
    world_dir = ASSETS_ROOT / "backgrounds" / meta["world"]
    if meta.get("bg_source") is None:
        # Look for an existing file at world/bg_key.<ext>
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            candidate = world_dir / (meta["bg_key"] + ext)
            if candidate.is_file():
                return candidate
        return None  # gap — will need `motive make-images` to generate
    src = ASSETS_ROOT / "backgrounds" / meta["bg_source"]
    if not src.is_file():
        raise FileNotFoundError(f"Missing source asset: {src}")
    world_dir.mkdir(parents=True, exist_ok=True)
    dst = world_dir / (meta["bg_key"] + src.suffix.lower())
    if not dst.is_file():
        shutil.copy2(src, dst)
    return dst


def write_spec(meta: dict, spec: dict) -> Path:
    out_dir = SPECS_OUT / meta["arc"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{meta['spec_id']}.yaml"
    out_path.write_text(
        yaml.dump(spec, sort_keys=False, default_flow_style=False, width=120),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    for meta in SCRIPTS:
        spec = build_spec(meta)
        asset = prep_asset(meta)
        spec_path = write_spec(meta, spec)
        asset_str = asset.relative_to(REPO) if asset else "(MISSING — run `motive make-images`)"
        print(f"OK {meta['spec_id']:38s} spec={spec_path.relative_to(REPO)} asset={asset_str}")
    print(f"\nGenerated {len(SCRIPTS)} specs under {SPECS_OUT.relative_to(REPO)}/")


if __name__ == "__main__":
    main()

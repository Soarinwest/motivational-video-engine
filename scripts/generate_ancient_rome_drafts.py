"""One-off transformer: content_library Roman script YAMLs -> ContentSpec YAMLs.

Mirror of generate_ancient_greece_drafts.py, scoped to the ancient_rome
region. For each script under content_library/scripts/ancient_rome/,
this generates a ContentSpec under outputs/specs/ancient_rome/ and copies
the chosen background asset to the pipeline-expected path
(assets/backgrounds/<world>/<bg_key>.<ext>).

After running this, render each spec with `motive render`.

Why a separate file per region: keeping Greek and Roman concerns
apart matches the per-region scripts/ and specs/ layout, and avoids
one giant SCRIPTS table.
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
    # Norse
    "norse_skald_chant": "norse_skald_chant",
    "norse_hall_of_slain": "norse_hall_of_slain",
    "norse_seeress": "norse_seeress",
    "norse_shieldmaiden": "norse_shieldmaiden",
}

# Per-script overrides. Asset choices reuse existing stoic_rome backgrounds
# from assets/backgrounds/stoic_rome/. The bg_key becomes the canonical
# pipeline filename under that world.
SCRIPTS = [
    # --- ancient_rome_stoic_discipline (Marcus, Book II) ---
    {
        "script_id": "001_marcus_morning_preparation",
        "arc": "stoic_discipline",
        "spec_id": "marcus_morning_preparation_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "self-command",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_forum_morning",
        "bg_source": "stoic_rome/stoic_rome_forum_morning_001.png",
        "motion": "slow_zoom",
    },
    {
        "script_id": "002_marcus_as_if_last_act",
        "arc": "stoic_discipline",
        "spec_id": "marcus_as_if_last_act_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "duty",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_temple_platform",
        "bg_source": "stoic_rome/stoic_rome_roman_temple_platform_001.png",
        "motion": "static",
    },
    {
        "script_id": "003_marcus_depart_this_moment",
        "arc": "stoic_discipline",
        "spec_id": "marcus_depart_this_moment_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_road_mist",
        "bg_source": "stoic_rome/stoic_rome_roman_road_mist_001.png",
        "motion": "slow_pan",
    },
    # --- ancient_rome_seneca_on_time ---
    {
        "script_id": "001_seneca_hold_every_hour",
        "arc": "seneca_on_time",
        "spec_id": "seneca_hold_every_hour_001",
        "author": "Seneca (Letters)",
        "theme": "self-command",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "seneca_writing_desk",
        "bg_source": "stoic_rome/stoic_rome_seneca_writing_desk_storm_001.png",
        "motion": "slow_zoom",
    },
    {
        "script_id": "002_seneca_remain_in_one_place",
        "arc": "seneca_on_time",
        "spec_id": "seneca_remain_in_one_place_001",
        "author": "Seneca (Letters)",
        "theme": "restraint",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "seneca_stone_room_morning",
        "bg_source": "stoic_rome/stoic_rome_epictetus_stone_room_001.png",
        "motion": "static",
    },
    {
        "script_id": "003_seneca_each_day_a_life",
        "arc": "seneca_on_time",
        "spec_id": "seneca_each_day_a_life_001",
        "author": "Seneca (Letters)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "seneca_stone_room_dusk",
        "bg_source": "stoic_rome/stoic_rome_epictetus_stone_room_002.png",
        "motion": "slow_zoom",
    },
    # --- ancient_rome_duty_and_self_mastery (umbrella arc — Marcus, Seneca, Cicero) ---
    {
        "script_id": "004_marcus_waste_no_time_arguing",
        "arc": "duty_and_self_mastery",
        "spec_id": "marcus_waste_no_time_arguing_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "duty",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_do_not_argue_goodness",
        "bg_source": None,  # already in place
        "motion": "static",
    },
    {
        "script_id": "005_seneca_life_long_enough",
        "arc": "duty_and_self_mastery",
        "spec_id": "seneca_life_long_enough_001",
        "author": "Seneca (On the Shortness of Life)",
        "theme": "self-command",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "seneca_shortness_of_life",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "006_seneca_imagined_suffering",
        "arc": "duty_and_self_mastery",
        "spec_id": "seneca_imagined_suffering_001",
        "author": "Seneca (Letters)",
        "theme": "restraint",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "seneca_imagined_suffering",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "007_cicero_duty_over_advantage",
        "arc": "duty_and_self_mastery",
        "spec_id": "cicero_duty_over_advantage_001",
        "author": "Cicero (On Duties)",
        "theme": "duty",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "cicero_duty_over_advantage",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    # --- ancient_rome_power_empire_corruption (Livy, Plutarch, Tacitus, Sallust) ---
    {
        "script_id": "001_cincinnatus_power_to_plow",
        "arc": "power_empire_corruption",
        "spec_id": "cincinnatus_power_to_plow_001",
        "author": "Livy (Ab Urbe Condita)",
        "theme": "public-responsibility",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "cincinnatus_power_to_plow",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "002_caesar_crossing_rubicon",
        "arc": "power_empire_corruption",
        "spec_id": "caesar_crossing_rubicon_001",
        "author": "Plutarch (Life of Caesar)",
        "theme": "ambition",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "caesar_crossing_rubicon",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "003_brutus_republic_over_blood",
        "arc": "power_empire_corruption",
        "spec_id": "brutus_republic_over_blood_001",
        "author": "Plutarch (Life of Brutus)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "brutus_republic_over_blood",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "004_tacitus_desert_and_peace",
        "arc": "power_empire_corruption",
        "spec_id": "tacitus_desert_and_peace_001",
        "author": "Tacitus (Agricola)",
        "theme": "tyranny",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "tacitus_desert_and_peace",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "005_sallust_republic_rots_appetite",
        "arc": "power_empire_corruption",
        "spec_id": "sallust_republic_rots_appetite_001",
        "author": "Sallust (Conspiracy of Catiline)",
        "theme": "corruption",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "sallust_republic_rots_appetite",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    # --- ancient_rome_death_fate_inner_citadel (Marcus, Seneca, Lucretius, Virgil) ---
    {
        "script_id": "001_marcus_leave_life_now",
        "arc": "death_fate_inner_citadel",
        "spec_id": "marcus_leave_life_now_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_leave_life_now",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "002_marcus_inner_citadel",
        "arc": "death_fate_inner_citadel",
        "spec_id": "marcus_inner_citadel_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "self-command",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "marcus_inner_citadel",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "003_marcus_universe_is_change",
        "arc": "death_fate_inner_citadel",
        "spec_id": "marcus_universe_is_change_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "ruined_forum_after_empire",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "004_marcus_soon_forgotten",
        "arc": "death_fate_inner_citadel",
        "spec_id": "marcus_soon_forgotten_001",
        "author": "Marcus Aurelius (Meditations)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "bronze_eagle",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "005_seneca_death_always_with_us",
        "arc": "death_fate_inner_citadel",
        "spec_id": "seneca_death_always_with_us_001",
        "author": "Seneca (Letters)",
        "theme": "mortality",
        "series": "stoic_practice",
        "world": "stoic_rome",
        "bg_key": "oil_lamp_and_scroll",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "006_lucretius_fear_of_death",
        "arc": "death_fate_inner_citadel",
        "spec_id": "lucretius_fear_of_death_001",
        "author": "Lucretius (De Rerum Natura)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "lucretius_fear_of_death",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "007_virgil_burden_of_destiny",
        "arc": "death_fate_inner_citadel",
        "spec_id": "virgil_burden_of_destiny_001",
        "author": "Virgil (Aeneid)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "virgil_burden_of_destiny",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "008_virgil_founding_through_loss",
        "arc": "death_fate_inner_citadel",
        "spec_id": "virgil_founding_through_loss_001",
        "author": "Virgil (Aeneid)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "stoic_rome",
        "bg_key": "virgil_founding_through_loss",
        "bg_source": None,
        "motion": "slow_zoom",
    },
]

REPO = Path(__file__).resolve().parent.parent
ASSETS_ROOT = REPO / "assets"
SCRIPTS_ROOT = REPO / "content_library" / "scripts" / "ancient_rome"
SPECS_OUT = REPO / "outputs" / "specs" / "ancient_rome"


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
    duration = max(10, min(90, duration))

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
    target file is assumed to exist already. Returns the target Path, or
    None if bg_source is None and no file exists yet.
    """
    world_dir = ASSETS_ROOT / "backgrounds" / meta["world"]
    if meta.get("bg_source") is None:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            candidate = world_dir / (meta["bg_key"] + ext)
            if candidate.is_file():
                return candidate
        return None
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

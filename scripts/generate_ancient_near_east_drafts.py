"""Transformer: ancient_near_east script YAMLs -> ContentSpec YAMLs."""

from __future__ import annotations

import shutil
from pathlib import Path
import yaml

VOICE_MAP = {
    "bm_george": "classical_male",
    "am_michael": "low_steady_male",
    "bm_lewis": "literary_male",
    "narrator_blend": "narrator_blend",
}

MUSIC_MAP = {
    # legacy ambient motifs (cross-arc compatible)
    "ancient_low_drone": "ambient_low",
    "low_strings": "ambient_strings_low",
    "soft_lyre_ambient": "soft_lyre_ambient",
    "somber_cinematic": "somber_cinematic",
    # ANE / Biblical motifs
    "desert_low_drone": "desert_low_drone",
    "slow_harp_and_desert_wind": "slow_harp_and_desert_wind",
    "whirlwind_drone": "whirlwind_drone",
    "steady_hand_drum_and_lyre": "steady_hand_drum_and_lyre",
    "low_judgment_drums": "low_judgment_drums",
    "threshold_tension_drone": "threshold_tension_drone",
    "desert_lament_with_flute": "desert_lament_with_flute",
    "prophetic_lift": "prophetic_lift",
    "mesopotamian_lament": "mesopotamian_lament",
    "egyptian_reed_and_drone": "egyptian_reed_and_drone",
    "imperial_judgment": "imperial_judgment",
    "sacred_opera_lament": "sacred_opera_lament",
    "battle_return_lament": "battle_return_lament",
}

SCRIPTS = [
    {
        "script_id": "001_ecclesiastes_all_is_vanity",
        "arc": "biblical_wisdom",
        "spec_id": "ecclesiastes_all_is_vanity_001",
        "author": "Ecclesiastes (Qoheleth)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "ecclesiastes_all_is_vanity",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "002_ecclesiastes_time_for_everything",
        "arc": "biblical_wisdom",
        "spec_id": "ecclesiastes_time_for_everything_001",
        "author": "Ecclesiastes (Qoheleth)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "ecclesiastes_time_for_everything",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "003_job_limits_of_understanding",
        "arc": "biblical_wisdom",
        "spec_id": "job_limits_of_understanding_001",
        "author": "Book of Job",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "job_limits_of_understanding",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "004_proverbs_wisdom_builds_house",
        "arc": "biblical_wisdom",
        "spec_id": "proverbs_wisdom_builds_house_001",
        "author": "Proverbs",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "proverbs_wisdom_builds_house",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "005_proverbs_pride_before_fall",
        "arc": "biblical_wisdom",
        "spec_id": "proverbs_pride_before_fall_001",
        "author": "Proverbs",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "proverbs_pride_before_fall",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "006_genesis_sin_at_the_door",
        "arc": "biblical_wisdom",
        "spec_id": "genesis_sin_at_the_door_001",
        "author": "Genesis",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "genesis_sin_at_the_door",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "007_psalm_valley_shadow",
        "arc": "biblical_wisdom",
        "spec_id": "psalm_valley_shadow_001",
        "author": "Psalms",
        "theme": "courage",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "psalm_valley_shadow",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "008_isaiah_strength_renewed",
        "arc": "biblical_wisdom",
        "spec_id": "isaiah_strength_renewed_001",
        "author": "Isaiah",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "isaiah_strength_renewed",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "009_gilgamesh_fear_of_death",
        "arc": "biblical_wisdom",
        "spec_id": "gilgamesh_fear_of_death_001",
        "author": "Anonymous (Gilgamesh)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "gilgamesh_fear_of_death",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "010_amenemope_listen_to_wisdom",
        "arc": "biblical_wisdom",
        "spec_id": "amenemope_listen_to_wisdom_001",
        "author": "Amenemope",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "amenemope_listen_to_wisdom",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "011_psalm_number_our_days",
        "arc": "biblical_wisdom",
        "spec_id": "psalm_number_our_days_001",
        "author": "Psalm 90",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "psalm_number_our_days",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "012_micah_do_justice_love_mercy",
        "arc": "biblical_wisdom",
        "spec_id": "micah_do_justice_love_mercy_001",
        "author": "Micah",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "micah_do_justice_love_mercy",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "013_isaiah_here_am_i",
        "arc": "biblical_wisdom",
        "spec_id": "isaiah_here_am_i_001",
        "author": "Isaiah",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "isaiah_here_am_i",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "014_jeremiah_fire_in_the_bones",
        "arc": "biblical_wisdom",
        "spec_id": "jeremiah_fire_in_the_bones_001",
        "author": "Jeremiah",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "jeremiah_fire_in_the_bones",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "015_lamentations_new_every_morning",
        "arc": "biblical_wisdom",
        "spec_id": "lamentations_new_every_morning_001",
        "author": "Lamentations",
        "theme": "courage",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "lamentations_new_every_morning",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "016_proverbs_soft_answer",
        "arc": "biblical_wisdom",
        "spec_id": "proverbs_soft_answer_001",
        "author": "Proverbs",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "proverbs_soft_answer",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "017_proverbs_keep_thy_heart",
        "arc": "biblical_wisdom",
        "spec_id": "proverbs_keep_thy_heart_001",
        "author": "Proverbs",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "proverbs_keep_thy_heart",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "018_daniel_refuse_defilement",
        "arc": "biblical_wisdom",
        "spec_id": "daniel_refuse_defilement_001",
        "author": "Daniel",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "daniel_refuse_defilement",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "019_jonah_mercy_wider_than_anger",
        "arc": "biblical_wisdom",
        "spec_id": "jonah_mercy_wider_than_anger_001",
        "author": "Jonah",
        "theme": "duty",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "jonah_mercy_wider_than_anger",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "020_gilgamesh_return_to_the_walls",
        "arc": "biblical_wisdom",
        "spec_id": "gilgamesh_return_to_the_walls_001",
        "author": "Anonymous (Gilgamesh)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "ancient_near_east",
        "bg_key": "gilgamesh_return_to_the_walls",
        "bg_source": None,
        "motion": "slow_zoom",
    },
]

REPO = Path(__file__).resolve().parent.parent
ASSETS_ROOT = REPO / "assets"
SCRIPTS_ROOT = REPO / "content_library" / "scripts" / "ancient_near_east"
SPECS_OUT = REPO / "outputs" / "specs" / "ancient_near_east"


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
        asset_str = asset.relative_to(REPO) if asset else "(MISSING)"
        print(f"OK {meta['spec_id']:38s} spec={spec_path.relative_to(REPO)} asset={asset_str}")
    print(f"\nGenerated {len(SCRIPTS)} specs under {SPECS_OUT.relative_to(REPO)}/")


if __name__ == "__main__":
    main()

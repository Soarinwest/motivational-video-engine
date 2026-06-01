"""Transformer: medieval_world script YAMLs -> ContentSpec YAMLs.

Mirror of generate_ancient_rome_drafts.py, scoped to the medieval_world
region (Norse / Anglo-Saxon material). Generates a ContentSpec under
outputs/specs/medieval_world/<arc>/<spec_id>.yaml and resolves the
spec's background asset from assets/backgrounds/<world>/<bg_key>.png.
"""

from __future__ import annotations

import shutil
from pathlib import Path
import yaml

VOICE_MAP = {
    "bm_george": "classical_male",
    "am_michael": "low_steady_male",
    "bm_lewis": "literary_male",
}

MUSIC_MAP = {
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
    # Norse / Anglo-Saxon (this arc's primary vocabulary)
    "low_war_drone": "low_war_drone",
    "cold_ambient": "cold_ambient",
    "dark_strings": "dark_strings",
    "nordic_chant_low": "nordic_chant_low",
    "distant_frame_drum": "distant_frame_drum",
    # Norse audio source folders (also exposed directly)
    "norse_skald_chant": "norse_skald_chant",
    "norse_hall_of_slain": "norse_hall_of_slain",
    "norse_seeress": "norse_seeress",
    "norse_shieldmaiden": "norse_shieldmaiden",
    # Samurai / Zen (Japan arc)
    "temple_drum_low": "temple_drum_low",
    "low_taiko_restraint": "low_taiko_restraint",
    "still_koto_dark": "still_koto_dark",
    "wooden_dojo_pulse": "wooden_dojo_pulse",
    "rain_and_low_koto": "rain_and_low_koto",
    "death_awareness_drone": "death_awareness_drone",
    "temple_bell_mist": "temple_bell_mist",
    "silence_and_bell": "silence_and_bell",
    "soft_shakuhachi_roomtone": "soft_shakuhachi_roomtone",
    "temple_drum_and_koto_resolve": "temple_drum_and_koto_resolve",
}

SCRIPTS = [
    # --- northern_fate_courage_under_doom ---
    {
        "script_id": "001_havamal_reputation_after_death",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "havamal_reputation_after_death_001",
        "author": "Anonymous (Hávamál)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "havamal_reputation_after_death",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "002_havamal_wisdom_and_silence",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "havamal_wisdom_and_silence_001",
        "author": "Anonymous (Hávamál)",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "havamal_wisdom_and_silence",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "003_odin_wisdom_cost",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "odin_wisdom_cost_001",
        "author": "Anonymous (Hávamál — Runatal)",
        "theme": "sacrifice",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "odin_wisdom_has_a_cost",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "004_voluspa_fate_of_gods",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "voluspa_fate_of_gods_001",
        "author": "Anonymous (Völuspá)",
        "theme": "fate",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "voluspa_fate_of_the_gods",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "005_ragnarok_even_gods_fall",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "ragnarok_even_gods_fall_001",
        "author": "Anonymous (Völuspá)",
        "theme": "courage",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "ragnarok_even_gods_fall",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "006_beowulf_face_the_monster",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "beowulf_face_the_monster_001",
        "author": "Anonymous (Beowulf)",
        "theme": "courage",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "beowulf_face_the_monster",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "007_beowulf_old_king_last_fight",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "beowulf_old_king_last_fight_001",
        "author": "Anonymous (Beowulf)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "beowulf_old_king_last_fight",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "008_wanderer_exile_and_memory",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "wanderer_exile_and_memory_001",
        "author": "Anonymous (The Wanderer)",
        "theme": "grief",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "wanderer_exile_and_memory",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "009_seafarer_cold_sea_trial",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "seafarer_cold_sea_trial_001",
        "author": "Anonymous (The Seafarer)",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "seafarer_cold_sea_trial",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "010_maldon_courage_after_defeat",
        "arc": "northern_fate_courage_under_doom",
        "spec_id": "maldon_courage_after_defeat_001",
        "author": "Anonymous (The Battle of Maldon)",
        "theme": "courage",
        "series": "literary_dark",
        "world": "northern_fate",
        "bg_key": "maldon_courage_after_defeat",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    # --- samurai_zen_discipline_death_form ---
    {
        "script_id": "001_nitobe_rectitude_straight_path",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "nitobe_rectitude_straight_path_001",
        "author": "Inazo Nitobe (Bushido)",
        "theme": "duty",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "rectitude_straight_path",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "002_nitobe_courage_and_right_action",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "nitobe_courage_and_right_action_001",
        "author": "Inazo Nitobe (Bushido)",
        "theme": "courage",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "courage_and_right_action",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "003_nitobe_honor_as_inner_judge",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "nitobe_honor_as_inner_judge_001",
        "author": "Inazo Nitobe (Bushido)",
        "theme": "honor_service",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "honor_as_inner_judge",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "004_musashi_the_way_is_practice",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "musashi_the_way_is_practice_001",
        "author": "Miyamoto Musashi (Five Rings)",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "way_is_practice",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "005_musashi_form_without_show",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "musashi_form_without_show_001",
        "author": "Miyamoto Musashi (Five Rings)",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "form_without_show",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "006_hagakure_death_before_panic",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "hagakure_death_before_panic_001",
        "author": "Yamamoto Tsunetomo (Hagakure)",
        "theme": "mortality",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "death_before_panic",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "007_zen_gateless_gate",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "zen_gateless_gate_001",
        "author": "Wumen Huikai (Gateless Gate)",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "gateless_gate",
        "bg_source": None,
        "motion": "slow_pan",
    },
    {
        "script_id": "008_zen_empty_mind_full_attention",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "zen_empty_mind_full_attention_001",
        "author": "Zen tradition",
        "theme": "self-command",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "empty_mind_full_attention",
        "bg_source": None,
        "motion": "static",
    },
    {
        "script_id": "009_tea_form_and_respect",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "tea_form_and_respect_001",
        "author": "Japanese tea tradition",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "tea_form_and_respect",
        "bg_source": None,
        "motion": "slow_zoom",
    },
    {
        "script_id": "010_samurai_restraint_power_under_form",
        "arc": "samurai_zen_discipline_death_form",
        "spec_id": "samurai_restraint_power_under_form_001",
        "author": "project synthesis",
        "theme": "restraint",
        "series": "literary_dark",
        "world": "samurai_zen",
        "bg_key": "power_under_form",
        "bg_source": None,
        "motion": "static",
    },
]

REPO = Path(__file__).resolve().parent.parent
ASSETS_ROOT = REPO / "assets"
SCRIPTS_ROOT = REPO / "content_library" / "scripts" / "medieval_world"
SPECS_OUT = REPO / "outputs" / "specs" / "medieval_world"


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
        asset_str = asset.relative_to(REPO) if asset else "(MISSING — run `motive make-images`)"
        print(f"OK {meta['spec_id']:38s} spec={spec_path.relative_to(REPO)} asset={asset_str}")
    print(f"\nGenerated {len(SCRIPTS)} specs under {SPECS_OUT.relative_to(REPO)}/")


if __name__ == "__main__":
    main()

"""Tests for the render stage.

End-to-end rendering (MoviePy + FFmpeg) is verified by running the CLI on a
real spec — too slow + fragile for the default pytest run. These tests cover
the pure helpers: asset resolution, resolution parsing.
"""

from pathlib import Path

import pytest

from motive_engine.schemas import ContentSpec
from motive_engine.stages.render import (
    ASSET_EXTENSIONS,
    resolve_assets,
    parse_resolution,
)
from motive_engine.utils import load_yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "specs"


def _spec(name: str) -> ContentSpec:
    return ContentSpec.model_validate(load_yaml(EXAMPLES / name))


def _make_asset(path: Path) -> None:
    """Create an empty file at `path` (sufficient for is_file() checks)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")


# ---- parse_resolution -----------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("1080x1920", (1080, 1920)),
        ("1920x1080", (1920, 1080)),
        ("720x1280", (720, 1280)),
    ],
)
def test_parse_resolution_valid(raw: str, expected: tuple[int, int]) -> None:
    assert parse_resolution(raw) == expected


@pytest.mark.parametrize("raw", ["1080", "1080x", "x1920", "1080x1920x60"])
def test_parse_resolution_invalid_raises(raw: str) -> None:
    with pytest.raises((ValueError, IndexError)):
        parse_resolution(raw)


# ---- resolve_assets -------------------------------------------------------


def test_resolve_assets_finds_background_and_figure(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    bg = tmp_path / "backgrounds" / spec.visual.world / f"{spec.visual.background_prompt_key}.png"
    fig = tmp_path / "figures" / spec.visual.world / f"{spec.visual.figure_prompt_key}.png"
    _make_asset(bg)
    _make_asset(fig)

    paths = resolve_assets(spec, assets_root=tmp_path)
    assert paths.background == bg
    assert paths.figure == fig


def test_resolve_assets_finds_jpg(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    bg = tmp_path / "backgrounds" / spec.visual.world / f"{spec.visual.background_prompt_key}.jpg"
    fig = tmp_path / "figures" / spec.visual.world / f"{spec.visual.figure_prompt_key}.jpg"
    _make_asset(bg)
    _make_asset(fig)

    paths = resolve_assets(spec, assets_root=tmp_path)
    assert paths.background.suffix == ".jpg"
    assert paths.figure is not None and paths.figure.suffix == ".jpg"


def test_resolve_assets_prefers_png_over_jpg(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    base = tmp_path / "backgrounds" / spec.visual.world / spec.visual.background_prompt_key
    _make_asset(base.with_suffix(".png"))
    _make_asset(base.with_suffix(".jpg"))
    # Also need the figure so resolve_assets doesn't fail elsewhere
    fig = tmp_path / "figures" / spec.visual.world / f"{spec.visual.figure_prompt_key}.png"
    _make_asset(fig)

    paths = resolve_assets(spec, assets_root=tmp_path)
    assert paths.background.suffix == ".png"  # png comes first in ASSET_EXTENSIONS


def test_asset_extensions_priority_order() -> None:
    """png should come first — it's the only format with reliable alpha for figures."""
    assert ASSET_EXTENSIONS[0] == ".png"


def test_resolve_assets_missing_background_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    fig = tmp_path / "figures" / spec.visual.world / f"{spec.visual.figure_prompt_key}.png"
    _make_asset(fig)

    with pytest.raises(FileNotFoundError, match="No background asset"):
        resolve_assets(spec, assets_root=tmp_path)


def test_resolve_assets_missing_figure_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    bg = tmp_path / "backgrounds" / spec.visual.world / f"{spec.visual.background_prompt_key}.png"
    _make_asset(bg)
    # No figure file

    with pytest.raises(FileNotFoundError, match="No figure asset"):
        resolve_assets(spec, assets_root=tmp_path)


def test_resolve_assets_background_override_path_wins(tmp_path: Path) -> None:
    """When spec.visual.background_override_path is set, use that file directly."""
    spec = _spec("marcus_self_command.yaml")
    # Put a fallback bg in the world/key location so we can tell which one was used
    fallback_bg = tmp_path / "backgrounds" / spec.visual.world / f"{spec.visual.background_prompt_key}.png"
    _make_asset(fallback_bg)
    # Put the figure where expected (figure layer still uses world/key)
    fig = tmp_path / "figures" / spec.visual.world / f"{spec.visual.figure_prompt_key}.png"
    _make_asset(fig)
    # Put the override file at a totally unrelated repo-relative path
    override_rel = "assets/figures/feminine/sirens/sirens_test.png"
    override_abs = tmp_path.parent / override_rel
    _make_asset(override_abs)

    spec_with_override = spec.model_copy(
        update={
            "visual": spec.visual.model_copy(update={"background_override_path": override_rel})
        }
    )
    paths = resolve_assets(spec_with_override, assets_root=tmp_path)
    assert paths.background.resolve() == override_abs.resolve()
    # Figure layer should still resolve via world/key
    assert paths.figure == fig


def test_resolve_assets_background_override_missing_file_raises(tmp_path: Path) -> None:
    spec = _spec("marcus_self_command.yaml")
    spec_with_override = spec.model_copy(
        update={
            "visual": spec.visual.model_copy(
                update={"background_override_path": "assets/does/not/exist.png"}
            )
        }
    )
    with pytest.raises(FileNotFoundError, match="background_override_path is set"):
        resolve_assets(spec_with_override, assets_root=tmp_path)


def test_resolve_assets_figure_none_skipped(tmp_path: Path) -> None:
    """field_notes spec has figure_prompt_key='none' — no figure file required."""
    spec = _spec("field_notes_resilience.yaml")
    assert spec.visual.figure_prompt_key == "none"

    bg = tmp_path / "backgrounds" / spec.visual.world / f"{spec.visual.background_prompt_key}.png"
    _make_asset(bg)

    paths = resolve_assets(spec, assets_root=tmp_path)
    assert paths.background == bg
    assert paths.figure is None


def test_resolve_assets_helpful_error_message_includes_make_image_prompt_hint(
    tmp_path: Path,
) -> None:
    spec = _spec("marcus_self_command.yaml")
    with pytest.raises(FileNotFoundError) as exc:
        resolve_assets(spec, assets_root=tmp_path)
    assert "make-image-prompt" in str(exc.value)

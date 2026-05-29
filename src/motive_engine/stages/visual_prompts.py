"""Visual-prompts stage: turn a ContentSpec + visual_worlds.yaml into a
ready-to-paste image-generator prompt and negative prompt.

This stage does not call any image API. It emits text.
"""

from dataclasses import dataclass
from pathlib import Path

from motive_engine.schemas import ContentSpec
from motive_engine.utils import load_yaml

# Default location of the visual-worlds config, relative to the project root.
DEFAULT_WORLDS_PATH = Path("config") / "visual_worlds.yaml"


@dataclass(frozen=True)
class ImagePrompt:
    """Result of the visual-prompts stage."""

    positive: str
    negative: str


def build_image_prompt(
    spec: ContentSpec,
    worlds_path: Path = DEFAULT_WORLDS_PATH,
) -> ImagePrompt:
    """Return positive + negative prompts for the spec's visual world."""
    worlds_data = load_yaml(worlds_path)
    try:
        worlds = worlds_data["worlds"]
    except (KeyError, TypeError) as e:
        raise ValueError(
            f"{worlds_path} is missing a top-level 'worlds:' mapping"
        ) from e

    world_id = spec.visual.world
    if world_id not in worlds:
        available = ", ".join(sorted(worlds)) or "<none>"
        raise KeyError(
            f"Unknown visual world '{world_id}' (available: {available})"
        )
    world = worlds[world_id]

    background = _resolve(world, "background_prompts", spec.visual.background_prompt_key, world_id)
    figure = _resolve(world, "figure_prompts", spec.visual.figure_prompt_key, world_id)

    template = world.get("image_prompt_template")
    if not template:
        raise ValueError(f"World '{world_id}' has no image_prompt_template")

    positive = template.format(
        background=background.strip(),
        figure=figure.strip(),
        author=spec.author or "an unnamed source",
        theme=spec.theme,
    ).strip()

    negative = str(world.get("negative_prompt", "")).strip()

    return ImagePrompt(positive=positive, negative=negative)


def _resolve(world: dict, catalog_name: str, key: str, world_id: str) -> str:
    """Look up a prompt phrase in a world's catalog. 'none' always resolves to ''."""
    if key == "none":
        return ""
    catalog = world.get(catalog_name) or {}
    if key not in catalog:
        raise KeyError(
            f"Key '{key}' not in {catalog_name} for world '{world_id}'. "
            f"Available: {sorted(catalog) or '<none>'}"
        )
    return str(catalog[key])

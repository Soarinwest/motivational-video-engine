"""Pydantic schemas for the YAML content specification.

A `ContentSpec` is the head-of-pipeline artifact: a single YAML file that
declares everything the engine needs to produce one motivational video.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class VisualSpec(BaseModel):
    """Visual composition: world, prompt keys, motion, overlays, captions."""

    model_config = ConfigDict(extra="forbid")

    world: str = Field(
        min_length=1,
        description=(
            "ID of a visual world defined in config/visual_worlds.yaml "
            "(e.g. 'stoic_rome', 'ancient_greece')."
        ),
    )
    background_prompt_key: str = Field(
        min_length=1,
        description="Key into the world's background prompts catalog.",
    )
    figure_prompt_key: str = Field(
        min_length=1,
        description="Key into the world's figure prompts catalog. Use 'none' for no figure.",
    )
    motion_profile: str = Field(
        min_length=1,
        description="Named motion profile (e.g. 'slow_zoom', 'static').",
    )
    overlays: list[str] = Field(
        default_factory=list,
        description="Named overlay effects composited on top of the scene.",
    )
    caption_style: str = Field(
        min_length=1,
        description="Named caption style preset.",
    )


class AudioSpec(BaseModel):
    """TTS provider, voice profile, music profile."""

    model_config = ConfigDict(extra="forbid")

    tts_provider: str = Field(
        min_length=1,
        description="TTS engine identifier (e.g. 'kokoro').",
    )
    voice_profile: str = Field(
        min_length=1,
        description="Named voice profile in config/voices.yaml.",
    )
    music_profile: str = Field(
        min_length=1,
        description="Named music profile in config/brand.yaml.",
    )


class RenderSpec(BaseModel):
    """Output format and quality."""

    model_config = ConfigDict(extra="forbid")

    resolution: str = Field(
        description="Output resolution as 'WIDTHxHEIGHT' (e.g. '1080x1920').",
        pattern=r"^\d+x\d+$",
    )
    fps: Literal[24, 30, 60] = Field(description="Output frames per second.")
    format: str = Field(default="mp4", min_length=1, description="Container format.")


class ContentSpec(BaseModel):
    """Top-level content specification for one motivational video."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        min_length=1,
        pattern=r"^[A-Za-z0-9_-]+$",
        description=(
            "Stable, unique identifier. Letters, digits, underscore, hyphen "
            "only (used as a directory name under outputs/drafts/)."
        ),
    )
    series: str = Field(min_length=1, description="Series ID (see config/series.yaml).")
    author: str | None = Field(
        default=None,
        description="Author or figure attribution. Null for field-notes style.",
    )
    theme: str = Field(min_length=1, description="Short theme tag (e.g. 'self-command').")
    duration_seconds: int = Field(
        ge=10,
        le=90,
        description="Target video duration in seconds. Must be between 10 and 90.",
    )
    message: str = Field(min_length=1, description="One-sentence core message.")
    hook: str = Field(min_length=1, description="Opening line of the script.")
    voiceover: str = Field(
        min_length=1,
        description="Full voiceover text. Must not be empty.",
    )
    final_line: str = Field(min_length=1, description="Closing line of the script.")
    visual: VisualSpec
    audio: AudioSpec
    render: RenderSpec

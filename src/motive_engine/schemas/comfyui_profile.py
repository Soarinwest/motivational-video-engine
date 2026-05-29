"""Schema for entries in config/comfyui.yaml."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ComfyUIProfile(BaseModel):
    """One named ComfyUI server profile.

    A profile binds a local ComfyUI endpoint to a specific workflow template
    and the resolution/timeout knobs we'll pass through. The default profile
    is named by `default_profile:` at the top of comfyui.yaml.
    """

    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    base_url: HttpUrl = Field(description="Base URL of the local ComfyUI server.")
    workflow_path: Path = Field(
        description="Path to the workflow JSON template (API format)."
    )
    width: int = Field(gt=0, description="Image width in pixels.")
    height: int = Field(gt=0, description="Image height in pixels.")
    timeout_seconds: float = Field(
        gt=0, description="Max seconds to wait for /history to report completion."
    )
    poll_interval_seconds: float = Field(
        gt=0, description="Seconds between /history polls."
    )

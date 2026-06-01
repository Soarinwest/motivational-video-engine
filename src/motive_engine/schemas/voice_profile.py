"""Schema for entries in config/voices.yaml."""

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BlendComponent(BaseModel):
    """One voice contributing to a blended voice profile."""

    model_config = ConfigDict(extra="forbid")

    voice_id: str = Field(min_length=1)
    weight: float = Field(gt=0, le=1.0)


class VoiceProfile(BaseModel):
    """One named voice profile.

    Two forms:
    - Single voice: `voice_id` set, `voice_blend` empty.
    - Blended voice: `voice_blend` set (list of {voice_id, weight}), `voice_id`
      may be empty (or used as a fallback label). The synthesizer will load
      each component voice's tensor and combine them as a weighted sum, then
      pass the resulting tensor to the Kokoro pipeline.
    """

    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    tts_provider: str = Field(min_length=1, description="TTS engine, e.g. 'kokoro'.")
    voice_id: str = Field(
        default="",
        description=(
            "Provider-specific voice id. Required when voice_blend is empty. "
            "Optional (label only) when voice_blend is set."
        ),
    )
    voice_blend: list[BlendComponent] = Field(
        default_factory=list,
        description=(
            "Optional list of components to blend. When non-empty, each "
            "component's voice tensor is loaded and combined as a weighted "
            "sum; weights are normalized to sum to 1.0. Empty = single voice."
        ),
    )
    lang_code: str = Field(
        min_length=1,
        description=(
            "Language code passed to the TTS pipeline (e.g. 'a' for American, "
            "'b' for British). For blended voices, this controls the "
            "text-to-phoneme step."
        ),
    )
    speed: float = Field(gt=0, le=2.0, description="Speech rate multiplier.")

    @model_validator(mode="after")
    def _voice_id_or_blend_required(self) -> "VoiceProfile":
        if not self.voice_id and not self.voice_blend:
            raise ValueError(
                "VoiceProfile must specify either voice_id or voice_blend."
            )
        return self

    @property
    def is_blend(self) -> bool:
        return bool(self.voice_blend)

"""Schema for entries in config/voices.yaml."""

from pydantic import BaseModel, ConfigDict, Field


class VoiceProfile(BaseModel):
    """One named voice profile (e.g. 'low_steady_male', 'classical_male')."""

    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    tts_provider: str = Field(min_length=1, description="TTS engine, e.g. 'kokoro'.")
    voice_id: str = Field(min_length=1, description="Provider-specific voice id.")
    lang_code: str = Field(
        min_length=1,
        description="Language code passed to the TTS pipeline (e.g. 'a', 'b').",
    )
    speed: float = Field(gt=0, le=2.0, description="Speech rate multiplier.")

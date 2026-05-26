from pydantic import BaseModel, Field, field_validator

from app.models.enums import Direction


class LaunchProbeRequest(BaseModel):
    x: int = Field(..., gt=0, description="Plateau upper-right X coordinate")
    y: int = Field(..., gt=0, description="Plateau upper-right Y coordinate")
    direction: Direction


class SendCommandsRequest(BaseModel):
    commands: str = Field(..., min_length=1, description="Sequence of M, L, R commands")

    @field_validator("commands")
    @classmethod
    def validate_commands(cls, v: str) -> str:
        normalized = v.upper()
        invalid = set(normalized) - {"M", "L", "R"}
        if invalid:
            raise ValueError(f"Invalid commands: {sorted(invalid)}. Only M, L, R are allowed.")
        return normalized


class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction

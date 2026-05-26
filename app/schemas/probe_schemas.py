from pydantic import BaseModel, Field

from app.models.enums import Direction


class LaunchProbeRequest(BaseModel):
    x: int = Field(..., gt=0, description="Plateau upper-right X coordinate")
    y: int = Field(..., gt=0, description="Plateau upper-right Y coordinate")
    direction: Direction


class SendCommandsRequest(BaseModel):
    commands: str = Field(..., min_length=1, description="Sequence of M, L, R commands")


class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction


class ProbeListResponse(BaseModel):
    probes: list[ProbeResponse]

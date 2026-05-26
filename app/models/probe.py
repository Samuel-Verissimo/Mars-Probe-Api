from dataclasses import dataclass

from app.models.enums import Direction


@dataclass
class Plateau:
    x: int
    y: int


@dataclass
class Probe:
    id: str
    x: int
    y: int
    direction: Direction

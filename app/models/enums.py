from enum import Enum


class Direction(str, Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Command(str, Enum):
    MOVE = "M"
    LEFT = "L"
    RIGHT = "R"

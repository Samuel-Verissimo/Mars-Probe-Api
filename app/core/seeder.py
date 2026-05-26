from app.models.enums import Direction
from app.services.probe_service import ProbeService

# M = move forward | L = turn left | R = turn right

_PLATEAU_X = 10
_PLATEAU_Y = 10


def seed(service: ProbeService) -> None:
    # 2 steps north, turn right, 2 steps east → (2, 2) facing EAST
    p1 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p1.id, "MMRMM")

    # 3 steps east, turn back (LL), 2 steps west → (1, 0) facing WEST
    p2 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p2.id, "MMMLLMM")

    # 5 steps north, turn right, 4 steps east → (4, 5) facing EAST
    p3 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p3.id, "MMMMMRMMMM")

    # 6 steps east, turn left, 4 steps north → (6, 4) facing NORTH
    p4 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p4.id, "MMMMMMLMMMM")

    # 7 steps north, turn right, 5 steps east → (5, 7) facing EAST
    p5 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p5.id, "MMMMMMMRMMMMM")

    # 9 steps east → (9, 0) facing EAST
    p6 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p6.id, "MMMMMMMMM")

    # 9 steps north, turn right, 3 steps east, turn right → (3, 9) facing SOUTH
    p7 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p7.id, "MMMMMMMMMRMMMR")

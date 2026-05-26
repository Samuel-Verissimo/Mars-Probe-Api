from app.models.enums import Direction
from app.services.probe_service import ProbeService

_PLATEAU_X = 5
_PLATEAU_Y = 5


def seed(service: ProbeService) -> None:
    # 2 north, turn right, 2 east → (2, 2) EAST
    p1 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p1.id, "MMRMM")

    # 3 east, reverse, 2 west → (1, 0) WEST
    p2 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p2.id, "MMMLLMM")

    # 3 north, turn right, 2 east → (2, 3) EAST
    p3 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p3.id, "MMMRMM")

    # 3 east, turn left, 2 north → (3, 2) NORTH
    p4 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p4.id, "MMMLMM")

    # 4 north, turn right, 2 east → (2, 4) EAST
    p5 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p5.id, "MMMMRMM")

    # 4 east → (4, 0) EAST
    p6 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.EAST)
    service.move(p6.id, "MMMM")

    # 4 north, turn right, 3 east, turn right → (3, 4) SOUTH
    p7 = service.launch(_PLATEAU_X, _PLATEAU_Y, Direction.NORTH)
    service.move(p7.id, "MMMMRMMMR")

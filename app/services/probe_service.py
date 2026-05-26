import uuid

from app.exceptions.probe_exceptions import ProbeNotFoundError, ProbeOutOfBoundsError
from app.models.enums import Command, Direction
from app.models.probe import Plateau, Probe
from app.repositories.plateau_repository import PlateauRepository
from app.repositories.probe_repository import ProbeRepository

_TURN_LEFT: dict[Direction, Direction] = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
}

_TURN_RIGHT: dict[Direction, Direction] = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

_MOVE_DELTA: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
}


class ProbeService:
    def __init__(self, probe_repository: ProbeRepository, plateau_repository: PlateauRepository) -> None:
        self._probes = probe_repository
        self._plateau = plateau_repository

    def launch(self, plateau_x: int, plateau_y: int, direction: Direction) -> Probe:
        self._plateau.set(Plateau(x=plateau_x, y=plateau_y))
        probe = Probe(id=str(uuid.uuid4()), x=0, y=0, direction=direction)
        return self._probes.save(probe)

    def move(self, probe_id: str, commands: str) -> Probe:
        probe = self._require_probe(probe_id)
        plateau = self._plateau.get()
        if plateau is None:
            raise RuntimeError("Plateau not configured. Launch a probe first.")

        x, y, direction = probe.x, probe.y, probe.direction

        for char in commands:
            command = Command(char)
            if command == Command.LEFT:
                direction = _TURN_LEFT[direction]
            elif command == Command.RIGHT:
                direction = _TURN_RIGHT[direction]
            elif command == Command.MOVE:
                dx, dy = _MOVE_DELTA[direction]
                new_x, new_y = x + dx, y + dy
                if not (0 <= new_x <= plateau.x and 0 <= new_y <= plateau.y):
                    raise ProbeOutOfBoundsError(new_x, new_y, plateau.x, plateau.y)
                x, y = new_x, new_y

        probe.x = x
        probe.y = y
        probe.direction = direction
        return self._probes.save(probe)

    def get_all(self) -> list[Probe]:
        return self._probes.find_all()

    def get_by_id(self, probe_id: str) -> Probe:
        return self._require_probe(probe_id)

    def get_plateau(self) -> Plateau | None:
        return self._plateau.get()

    def delete(self, probe_id: str) -> None:
        if not self._probes.delete(probe_id):
            raise ProbeNotFoundError(probe_id)

    def _require_probe(self, probe_id: str) -> Probe:
        probe = self._probes.find_by_id(probe_id)
        if probe is None:
            raise ProbeNotFoundError(probe_id)
        return probe

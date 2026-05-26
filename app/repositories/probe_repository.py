from typing import Optional

from app.models.probe import Probe


class ProbeRepository:
    def __init__(self) -> None:
        self._storage: dict[str, Probe] = {}

    def save(self, probe: Probe) -> Probe:
        self._storage[probe.id] = probe
        return probe

    def find_by_id(self, probe_id: str) -> Optional[Probe]:
        return self._storage.get(probe_id)

    def find_all(self) -> list[Probe]:
        return list(self._storage.values())

    def delete(self, probe_id: str) -> bool:
        if probe_id not in self._storage:
            return False
        del self._storage[probe_id]
        return True

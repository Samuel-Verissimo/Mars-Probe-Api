from app.models.enums import Direction
from app.models.probe import Plateau, Probe
from app.repositories.plateau_repository import PlateauRepository
from app.repositories.probe_repository import ProbeRepository


def _make_probe(probe_id: str = "test-id") -> Probe:
    return Probe(id=probe_id, x=0, y=0, direction=Direction.NORTH)


class TestProbeRepository:
    def test_save_and_find_by_id(self) -> None:
        repo = ProbeRepository()
        probe = _make_probe()
        repo.save(probe)
        assert repo.find_by_id("test-id") == probe

    def test_find_by_id_returns_none_for_unknown(self) -> None:
        assert ProbeRepository().find_by_id("unknown") is None

    def test_find_all_returns_all_saved_probes(self) -> None:
        repo = ProbeRepository()
        repo.save(_make_probe("a"))
        repo.save(_make_probe("b"))
        assert len(repo.find_all()) == 2

    def test_find_all_empty(self) -> None:
        assert ProbeRepository().find_all() == []

    def test_save_overwrites_existing_probe(self) -> None:
        repo = ProbeRepository()
        probe = _make_probe()
        repo.save(probe)
        probe.x = 3
        repo.save(probe)
        assert repo.find_by_id("test-id").x == 3

    def test_find_all_returns_independent_list(self) -> None:
        repo = ProbeRepository()
        repo.save(_make_probe("a"))
        repo.find_all().clear()
        assert len(repo.find_all()) == 1

    def test_delete_removes_probe(self) -> None:
        repo = ProbeRepository()
        repo.save(_make_probe("a"))
        assert repo.delete("a") is True
        assert repo.find_by_id("a") is None

    def test_delete_returns_false_for_unknown(self) -> None:
        assert ProbeRepository().delete("nonexistent") is False


class TestPlateauRepository:
    def test_get_returns_none_initially(self) -> None:
        assert PlateauRepository().get() is None

    def test_set_and_get(self) -> None:
        repo = PlateauRepository()
        repo.set(Plateau(5, 10))
        assert repo.get().x == 5
        assert repo.get().y == 10

    def test_set_overwrites_previous(self) -> None:
        repo = PlateauRepository()
        repo.set(Plateau(5, 5))
        repo.set(Plateau(10, 10))
        assert repo.get().x == 10

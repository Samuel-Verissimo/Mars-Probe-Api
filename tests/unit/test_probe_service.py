import pytest

from app.exceptions.probe_exceptions import (
    InvalidCommandError,
    PlateauShrinkError,
    ProbeNotFoundError,
    ProbeOutOfBoundsError,
)
from app.models.enums import Direction
from app.repositories.plateau_repository import PlateauRepository
from app.repositories.probe_repository import ProbeRepository
from app.services.probe_service import ProbeService


@pytest.fixture
def service() -> ProbeService:
    return ProbeService(ProbeRepository(), PlateauRepository())


class TestLaunch:
    def test_creates_probe_at_origin(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        assert probe.x == 0
        assert probe.y == 0

    def test_assigns_given_direction(self, service: ProbeService) -> None:
        assert service.launch(5, 5, Direction.EAST).direction == Direction.EAST

    def test_configures_global_plateau(self, service: ProbeService) -> None:
        service.launch(10, 8, Direction.NORTH)
        assert service.get_plateau().x == 10
        assert service.get_plateau().y == 8

    def test_subsequent_launch_updates_plateau(self, service: ProbeService) -> None:
        service.launch(5, 5, Direction.NORTH)
        service.launch(10, 10, Direction.EAST)
        assert service.get_plateau().x == 10

    def test_generates_unique_ids(self, service: ProbeService) -> None:
        assert service.launch(5, 5, Direction.NORTH).id != service.launch(5, 5, Direction.NORTH).id

    def test_shrink_plateau_below_existing_probe_raises_error(self, service: ProbeService) -> None:
        probe = service.launch(10, 10, Direction.NORTH)
        service.move(probe.id, "MMMMM")
        with pytest.raises(PlateauShrinkError):
            service.launch(3, 3, Direction.NORTH)

    def test_expand_plateau_with_existing_probes_is_allowed(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        service.move(probe.id, "MM")
        new_probe = service.launch(10, 10, Direction.EAST)
        assert service.get_plateau().x == 10
        assert new_probe.x == 0

    def test_same_size_plateau_with_existing_probes_is_allowed(self, service: ProbeService) -> None:
        service.launch(5, 5, Direction.NORTH)
        service.launch(5, 5, Direction.EAST)
        assert service.get_plateau().x == 5


class TestMove:
    def test_move_forward_north(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        result = service.move(probe.id, "M")
        assert result.x == 0
        assert result.y == 1

    def test_move_forward_east(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.EAST)
        assert service.move(probe.id, "M").x == 1

    def test_turn_left_from_north(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        assert service.move(probe.id, "L").direction == Direction.WEST

    def test_turn_right_from_north(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        assert service.move(probe.id, "R").direction == Direction.EAST

    def test_full_circle_left(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        assert service.move(probe.id, "LLLL").direction == Direction.NORTH

    def test_full_circle_right(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        assert service.move(probe.id, "RRRR").direction == Direction.NORTH

    def test_combined_sequence(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        result = service.move(probe.id, "MMRMM")
        assert result.x == 2
        assert result.y == 2
        assert result.direction == Direction.EAST

    def test_position_persists_between_calls(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        service.move(probe.id, "MM")
        assert service.move(probe.id, "M").y == 3

    def test_move_out_of_bounds_raises_error(self, service: ProbeService) -> None:
        probe = service.launch(1, 1, Direction.NORTH)
        with pytest.raises(ProbeOutOfBoundsError):
            service.move(probe.id, "MMM")

    def test_move_south_below_zero_raises_error(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.SOUTH)
        with pytest.raises(ProbeOutOfBoundsError):
            service.move(probe.id, "M")

    def test_move_west_below_zero_raises_error(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.WEST)
        with pytest.raises(ProbeOutOfBoundsError):
            service.move(probe.id, "M")

    def test_invalid_probe_id_raises_error(self, service: ProbeService) -> None:
        with pytest.raises(ProbeNotFoundError):
            service.move("nonexistent-id", "M")

    def test_out_of_bounds_does_not_partially_apply_commands(self, service: ProbeService) -> None:
        probe = service.launch(2, 2, Direction.NORTH)
        with pytest.raises(ProbeOutOfBoundsError):
            service.move(probe.id, "MMMM")
        assert service.get_by_id(probe.id).y == 0

    def test_invalid_command_chars_raise_error(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        with pytest.raises(InvalidCommandError):
            service.move(probe.id, "MXZ")

    def test_invalid_commands_do_not_partially_apply(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        with pytest.raises(InvalidCommandError):
            service.move(probe.id, "MMX")
        assert service.get_by_id(probe.id).y == 0

    def test_lowercase_commands_are_accepted(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        result = service.move(probe.id, "mm")
        assert result.y == 2


class TestGetPlateau:
    def test_returns_none_when_no_probes(self, service: ProbeService) -> None:
        assert service.get_plateau() is None

    def test_returns_configured_plateau(self, service: ProbeService) -> None:
        service.launch(10, 8, Direction.NORTH)
        plateau = service.get_plateau()
        assert plateau.x == 10
        assert plateau.y == 8


class TestGetAll:
    def test_returns_all_launched_probes(self, service: ProbeService) -> None:
        service.launch(5, 5, Direction.NORTH)
        service.launch(5, 5, Direction.EAST)
        assert len(service.get_all()) == 2

    def test_returns_empty_list_when_no_probes(self, service: ProbeService) -> None:
        assert service.get_all() == []


class TestGetById:
    def test_returns_correct_probe(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.SOUTH)
        assert service.get_by_id(probe.id).id == probe.id

    def test_nonexistent_id_raises_error(self, service: ProbeService) -> None:
        with pytest.raises(ProbeNotFoundError):
            service.get_by_id("nonexistent-id")


class TestDelete:
    def test_removes_probe(self, service: ProbeService) -> None:
        probe = service.launch(5, 5, Direction.NORTH)
        service.delete(probe.id)
        with pytest.raises(ProbeNotFoundError):
            service.get_by_id(probe.id)

    def test_nonexistent_id_raises_error(self, service: ProbeService) -> None:
        with pytest.raises(ProbeNotFoundError):
            service.delete("nonexistent-id")

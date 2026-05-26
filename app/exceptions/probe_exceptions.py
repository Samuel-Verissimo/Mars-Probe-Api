class ProbeNotFoundError(Exception):
    def __init__(self, probe_id: str) -> None:
        self.probe_id = probe_id
        super().__init__(f"Probe '{probe_id}' not found")


class ProbeOutOfBoundsError(Exception):
    def __init__(self, x: int, y: int, plateau_x: int, plateau_y: int) -> None:
        super().__init__(
            f"Move would place probe at ({x}, {y}), "
            f"which is outside plateau bounds (0-{plateau_x}, 0-{plateau_y})"
        )


class InvalidCommandError(Exception):
    def __init__(self, invalid_chars: list[str]) -> None:
        super().__init__(f"Invalid commands: {invalid_chars}. Only M, L, R are allowed.")


class PlateauShrinkError(Exception):
    def __init__(self, new_x: int, new_y: int, probe_ids: list[str]) -> None:
        super().__init__(
            f"Cannot resize plateau to ({new_x}, {new_y}): "
            f"probes {probe_ids} would be placed out of bounds."
        )

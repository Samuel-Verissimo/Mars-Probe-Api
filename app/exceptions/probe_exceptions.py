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

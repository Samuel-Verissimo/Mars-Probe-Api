from app.models.probe import Plateau


class PlateauRepository:
    def __init__(self) -> None:
        self._plateau: Plateau | None = None

    def set(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def get(self) -> Plateau | None:
        return self._plateau

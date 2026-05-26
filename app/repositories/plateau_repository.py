from typing import Optional

from app.models.probe import Plateau


class PlateauRepository:
    def __init__(self) -> None:
        self._plateau: Optional[Plateau] = None

    def set(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def get(self) -> Optional[Plateau]:
        return self._plateau

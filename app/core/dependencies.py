from app.repositories.plateau_repository import PlateauRepository
from app.repositories.probe_repository import ProbeRepository
from app.services.probe_service import ProbeService

_probe_repository = ProbeRepository()
_plateau_repository = PlateauRepository()
_service = ProbeService(_probe_repository, _plateau_repository)


def get_probe_service() -> ProbeService:
    return _service

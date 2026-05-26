import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_probe_service
from app.main import app
from app.repositories.plateau_repository import PlateauRepository
from app.repositories.probe_repository import ProbeRepository
from app.services.probe_service import ProbeService


@pytest.fixture
def probe_repository() -> ProbeRepository:
    return ProbeRepository()


@pytest.fixture
def plateau_repository() -> PlateauRepository:
    return PlateauRepository()


@pytest.fixture
def service(probe_repository: ProbeRepository, plateau_repository: PlateauRepository) -> ProbeService:
    return ProbeService(probe_repository, plateau_repository)


@pytest.fixture
def client(service: ProbeService) -> TestClient:
    app.dependency_overrides[get_probe_service] = lambda: service
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

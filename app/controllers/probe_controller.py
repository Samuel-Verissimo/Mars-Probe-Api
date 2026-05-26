from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_probe_service
from app.models.probe import Probe
from app.schemas.probe_schemas import LaunchProbeRequest, ProbeResponse, SendCommandsRequest
from app.services.probe_service import ProbeService

router = APIRouter(prefix="/probes", tags=["Probes"])


def _to_response(probe: Probe) -> ProbeResponse:
    return ProbeResponse(id=probe.id, x=probe.x, y=probe.y, direction=probe.direction)


@router.post(
    "",
    response_model=ProbeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Launch a probe and configure its plateau",
)
def launch_probe(
    body: LaunchProbeRequest,
    service: ProbeService = Depends(get_probe_service),
) -> ProbeResponse:
    probe = service.launch(body.x, body.y, body.direction)
    return _to_response(probe)


@router.post(
    "/{probe_id}/commands",
    response_model=ProbeResponse,
    summary="Send movement commands to a probe",
)
def send_commands(
    probe_id: str,
    body: SendCommandsRequest,
    service: ProbeService = Depends(get_probe_service),
) -> ProbeResponse:
    probe = service.move(probe_id, body.commands)
    return _to_response(probe)


@router.get(
    "",
    response_model=list[ProbeResponse],
    summary="List all probes and their current positions",
)
def list_probes(service: ProbeService = Depends(get_probe_service)) -> list[ProbeResponse]:
    return [_to_response(p) for p in service.get_all()]


@router.get(
    "/{probe_id}",
    response_model=ProbeResponse,
    summary="Get the current position of a specific probe",
)
def get_probe(
    probe_id: str,
    service: ProbeService = Depends(get_probe_service),
) -> ProbeResponse:
    probe = service.get_by_id(probe_id)
    return _to_response(probe)


@router.delete(
    "/{probe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Decommission a probe",
)
def delete_probe(
    probe_id: str,
    service: ProbeService = Depends(get_probe_service),
) -> None:
    service.delete(probe_id)

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.core.dependencies import get_probe_service
from app.services.probe_service import ProbeService

router = APIRouter(tags=["Visual"])

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

_ARROWS = {"NORTH": "↑", "SOUTH": "↓", "EAST": "→", "WEST": "←"}


@router.get("/", include_in_schema=False)
def visual_map(request: Request, service: ProbeService = Depends(get_probe_service)):
    probes = service.get_all()
    probe_map = {f"{p.x},{p.y}": _ARROWS[p.direction.value] for p in probes}

    return templates.TemplateResponse(request, "map.html", {
        "plateau": service.get_plateau(),
        "probes": probes,
        "probe_map": probe_map,
        "arrows": _ARROWS,
    })

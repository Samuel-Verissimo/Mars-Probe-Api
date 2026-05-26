from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.controllers.probe_controller import router as probe_router
from app.controllers.visual_controller import router as visual_router
from app.core.config import settings
from app.core.dependencies import get_probe_service
from app.core.seeder import seed
from app.exceptions.probe_exceptions import (
    InvalidCommandError,
    PlateauShrinkError,
    ProbeNotFoundError,
    ProbeOutOfBoundsError,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    seed(get_probe_service())
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para controle de sondas exploradoras em Marte.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(visual_router)
app.include_router(probe_router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    messages = [err.get("msg", "Invalid input") for err in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": "; ".join(messages)})


@app.exception_handler(ProbeNotFoundError)
async def probe_not_found_handler(_: Request, exc: ProbeNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ProbeOutOfBoundsError)
async def probe_out_of_bounds_handler(_: Request, exc: ProbeOutOfBoundsError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(InvalidCommandError)
async def invalid_command_handler(_: Request, exc: InvalidCommandError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(PlateauShrinkError)
async def plateau_shrink_handler(_: Request, exc: PlateauShrinkError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.get("/health", tags=["Health"], summary="Health check")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": settings.app_version}

"""Application implementation - ASGI."""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import config
from app.controllers import base
from app.models.exception import HttpException
from app.router import root_api_router
from app.utils import utils


def exception_handler(request: Request, e: HttpException):
    return JSONResponse(
        status_code=e.status_code,
        content=utils.get_response(e.status_code, e.data, e.message),
    )


def validation_exception_handler(request: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=utils.get_response(
            status=400, data=e.errors(), message="field required"
        ),
    )


PROTECTED_MEDIA_PREFIXES = ("/tasks",)


def _is_railway_or_production() -> bool:
    return bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID")) or os.getenv(
        "ENVIRONMENT", ""
    ).lower() in {"prod", "production"}


def _cors_origins() -> list[str]:
    origins = [
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]
    if origins:
        return origins
    if _is_railway_or_production():
        logger.warning(
            "CORS_ALLOWED_ORIGINS is empty in production/Railway; no browser origins are allowed."
        )
        return []
    return ["*"]


async def _operator_token_middleware(request: Request, call_next):
    # Static task files are convenient for local operator review only. They are
    # not safe as a public customer-facing mount, so protect them with the same
    # operator token used by the API endpoints.
    if request.url.path.startswith(PROTECTED_MEDIA_PREFIXES):
        try:
            base.verify_token(request)
        except HttpException as exc:
            return exception_handler(request, exc)
    return await call_next(request)


def get_application() -> FastAPI:
    """Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.

    """
    instance = FastAPI(
        title=config.project_name,
        description=config.project_description,
        version=config.project_version,
        debug=False,
    )
    instance.middleware("http")(_operator_token_middleware)
    instance.include_router(root_api_router)
    instance.add_exception_handler(HttpException, exception_handler)
    instance.add_exception_handler(RequestValidationError, validation_exception_handler)
    return instance


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


task_dir = utils.task_dir()
app.mount(
    "/tasks", StaticFiles(directory=task_dir, html=True, follow_symlink=True), name=""
)

@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"status": "ok", "service": "cenara"}


public_dir = utils.public_dir()
app.mount("/", StaticFiles(directory=public_dir, html=True), name="")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown event")


@app.on_event("startup")
def startup_event():
    logger.info("startup event")

"""Application implementation - ASGI."""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

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
    instance.include_router(root_api_router)
    instance.add_exception_handler(HttpException, exception_handler)
    instance.add_exception_handler(RequestValidationError, validation_exception_handler)
    return instance


app = get_application()

# Configures the CORS middleware for the FastAPI app. Railway/production
# runtimes must fail closed unless CORS_ALLOWED_ORIGINS is explicitly set.
def _is_production_like_runtime() -> bool:
    environment = os.getenv("ENVIRONMENT", "").strip().lower()
    return environment in {"production", "railway", "prod"} or any(
        os.getenv(name)
        for name in (
            "RAILWAY_ENVIRONMENT",
            "RAILWAY_PROJECT_ID",
            "RAILWAY_SERVICE_ID",
        )
    )


def _get_cors_allowed_origins() -> list[str]:
    cors_allowed_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
    origins = [
        origin.strip()
        for origin in cors_allowed_origins_str.split(",")
        if origin.strip()
    ]
    if _is_production_like_runtime():
        # Wildcard CORS is forbidden in Railway/production, even if explicitly
        # supplied. Keep only concrete origins and fail closed when none remain.
        return [origin for origin in origins if origin != "*"]
    if origins:
        return origins
    return ["*"]


origins = _get_cors_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskMediaTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/tasks" or request.url.path.startswith("/tasks/"):
            expected_token = base.get_expected_token()
            supplied_token = base.get_bearer_token(request) or (
                base.get_api_key(request) or ""
            ).strip()
            if (
                not expected_token
                or not supplied_token
                or supplied_token != expected_token
            ):
                return JSONResponse(
                    status_code=401,
                    content=utils.get_response(401, message="invalid token"),
                )
        return await call_next(request)


app.add_middleware(TaskMediaTokenMiddleware)

task_dir = utils.task_dir()
app.mount(
    "/tasks", StaticFiles(directory=task_dir, html=True, follow_symlink=True), name=""
)

public_dir = utils.public_dir()
app.mount("/", StaticFiles(directory=public_dir, html=True), name="")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown event")


@app.on_event("startup")
def startup_event():
    logger.info("startup event")

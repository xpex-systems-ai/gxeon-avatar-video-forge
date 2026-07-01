"""Application implementation - ASGI."""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import config
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


def _is_production() -> bool:
    return os.getenv("ENVIRONMENT", "").lower() in {"production", "prod", "railway"} or bool(os.getenv("RAILWAY_ENVIRONMENT"))


def _cors_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    if _is_production() and (not origins or "*" in origins):
        raise RuntimeError("CORS_ALLOWED_ORIGINS must be explicit in Railway/production; wildcard is not allowed")
    return origins or ["*"]


class TaskMediaTokenMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and scope.get("path", "").startswith("/tasks"):
            headers = {key.decode("latin1").lower(): value.decode("latin1") for key, value in scope.get("headers", [])}
            auth_header = headers.get("authorization", "")
            token = None
            if auth_header.lower().startswith("bearer "):
                token = auth_header[7:].strip()
            token = token or headers.get("x-api-key")
            expected = os.getenv("GX1_ACCESS_TOKEN") or config.app.get("api_key", "")
            if not expected or token != expected:
                response = JSONResponse({"message": "unauthorized task media access"}, status_code=401)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


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

# Configures the CORS middleware for the FastAPI app
origins = _cors_origins()
app.add_middleware(TaskMediaTokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

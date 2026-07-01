"""Application implementation - ASGI."""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import config
from app.models.exception import HttpException
from app.controllers import base
from app.router import root_api_router
from app.utils import utils



def _is_production_like_runtime() -> bool:
    environment = os.getenv("ENVIRONMENT", "").lower()
    railway_environment = os.getenv("RAILWAY_ENVIRONMENT", "")
    railway_ids = (os.getenv("RAILWAY_PROJECT_ID"), os.getenv("RAILWAY_SERVICE_ID"))
    return environment in {"production", "prod", "staging"} or bool(railway_environment) or any(railway_ids)


def _cors_origins() -> list[str]:
    cors_allowed_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
    origins = [origin.strip() for origin in cors_allowed_origins_str.split(",") if origin.strip()]
    if origins:
        return origins
    if _is_production_like_runtime():
        logger.warning("CORS_ALLOWED_ORIGINS is empty in production-like runtime; wildcard CORS disabled")
        return []
    return ["*"]


class TaskMediaTokenMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or not scope.get("path", "").startswith("/tasks"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        expected_token = base.get_expected_api_key()
        supplied_token = base.get_api_key(request) or request.query_params.get("token")
        if expected_token and supplied_token != expected_token:
            response = Response(status_code=401)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

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

# Configures the CORS middleware for the FastAPI app
origins = _cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

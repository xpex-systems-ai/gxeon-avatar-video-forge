"""Application implementation - ASGI."""

import os
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import config
from app.controllers.base import get_expected_token
from app.models.exception import HttpException
from app.router import root_api_router
from app.utils import utils


class TaskMediaTokenMiddleware:
    """Protect generated task media with the operator access token."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        protects_tasks_path = path == "/tasks" or path.startswith("/tasks/")
        if scope.get("type") != "http" or not protects_tasks_path:
            await self.app(scope, receive, send)
            return

        expected_token = get_expected_token()
        supplied_token = self._get_supplied_token(scope)
        if not expected_token or not supplied_token or supplied_token != expected_token:
            response = PlainTextResponse("unauthorized", status_code=401)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    @staticmethod
    def _get_supplied_token(scope):
        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        authorization = headers.get("authorization", "")
        scheme, _, bearer_token = authorization.partition(" ")
        if scheme.lower() == "bearer" and bearer_token.strip():
            return bearer_token.strip()

        api_key = headers.get("x-api-key", "").strip()
        if api_key:
            return api_key

        query_string = scope.get("query_string", b"").decode("latin-1")
        query_tokens = parse_qs(query_string).get("token", [])
        if query_tokens and query_tokens[0].strip():
            return query_tokens[0].strip()

        return ""


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
cors_allowed_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
origins = cors_allowed_origins_str.split(",") if cors_allowed_origins_str else ["*"]
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

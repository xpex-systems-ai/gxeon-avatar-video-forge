import os
from uuid import uuid4

from fastapi import Request

from app.config import config
from app.models.exception import HttpException


def get_task_id(request: Request):
    task_id = request.headers.get("x-task-id")
    if not task_id:
        task_id = uuid4()
    return str(task_id)


def get_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    return api_key


def verify_token(request: Request):
    token = get_api_key(request)
    if token != config.app.get("api_key", ""):
        request_id = get_task_id(request)
        request_url = request.url
        user_agent = request.headers.get("user-agent")
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message=f"invalid token: {request_url}, {user_agent}",
        )


def _is_private_operator_mode():
    return bool(
        os.getenv("GX1_ACCESS_TOKEN")
        or os.getenv("APP_ENV", "").lower() == "production"
        or os.getenv("RAILWAY_ENVIRONMENT")
    )


def require_gx1_operator(request: Request):
    if not _is_private_operator_mode():
        return True

    expected_token = os.getenv("GX1_ACCESS_TOKEN", "")
    request_id = get_task_id(request)
    if not expected_token:
        raise HttpException(
            task_id=request_id,
            status_code=503,
            message="private operator access is closed until GX1_ACCESS_TOKEN is configured",
        )

    supplied_token = get_api_key(request) or request.headers.get("authorization", "")
    if supplied_token.lower().startswith("bearer "):
        supplied_token = supplied_token[7:].strip()
    if supplied_token != expected_token:
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message="invalid private operator token",
        )
    return True

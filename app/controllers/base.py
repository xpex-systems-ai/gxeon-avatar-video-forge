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
    authorization = request.headers.get("authorization", "")
    scheme, _, bearer_token = authorization.partition(" ")
    if scheme.lower() == "bearer" and bearer_token.strip():
        return bearer_token.strip()

    return request.headers.get("x-api-key", "").strip()


def get_expected_token():
    return (os.getenv("GX1_ACCESS_TOKEN") or config.app.get("api_key", "") or "").strip()


def _raise_unauthorized(request: Request, message: str = "unauthorized"):
    raise HttpException(
        task_id=get_task_id(request),
        status_code=401,
        message=message,
    )


def verify_token(request: Request):
    expected_token = get_expected_token()
    if not expected_token:
        _raise_unauthorized(request, "operator token is not configured")

    token = get_api_key(request)
    if not token:
        _raise_unauthorized(request)

    if token != expected_token:
        _raise_unauthorized(request)

from uuid import uuid4

import os

from fastapi import Request

from app.config import config
from app.models.exception import HttpException


def get_task_id(request: Request):
    task_id = request.headers.get("x-task-id")
    if not task_id:
        task_id = uuid4()
    return str(task_id)


def get_api_key(request: Request):
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return request.headers.get("x-api-key")


def _expected_token() -> str:
    return os.getenv("GX1_ACCESS_TOKEN") or config.app.get("api_key", "")


def verify_token(request: Request):
    token = get_api_key(request)
    expected_token = _expected_token()
    if not expected_token or token != expected_token:
        request_id = get_task_id(request)
        request_url = request.url
        user_agent = request.headers.get("user-agent")
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message=f"invalid token: {request_url}, {user_agent}",
        )

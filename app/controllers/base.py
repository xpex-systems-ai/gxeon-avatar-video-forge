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
    if authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    api_key = request.headers.get("x-api-key")
    return api_key


def get_expected_operator_token():
    return os.getenv("GX1_ACCESS_TOKEN") or config.app.get("api_key", "")


def verify_token(request: Request):
    token = get_api_key(request)
    if not token or token != get_expected_operator_token():
        request_id = get_task_id(request)
        request_url = request.url
        user_agent = request.headers.get("user-agent")
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message=f"invalid token: {request_url}, {user_agent}",
        )

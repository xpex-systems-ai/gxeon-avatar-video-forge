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


def get_expected_token():
    return (
        os.getenv("GX1_ACCESS_TOKEN")
        or str(config.app.get("api_key", "") or "")
    ).strip()


def get_bearer_token(request: Request):
    authorization = request.headers.get("authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() == "bearer" and token.strip():
        return token.strip()
    return ""


def verify_token(request: Request):
    expected_token = get_expected_token()
    supplied_token = get_bearer_token(request) or (get_api_key(request) or "").strip()
    if not expected_token or not supplied_token or supplied_token != expected_token:
        request_id = get_task_id(request)
        request_url = request.url
        user_agent = request.headers.get("user-agent")
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message=f"invalid token: {request_url}, {user_agent}",
        )

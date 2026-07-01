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
    api_key = request.headers.get("x-api-key") or request.headers.get("authorization", "")
    if isinstance(api_key, str) and api_key.lower().startswith("bearer "):
        api_key = api_key[7:].strip()
    return api_key


def _operator_token():
    # GX1_ACCESS_TOKEN is retained as the compatibility env var, but the
    # user-facing product name is Cenara. config.app.api_key remains supported
    # for local upstream-compatible deployments.
    return config.app.get("api_key", "") or __import__("os").getenv("GX1_ACCESS_TOKEN", "")


def verify_token(request: Request):
    token = get_api_key(request)
    expected_token = _operator_token()
    if not expected_token or token != expected_token:
        request_id = get_task_id(request)
        request_url = request.url
        user_agent = request.headers.get("user-agent")
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message=f"invalid token: {request_url}, {user_agent}",
        )

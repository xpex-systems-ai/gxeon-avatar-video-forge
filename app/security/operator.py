"""GX1 private operator security helpers."""

import os
import secrets

from fastapi import Request

from app.controllers import base
from app.models.exception import HttpException

_TOKEN_HEADER = "x-gx1-access-token"
_BEARER_PREFIX = "bearer "
_PRODUCTION_ENVS = {"production", "prod", "railway"}
_TRUTHY = {"1", "true", "yes", "on"}
_LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def get_gx1_access_token() -> str:
    return os.getenv("GX1_ACCESS_TOKEN", "").strip()


def is_private_operator_mode() -> bool:
    env_name = os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "")).strip().lower()
    return (
        bool(get_gx1_access_token())
        or os.getenv("GX1_PRIVATE_OPERATOR_MODE", "").strip().lower() in _TRUTHY
        or env_name in _PRODUCTION_ENVS
        or bool(os.getenv("RAILWAY_ENVIRONMENT"))
    )


def _request_token(request: Request) -> str:
    header_token = request.headers.get(_TOKEN_HEADER, "").strip()
    if header_token:
        return header_token

    authorization = request.headers.get("authorization", "").strip()
    if authorization.lower().startswith(_BEARER_PREFIX):
        return authorization[len(_BEARER_PREFIX) :].strip()
    return ""


def _is_loopback_request(request: Request) -> bool:
    client_host = request.client.host if request.client else ""
    host_header = request.headers.get("host", "").split(":", 1)[0]
    return client_host in _LOOPBACK_HOSTS or host_header in _LOOPBACK_HOSTS


def require_gx1_operator(request: Request):
    """Protect API operations when GX1 private operator mode is active.

    Local development remains usable without a token unless production/private mode is
    explicitly enabled. In production-like environments, a missing GX1_ACCESS_TOKEN
    fails closed so public domains cannot expose generation, upload, list, or delete
    APIs by accident.
    """
    if not is_private_operator_mode():
        return

    request_id = base.get_task_id(request)
    expected_token = get_gx1_access_token()
    if not expected_token:
        if _is_loopback_request(request):
            return
        raise HttpException(
            task_id=request_id,
            status_code=503,
            message="GX1_ACCESS_TOKEN is required before exposing protected APIs",
        )

    supplied_token = _request_token(request)
    if not secrets.compare_digest(supplied_token, expected_token):
        raise HttpException(
            task_id=request_id,
            status_code=401,
            message="invalid GX1 operator token",
        )

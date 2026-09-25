"""Turns errors into the one error model of the API: 400, 404, 405, 409 and 500.

FastAPI's defaults (422 for validation, ``{"detail": ...}`` for the rest) contradict the
contract, so every handler is replaced here (docs/API_DESIGN.md, DQ-API-01 and DQ-API-02).
"""

from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors import InvalidTransitionError, NotFoundError, error_body


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content=error_body(code, message, details), headers=headers
    )


def _field_name(location: tuple[Any, ...]) -> str:
    """``("body", "text")`` -> ``"text"``; ``("query", "page_size")`` -> ``"page_size"``."""
    parts = [str(part) for part in location if part not in ("body", "query", "path")]
    return ".".join(parts) or "body"


async def _validation_error(_request: Request, error: Exception) -> JSONResponse:
    error = cast(RequestValidationError, error)
    details = [
        {"field": _field_name(tuple(issue["loc"])), "message": str(issue["msg"])}
        for issue in error.errors()
    ]
    return error_response(400, "validation_error", "Invalid request", details)


async def _not_found(_request: Request, error: Exception) -> JSONResponse:
    error = cast(NotFoundError, error)
    return error_response(404, "not_found", str(error))


async def _invalid_transition(_request: Request, error: Exception) -> JSONResponse:
    error = cast(InvalidTransitionError, error)
    return error_response(
        409,
        "invalid_transition",
        str(error),
        [{"from": error.current.value, "to": error.target.value}],
    )


async def _http_exception(_request: Request, error: Exception) -> JSONResponse:
    error = cast(StarletteHTTPException, error)
    codes = {404: "not_found", 405: "method_not_allowed"}
    code = codes.get(error.status_code, "http_error")
    messages = {404: "Not found", 405: "Method not allowed"}
    message = messages.get(error.status_code, str(error.detail))
    return error_response(error.status_code, code, message, headers=dict(error.headers or {}))


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(NotFoundError, _not_found)
    app.add_exception_handler(InvalidTransitionError, _invalid_transition)
    app.add_exception_handler(StarletteHTTPException, _http_exception)

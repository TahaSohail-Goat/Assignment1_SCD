"""Request context: request id, access log line, metrics (ASG-NFR-010, DQ-API-12/13).

A plain ASGI middleware, so the request id set here is visible to everything the request
touches and is echoed on every response, including the 500 produced here.
"""

import logging
import re
import time
import uuid
from typing import Any

from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app import metrics
from app.errors import error_response
from app.logging import request_id_var

REQUEST_ID_HEADER = "X-Request-ID"
_VALID_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")

logger = logging.getLogger("app.request")


def resolve_request_id(incoming: str | None) -> str:
    """Accept a well-formed incoming id, otherwise generate one."""
    if incoming and _VALID_REQUEST_ID.fullmatch(incoming):
        return incoming
    return uuid.uuid4().hex


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = resolve_request_id(Headers(scope=scope).get(REQUEST_ID_HEADER))
        token = request_id_var.set(request_id)
        started = time.perf_counter()
        status_code = 500
        response_started = False

        async def send_with_request_id(message: Message) -> None:
            nonlocal status_code, response_started
            if message["type"] == "http.response.start":
                response_started = True
                status_code = message["status"]
                MutableHeaders(scope=message)[REQUEST_ID_HEADER] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        except Exception:
            logger.exception("unhandled error")
            if not response_started:
                status_code = 500
                response: Response = error_response(500, "internal_error", "Internal server error")
                await response(scope, receive, send_with_request_id)
        finally:
            duration = time.perf_counter() - started
            route: Any = scope.get("route")
            template = getattr(route, "path", None) or "unmatched"
            method = scope["method"]
            metrics.HTTP_REQUESTS.labels(method, template, str(status_code)).inc()
            metrics.HTTP_DURATION.labels(method, template).observe(duration)
            logger.info(
                "request",
                extra={
                    "method": method,
                    "route": template,
                    "status": status_code,
                    "duration_ms": round(duration * 1000, 1),
                },
            )
            request_id_var.reset(token)

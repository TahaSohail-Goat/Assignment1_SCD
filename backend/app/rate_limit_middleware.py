"""Apply the limiter before FastAPI validates the POST body."""

import asyncio
import ipaddress

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

from app.http_errors import error_response
from app.services.rate_limit import RateLimitService


def client_ip(scope: Scope, trust_forwarded_for: bool) -> str:
    peer = scope.get("client")
    direct = str(peer[0]) if peer else "unknown"
    if not trust_forwarded_for:
        return direct
    forwarded = Headers(scope=scope).get("X-Forwarded-For")
    if not forwarded:
        return direct
    candidate = forwarded.split(",", 1)[0].strip()
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return direct


class RateLimitMiddleware:
    def __init__(self, app: ASGIApp, trust_forwarded_for: bool = False) -> None:
        self.app = app
        self.trust_forwarded_for = trust_forwarded_for

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] == "http"
            and scope["method"] == "POST"
            and scope["path"] == "/api/complaints"
        ):
            limiter: RateLimitService | None = getattr(scope["app"].state, "rate_limiter", None)
            if limiter is not None:
                admission = await asyncio.to_thread(
                    limiter.check, client_ip(scope, self.trust_forwarded_for)
                )
                if not admission.allowed:
                    response = error_response(
                        429,
                        "rate_limited",
                        "Too many complaint submissions",
                        headers={"Retry-After": str(admission.retry_after)},
                    )
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)

"""Liveness and readiness (ASG-FR-031, ASG-FR-032).

``/health`` checks nothing external: a liveness probe that depends on the database would
turn a slow database into a restart loop (assignment section 2.2).
"""

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.http_errors import error_response
from app.services.readiness import ReadinessService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready", response_model=None)
def ready(request: Request) -> JSONResponse | dict[str, Any]:
    readiness: ReadinessService = request.app.state.readiness
    report = readiness.run()
    if report.ready:
        return {"status": "ready", "checks": report.checks}
    failed = report.failed
    message = "Not ready: " + ", ".join(f"{name} {state}" for name, state in failed.items())
    details = [{"dependency": name, "message": state} for name, state in failed.items()]
    return error_response(503, "not_ready", message, details)

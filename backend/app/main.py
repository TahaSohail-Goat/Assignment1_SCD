"""Application factory.

Start it with ``uvicorn app.main:create_app --factory --no-access-log``: the request log line is
written by the middleware, with the request id, so uvicorn's own access log is not needed.

Graceful shutdown (ASG-NFR-008): on SIGTERM uvicorn stops accepting connections and lets
in-flight requests finish; the lifespan below then closes the connection pools before exit.
"""

import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine

from app.config import Settings, get_settings
from app.database import create_db_engine, create_session_factory
from app.http_errors import install_error_handlers
from app.logging import configure_logging
from app.middleware import RequestContextMiddleware
from app.providers.cache import RedisCache
from app.providers.triage.factory import build_provider
from app.repositories.health import DatabaseHealthRepository
from app.repositories.uow import SqlUnitOfWork, UnitOfWork
from app.routes import complaints, health, metrics
from app.services.complaints import ComplaintService, Triager
from app.services.readiness import DependencyProbe, ReadinessService
from app.services.triage import TriageService

logger = logging.getLogger("app.main")


def create_app(
    settings: Settings | None = None,
    probes: list[DependencyProbe] | None = None,
    triager: Triager | None = None,
    unit_of_work: Callable[[], UnitOfWork] | None = None,
) -> FastAPI:
    """Build the app.

    ``probes``, ``triager`` and ``unit_of_work`` let tests replace PostgreSQL, Redis and the
    triage providers; in production they are built from the settings.
    """
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        closers: list[Callable[[], None]] = []
        engine: Engine | None = None
        if probes is None or unit_of_work is None:
            engine = create_db_engine(
                settings.database_url, settings.dependency_check_timeout_seconds
            )
            closers.append(engine.dispose)

        active_probes: list[DependencyProbe]
        if probes is None and engine is not None:
            cache = RedisCache(settings.redis_url, settings.dependency_check_timeout_seconds)
            closers.append(cache.close)
            active_probes = [DatabaseHealthRepository(engine), cache]
        else:
            active_probes = probes or []

        active_unit_of_work: Callable[[], UnitOfWork]
        if unit_of_work is not None:
            active_unit_of_work = unit_of_work
        elif engine is not None:
            session_factory = create_session_factory(engine)

            def open_unit_of_work() -> UnitOfWork:
                return SqlUnitOfWork(session_factory)

            active_unit_of_work = open_unit_of_work
        else:  # unreachable: the engine exists whenever no unit of work was given
            raise RuntimeError("no unit of work and no engine")

        active_triager: Triager
        if triager is not None:
            active_triager = triager
        else:
            triage_service = TriageService(build_provider(settings.triage_provider, settings))
            closers.append(triage_service.close)
            active_triager = triage_service

        readiness = ReadinessService(active_probes, settings.dependency_check_timeout_seconds)
        app.state.readiness = readiness
        app.state.complaints = ComplaintService(active_unit_of_work, active_triager)
        logger.info("startup complete")
        try:
            yield
        finally:
            logger.info("shutdown: closing connection pools")
            readiness.close()
            for close in closers:
                close()

    app = FastAPI(title="CivicPulse API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(RequestContextMiddleware)
    install_error_handlers(app)
    app.include_router(health.router)
    app.include_router(metrics.router)
    app.include_router(complaints.router)
    return app

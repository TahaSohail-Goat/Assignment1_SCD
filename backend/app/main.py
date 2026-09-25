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
from app.openapi import install_openapi
from app.providers.cache import KeyValueCache, RedisCache
from app.providers.triage.factory import build_provider
from app.rate_limit_middleware import RateLimitMiddleware
from app.repositories.health import DatabaseHealthRepository
from app.repositories.uow import SqlUnitOfWork, UnitOfWork
from app.routes import complaints, health, meta, metrics, stats
from app.services.complaints import ComplaintService, Triager
from app.services.meta import MetaService
from app.services.rate_limit import RateLimitService
from app.services.readiness import DependencyProbe, ReadinessService
from app.services.stats import StatsService
from app.services.triage import TriageService
from app.services.triage_cache import TriageCache

logger = logging.getLogger("app.main")


def create_app(
    settings: Settings | None = None,
    probes: list[DependencyProbe] | None = None,
    triager: Triager | None = None,
    unit_of_work: Callable[[], UnitOfWork] | None = None,
    cache: KeyValueCache | None = None,
) -> FastAPI:
    """Build the app.

    ``probes``, ``triager``, ``unit_of_work`` and ``cache`` let tests replace PostgreSQL, Redis
    and the triage providers; in production they are built from the settings.
    """
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        closers: list[Callable[[], None]] = []
        timeout = settings.dependency_check_timeout_seconds

        engine: Engine | None = None
        if probes is None or unit_of_work is None:
            engine = create_db_engine(settings.database_url, timeout)
            closers.append(engine.dispose)

        redis_cache: RedisCache | None = None
        if probes is None or cache is None:
            redis_cache = RedisCache(settings.redis_url, timeout)
            closers.append(redis_cache.close)

        active_probes: list[DependencyProbe]
        if probes is not None:
            active_probes = probes
        elif engine is not None and redis_cache is not None:
            active_probes = [DatabaseHealthRepository(engine), redis_cache]
        else:  # unreachable: both exist whenever no probes were given
            raise RuntimeError("no probes and no connections")

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

        active_cache: KeyValueCache | None = cache or redis_cache
        if active_cache is None:  # unreachable: a Redis cache is built whenever none was given
            raise RuntimeError("no cache")

        active_triager: Triager
        if triager is not None:
            active_triager = triager
        else:
            triage_service = TriageService(
                build_provider(settings.triage_provider, settings), cache=TriageCache(active_cache)
            )
            closers.append(triage_service.close)
            active_triager = triage_service

        stats_service = StatsService(active_unit_of_work, active_cache)
        readiness = ReadinessService(active_probes, timeout)
        app.state.readiness = readiness
        app.state.stats = stats_service
        app.state.rate_limiter = (
            RateLimitService(
                active_cache,
                limit=settings.rate_limit_requests,
                window_seconds=settings.rate_limit_window_seconds,
            )
            if isinstance(active_cache, RedisCache)
            else None
        )
        app.state.unit_of_work = active_unit_of_work
        app.state.meta = MetaService(active_unit_of_work)
        app.state.active_provider = settings.triage_provider
        app.state.complaints = ComplaintService(
            active_unit_of_work, active_triager, after_create=stats_service.invalidate
        )
        logger.info("startup complete")
        try:
            yield
        finally:
            logger.info("shutdown: closing connection pools")
            readiness.close()
            for close in closers:
                close()

    app = FastAPI(title="CivicPulse API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(RateLimitMiddleware, trust_forwarded_for=settings.trust_forwarded_for)
    app.add_middleware(RequestContextMiddleware)
    install_error_handlers(app)
    install_openapi(app)
    app.include_router(health.router)
    app.include_router(metrics.router)
    app.include_router(complaints.router)
    app.include_router(stats.router)
    app.include_router(meta.router)
    return app

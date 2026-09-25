"""Application factory.

Start it with ``uvicorn app.main:create_app --factory --no-access-log``: the request log line is
written by the middleware, with the request id, so uvicorn's own access log is not needed.

Graceful shutdown (ASG-NFR-008): on SIGTERM uvicorn stops accepting connections and lets
in-flight requests finish; the lifespan below then closes the connection pools before exit.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine

from app.config import Settings, get_settings
from app.logging import configure_logging
from app.middleware import RequestContextMiddleware
from app.providers.cache import RedisCache
from app.repositories.health import DatabaseHealthRepository
from app.routes import health, metrics
from app.services.readiness import DependencyProbe, ReadinessService

logger = logging.getLogger("app.main")


def create_app(
    settings: Settings | None = None, probes: list[DependencyProbe] | None = None
) -> FastAPI:
    """Build the app. ``probes`` lets tests replace the real PostgreSQL and Redis probes."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        closers = []
        if probes is None:
            engine = create_engine(
                settings.database_url,
                pool_pre_ping=True,
                connect_args={
                    "connect_timeout": max(1, round(settings.dependency_check_timeout_seconds))
                },
            )
            cache = RedisCache(settings.redis_url, settings.dependency_check_timeout_seconds)
            active_probes: list[DependencyProbe] = [DatabaseHealthRepository(engine), cache]
            closers = [cache.close, engine.dispose]
        else:
            active_probes = probes
        readiness = ReadinessService(active_probes, settings.dependency_check_timeout_seconds)
        app.state.readiness = readiness
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
    app.include_router(health.router)
    app.include_router(metrics.router)
    return app

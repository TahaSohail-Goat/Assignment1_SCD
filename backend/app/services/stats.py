"""Statistics with a read-through Redis cache (ASG-FR-029, ASG-CACHE-002 to 005).

- read-through: a hit is served from Redis; a miss is aggregated from PostgreSQL, stored with a
  TTL of 30 seconds and answered with ``X-Cache: MISS``;
- invalidation on write: a new complaint deletes the entry after its transaction has committed,
  so it appears in the statistics immediately instead of up to 30 seconds later;
- the TTL stays anyway: it bounds staleness when an invalidation is lost (a Redis outage at that
  moment) or races with a concurrent read that cached the counts of a moment before the commit;
- Redis being down never fails the request: the answer is computed from PostgreSQL as a MISS
  (docs/API_DESIGN.md, DQ-API-15).
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from pydantic import ValidationError

from app import metrics
from app.domain import Category, Priority
from app.providers.cache import CacheUnavailableError, KeyValueCache
from app.repositories.uow import UnitOfWork
from app.schemas.stats import Stats

logger = logging.getLogger("app.stats")

CACHE_KEY = "stats:v1"
TTL_SECONDS = 30  # assignment section 2.4 (Job 1)

CacheState = Literal["HIT", "MISS"]


@dataclass(frozen=True)
class StatsResult:
    stats: Stats
    cache: CacheState


class StatsService:
    def __init__(
        self,
        unit_of_work: Callable[[], UnitOfWork],
        cache: KeyValueCache,
        ttl_seconds: int = TTL_SECONDS,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._cache = cache
        self._ttl = ttl_seconds

    def get(self) -> StatsResult:
        cached = self._read_cache()
        if cached is not None:
            metrics.STATS_CACHE.labels("hit").inc()
            return StatsResult(cached, "HIT")
        metrics.STATS_CACHE.labels("miss").inc()
        stats = self._aggregate()
        self._write_cache(stats)
        return StatsResult(stats, "MISS")

    def invalidate(self) -> None:
        """Drop the cached statistics; called after a complaint has been committed."""
        try:
            self._cache.delete(CACHE_KEY)
        except CacheUnavailableError as error:
            logger.warning(
                "could not invalidate the stats cache", extra={"error_class": str(error)}
            )

    def _aggregate(self) -> Stats:
        with self._unit_of_work() as repository:
            counts = repository.counts()
        return Stats(
            total=counts.total,
            by_category={category: counts.by_category.get(category, 0) for category in Category},
            by_priority={priority: counts.by_priority.get(priority, 0) for priority in Priority},
        )

    def _read_cache(self) -> Stats | None:
        try:
            raw = self._cache.get(CACHE_KEY)
        except CacheUnavailableError as error:
            logger.warning(
                "stats cache unavailable, reading from the database",
                extra={"error_class": str(error)},
            )
            return None
        if raw is None:
            return None
        try:
            return Stats.model_validate(json.loads(raw))
        except (ValueError, ValidationError):
            logger.warning("ignoring a malformed stats cache entry")
            return None

    def _write_cache(self, stats: Stats) -> None:
        try:
            self._cache.set(CACHE_KEY, stats.model_dump_json(), self._ttl)
        except CacheUnavailableError as error:
            logger.warning(
                "could not store the stats in the cache", extra={"error_class": str(error)}
            )

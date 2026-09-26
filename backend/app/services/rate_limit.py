"""Distributed fixed-window admission for complaint creation (ASG-CACHE-007…010)."""

import hashlib
import logging
import math
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from app import metrics
from app.providers.cache import CacheUnavailableError

logger = logging.getLogger("app.rate_limit")


class CounterStore(Protocol):
    def increment_with_ttl(self, key: str, ttl_seconds: int) -> int: ...


@dataclass(frozen=True)
class Admission:
    allowed: bool
    retry_after: int = 0


class RateLimitService:
    def __init__(
        self,
        store: CounterStore,
        limit: int = 10,
        window_seconds: int = 60,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if limit < 1 or window_seconds < 1:
            raise ValueError("rate limit and window must be positive")
        self._store = store
        self._limit = limit
        self._window = window_seconds
        self._clock = clock

    def check(self, client_ip: str) -> Admission:
        now = self._clock()
        bucket = math.floor(now / self._window)
        # A stable hash avoids retaining a readable client address in Redis keys.
        client_hash = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()
        key = f"rate:complaints:v1:{client_hash}:{bucket}"
        try:
            count = self._store.increment_with_ttl(key, self._window)
        except CacheUnavailableError as error:
            logger.warning(
                "rate limit unavailable; admitting request",
                extra={"error_class": type(error).__name__},
            )
            return Admission(True)
        if count <= self._limit:
            return Admission(True)
        metrics.RATE_LIMITED.inc()
        remaining = max(1, math.ceil((bucket + 1) * self._window - now))
        return Admission(False, remaining)

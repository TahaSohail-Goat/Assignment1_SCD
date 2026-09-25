"""Triage orchestration: the engineering around the model (assignment section 2.5).

What this module guarantees, whatever the provider does:

- a hard timeout on every call (10 seconds);
- one retry, with jitter, on a timeout, a 429 or a 5xx, and never on a 400;
- the provider's result is validated against ``TriageResult`` again (model output is untrusted);
- on any failure the rule-based provider decides, ``triaged_by`` is ``rules:fallback`` and exactly
  one WARNING is logged with the complaint id, the provider and the error class;
- so a third party being down or rate-limited never becomes a 500 for the citizen.
"""

import logging
import random
import time
import uuid
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout

from app import metrics
from app.providers.triage.base import (
    MalformedOutputError,
    ProviderTimeoutError,
    TriageProvider,
    TriageProviderError,
    TriageResult,
)
from app.providers.triage.rules import RuleBasedTriage
from app.services.complaints import TriageDecision
from app.services.triage_cache import TriageCache

logger = logging.getLogger("app.triage")

FALLBACK_NAME = "rules:fallback"
DEFAULT_TIMEOUT_SECONDS = 10.0  # assignment section 2.5, item 2
RETRY_JITTER_SECONDS = (0.1, 0.5)


class TriageService:
    def __init__(
        self,
        provider: TriageProvider,
        fallback: TriageProvider | None = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        sleep: Callable[[float], None] = time.sleep,
        jitter: Callable[[], float] = lambda: random.uniform(*RETRY_JITTER_SECONDS),  # noqa: S311
        clock: Callable[[], float] = time.perf_counter,
        cache: TriageCache | None = None,
    ) -> None:
        self._provider = provider
        self._fallback = fallback or RuleBasedTriage()
        self._timeout = timeout_seconds
        self._sleep = sleep
        self._jitter = jitter
        self._clock = clock
        self._cache = cache
        self._executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="triage")

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)

    def triage(self, text: str, location: str, complaint_id: uuid.UUID) -> TriageDecision:
        started = self._clock()
        cached = (
            self._cache.get(text, location, self._provider.name, self._validated)
            if self._cache
            else None
        )
        if self._cache:
            metrics.TRIAGE_CACHE.labels("hit" if cached else "miss").inc()
        if cached is not None:
            result, triaged_by = cached
        else:
            try:
                result = self._call_with_one_retry(text, location)
                triaged_by = self._provider.name
            except Exception as error:  # any provider failure must not become a citizen-facing 500
                result = self._validated(self._fallback.triage(text, location))
                triaged_by = FALLBACK_NAME
                self._record_fallback(complaint_id, error)
            if self._cache and triaged_by != FALLBACK_NAME:
                self._cache.put(
                    text, location, result, triaged_by, lambda value: value.model_dump()
                )
        elapsed = self._clock() - started
        metrics.TRIAGE_DURATION.labels(self._provider.name).observe(elapsed)
        return TriageDecision(
            category=result.category,
            priority=result.priority,
            ai_summary=result.summary,
            triaged_by=triaged_by,
            latency_ms=max(0, round(elapsed * 1000)),
        )

    def _call_with_one_retry(self, text: str, location: str) -> TriageResult:
        try:
            return self._call(text, location)
        except TriageProviderError as error:
            if not error.retryable:
                raise
        self._sleep(self._jitter())
        return self._call(text, location)

    def _call(self, text: str, location: str) -> TriageResult:
        future = self._executor.submit(self._provider.triage, text, location)
        try:
            raw = future.result(timeout=self._timeout)
        except FutureTimeout:
            future.cancel()
            raise ProviderTimeoutError(f"no answer within {self._timeout} seconds") from None
        return self._validated(raw)

    @staticmethod
    def _validated(raw: object) -> TriageResult:
        """Validate again, whatever the provider says it did (assignment section 2.5, item 1)."""
        try:
            return TriageResult.model_validate(raw)
        except ValueError as error:  # pydantic's ValidationError is a ValueError
            raise MalformedOutputError(str(error)) from error

    def _record_fallback(self, complaint_id: uuid.UUID, error: Exception) -> None:
        error_class = type(error).__name__
        metrics.TRIAGE_FALLBACK.labels(self._provider.name, error_class).inc()
        logger.warning(
            "triage fallback",
            extra={
                "complaint_id": str(complaint_id),
                "provider": self._provider.name,
                "error_class": error_class,
            },
        )

"""SimulatedTriage: the deterministic fake for CI (ASG-AI-008).

Seeded (the same seed and text always give the same result), no network, and it can be told
how to fail: each call takes the next failure mode from the list, which is how the tests
inject a provider that always raises, one that returns malformed output, or a 429 followed by
a success. Nothing here sleeps or reads a clock.
"""

import hashlib
from collections.abc import Sequence
from enum import StrEnum
from typing import Any, cast

from app.domain import Category, Priority
from app.providers.triage.base import (
    ProviderRateLimitedError,
    ProviderRequestError,
    ProviderServerError,
    ProviderTimeoutError,
    TriageResult,
)


class Failure(StrEnum):
    TIMEOUT = "timeout"  # ProviderTimeoutError (retryable)
    RATE_LIMITED = "rate_limited"  # ProviderRateLimitedError, a 429 (retryable)
    SERVER_ERROR = "server_error"  # ProviderServerError, a 5xx (retryable)
    BAD_REQUEST = "bad_request"  # ProviderRequestError, a 400 (never retried)
    CRASH = "crash"  # an unexpected RuntimeError
    MALFORMED = "malformed"  # a result that is not a valid TriageResult


class SimulatedTriage:
    name = "simulated"

    def __init__(
        self,
        seed: int = 0,
        failures: Sequence[Failure | None] = (),
        repeat_last: bool = False,
    ) -> None:
        """``failures`` is consumed one entry per call (``None`` means succeed); with
        ``repeat_last`` the last entry applies to every later call, so ``[Failure.CRASH]``
        with ``repeat_last=True`` is a provider that always raises."""
        self._seed = seed
        self._failures = list(failures)
        self._repeat_last = repeat_last
        self.calls = 0

    @classmethod
    def always_failing(cls, failure: Failure = Failure.CRASH) -> "SimulatedTriage":
        return cls(failures=[failure], repeat_last=True)

    def _next_failure(self) -> Failure | None:
        index = self.calls - 1
        if index < len(self._failures):
            return self._failures[index]
        if self._repeat_last and self._failures:
            return self._failures[-1]
        return None

    def triage(self, text: str, location: str) -> TriageResult:
        self.calls += 1
        failure = self._next_failure()
        if failure is Failure.TIMEOUT:
            raise ProviderTimeoutError("simulated timeout")
        if failure is Failure.RATE_LIMITED:
            raise ProviderRateLimitedError("simulated 429")
        if failure is Failure.SERVER_ERROR:
            raise ProviderServerError("simulated 503")
        if failure is Failure.BAD_REQUEST:
            raise ProviderRequestError("simulated 400")
        if failure is Failure.CRASH:
            raise RuntimeError("simulated crash")
        if failure is Failure.MALFORMED:
            # Built without validation on purpose: a category outside the enum, a summary far
            # over the limit and a confidence outside 0..1. The orchestration must reject it.
            return TriageResult.model_construct(
                category=cast(Any, "potholes"),
                priority=cast(Any, "urgent"),
                summary="x" * 400,
                confidence=7.5,
            )

        digest = hashlib.sha256(f"{self._seed}:{text}:{location}".encode()).digest()
        categories, priorities = list(Category), list(Priority)
        return TriageResult(
            category=categories[digest[0] % len(categories)],
            priority=priorities[digest[1] % len(priorities)],
            summary=f"Simulated triage of: {' '.join(text.split())[:60]}",
            confidence=round(digest[2] / 255, 2),
        )

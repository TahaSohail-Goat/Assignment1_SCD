"""The triage orchestration: timeout, one retry with jitter, validation, fallback, one WARNING.

ASG-AI-013 to ASG-AI-015, ASG-AI-021, ASG-AI-022, ASG-NFR-011. Nothing here sleeps or reads a
real clock: the sleeper and the jitter are injected, and blocking is done with events.
"""

import logging
import threading
import uuid
from collections.abc import Callable, Iterator

import pytest

from app import metrics
from app.domain import Category
from app.providers.triage.base import TriageResult
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import Failure, SimulatedTriage
from app.services.triage import FALLBACK_NAME, TriageService

TEXT = "The water pipe on our street has been leaking since Monday."
LOCATION = "Street 12, Johar Town"
COMPLAINT_ID = uuid.UUID(int=42)


class Recorder:
    """An injected sleeper and clock: records the jitter it was asked to wait, never waits."""

    def __init__(self) -> None:
        self.slept: list[float] = []
        self._now = 0.0

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)

    def clock(self) -> float:
        self._now += 0.25  # every reading is 250 ms later than the previous one
        return self._now


@pytest.fixture
def recorder() -> Recorder:
    return Recorder()


@pytest.fixture
def make_service(recorder: Recorder) -> Iterator[Callable[..., TriageService]]:
    created: list[TriageService] = []

    def make(provider: object, **kwargs: object) -> TriageService:
        service = TriageService(
            provider,  # type: ignore[arg-type]
            sleep=recorder.sleep,
            jitter=lambda: 0.123,
            clock=recorder.clock,
            **kwargs,  # type: ignore[arg-type]
        )
        created.append(service)
        return service

    yield make
    for service in created:
        service.close()


def _warnings(caplog: pytest.LogCaptureFixture) -> list[logging.LogRecord]:
    return [r for r in caplog.records if r.name == "app.triage" and r.levelno == logging.WARNING]


def test_a_healthy_provider_is_used_and_recorded_by_name(make_service, recorder, caplog) -> None:
    provider = SimulatedTriage(seed=3)
    service = make_service(provider)

    decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert decision.triaged_by == "simulated"
    assert decision.ai_summary and decision.ai_summary.startswith("Simulated triage of:")
    assert decision.latency_ms == 250  # two clock readings, 250 ms apart
    assert provider.calls == 1
    assert _warnings(caplog) == []


def test_the_mandatory_case_a_provider_that_always_raises_falls_back_to_rules(
    make_service, caplog
) -> None:
    provider = SimulatedTriage.always_failing()
    service = make_service(provider)
    expected = RuleBasedTriage().triage(TEXT, LOCATION)

    with caplog.at_level(logging.WARNING, logger="app.triage"):
        decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert decision.triaged_by == FALLBACK_NAME == "rules:fallback"
    assert (decision.category, decision.priority) == (expected.category, expected.priority)
    assert decision.ai_summary == expected.summary
    assert provider.calls == 1  # a crash is not retryable


def test_exactly_one_warning_per_fallback_with_complaint_id_provider_and_error_class(
    make_service, caplog
) -> None:
    service = make_service(SimulatedTriage.always_failing())

    with caplog.at_level(logging.WARNING, logger="app.triage"):
        service.triage(TEXT, LOCATION, COMPLAINT_ID)

    (record,) = _warnings(caplog)
    assert record.complaint_id == str(COMPLAINT_ID)  # type: ignore[attr-defined]
    assert record.provider == "simulated"  # type: ignore[attr-defined]
    assert record.error_class == "RuntimeError"  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "first",
    [Failure.TIMEOUT, Failure.RATE_LIMITED, Failure.SERVER_ERROR],
)
def test_a_timeout_a_429_and_a_5xx_are_retried_once_with_jitter(
    make_service, recorder, caplog, first: Failure
) -> None:
    provider = SimulatedTriage(failures=[first, None])
    service = make_service(provider)

    decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert provider.calls == 2
    assert recorder.slept == [0.123]  # waited once, by the jitter
    assert decision.triaged_by == "simulated"  # the retry succeeded: no fallback
    assert _warnings(caplog) == []


def test_after_the_one_retry_fails_too_the_rules_decide(make_service, recorder, caplog) -> None:
    provider = SimulatedTriage(failures=[Failure.RATE_LIMITED, Failure.SERVER_ERROR])
    service = make_service(provider)

    with caplog.at_level(logging.WARNING, logger="app.triage"):
        decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert provider.calls == 2  # retried once, not twice
    assert recorder.slept == [0.123]
    assert decision.triaged_by == "rules:fallback"
    (record,) = _warnings(caplog)
    assert record.error_class == "ProviderServerError"  # type: ignore[attr-defined]


def test_a_400_is_never_retried(make_service, recorder, caplog) -> None:
    provider = SimulatedTriage(failures=[Failure.BAD_REQUEST, None])
    service = make_service(provider)

    with caplog.at_level(logging.WARNING, logger="app.triage"):
        decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert provider.calls == 1
    assert recorder.slept == []
    assert decision.triaged_by == "rules:fallback"


def test_malformed_output_is_rejected_not_retried_and_never_reaches_the_decision(
    make_service, recorder, caplog
) -> None:
    provider = SimulatedTriage(failures=[Failure.MALFORMED])
    service = make_service(provider)

    with caplog.at_level(logging.WARNING, logger="app.triage"):
        decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert provider.calls == 1 and recorder.slept == []
    assert decision.triaged_by == "rules:fallback"
    assert decision.category in set(Category) and len(decision.ai_summary or "") <= 140
    (record,) = _warnings(caplog)
    assert record.error_class == "MalformedOutputError"  # type: ignore[attr-defined]


def test_a_provider_that_returns_the_wrong_type_is_rejected(make_service) -> None:
    class ReturnsProse:
        name = "prose"

        def triage(self, text: str, location: str) -> object:
            return "Sure! Here is the JSON you asked for: ```json {...}```"

    decision = make_service(ReturnsProse()).triage(TEXT, LOCATION, COMPLAINT_ID)

    assert decision.triaged_by == "rules:fallback"


def test_a_provider_that_never_answers_is_cut_off_and_retried_then_the_rules_decide(
    make_service, recorder, caplog
) -> None:
    release = threading.Event()

    class Hangs:
        name = "hangs"
        calls = 0

        def triage(self, text: str, location: str) -> TriageResult:
            Hangs.calls += 1
            release.wait(timeout=10)  # released at the end of the test, never slept
            return RuleBasedTriage().triage(text, location)

    service = make_service(Hangs(), timeout_seconds=0.05)

    try:
        with caplog.at_level(logging.WARNING, logger="app.triage"):
            decision = service.triage(TEXT, LOCATION, COMPLAINT_ID)
    finally:
        release.set()

    assert Hangs.calls == 2  # a timeout is retryable: one retry
    assert recorder.slept == [0.123]
    assert decision.triaged_by == "rules:fallback"
    (record,) = _warnings(caplog)
    assert record.error_class == "ProviderTimeoutError"  # type: ignore[attr-defined]


def test_the_default_timeout_is_ten_seconds() -> None:
    from app.services.triage import DEFAULT_TIMEOUT_SECONDS

    assert DEFAULT_TIMEOUT_SECONDS == 10.0


def test_when_the_configured_provider_is_rules_there_is_no_fallback_label(make_service) -> None:
    decision = make_service(RuleBasedTriage()).triage(TEXT, LOCATION, COMPLAINT_ID)

    assert decision.triaged_by == "rules"


def test_metrics_count_the_fallback_and_observe_the_triage_latency(make_service) -> None:
    def fallbacks() -> float:
        return (
            metrics.REGISTRY.get_sample_value(
                "triage_fallback_total", {"provider": "simulated", "error_class": "RuntimeError"}
            )
            or 0.0
        )

    def observations() -> float:
        return (
            metrics.REGISTRY.get_sample_value(
                "triage_duration_seconds_count", {"provider": "simulated"}
            )
            or 0.0
        )

    before_fallbacks, before_observations = fallbacks(), observations()
    service = make_service(SimulatedTriage.always_failing())

    service.triage(TEXT, LOCATION, COMPLAINT_ID)

    assert fallbacks() == before_fallbacks + 1
    assert observations() == before_observations + 1

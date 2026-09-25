"""RuleBasedTriage, SimulatedTriage and the factory (ASG-AI-001…004, 007, 008)."""

import pytest
from pydantic import ValidationError

from app.config import Settings
from app.domain import Category, Priority
from app.providers.triage.base import (
    ProviderRateLimitedError,
    ProviderRequestError,
    ProviderServerError,
    ProviderTimeoutError,
    TriageResult,
)
from app.providers.triage.factory import PROVIDERS, UnknownProviderError, build_provider
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import Failure, SimulatedTriage

# ---- TriageResult ---------------------------------------------------------


def test_triage_result_accepts_the_model_of_the_assignment() -> None:
    result = TriageResult(
        category="water", priority="high", summary="No water for three days", confidence=0.8
    )

    assert result.category is Category.WATER and result.priority is Priority.HIGH


@pytest.mark.parametrize(
    "bad",
    [
        {"category": "potholes"},
        {"priority": "urgent"},
        {"summary": "x" * 141},
        {"summary": ""},
        {"summary": "two\nlines"},
        {"confidence": -0.01},
        {"confidence": 1.01},
        {"unexpected": "field"},
    ],
)
def test_triage_result_rejects_everything_outside_the_model(bad: dict[str, object]) -> None:
    valid = {"category": "water", "priority": "high", "summary": "ok", "confidence": 0.5}

    with pytest.raises(ValidationError):
        TriageResult(**{**valid, **bad})  # type: ignore[arg-type]


def test_a_result_built_without_validation_is_validated_again_on_use() -> None:
    unchecked = TriageResult.model_construct(
        category="potholes", priority="urgent", summary="x" * 400, confidence=7.5
    )

    with pytest.raises(ValidationError):
        TriageResult.model_validate(unchecked)


def test_the_summary_boundary_is_140_characters() -> None:
    ok = TriageResult(category="other", priority="low", summary="s" * 140, confidence=1.0)

    assert len(ok.summary) == 140


# ---- RuleBasedTriage ------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("Water supply has stopped and the tap is dry.", Category.WATER),
        ("The transformer is sparking and the power is off.", Category.ELECTRICITY),
        ("Garbage is piled up and the drain smells terrible.", Category.SANITATION),
        ("A deep pothole on the main road near the bridge.", Category.ROADS),
        ("The street light on our lane is out.", Category.STREETLIGHTS),
        ("I would like to suggest a bench in the park.", Category.OTHER),
    ],
)
def test_rules_pick_the_category_from_keywords(text: str, category: Category) -> None:
    assert RuleBasedTriage().triage(text, "Sector 5").category is category


@pytest.mark.parametrize(
    ("text", "priority"),
    [
        ("There is a live wire in the street, very dangerous for children.", Priority.HIGH),
        ("A minor crack in the pavement, no hurry.", Priority.LOW),
        ("The tap in our lane drips at night.", Priority.NORMAL),
    ],
)
def test_rules_pick_the_priority_from_keywords(text: str, priority: Priority) -> None:
    assert RuleBasedTriage().triage(text, "Block C").priority is priority


def test_rules_are_deterministic() -> None:
    text = "Sewage is overflowing on the main road. Please send a team."

    first = RuleBasedTriage().triage(text, "Lane 2")
    second = RuleBasedTriage().triage(text, "Lane 2")

    assert first == second


@pytest.mark.parametrize(
    "text",
    ["", "   ", "\n\n", "x", "😀" * 500, "a" * 5000, "Ünïcödé çomplaint about wäter", "ﷺ"],
)
def test_rules_never_fail_and_always_return_a_valid_one_line_summary(text: str) -> None:
    result = RuleBasedTriage().triage(text, "")

    assert 1 <= len(result.summary) <= 140
    assert "\n" not in result.summary and "\r" not in result.summary
    assert 0.0 <= result.confidence <= 1.0


def test_the_summary_is_the_first_sentence_cut_to_the_limit() -> None:
    long_sentence = "The water pipe on our street has been leaking " + "badly " * 40 + "today."

    result = RuleBasedTriage().triage(long_sentence + " Second sentence.", "X")

    assert len(result.summary) <= 140 and result.summary.startswith("The water pipe")
    assert "Second sentence" not in result.summary


def test_the_provider_is_named_rules() -> None:
    assert RuleBasedTriage().name == "rules"


# ---- SimulatedTriage ------------------------------------------------------


def test_simulated_is_deterministic_for_a_seed_and_differs_across_seeds() -> None:
    text = "Some complaint text that is long enough."

    a = SimulatedTriage(seed=1).triage(text, "Here")
    b = SimulatedTriage(seed=1).triage(text, "Here")
    outcomes = {
        (r.category, r.priority, r.confidence)
        for r in (SimulatedTriage(seed=s).triage(text, "Here") for s in range(20))
    }

    assert a == b
    assert len(outcomes) > 1


@pytest.mark.parametrize(
    ("failure", "error"),
    [
        (Failure.TIMEOUT, ProviderTimeoutError),
        (Failure.RATE_LIMITED, ProviderRateLimitedError),
        (Failure.SERVER_ERROR, ProviderServerError),
        (Failure.BAD_REQUEST, ProviderRequestError),
        (Failure.CRASH, RuntimeError),
    ],
)
def test_simulated_injects_each_failure_mode(failure: Failure, error: type[Exception]) -> None:
    provider = SimulatedTriage(failures=[failure])

    with pytest.raises(error):
        provider.triage("text long enough", "loc")


def test_simulated_consumes_one_failure_mode_per_call_then_succeeds() -> None:
    provider = SimulatedTriage(failures=[Failure.RATE_LIMITED, None])

    with pytest.raises(ProviderRateLimitedError):
        provider.triage("text long enough", "loc")
    assert provider.triage("text long enough", "loc").summary
    assert provider.triage("text long enough", "loc").summary  # and keeps succeeding
    assert provider.calls == 3


def test_an_always_failing_simulated_provider_fails_on_every_call() -> None:
    provider = SimulatedTriage.always_failing()

    for _ in range(3):
        with pytest.raises(RuntimeError):
            provider.triage("text long enough", "loc")


def test_simulated_malformed_mode_returns_something_the_model_refuses() -> None:
    result = SimulatedTriage(failures=[Failure.MALFORMED]).triage("text long enough", "loc")

    with pytest.raises(ValidationError):
        TriageResult.model_validate(result)


# ---- factory --------------------------------------------------------------


def _settings(provider: str) -> Settings:
    return Settings(
        database_url="postgresql+psycopg://u@postgres:5432/d",
        redis_url="redis://redis:6379/0",
        triage_provider=provider,
    )


@pytest.mark.parametrize(
    ("name", "cls"), [("rules", RuleBasedTriage), ("simulated", SimulatedTriage)]
)
def test_the_factory_selects_the_provider_by_name(name: str, cls: type) -> None:
    assert isinstance(build_provider(name, _settings(name)), cls)


def test_the_factory_ignores_case_and_spaces() -> None:
    assert isinstance(build_provider("  Simulated ", _settings("simulated")), SimulatedTriage)


def test_the_factory_refuses_an_unknown_name_and_lists_the_available_ones() -> None:
    with pytest.raises(UnknownProviderError) as error:
        build_provider("gpt-9", _settings("gpt-9"))

    message = str(error.value)
    assert "gpt-9" in message and all(name in message for name in PROVIDERS)


def test_the_provider_is_read_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u@postgres:5432/d")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("TRIAGE_PROVIDER", "simulated")

    settings = Settings()  # type: ignore[call-arg]

    assert isinstance(build_provider(settings.triage_provider, settings), SimulatedTriage)


def test_the_default_provider_needs_no_network() -> None:
    settings = Settings(
        database_url="postgresql+psycopg://u@postgres:5432/d", redis_url="redis://r/0"
    )

    assert settings.triage_provider == "rules"

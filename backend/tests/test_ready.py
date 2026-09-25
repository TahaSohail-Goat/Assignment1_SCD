"""ASG-FR-032: /ready is 200 only when PostgreSQL and Redis answer; else 503 naming the failure."""

import threading

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe


def _ready(settings: Settings, postgres: FakeProbe, redis: FakeProbe) -> tuple[int, dict]:  # type: ignore[type-arg]
    with TestClient(create_app(settings, probes=[postgres, redis])) as client:
        response = client.get("/ready")
    return response.status_code, response.json()


def test_ready_when_both_dependencies_answer(settings: Settings) -> None:
    status, body = _ready(settings, FakeProbe("postgres"), FakeProbe("redis"))

    assert status == 200
    assert body == {"status": "ready", "checks": {"postgres": "ok", "redis": "ok"}}


def test_not_ready_names_postgres_when_only_postgres_is_down(settings: Settings) -> None:
    status, body = _ready(
        settings, FakeProbe("postgres", error=ConnectionError("down")), FakeProbe("redis")
    )

    assert status == 503
    assert body["error"]["code"] == "not_ready"
    assert body["error"]["details"] == [{"dependency": "postgres", "message": "unreachable"}]
    assert "postgres" in body["error"]["message"]
    assert "redis" not in body["error"]["message"]


def test_not_ready_names_redis_when_only_redis_is_down(settings: Settings) -> None:
    status, body = _ready(
        settings, FakeProbe("postgres"), FakeProbe("redis", error=ConnectionError("down"))
    )

    assert status == 503
    assert body["error"]["details"] == [{"dependency": "redis", "message": "unreachable"}]
    assert "postgres" not in body["error"]["message"]


def test_not_ready_names_every_failed_dependency(settings: Settings) -> None:
    status, body = _ready(
        settings,
        FakeProbe("postgres", error=ConnectionError("down")),
        FakeProbe("redis", error=ConnectionError("down")),
    )

    assert status == 503
    named = {detail["dependency"] for detail in body["error"]["details"]}
    assert named == {"postgres", "redis"}


def test_a_dependency_that_does_not_answer_in_time_is_reported_as_timed_out(
    settings: Settings, release: threading.Event
) -> None:
    status, body = _ready(settings, FakeProbe("postgres", block=release), FakeProbe("redis"))

    assert status == 503
    assert body["error"]["details"] == [{"dependency": "postgres", "message": "timed out"}]


def test_failure_details_never_leak_the_exception_text(settings: Settings) -> None:
    secret_error = RuntimeError("could not connect with password=hunter2")
    status, body = _ready(settings, FakeProbe("postgres", error=secret_error), FakeProbe("redis"))

    assert status == 503
    assert "hunter2" not in str(body)

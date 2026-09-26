"""ASG-FR-031: /health is liveness and must not touch any dependency."""

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe


def test_health_answers_while_every_dependency_is_down(settings: Settings) -> None:
    postgres = FakeProbe("postgres", error=ConnectionError("down"))
    redis = FakeProbe("redis", error=ConnectionError("down"))
    with TestClient(create_app(settings, probes=[postgres, redis])) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert postgres.calls == 0
    assert redis.calls == 0

"""ASG-NFR-010 and DQ-API-13: the request id is accepted, generated, echoed and logged."""

import re

import pytest
from fastapi.testclient import TestClient

from app import metrics
from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe


def _client(settings: Settings, **kwargs: object) -> TestClient:
    app = create_app(settings, probes=[FakeProbe("postgres"), FakeProbe("redis")])

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("boom")

    return TestClient(app, raise_server_exceptions=False, **kwargs)  # type: ignore[arg-type]


def test_a_request_id_is_generated_when_absent_and_echoed(settings: Settings) -> None:
    with _client(settings) as client:
        response = client.get("/health")

    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["X-Request-ID"])


def test_a_well_formed_incoming_request_id_is_kept(settings: Settings) -> None:
    with _client(settings) as client:
        response = client.get("/health", headers={"X-Request-ID": "trace-42.abc_DEF"})

    assert response.headers["X-Request-ID"] == "trace-42.abc_DEF"


@pytest.mark.parametrize("bad", ["has space", "x" * 65, "semi;colon", "new\tline"])
def test_a_malformed_incoming_request_id_is_replaced(settings: Settings, bad: str) -> None:
    with _client(settings) as client:
        response = client.get("/health", headers={"X-Request-ID": bad})

    assert response.headers["X-Request-ID"] != bad
    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["X-Request-ID"])


def test_an_unhandled_error_becomes_a_500_in_the_error_model_with_the_request_id(
    settings: Settings,
) -> None:
    with _client(settings) as client:
        response = client.get("/boom", headers={"X-Request-ID": "err-1"})

    assert response.status_code == 500
    assert response.headers["X-Request-ID"] == "err-1"
    assert response.json() == {
        "error": {"code": "internal_error", "message": "Internal server error"}
    }


def test_metrics_use_the_route_template_and_count_unknown_paths_as_unmatched(
    settings: Settings,
) -> None:
    def count(route: str, status: str) -> float:
        value = metrics.REGISTRY.get_sample_value(
            "http_requests_total", {"method": "GET", "route": route, "status": status}
        )
        return value or 0.0

    before_health = count("/health", "200")
    before_unmatched = count("unmatched", "404")
    with _client(settings) as client:
        client.get("/health")
        client.get("/no/such/path/123")

    assert count("/health", "200") == before_health + 1
    assert count("unmatched", "404") == before_unmatched + 1

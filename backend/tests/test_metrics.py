"""ASG-FR-033: /metrics is Prometheus text with the four families the assignment names."""

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe


def test_metrics_exposes_request_count_latency_triage_latency_and_fallback_counter(
    settings: Settings,
) -> None:
    with TestClient(create_app(settings, probes=[FakeProbe("postgres")])) as client:
        client.get("/health")
        response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain; version=")
    text = response.text
    assert "# TYPE http_requests_total counter" in text
    assert "# TYPE http_request_duration_seconds histogram" in text
    assert "# TYPE triage_duration_seconds histogram" in text
    assert "# TYPE triage_fallback_total counter" in text
    assert 'http_requests_total{method="GET",route="/health",status="200"}' in text

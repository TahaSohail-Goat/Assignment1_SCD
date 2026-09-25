"""Provider metadata comes from persisted outcomes, not a per-process list."""

from fastapi.testclient import TestClient

from app.config import Settings
from app.domain import Category, Priority
from app.main import create_app
from app.repositories.complaints import NewComplaint
from tests.conftest import FakeProbe
from tests.fakes import FakeCache, FakeUnitOfWork, StubTriager


def test_meta_lists_active_provider_and_newest_twenty(settings: Settings) -> None:
    uow = FakeUnitOfWork()
    for index in range(21):
        uow.repository.add(
            NewComplaint(
                text=f"Water outage number {index}",
                location="Ward 2",
                reporter_contact=None,
                category=Category.WATER,
                priority=Priority.HIGH,
                ai_summary="Water outage",
                triaged_by="rules:fallback" if index == 20 else "simulated",
                triage_latency_ms=index,
            )
        )
    app = create_app(
        settings,
        probes=[FakeProbe("postgres"), FakeProbe("redis")],
        triager=StubTriager(),
        unit_of_work=uow,
        cache=FakeCache(),
    )
    with TestClient(app) as client:
        response = client.get("/api/meta/providers")

    assert response.status_code == 200
    body = response.json()
    assert body["active_provider"] == "rules"
    assert len(body["recent"]) == 20
    assert body["recent"][0]["latency_ms"] == 20
    assert body["recent"][0]["fallback"] is True
    assert body["recent"][-1]["latency_ms"] == 1

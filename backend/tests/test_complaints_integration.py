"""The whole path against a real PostgreSQL: HTTP -> service -> unit of work -> SQL -> rows."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text

from app.config import Settings
from app.main import create_app
from app.providers.triage.simulated import SimulatedTriage
from app.services.triage import TriageService
from tests.conftest import FakeProbe
from tests.fakes import FakeCache, StubTriager

pytestmark = pytest.mark.integration


@pytest.fixture
def client(migrated: Engine, db_url: str) -> Iterator[TestClient]:
    with migrated.begin() as connection:
        connection.execute(text("TRUNCATE complaints"))
    settings = Settings(
        database_url=db_url,
        redis_url="redis://redis:6379/0",
        dependency_check_timeout_seconds=1,
    )
    app = create_app(
        settings, probes=[FakeProbe("postgres")], triager=StubTriager(), cache=FakeCache()
    )
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    with migrated.begin() as connection:
        connection.execute(text("TRUNCATE complaints"))


def test_create_get_change_status_and_list_round_trip(client: TestClient, migrated: Engine) -> None:
    created = client.post(
        "/api/complaints",
        json={"text": "There is no water in our lane since Monday.", "location": "Lane 3, Gulberg"},
    )
    assert created.status_code == 201
    body = created.json()

    fetched = client.get(f"/api/complaints/{body['id']}")
    moved = client.patch(f"/api/complaints/{body['id']}/status", json={"status": "in_progress"})
    refused = client.patch(f"/api/complaints/{body['id']}/status", json={"status": "open"})
    listed = client.get("/api/complaints", params={"status": "in_progress"})

    assert fetched.status_code == 200 and fetched.json() == body
    assert moved.status_code == 200 and moved.json()["status"] == "in_progress"
    assert moved.json()["updated_at"] >= body["updated_at"]
    assert refused.status_code == 409
    assert listed.json()["total"] == 1
    with migrated.connect() as connection:
        stored = connection.execute(text("SELECT status::text, triaged_by FROM complaints")).one()
    assert tuple(stored) == ("in_progress", "simulated")


def test_a_failed_request_leaves_no_row_behind(client: TestClient, migrated: Engine) -> None:
    client.post("/api/complaints", json={"text": "short", "location": "x"})

    with migrated.connect() as connection:
        count = connection.execute(text("SELECT count(*) FROM complaints")).scalar_one()
    assert count == 0


def test_the_list_is_paged_newest_first_on_a_real_table(client: TestClient) -> None:
    for number in range(5):
        client.post(
            "/api/complaints",
            json={"text": f"complaint number {number} for the paging test", "location": "Sector 9"},
        )

    first = client.get("/api/complaints", params={"page_size": 2}).json()
    everything = client.get("/api/complaints").json()

    assert first["total"] == 5 and len(first["items"]) == 2
    assert first["items"] == everything["items"][:2]
    stamps = [item["created_at"] for item in everything["items"]]
    assert stamps == sorted(stamps, reverse=True)


def test_the_mandatory_case_on_a_real_table_an_always_raising_provider_stores_rules_fallback(
    migrated: Engine, db_url: str
) -> None:
    with migrated.begin() as connection:
        connection.execute(text("TRUNCATE complaints"))
    settings = Settings(
        database_url=db_url, redis_url="redis://redis:6379/0", dependency_check_timeout_seconds=1
    )
    triage = TriageService(SimulatedTriage.always_failing())
    app = create_app(settings, probes=[FakeProbe("postgres")], triager=triage, cache=FakeCache())

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post(
            "/api/complaints",
            json={"text": "The transformer near our house is sparking.", "location": "Block B"},
        )
    triage.close()

    assert response.status_code == 201 and response.json()["triaged_by"] == "rules:fallback"
    with migrated.connect() as connection:
        stored = connection.execute(
            text("SELECT triaged_by, category::text, priority::text FROM complaints")
        ).one()
    assert tuple(stored) == ("rules:fallback", "electricity", "high")
    with migrated.begin() as connection:
        connection.execute(text("TRUNCATE complaints"))

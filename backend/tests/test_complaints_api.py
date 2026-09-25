"""The complaint endpoints over HTTP, with a fake repository and triage provider.

ASG-FR-020, 021, 023, 024, 025, 026, 027, 028, 036 and the error model of docs/API_DESIGN.md.
"""

import uuid
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.domain import Category, Priority, Status
from app.main import create_app
from app.providers.triage.simulated import SimulatedTriage
from app.services.complaints import TriageDecision
from app.services.triage import TriageService
from tests.conftest import FakeProbe
from tests.fakes import FakeCache, FakeUnitOfWork, StubTriager

VALID = {
    "text": "The street light on our lane has been out for a week.",
    "location": "Lane 3, Gulberg",
}


@pytest.fixture
def unit_of_work() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture
def triager() -> StubTriager:
    return StubTriager()


@pytest.fixture
def client(
    settings: Settings, unit_of_work: FakeUnitOfWork, triager: StubTriager
) -> Iterator[TestClient]:
    app = create_app(
        settings,
        probes=[FakeProbe("postgres"), FakeProbe("redis")],
        triager=triager,
        unit_of_work=unit_of_work,
        cache=FakeCache(),
    )
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def _create(client: TestClient, **overrides: object) -> dict[str, Any]:
    response = client.post("/api/complaints", json={**VALID, **overrides})
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def _error(response: Any) -> dict[str, Any]:
    body: dict[str, Any] = response.json()
    assert set(body) == {"error"}
    return dict(body["error"])


# ---- POST /api/complaints -------------------------------------------------


def test_create_answers_201_with_the_stored_complaint_and_a_location_header(
    client: TestClient, triager: StubTriager
) -> None:
    response = client.post("/api/complaints", json={**VALID, "reporter_contact": "0300-1234567"})

    assert response.status_code == 201
    body = response.json()
    assert uuid.UUID(body["id"])
    assert response.headers["Location"] == f"/api/complaints/{body['id']}"
    assert body["text"] == VALID["text"] and body["reporter_contact"] == "0300-1234567"
    assert body["status"] == "open"
    assert (body["category"], body["priority"]) == ("water", "high")
    assert (body["ai_summary"], body["triaged_by"], body["triage_latency_ms"]) == (
        "No water for three days",
        "simulated",
        7,
    )
    assert body["created_at"].endswith("Z") or "+00:00" in body["created_at"]
    assert triager.calls == [(VALID["text"], VALID["location"])]


def test_create_strips_surrounding_whitespace_and_ignores_unknown_fields(
    client: TestClient,
) -> None:
    body = _create(client, text="   " + VALID["text"] + "   ", surprise="ignored")

    assert body["text"] == VALID["text"]
    assert "surprise" not in body


def test_create_ignores_a_client_supplied_category_priority_status_and_id(
    client: TestClient,
) -> None:
    body = _create(
        client, category="roads", priority="low", status="resolved", id=str(uuid.uuid4())
    )

    assert (body["category"], body["priority"], body["status"]) == ("water", "high", "open")


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({**VALID, "text": "x" * 9}, "text"),
        ({**VALID, "text": "x" * 2001}, "text"),
        ({**VALID, "location": "ab"}, "location"),
        ({**VALID, "location": "y" * 201}, "location"),
        ({**VALID, "reporter_contact": "c" * 201}, "reporter_contact"),
        ({"location": VALID["location"]}, "text"),
        ({"text": VALID["text"]}, "location"),
        ({**VALID, "text": 12345678901}, "text"),
    ],
)
def test_create_answers_400_with_a_field_level_error(
    client: TestClient, payload: dict[str, object], field: str
) -> None:
    response = client.post("/api/complaints", json=payload)

    assert response.status_code == 400  # not FastAPI's default 422
    error = _error(response)
    assert error["code"] == "validation_error"
    assert error["message"] == "Invalid request"
    assert field in {detail["field"] for detail in error["details"]}
    assert all(set(detail) == {"field", "message"} for detail in error["details"])


def test_create_reports_every_invalid_field_at_once(client: TestClient) -> None:
    response = client.post("/api/complaints", json={"text": "short", "location": "x"})

    fields = {detail["field"] for detail in _error(response)["details"]}
    assert fields == {"text", "location"}


def test_create_with_a_body_that_is_not_json_is_a_400_in_the_same_model(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/complaints", content=b"{not json", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400
    assert _error(response)["code"] == "validation_error"


def test_a_validation_error_never_reaches_triage_or_the_repository(
    client: TestClient, triager: StubTriager, unit_of_work: FakeUnitOfWork
) -> None:
    client.post("/api/complaints", json={**VALID, "text": "x"})

    assert triager.calls == []
    assert unit_of_work.repository.rows == {}


def test_without_an_injected_triager_the_configured_provider_is_used(
    settings: Settings, unit_of_work: FakeUnitOfWork
) -> None:
    app = create_app(
        settings, probes=[FakeProbe("postgres")], unit_of_work=unit_of_work, cache=FakeCache()
    )
    with TestClient(app, raise_server_exceptions=False) as client:
        body = _create(client)

    assert body["triaged_by"] == "rules"  # the default TRIAGE_PROVIDER: deterministic, no network


def test_the_mandatory_test_a_provider_that_always_raises_still_gives_201_and_rules_fallback(
    settings: Settings, unit_of_work: FakeUnitOfWork
) -> None:
    """Assignment section 2.5 p12: "Write this test if you write no other"."""
    triage = TriageService(SimulatedTriage.always_failing())
    app = create_app(
        settings,
        probes=[FakeProbe("postgres")],
        triager=triage,
        unit_of_work=unit_of_work,
        cache=FakeCache(),
    )
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post("/api/complaints", json=VALID)
    triage.close()

    assert response.status_code == 201
    body = response.json()
    assert body["triaged_by"] == "rules:fallback"
    assert body["category"] in {c.value for c in Category}
    assert unit_of_work.repository.rows[uuid.UUID(body["id"])].triaged_by == "rules:fallback"


# ---- GET /api/complaints/{id} ---------------------------------------------


def test_get_returns_the_complaint(client: TestClient) -> None:
    created = _create(client)

    response = client.get(f"/api/complaints/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


@pytest.mark.parametrize("bad_id", [str(uuid.uuid4()), "not-a-uuid", "123"])
def test_get_answers_404_for_an_unknown_or_malformed_id(client: TestClient, bad_id: str) -> None:
    response = client.get(f"/api/complaints/{bad_id}")

    assert response.status_code == 404
    assert _error(response) == {"code": "not_found", "message": "Complaint not found"}


# ---- GET /api/complaints --------------------------------------------------


def _seed(client: TestClient, unit_of_work: FakeUnitOfWork, triager: StubTriager) -> None:
    combos = [
        (Category.WATER, Priority.HIGH),
        (Category.WATER, Priority.LOW),
        (Category.ROADS, Priority.HIGH),
        (Category.ROADS, Priority.NORMAL),
        (Category.OTHER, Priority.LOW),
    ]
    for number, (category, priority) in enumerate(combos):
        triager.decision = TriageDecision(category, priority, None, "rules", 1)
        _create(client, text=f"complaint number {number} in the seeded set")


def test_list_returns_the_envelope_newest_first_with_defaults(
    client: TestClient, unit_of_work: FakeUnitOfWork, triager: StubTriager
) -> None:
    _seed(client, unit_of_work, triager)

    body = client.get("/api/complaints").json()

    assert set(body) == {"items", "total", "page", "page_size"}
    assert (body["total"], body["page"], body["page_size"]) == (5, 1, 20)
    assert body["items"][0]["text"].startswith("complaint number 4")  # newest first


def test_list_filters_combine_with_and(
    client: TestClient, unit_of_work: FakeUnitOfWork, triager: StubTriager
) -> None:
    _seed(client, unit_of_work, triager)

    water = client.get("/api/complaints", params={"category": "water"}).json()
    water_high = client.get(
        "/api/complaints", params={"category": "water", "priority": "high"}
    ).json()
    nothing = client.get("/api/complaints", params={"status": "resolved"}).json()

    assert water["total"] == 2
    assert water_high["total"] == 1 and water_high["items"][0]["priority"] == "high"
    assert nothing == {"items": [], "total": 0, "page": 1, "page_size": 20}


def test_list_pages_without_overlap_and_reports_the_total(
    client: TestClient, unit_of_work: FakeUnitOfWork, triager: StubTriager
) -> None:
    _seed(client, unit_of_work, triager)

    first = client.get("/api/complaints", params={"page": 1, "page_size": 2}).json()
    third = client.get("/api/complaints", params={"page": 3, "page_size": 2}).json()
    beyond = client.get("/api/complaints", params={"page": 4, "page_size": 2}).json()

    assert (len(first["items"]), len(third["items"]), len(beyond["items"])) == (2, 1, 0)
    assert first["total"] == third["total"] == beyond["total"] == 5
    assert {i["id"] for i in first["items"]}.isdisjoint({i["id"] for i in third["items"]})


def test_list_accepts_the_maximum_page_size_of_100(client: TestClient) -> None:
    assert client.get("/api/complaints", params={"page_size": 100}).status_code == 200


@pytest.mark.parametrize(
    ("params", "field"),
    [
        ({"page_size": 101}, "page_size"),  # rejected, not clamped (DQ-API-03)
        ({"page_size": 0}, "page_size"),
        ({"page": 0}, "page"),
        ({"page": "one"}, "page"),
        ({"category": "potholes"}, "category"),
        ({"priority": "urgent"}, "priority"),
        ({"status": "closed"}, "status"),
    ],
)
def test_list_answers_400_naming_the_invalid_query_parameter(
    client: TestClient, params: dict[str, object], field: str
) -> None:
    response = client.get("/api/complaints", params=params)  # type: ignore[arg-type]

    assert response.status_code == 400
    assert field in {detail["field"] for detail in _error(response)["details"]}


# ---- PATCH /api/complaints/{id}/status ------------------------------------


def _patch(client: TestClient, complaint_id: str, status: object) -> Any:
    return client.patch(f"/api/complaints/{complaint_id}/status", json={"status": status})


def test_patch_applies_an_allowed_transition_and_returns_the_updated_complaint(
    client: TestClient,
) -> None:
    created = _create(client)

    response = _patch(client, created["id"], "in_progress")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress" and body["id"] == created["id"]
    assert client.get(f"/api/complaints/{created['id']}").json()["status"] == "in_progress"


@pytest.mark.parametrize(
    ("path", "target"),
    [
        (["in_progress"], "open"),
        ([], "resolved"),  # open -> resolved
        (["in_progress", "resolved"], "in_progress"),
        (["in_progress", "resolved"], "open"),
        (["rejected"], "in_progress"),
        ([], "open"),  # the same status
    ],
)
def test_patch_answers_409_naming_the_attempted_transition(
    client: TestClient, path: list[str], target: str
) -> None:
    created = _create(client)
    current = "open"
    for step in path:
        assert _patch(client, created["id"], step).status_code == 200
        current = step

    response = _patch(client, created["id"], target)

    assert response.status_code == 409
    error = _error(response)
    assert error["code"] == "invalid_transition"
    assert error["message"] == f"Cannot change status from {current} to {target}"
    assert error["details"] == [{"from": current, "to": target}]
    assert client.get(f"/api/complaints/{created['id']}").json()["status"] == current


def test_patch_with_an_unknown_status_value_is_a_400_not_a_409(client: TestClient) -> None:
    created = _create(client)

    response = _patch(client, created["id"], "archived")

    assert response.status_code == 400
    assert "status" in {detail["field"] for detail in _error(response)["details"]}


def test_patch_without_a_body_or_with_a_wrong_type_is_a_400(client: TestClient) -> None:
    created = _create(client)

    assert client.patch(f"/api/complaints/{created['id']}/status", json={}).status_code == 400
    assert _patch(client, created["id"], 5).status_code == 400


@pytest.mark.parametrize("bad_id", [str(uuid.uuid4()), "not-a-uuid"])
def test_patch_answers_404_for_an_unknown_or_malformed_id(client: TestClient, bad_id: str) -> None:
    response = _patch(client, bad_id, "in_progress")

    assert response.status_code == 404
    assert _error(response)["code"] == "not_found"


def test_every_status_change_is_one_committed_transaction(
    client: TestClient, unit_of_work: FakeUnitOfWork
) -> None:
    created = _create(client)
    before = unit_of_work.commits

    _patch(client, created["id"], "in_progress")
    _patch(client, created["id"], "open")  # refused

    assert unit_of_work.commits == before + 1
    assert unit_of_work.rollbacks == 1


# ---- errors outside the complaint routes ----------------------------------


def test_an_unknown_route_and_a_wrong_method_use_the_same_error_model(client: TestClient) -> None:
    unknown = client.get("/api/nothing-here")
    wrong_method = client.delete(f"/api/complaints/{uuid.uuid4()}")

    assert unknown.status_code == 404
    assert _error(unknown) == {"code": "not_found", "message": "Not found"}
    assert wrong_method.status_code == 405
    assert _error(wrong_method)["code"] == "method_not_allowed"


def test_errors_carry_the_request_id_of_the_request(client: TestClient) -> None:
    response = client.get("/api/complaints/not-a-uuid", headers={"X-Request-ID": "trace-9"})

    assert response.status_code == 404
    assert response.headers["X-Request-ID"] == "trace-9"


def test_the_openapi_document_names_the_error_responses_and_the_status_codes(
    client: TestClient,
) -> None:
    schema = client.get("/openapi.json").json()

    post = schema["paths"]["/api/complaints"]["post"]
    patch = schema["paths"]["/api/complaints/{complaint_id}/status"]["patch"]
    assert {"201", "400", "429"} <= set(post["responses"])
    assert {"200", "400", "404", "409"} <= set(patch["responses"])
    assert "ErrorResponse" in schema["components"]["schemas"]
    assert Status.OPEN.value in schema["components"]["schemas"]["Status"]["enum"]

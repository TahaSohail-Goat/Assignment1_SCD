"""The contract of assignment section 2.2 (ASG-FR-036): every endpoint, its status codes, and the
agreement between the backend's OpenAPI document and the frontend's typed-client snapshot
(ASG-FR-013).

The nine operations of the API table are: POST and GET /api/complaints, GET
/api/complaints/{id}, PATCH /api/complaints/{id}/status, GET /api/stats,
GET /api/meta/providers, GET /health, GET /ready and GET /metrics.
"""

import json
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.openapi import build_schema
from tests.conftest import FakeProbe
from tests.fakes import FakeCache, FakeUnitOfWork, StubTriager

REPOSITORY = Path(__file__).resolve().parents[2]
DESIGN_SNAPSHOT = REPOSITORY / "frontend" / "src" / "api" / "design.openapi.json"

CONTRACT: dict[tuple[str, str], set[str]] = {  # (method, path) -> status codes the API declares
    ("post", "/api/complaints"): {"201", "400", "429"},
    ("get", "/api/complaints"): {"200", "400"},
    ("get", "/api/complaints/{id}"): {"200", "404"},
    ("patch", "/api/complaints/{id}/status"): {"200", "400", "404", "409"},
    ("get", "/api/stats"): {"200"},
    ("get", "/api/meta/providers"): {"200"},
    ("get", "/health"): {"200"},
    ("get", "/ready"): {"200", "503"},
    ("get", "/metrics"): {"200"},
}
NOT_YET_IMPLEMENTED = {
    ("get", "/api/meta/providers")
}  # issue #46 adds it; the test then enforces it

VALID = {"text": "The street light on our lane has been out for a week.", "location": "Lane 3"}


@pytest.fixture
def schema() -> dict[str, Any]:
    return build_schema()


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    app = create_app(
        settings,
        probes=[FakeProbe("postgres"), FakeProbe("redis")],
        triager=StubTriager(),
        unit_of_work=FakeUnitOfWork(),
        cache=FakeCache(),
    )
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


# ---- the OpenAPI document ----------------------------------------------------


@pytest.mark.parametrize(("method", "path"), sorted(CONTRACT))
def test_each_endpoint_of_the_contract_declares_its_status_codes(
    schema: dict[str, Any], method: str, path: str
) -> None:
    if (method, path) in NOT_YET_IMPLEMENTED and path not in schema["paths"]:
        pytest.skip("GET /api/meta/providers arrives with issue #46")

    declared = set(schema["paths"][path][method]["responses"])

    assert declared == CONTRACT[(method, path)]


def test_the_document_declares_no_422_because_validation_errors_are_400(
    schema: dict[str, Any],
) -> None:
    every_status = {
        code
        for operations in schema["paths"].values()
        for operation in operations.values()
        for code in operation["responses"]
    }

    assert "422" not in every_status
    assert "HTTPValidationError" not in schema["components"]["schemas"]


def test_nothing_outside_the_contract_is_exposed(schema: dict[str, Any]) -> None:
    exposed = {(m, p) for p, ops in schema["paths"].items() for m in ops}

    assert exposed <= set(CONTRACT)


# ---- behaviour, one call per endpoint --------------------------------------------


def test_every_implemented_endpoint_answers_with_the_status_the_assignment_states(
    client: TestClient,
) -> None:
    created = client.post("/api/complaints", json=VALID)
    complaint_id = created.json()["id"]

    answers = {
        "POST /api/complaints": created.status_code,
        "POST /api/complaints (invalid)": client.post("/api/complaints", json={}).status_code,
        "GET /api/complaints": client.get("/api/complaints").status_code,
        "GET /api/complaints/{id}": client.get(f"/api/complaints/{complaint_id}").status_code,
        "GET /api/complaints/{id} (unknown)": client.get(
            f"/api/complaints/{uuid.uuid4()}"
        ).status_code,
        "PATCH status": client.patch(
            f"/api/complaints/{complaint_id}/status", json={"status": "in_progress"}
        ).status_code,
        "PATCH status (invalid transition)": client.patch(
            f"/api/complaints/{complaint_id}/status", json={"status": "open"}
        ).status_code,
        "GET /api/stats": client.get("/api/stats").status_code,
        "GET /health": client.get("/health").status_code,
        "GET /ready": client.get("/ready").status_code,
        "GET /metrics": client.get("/metrics").status_code,
    }

    assert answers == {
        "POST /api/complaints": 201,
        "POST /api/complaints (invalid)": 400,
        "GET /api/complaints": 200,
        "GET /api/complaints/{id}": 200,
        "GET /api/complaints/{id} (unknown)": 404,
        "PATCH status": 200,
        "PATCH status (invalid transition)": 409,
        "GET /api/stats": 200,
        "GET /health": 200,
        "GET /ready": 200,
        "GET /metrics": 200,
    }


def test_ready_answers_503_when_a_dependency_is_down(settings: Settings) -> None:
    down = FakeProbe("redis", error=ConnectionError("down"))
    app = create_app(
        settings,
        probes=[FakeProbe("postgres"), down],
        triager=StubTriager(),
        unit_of_work=FakeUnitOfWork(),
        cache=FakeCache(),
    )
    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["error"]["details"] == [
        {"dependency": "redis", "message": "unreachable"}
    ]


def test_the_stats_header_and_the_metrics_content_type(client: TestClient) -> None:
    assert client.get("/api/stats").headers["X-Cache"] in {"HIT", "MISS"}
    assert client.get("/metrics").headers["content-type"].startswith("text/plain")


# ---- agreement with the frontend's typed-client snapshot (ASG-FR-013) ----------------


@pytest.fixture
def snapshot() -> dict[str, Any]:
    if not DESIGN_SNAPSHOT.exists():
        pytest.skip("the frontend snapshot is not part of this checkout")
    data: dict[str, Any] = json.loads(DESIGN_SNAPSHOT.read_text(encoding="utf-8"))
    return data


def _properties(schema: dict[str, Any], name: str) -> set[str]:
    return set(schema["components"]["schemas"][name]["properties"])


def _required(schema: dict[str, Any], name: str) -> set[str]:
    return set(schema["components"]["schemas"][name].get("required", []))


def test_the_backend_and_the_snapshot_expose_the_same_operations(
    schema: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    backend = {(m, p) for p, ops in schema["paths"].items() for m in ops}
    frontend = {(m, p) for p, ops in snapshot["paths"].items() for m in ops}

    assert frontend - backend <= NOT_YET_IMPLEMENTED
    assert (backend & set(CONTRACT)) - frontend == {
        ("get", "/health"),
        ("get", "/ready"),
        ("get", "/metrics"),
    }  # the probes and the metrics are not used by the browser client


@pytest.mark.parametrize(
    "name", ["Complaint", "ComplaintCreate", "ComplaintPage", "StatusUpdate", "Stats"]
)
def test_each_shared_schema_has_the_same_fields_and_required_fields(
    schema: dict[str, Any], snapshot: dict[str, Any], name: str
) -> None:
    assert _properties(schema, name) == _properties(snapshot, name)
    assert _required(schema, name) == _required(snapshot, name)


def test_the_error_model_matches_the_snapshot(
    schema: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    backend = schema["components"]["schemas"]["ErrorDetail"]
    frontend = snapshot["components"]["schemas"]["ApiError"]["properties"]["error"]

    assert set(backend["properties"]) == set(frontend["properties"])
    assert set(backend["required"]) == set(frontend["required"])


def test_the_enums_and_the_list_parameters_match_the_snapshot(
    schema: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    for name in ("Category", "Priority", "Status"):
        assert (
            schema["components"]["schemas"][name]["enum"]
            == snapshot["components"]["schemas"][name]["enum"]
        )

    def names(document: dict[str, Any]) -> set[str]:
        parameters = document["paths"]["/api/complaints"]["get"]["parameters"]
        return {p["name"] for p in parameters}

    assert names(schema) == names(snapshot)

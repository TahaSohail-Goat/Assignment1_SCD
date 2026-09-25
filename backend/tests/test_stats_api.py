"""GET /api/stats over HTTP: the X-Cache header on every response, HIT and MISS, invalidation."""

import uuid
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe
from tests.fakes import FakeCache, FakeUnitOfWork, StubTriager

VALID = {"text": "The street light on our lane has been out for a week.", "location": "Lane 3"}


@pytest.fixture
def cache() -> FakeCache:
    return FakeCache()


@pytest.fixture
def client(settings: Settings, cache: FakeCache) -> Iterator[TestClient]:
    app = create_app(
        settings,
        probes=[FakeProbe("postgres"), FakeProbe("redis")],
        triager=StubTriager(),
        unit_of_work=FakeUnitOfWork(),
        cache=cache,
    )
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def test_first_call_miss_second_call_hit_with_an_identical_body(client: TestClient) -> None:
    first = client.get("/api/stats")
    second = client.get("/api/stats")

    assert (first.headers["X-Cache"], second.headers["X-Cache"]) == ("MISS", "HIT")
    assert first.json() == second.json()
    assert first.status_code == second.status_code == 200


def test_the_body_has_the_designed_shape_with_every_enum_value(client: TestClient) -> None:
    body = client.get("/api/stats").json()

    assert set(body) == {"total", "by_category", "by_priority"}
    assert set(body["by_category"]) == {
        "water",
        "electricity",
        "sanitation",
        "roads",
        "streetlights",
        "other",
    }
    assert set(body["by_priority"]) == {"high", "normal", "low"}


def test_after_a_post_the_next_call_is_a_miss_that_includes_the_new_complaint(
    client: TestClient,
) -> None:
    client.get("/api/stats")
    assert client.get("/api/stats").headers["X-Cache"] == "HIT"

    assert client.post("/api/complaints", json=VALID).status_code == 201
    after = client.get("/api/stats")

    assert after.headers["X-Cache"] == "MISS"
    assert after.json()["total"] == 1
    assert after.json()["by_category"]["water"] == 1  # the stub triager decides "water"


def test_a_rejected_post_does_not_invalidate_the_cache(client: TestClient) -> None:
    client.get("/api/stats")

    client.post("/api/complaints", json={**VALID, "text": "short"})  # 400

    assert client.get("/api/stats").headers["X-Cache"] == "HIT"


def test_a_status_change_leaves_the_cache_alone(client: TestClient) -> None:
    created = client.post("/api/complaints", json=VALID).json()
    client.get("/api/stats")

    client.patch(f"/api/complaints/{created['id']}/status", json={"status": "in_progress"})

    assert client.get("/api/stats").headers["X-Cache"] == "HIT"


def test_the_ttl_expiry_is_a_miss_again(client: TestClient, cache: FakeCache) -> None:
    client.get("/api/stats")
    cache.advance(30.1)

    assert client.get("/api/stats").headers["X-Cache"] == "MISS"


def test_with_redis_down_stats_still_answer_200_as_a_miss(
    client: TestClient, cache: FakeCache
) -> None:
    client.post("/api/complaints", json=VALID)
    cache.down = True

    response = client.get("/api/stats")

    assert response.status_code == 200
    assert response.headers["X-Cache"] == "MISS"
    assert response.json()["total"] == 1


def test_the_header_is_present_and_valid_on_every_stats_response(
    client: TestClient, cache: FakeCache
) -> None:
    seen = []
    for step in range(6):
        if step == 2:
            client.post("/api/complaints", json=VALID)
        if step == 4:
            cache.advance(31)
        seen.append(client.get("/api/stats").headers.get("X-Cache"))

    assert all(value in {"HIT", "MISS"} for value in seen)
    assert seen == ["MISS", "HIT", "MISS", "HIT", "MISS", "HIT"]


def test_the_error_model_still_applies_to_unknown_stats_paths(client: TestClient) -> None:
    response = client.get(f"/api/stats/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"

"""Shared Redis admission and the observable 429 response."""

import fakeredis
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.providers.cache import CacheUnavailableError, RedisCache
from app.rate_limit_middleware import client_ip
from app.services.rate_limit import RateLimitService
from tests.conftest import FakeProbe
from tests.fakes import FakeUnitOfWork, StubTriager

VALID = {"text": "The street light has been broken for several days.", "location": "Ward 2"}


class FakeCounter:
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def increment_with_ttl(self, key: str, ttl_seconds: int) -> int:
        assert ttl_seconds == 60
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]


def test_fixed_window_resets_and_clients_have_separate_keys() -> None:
    now = [0.0]
    service = RateLimitService(FakeCounter(), limit=2, window_seconds=60, clock=lambda: now[0])
    assert service.check("192.0.2.1").allowed
    assert service.check("192.0.2.1").allowed
    third = service.check("192.0.2.1")
    assert not third.allowed and third.retry_after == 60
    assert service.check("192.0.2.2").allowed
    now[0] = 60.0
    assert service.check("192.0.2.1").allowed


def test_redis_outage_fails_open() -> None:
    class BrokenCounter:
        def increment_with_ttl(self, key: str, ttl_seconds: int) -> int:
            raise CacheUnavailableError("connection down")

    assert RateLimitService(BrokenCounter()).check("192.0.2.1").allowed


def test_two_app_instances_share_the_same_redis_limit(settings: Settings) -> None:
    server = fakeredis.FakeServer()
    settings = settings.model_copy(update={"rate_limit_requests": 2})

    def application() -> object:
        cache = RedisCache(client=fakeredis.FakeRedis(server=server, decode_responses=True))
        return create_app(
            settings,
            probes=[FakeProbe("postgres"), FakeProbe("redis")],
            triager=StubTriager(),
            unit_of_work=FakeUnitOfWork(),
            cache=cache,
        )

    with TestClient(application()) as first, TestClient(application()) as second:
        assert first.post("/api/complaints", json=VALID).status_code == 201
        assert second.post("/api/complaints", json=VALID).status_code == 201
        denied = first.post("/api/complaints", json=VALID)
        denied_before_validation = second.post("/api/complaints", json={})
        unaffected_get = first.get("/api/complaints")

    assert denied.status_code == 429
    assert denied_before_validation.status_code == 429
    assert unaffected_get.status_code == 200
    assert denied.json()["error"]["code"] == "rate_limited"
    assert int(denied.headers["Retry-After"]) > 0
    assert denied.headers["X-Request-ID"]


def test_forwarded_ip_is_used_only_when_trusted_and_valid() -> None:
    scope = {
        "type": "http",
        "client": ("192.0.2.1", 1234),
        "headers": [(b"x-forwarded-for", b"198.51.100.4, 203.0.113.7")],
    }
    assert client_ip(scope, False) == "192.0.2.1"  # type: ignore[arg-type]
    assert client_ip(scope, True) == "198.51.100.4"  # type: ignore[arg-type]
    scope["headers"] = [(b"x-forwarded-for", b"invalid")]
    assert client_ip(scope, True) == "192.0.2.1"  # type: ignore[arg-type]

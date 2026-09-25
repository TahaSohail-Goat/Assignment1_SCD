"""The Redis cache provider, against an in-memory Redis (fakeredis): TTL, get, delete, outage."""

import fakeredis
import pytest
import redis

from app.providers.cache import CacheUnavailableError, RedisCache


@pytest.fixture
def client() -> "fakeredis.FakeRedis":
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def cache(client: "fakeredis.FakeRedis") -> RedisCache:
    return RedisCache(client=client)


def test_set_stores_the_value_with_the_given_ttl(
    cache: RedisCache, client: "fakeredis.FakeRedis"
) -> None:
    cache.set("stats:v1", "{}", 30)

    assert cache.get("stats:v1") == "{}"
    assert client.ttl("stats:v1") == 30


def test_a_missing_key_is_none(cache: RedisCache) -> None:
    assert cache.get("absent") is None


def test_delete_removes_the_key_and_is_harmless_when_absent(cache: RedisCache) -> None:
    cache.set("k", "v", 30)

    cache.delete("k")
    cache.delete("k")

    assert cache.get("k") is None


def test_the_probe_answers_ping(cache: RedisCache) -> None:
    cache.check()  # no exception


def test_an_outage_is_reported_as_one_error_type_for_every_operation() -> None:
    server = fakeredis.FakeServer()
    server.connected = False
    cache = RedisCache(client=fakeredis.FakeRedis(server=server, decode_responses=True))

    with pytest.raises(CacheUnavailableError):
        cache.get("k")
    with pytest.raises(CacheUnavailableError):
        cache.set("k", "v", 30)
    with pytest.raises(CacheUnavailableError):
        cache.delete("k")
    with pytest.raises(redis.RedisError):  # the probe keeps the library's own error
        cache.check()


def test_a_client_is_built_from_the_url_when_none_is_given() -> None:
    cache = RedisCache("redis://redis:6379/0", timeout_seconds=0.5)

    assert cache.client.connection_pool.connection_kwargs["host"] == "redis"
    cache.close()

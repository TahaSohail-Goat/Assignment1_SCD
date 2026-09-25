"""Redis behind an interface: a key-value cache with a TTL, and the reachability probe.

Services depend on the ``KeyValueCache`` protocol and on ``CacheUnavailableError``, never on
the Redis library, so a Redis outage is one error type they can handle (DQ-API-15).
"""

from typing import Protocol, cast

import redis


class CacheUnavailableError(Exception):
    """Redis did not answer (connection refused, timeout, protocol error)."""


class KeyValueCache(Protocol):
    def get(self, key: str) -> str | None: ...

    def set(self, key: str, value: str, ttl_seconds: int) -> None: ...

    def delete(self, key: str) -> None: ...


class RedisCache:
    name = "redis"

    def __init__(
        self,
        url: str = "",
        timeout_seconds: float = 1.0,
        client: redis.Redis | None = None,
    ) -> None:
        """``client`` lets tests pass an in-memory Redis; otherwise one is built from ``url``."""
        self.client: redis.Redis = client or redis.Redis.from_url(
            url,
            socket_connect_timeout=timeout_seconds,
            socket_timeout=timeout_seconds,
            decode_responses=True,
        )

    def check(self) -> None:
        """Raise if Redis does not answer PING."""
        self.client.ping()

    def get(self, key: str) -> str | None:
        try:
            return cast("str | None", self.client.get(key))
        except redis.RedisError as error:
            raise CacheUnavailableError(type(error).__name__) from error

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        try:
            self.client.set(key, value, ex=ttl_seconds)
        except redis.RedisError as error:
            raise CacheUnavailableError(type(error).__name__) from error

    def delete(self, key: str) -> None:
        try:
            self.client.delete(key)
        except redis.RedisError as error:
            raise CacheUnavailableError(type(error).__name__) from error

    def close(self) -> None:
        self.client.close()

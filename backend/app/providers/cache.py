"""Redis connection and its reachability probe."""

import redis


class RedisCache:
    name = "redis"

    def __init__(self, url: str, timeout_seconds: float = 1.0) -> None:
        self.client: redis.Redis = redis.Redis.from_url(
            url,
            socket_connect_timeout=timeout_seconds,
            socket_timeout=timeout_seconds,
        )

    def check(self) -> None:
        """Raise if Redis does not answer PING."""
        self.client.ping()

    def close(self) -> None:
        self.client.close()

"""Redis cache for validated triage results (ASG-AI-016).

The cache never stores the raw complaint in its key. The caller supplies its
Pydantic model's validation and serialization functions, so even cached data
must pass the same schema as a fresh provider response.
"""

import hashlib
import json
import logging
from collections.abc import Callable, Mapping
from typing import TypeVar

from app.providers.cache import KeyValueCache
from app.providers.triage.base import MalformedOutputError

logger = logging.getLogger("app.triage_cache")

TTL_SECONDS = 24 * 60 * 60
_PREFIX = "triage:v1:"
T = TypeVar("T")


def content_key(text: str, location: str) -> str:
    """Hash both provider inputs; separators prevent ambiguous concatenation."""
    payload = json.dumps([text, location], ensure_ascii=False, separators=(",", ":"))
    return _PREFIX + hashlib.sha256(payload.encode("utf-8")).hexdigest()


class TriageCache:
    def __init__(self, store: KeyValueCache) -> None:
        self._store = store

    def get(
        self, text: str, location: str, validate: Callable[[object], T]
    ) -> tuple[T, str] | None:
        key = content_key(text, location)
        try:
            raw = self._store.get(key)
        except Exception as error:
            logger.warning("triage cache read failed", extra={"error_class": type(error).__name__})
            return None
        if raw is None:
            return None
        try:
            entry = json.loads(raw)
            if not isinstance(entry, dict) or not isinstance(entry.get("provider"), str):
                raise ValueError("invalid cache envelope")
            return validate(entry["result"]), entry["provider"]
        except (ValueError, KeyError, TypeError, MalformedOutputError) as error:
            logger.warning(
                "invalid triage cache entry", extra={"error_class": type(error).__name__}
            )
            try:
                self._store.delete(key)
            except Exception as delete_error:
                logger.warning(
                    "triage cache cleanup failed",
                    extra={"error_class": type(delete_error).__name__},
                )
            return None

    def put(
        self,
        text: str,
        location: str,
        result: T,
        provider: str,
        serialize: Callable[[T], Mapping[str, object]],
    ) -> None:
        key = content_key(text, location)
        entry = json.dumps(
            {"provider": provider, "result": serialize(result)},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        try:
            self._store.set(key, entry, TTL_SECONDS)
        except Exception as error:
            logger.warning("triage cache write failed", extra={"error_class": type(error).__name__})

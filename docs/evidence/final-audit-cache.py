"""Run via docker compose exec -T backend python - < this file (bash).

PowerShell: Get-Content -Raw docs/evidence/final-audit-cache.py |
    docker compose exec -T backend python -
Uses real Redis and rules triage, no hosted provider or database writes.
"""

import json
import os
import uuid
from datetime import datetime, timezone

from app.providers.cache import RedisCache
from app.providers.triage.rules import RuleBasedTriage
from app.services.triage import TriageService
from app.services.triage_cache import TriageCache, content_key


class CountingRules(RuleBasedTriage):
    calls = 0

    def triage(self, text, location):
        self.calls += 1
        return super().triage(text, location)


class CountingCache(TriageCache):
    hits = 0
    misses = 0

    def get(self, *args):
        result = super().get(*args)
        if result is None:
            self.misses += 1
        else:
            self.hits += 1
        return result


store = RedisCache(os.environ["REDIS_URL"])
provider = CountingRules()
cache = CountingCache(store)
service = TriageService(provider, cache=cache)
text = "Small pothole needs repair. Synthetic audit " + uuid.uuid4().hex
location = "Synthetic audit ward"
key = content_key(text, location, provider.name)
try:
    assert store.get(key) is None, "unique audit key unexpectedly exists"
    first = service.triage(text, location, uuid.uuid4())
    second = service.triage(text, location, uuid.uuid4())
    ttl = store.client.ttl(key)
    assert (cache.hits, cache.misses, provider.calls) == (1, 1, 1)
    assert 86390 <= ttl <= 86400
    assert (first.category, first.priority, first.ai_summary) == (
        second.category, second.priority, second.ai_summary
    )
    print(json.dumps({
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "redis_version": store.client.info("server")["redis_version"],
        "provider": provider.name, "requests": 2, "hits": cache.hits,
        "misses": cache.misses, "provider_calls": provider.calls,
        "hit_rate": cache.hits / (cache.hits + cache.misses),
        "ttl_seconds": ttl, "category": first.category.value,
        "priority": first.priority.value, "first_latency_ms": first.latency_ms,
        "second_latency_ms": second.latency_ms,
        "scope": "two-request synthetic service-level run against real Redis; not hosted/offline comparison",
    }, indent=2))
finally:
    store.delete(key)  # delete only this invocation's unique synthetic entry
    service.close()
    store.close()

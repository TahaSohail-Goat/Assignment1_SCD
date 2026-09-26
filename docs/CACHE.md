# Cache Layer

Redis 7 does **two different jobs**, deliberately (assignment §2.4 p8): a read-through cache for `/api/stats` (Job 1, below) and a distributed rate limiter for `POST /api/complaints` (Job 2, written by issue #43). Redis is reached only through `backend/app/providers/cache.py`; the services depend on the `KeyValueCache` protocol and on one error type, `CacheUnavailableError`.

## Job 1 — the statistics cache (`ASG-FR-029`, `ASG-CACHE-002…006`)

| Aspect | Decision |
|---|---|
| Key | one key, `stats:v1`: the statistics are global (counts over all complaints), so there is nothing to key by. The `v1` is the version of the cached JSON shape; a change of shape changes the key, so an old entry is never misread. |
| Value | the response body as JSON (`total`, `by_category`, `by_priority`, every enum value present, 0 when empty) |
| TTL | **30 seconds** (`ASG-CACHE-003`), set with `SET … EX 30`; a test checks the TTL Redis reports |
| Read path | read-through: hit → the cached body and `X-Cache: HIT`; miss → aggregate from PostgreSQL, store, answer with `X-Cache: MISS` (`ASG-CACHE-002`, `ASG-CACHE-004`) |
| Invalidation | on write: a new complaint deletes the key **after its transaction has committed** (`ASG-CACHE-005`), so the next call is a miss that already counts it. A status change does **not** invalidate: the counts by category and priority do not change (`docs/API_DESIGN.md` DQ-API-07) |
| Failure | Redis unreachable: the answer is computed from PostgreSQL as a `MISS` and one WARNING is logged; a failed invalidation is logged and never fails the request (`docs/API_DESIGN.md` DQ-API-15) |
| Observability | `stats_cache_total{result="hit\|miss"}` on `/metrics` |

### Why the TTL **and** explicit invalidation (`ASG-CACHE-006`)

Either alone looks sufficient, and each alone is wrong:

- **Invalidation alone** gives fresh data after a write, but only while every invalidation succeeds and arrives in the right order. It is *lost* when Redis is unreachable at the moment of the write. It also *races*: a reader that missed and read the counts just before a commit can store its old result just after the writer deleted the key, and that stale entry would then live forever. The tests reproduce the lost case (`test_the_ttl_covers_a_lost_invalidation`).
- **TTL alone** always ends the staleness, but a citizen who has just submitted a complaint would see the statistics wrong for up to 30 seconds — the assignment asks for the new complaint to appear immediately.

Together: invalidation gives freshness in the normal case, and the TTL is the upper bound (30 seconds) on how wrong the cache can ever be. The delete happens after the commit because deleting before it would let a concurrent reader re-cache the pre-commit counts.

### Evidence

`backend/tests/test_stats_service.py` (first call MISS, second HIT with an identical body; a new complaint makes the next call a MISS that counts it; expiry at 30 seconds tested with a clock moved by hand, without sleeping; Redis down), `backend/tests/test_stats_api.py` (the header on every response), `backend/tests/test_redis_cache.py` (the TTL against an in-memory Redis). The behaviour against a real Redis 7 container is part of the Compose evidence (Phase 08/11).

## Job 2 — the distributed rate limiter (`ASG-FR-022`, `ASG-CACHE-007…010`)

`RateLimitService` uses a fixed 60-second window, with a default allowance of 10 POSTs per client IP. Both values are configurable by `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS`. The Redis key contains a SHA-256 digest of the IP and the window number, so it does not expose a readable address. A Redis `MULTI/EXEC` transaction performs `INCR` and `EXPIRE` together. All backend replicas see the same count; a process-local counter would reset on every restart and split the allowance across HPA pods.

Only `POST /api/complaints` is checked, before FastAPI validates the body. A request beyond the limit receives the shared 429 error body and a positive `Retry-After` value equal to the remaining seconds in the current window. `GET` and `PATCH` are unaffected. The default client address is the socket peer; only when `TRUST_FORWARDED_FOR=true` behind the trusted Ingress does the first valid `X-Forwarded-For` address replace it. Do not enable that setting for a directly exposed backend, because a caller could forge the header. If Redis is unavailable, the request is admitted and one WARNING is logged for that request (DQ-API-15).

`backend/tests/test_rate_limit.py` checks the window reset, 429 and header, Redis-down path, and two app instances sharing one fakeredis server. A real Redis 7 multi-replica run remains deployment evidence.

## Redis persistence (AOF) and the volume (`ASG-CACHE-011…012`)

`compose.yaml` runs Redis with `--appendonly yes --appendfsync everysec` and mounts the named `redisdata` volume at `/data`. Aggregate stats and triage results can be recomputed, but doing so immediately after a restart creates avoidable database and provider load. More importantly, losing the rate counters would reopen every client's allowance at once and permit a burst against the free hosted provider. The AOF and volume keep recent cache entries and counters across an ordinary container restart. With `appendfsync everysec`, the last second of acknowledged writes may still be lost on a crash; this is a bounded operational trade-off, not a claim of perfect durability.

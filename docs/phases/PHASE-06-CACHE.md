# Phase 06 — Cache, Rate Limiting & Reliability

## Read
- assignment cache section
- CACHE
- NFRs
- BACKEND
- AI

## Implement
Redis 7 must serve two roles:

1. `/api/stats` read-through cache:
   - TTL 30s
   - `X-Cache: HIT|MISS`
   - invalidate on write

2. Distributed complaint POST limiter:
   - IP keyed
   - 429
   - Retry-After
   - works across multiple backend replicas

Enable Redis AOF on a named volume and justify the design.

Add failure-path tests and document cache consistency and rate-limiter behavior.

## Gate
Cache behavior and limiter are demonstrated, not merely implemented.

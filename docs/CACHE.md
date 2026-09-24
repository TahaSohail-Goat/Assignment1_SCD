# Cache Layer

Two Redis responsibilities:
1. Read-through cache for `/api/stats`, TTL 30 seconds, `X-Cache`, invalidation after writes.
2. Distributed IP-based rate limiter for `POST /api/complaints`.

Document:
- key strategy
- TTL
- invalidation
- consistency
- rate-limit window/bucket design
- `429`
- `Retry-After`
- Redis AOF
- persistence
- failure behavior

# Phase 05 — Data Layer

## Read
- assignment data layer
- DATA_MODEL
- FRs/NFRs
- backend docs

## Implement
PostgreSQL 16 + Alembic.

Required:
- exact minimum complaint schema
- appropriate enum representation
- server-generated UUID
- DB-level text constraints
- timestamps UTC
- required indexes
- index rationale
- migrations only
- no startup DDL
- idempotent seed with ≥30 realistic Urdu-influenced English complaints
- persistence across Compose restart

Do not add schema solely for aesthetic complexity.

## Gate
Migrations, seed, constraints, indexes, persistence, and tests are demonstrable.

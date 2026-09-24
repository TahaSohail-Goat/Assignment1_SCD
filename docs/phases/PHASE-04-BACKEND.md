# Phase 04 — Backend & Domain Layer

## Read
- assignment backend contract
- ARCHITECTURE
- BACKEND
- FRs/NFRs
- DATA_MODEL
- API requirements

## Implement
FastAPI + Pydantic v2 unless the repository already explicitly uses Flask and the exception is documented.

Required layer separation:
- routes
- services
- repositories
- providers

Implement the complete assignment API contract, validation/error model, explicit state machine, health/readiness, metrics, request IDs, structured JSON logs, graceful SIGTERM, and deterministic tests.

Do not place SQL in routes/services.
Do not place business-state transitions in the frontend.

## Gate
All mandatory backend contracts and tests pass.

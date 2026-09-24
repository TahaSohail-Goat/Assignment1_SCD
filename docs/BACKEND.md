# Backend Engineering Contract

Recommended stack:
FastAPI + Pydantic v2.

Required layering:
- `routes/` HTTP only
- `services/` business rules
- `repositories/` SQL/persistence
- `providers/` external integrations

Routes must not:
- contain business state machines
- open DB sessions directly
- call SQL directly.

Document and test:
- request validation
- response contracts
- status codes
- error model
- state machine
- logging
- request IDs
- graceful shutdown
- health/readiness
- metrics.

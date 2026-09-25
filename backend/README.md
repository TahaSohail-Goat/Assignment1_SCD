# CivicPulse backend

FastAPI + Pydantic v2, four layers (`app/routes`, `app/services`, `app/repositories`, `app/providers`), PostgreSQL 16 through SQLAlchemy and Alembic, Redis 7.

## Run the checks

```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt     # Windows; on Linux: .venv/bin/python
ruff check .
ruff format --check .
mypy
pytest
```

`pytest` runs the whole suite. The tests that need PostgreSQL 16 are skipped unless `TEST_DATABASE_URL` points at a database that may be wiped (the tests drop and recreate its `public` schema), for example `postgresql+psycopg://postgres@127.0.0.1:5433/civicpulse_test`. In CI it is the service container. Coverage on `app/` must stay at or above 65% (`--cov-fail-under` in `pyproject.toml`).

## Migrations

```
DATABASE_URL=postgresql+psycopg://user:password@postgres:5432/civicpulse alembic upgrade head
alembic downgrade base
```

## OpenAPI

```
python -m app.openapi > openapi.json
```

Prints the schema the API really serves (no 422, the one error model). `tests/test_contract.py` compares it with the frontend's typed-client snapshot `frontend/src/api/design.openapi.json`; `npm run check:api-contract` can be pointed at the printed file with `OPENAPI_SCHEMA`.

The schema is described in [`docs/DATA_MODEL.md`](../docs/DATA_MODEL.md); the design of the API in [`docs/API_DESIGN.md`](../docs/API_DESIGN.md).

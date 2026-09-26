"""The OpenAPI document of the API, as the typed client and the contract tests use it.

FastAPI adds a 422 response and two validation schemas to every route by default. This API
answers validation errors with 400 in its own error model (docs/API_DESIGN.md, DQ-API-02),
so those defaults are removed: the document says what the API really does.
"""

import json
import sys
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

_FRAMEWORK_SCHEMAS = ("HTTPValidationError", "ValidationError")


def install_openapi(app: FastAPI) -> None:
    def build() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
        for operations in schema["paths"].values():
            for operation in operations.values():
                operation.get("responses", {}).pop("422", None)
        for name in _FRAMEWORK_SCHEMAS:
            schema.get("components", {}).get("schemas", {}).pop(name, None)
        app.openapi_schema = schema
        return schema

    app.openapi = build  # type: ignore[method-assign]


def build_schema() -> dict[str, Any]:
    """The schema of an app built with placeholder settings; no connection is opened."""
    from app.config import Settings
    from app.main import create_app

    settings = Settings(
        database_url="postgresql+psycopg://placeholder@postgres:5432/civicpulse",
        redis_url="redis://redis:6379/0",
    )
    return create_app(settings).openapi()


if __name__ == "__main__":  # python -m app.openapi > openapi.json
    json.dump(build_schema(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")

"""ASG-NFR-002 to ASG-NFR-007: four layers, and the dependency arrows point one way only.

routes -> services -> repositories / providers. These are checks on the imports of every
module, so a violation fails the build instead of waiting for a review to notice it.
"""

import ast
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"

DATABASE_LIBRARIES = ("sqlalchemy", "psycopg", "alembic")
HTTP_LIBRARIES = ("fastapi", "starlette")


def _imports(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def _modules(package: str) -> list[Path]:
    return sorted((APP / package).glob("*.py"))


def _offenders(package: str, forbidden: tuple[str, ...]) -> list[str]:
    return [
        f"{path.relative_to(APP.parent)} imports {name}"
        for path in _modules(package)
        for name in sorted(_imports(path))
        if any(name == bad or name.startswith(bad + ".") for bad in forbidden)
    ]


def test_routes_neither_open_database_sessions_nor_touch_sql_libraries() -> None:
    forbidden = (
        *DATABASE_LIBRARIES,
        "app.database",
        "app.repositories.uow",
        "app.repositories.models",
        "app.repositories.health",
    )

    assert _offenders("routes", forbidden) == []


def test_services_know_neither_http_nor_sql() -> None:
    assert _offenders("services", (*HTTP_LIBRARIES, *DATABASE_LIBRARIES, "app.routes")) == []


def test_repositories_and_providers_depend_on_nothing_above_them() -> None:
    above = ("app.routes", "app.services", "app.http_errors", "app.middleware", "app.main")

    assert _offenders("repositories", (*HTTP_LIBRARIES, *above)) == []
    assert _offenders("providers", (*HTTP_LIBRARIES, *above, *DATABASE_LIBRARIES)) == []


def test_the_domain_and_the_error_types_are_free_of_frameworks() -> None:
    forbidden = (*HTTP_LIBRARIES, *DATABASE_LIBRARIES, "redis", "pydantic")
    offenders = [
        f"{name}.py imports {imported}"
        for name in ("domain", "errors")
        for imported in sorted(_imports(APP / f"{name}.py"))
        if any(imported == bad or imported.startswith(bad + ".") for bad in forbidden)
    ]

    assert offenders == []

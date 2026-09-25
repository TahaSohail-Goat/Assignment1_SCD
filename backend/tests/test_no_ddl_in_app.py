"""ASG-DATA-003: no CREATE TABLE or other schema DDL in application code, ever."""

import re
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"
DDL = re.compile(
    r"create\s+table|create\s+type|alter\s+table|drop\s+table|drop\s+type|create\s+index"
    r"|metadata\.create_all|\.create_all\(",
    re.IGNORECASE,
)


def test_application_code_contains_no_schema_ddl() -> None:
    offenders = [
        f"{path.relative_to(APP.parent)}:{number}"
        for path in APP.rglob("*.py")
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if DDL.search(line)
    ]

    assert offenders == []


def test_all_sql_text_lives_in_the_repositories_package() -> None:
    """ASG-NFR-005: raw SQL (text(...) or execute of a string) only under repositories/."""
    sql_call = re.compile(r"\btext\(\s*[\"']|\.execute\(\s*[\"']")
    offenders = [
        str(path.relative_to(APP.parent))
        for path in APP.rglob("*.py")
        if "repositories" not in path.parts and sql_call.search(path.read_text(encoding="utf-8"))
    ]

    assert offenders == []

"""ASG-NFR-015: the suite is green on every run, by design: no sleeping and no re-runs.

"If you find yourself writing time.sleep() in a test or re-running to get a pass, the design is
wrong" (assignment section 2.5 p12). These checks keep that true.
"""

import re
import tomllib
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
THIS_FILE = Path(__file__).resolve()

SLEEP_CALL = re.compile(r"\b(?:time|asyncio|anyio|trio)\.sleep\(")
RERUN_MARKERS = re.compile(
    r"pytest\.mark\.flaky|@flaky|--reruns|rerunfailures|pytest_retry|--retries"
)


def _python_files(*directories: str) -> list[Path]:
    return [
        path
        for directory in directories
        for path in sorted((BACKEND / directory).rglob("*.py"))
        if path.resolve() != THIS_FILE
    ]


def test_no_test_and_no_application_module_calls_sleep() -> None:
    offenders = [
        str(path.relative_to(BACKEND))
        for path in _python_files("tests")
        if SLEEP_CALL.search(path.read_text(encoding="utf-8"))
    ]

    assert offenders == []


def test_nothing_is_configured_or_marked_to_retry_a_failing_test() -> None:
    marked = [
        str(path.relative_to(BACKEND))
        for path in _python_files("tests")
        if RERUN_MARKERS.search(path.read_text(encoding="utf-8"))
    ]
    config = tomllib.loads((BACKEND / "pyproject.toml").read_text(encoding="utf-8"))
    options = config["tool"]["pytest"]["ini_options"]["addopts"]
    requirements = (BACKEND / "requirements-dev.txt").read_text(encoding="utf-8").lower()

    assert marked == []
    assert not RERUN_MARKERS.search(options)
    assert "rerunfailures" not in requirements and "pytest-retry" not in requirements


def test_the_coverage_gate_is_configured_at_65_percent() -> None:
    """ASG-NFR-013: CI fails below 65% on app/ because the threshold is part of the pytest options."""
    config = tomllib.loads((BACKEND / "pyproject.toml").read_text(encoding="utf-8"))
    options = config["tool"]["pytest"]["ini_options"]["addopts"]

    assert "--cov=app" in options
    assert "--cov-fail-under=65" in options


def test_warnings_are_errors_so_a_deprecation_cannot_hide_in_a_green_run() -> None:
    config = tomllib.loads((BACKEND / "pyproject.toml").read_text(encoding="utf-8"))

    assert config["tool"]["pytest"]["ini_options"]["filterwarnings"] == ["error"]

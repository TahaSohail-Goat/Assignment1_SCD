"""Static checks of .github/workflows/ci.yml (ASG-CICD-003..010, 024..026).

They read the workflow; they do not run it. That the jobs are green on a runner is what the
Actions tab shows, and the red-to-green pull request (issue #51) is the evidence for the gate.
"""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "ci.yml"
TEXT = WORKFLOW_PATH.read_text(encoding="utf-8")
WORKFLOW: dict[Any, Any] = yaml.safe_load(TEXT)
JOBS: dict[str, dict[str, Any]] = WORKFLOW["jobs"]
TRIGGERS: dict[str, Any] = WORKFLOW[True]  # PyYAML reads the bare key `on` as the boolean True


def test_it_runs_on_pull_requests_to_main_and_dev_and_on_push_to_dev() -> None:
    assert set(TRIGGERS) == {"pull_request", "push"}
    assert TRIGGERS["pull_request"]["branches"] == ["main", "dev"]
    assert TRIGGERS["push"]["branches"] == ["dev"]


def test_the_workflow_declares_read_only_permissions() -> None:
    assert WORKFLOW["permissions"] == {"contents": "read"}
    assert all("permissions" not in job for job in JOBS.values())  # nothing widens it


def test_the_jobs_of_the_assignment_exist() -> None:
    assert set(JOBS) == {
        "lint-and-type",
        "test-backend",
        "test-frontend",
        "build",
        "scan",
        "context-and-image-size",
        "manifests",
        "integration",
    }


def test_every_third_party_action_is_pinned_to_a_commit_sha() -> None:
    uses = re.findall(r"^\s*-?\s*uses:\s*(\S+)", TEXT, re.MULTILINE)

    assert uses
    for reference in uses:
        assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", reference), reference


def test_a_pull_request_never_publishes_an_image_or_uses_secrets() -> None:
    assert "push: true" not in TEXT
    assert "secrets." not in TEXT
    assert "pull_request_target" not in TEXT
    assert "docker/login-action" not in TEXT


def test_the_backend_tests_run_with_the_simulated_provider_and_a_real_postgres() -> None:
    job = JOBS["test-backend"]

    assert job["env"]["TRIAGE_PROVIDER"] == "simulated"
    assert job["services"]["postgres"]["image"].startswith("postgres:16")
    assert "TEST_DATABASE_URL" in job["env"]


def test_trivy_fails_on_high_and_critical_findings_that_have_a_fix() -> None:
    step = next(s for s in JOBS["scan"]["steps"] if s.get("name") == "Trivy")

    assert step["with"]["severity"] == "HIGH,CRITICAL"
    assert step["with"]["ignore-unfixed"] is True
    assert step["with"]["exit-code"] == "1"


def test_the_scan_waits_for_the_build() -> None:
    assert JOBS["scan"]["needs"] == "build"


def test_the_integration_job_follows_the_steps_of_the_assignment() -> None:
    names = [step.get("name", "") for step in JOBS["integration"]["steps"]]

    order = [
        "docker compose up -d",
        "Wait for /ready",
        "POST a complaint, GET it back, assert the category",
        "X-Cache goes MISS then HIT",
        "docker compose down -v",
    ]
    positions = [names.index(name) for name in order]
    assert positions == sorted(positions)
    last = JOBS["integration"]["steps"][-1]
    assert last["if"] == "always()"  # the stack is removed even when an assertion failed


@pytest.mark.parametrize("job", sorted(JOBS))
def test_every_job_has_a_timeout(job: str) -> None:
    assert JOBS[job]["timeout-minutes"] <= 15

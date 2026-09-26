"""The README may only point at things that exist (ASG-GEN-010: every claim can be demonstrated)."""

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
README = (REPOSITORY / "README.md").read_text(encoding="utf-8")


def _relative_targets() -> list[str]:
    targets = re.findall(r"\]\(([^)\s]+)\)", README)
    return [t.split("#")[0] for t in targets if not t.startswith(("http://", "https://", "#"))]


def test_every_relative_link_and_image_in_the_readme_exists() -> None:
    missing = [t for t in _relative_targets() if t and not (REPOSITORY / t).exists()]

    assert missing == []


def test_the_readme_has_what_the_assignment_lists() -> None:
    for heading in ("## The problem", "## Architecture", "## Quickstart", "## API"):
        assert heading in README
    assert "```mermaid" in README
    assert "![" in README  # screenshots
    assert "badge.svg" in README


def test_the_quickstart_command_is_the_one_the_ci_job_runs() -> None:
    assert "cp .env.example .env && docker compose up --build" in README
    assert (REPOSITORY / ".env.example").exists()
    assert "bash scripts/k8s-up.sh" in README
    assert (REPOSITORY / "scripts" / "k8s-up.sh").exists()

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
    for heading in ("## Architecture", "## API", "## Kubernetes"):
        assert heading in README
    assert "screenshots" in README.lower()
    assert "```mermaid" in README
    assert "![" in README  # screenshots
    assert "badge.svg" in README  # badges
    assert "FastAPI" in README  # the backend framework is stated (ASG-DOC-007)


def test_every_endpoint_of_the_api_table_is_in_the_readme() -> None:
    for path in (
        "/api/complaints",
        "/api/complaints/{id}",
        "/api/complaints/{id}/status",
        "/api/stats",
        "/api/meta/providers",
        "/health",
        "/ready",
        "/metrics",
    ):
        assert f"`{path}`" in README


def test_the_quickstart_commands_exist_and_are_the_ones_ci_runs() -> None:
    assert "docker compose up" in README
    assert (REPOSITORY / ".env.example").exists()
    assert "bash scripts/k8s-up.sh" in README
    assert (REPOSITORY / "scripts" / "k8s-up.sh").exists()
    assert (REPOSITORY / "LICENSE").exists()


def test_the_readme_links_the_uploaded_demo_and_discloses_audit_limits() -> None:
    assert "https://youtu.be/bExMGzoHYow" in README
    assert "https://drive.google.com/file/d/1uNGCvKnzy_vpxxolNp6qQp8R4ht3Ip58/view" in README
    assert "docs/evidence/submission-final-README.md" in README
    assert "docs/FINAL_SUBMISSION_CHECKLIST.md" in README
    assert "historical rubric caveats" in README.lower()

"""Submission checks use the chosen history and detect deleted credential fixtures."""

import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/check_submission.py"


def load_checker(root):
    spec = importlib.util.spec_from_file_location("submission_checker", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = root
    module.results.clear()
    return module


def git(root, *args, author="Artfever"):
    env = dict(os.environ, GIT_AUTHOR_NAME=author, GIT_COMMITTER_NAME=author,
               GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_EMAIL="fixture@example.invalid")
    return subprocess.run(  # noqa: S603
        [shutil.which("git"), "-c", "commit.gpgsign=false", *args], cwd=root, env=env,
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def test_share_uses_selected_ref_not_unmerged_branch(tmp_path):
    git(tmp_path, "init")
    for _ in range(7):
        git(tmp_path, "commit", "--allow-empty", "-m", "fixture", author="Taha Sohail")
    for _ in range(3):
        git(tmp_path, "commit", "--allow-empty", "-m", "fixture")
    selected = git(tmp_path, "rev-parse", "HEAD")
    for _ in range(4):
        git(tmp_path, "commit", "--allow-empty", "-m", "unmerged fixture")
    checker = load_checker(tmp_path)
    checker.check_authorship(selected)
    assert checker.results[-1][0] == checker.FAIL
    assert "3/10" in checker.results[-1][2]
    checker.check_authorship("HEAD")
    assert checker.results[-1][0] == checker.PASS
    checker.check_authorship("missing-ref")
    assert checker.results[-1][0] == checker.FAIL


@pytest.mark.parametrize("path", ["docs/removed.md", "backend/tests/removed.py"])
def test_history_scan_detects_deleted_secret_in_documentation_and_tests(tmp_path, path):
    git(tmp_path, "init")
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    # Synthetic fixture assembled at runtime, never a credential stored in this repository.
    marker = "gsk_" + "x" * 30
    target.write_text(marker)
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "fixture")
    target.unlink()
    git(tmp_path, "add", "-u")
    git(tmp_path, "commit", "-m", "remove fixture")
    checker = load_checker(tmp_path)
    checker.FILES = []
    checker.check_secrets()
    history = [row for row in checker.results if "all tracked paths" in row[1]]
    assert history[0][0] == checker.FAIL
    assert marker not in str(checker.results)


def test_checklist_requires_unique_status_for_every_requirement(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "ASSIGNMENT_TRACEABILITY.md").write_text("| ASG-K8S-005 | requirement |\n")
    checker = load_checker(tmp_path)
    checker.check_documents()
    assert checker.results[0][0] == checker.FAIL
    checklist = docs / "FINAL_SUBMISSION_CHECKLIST.md"
    checklist.write_text("| ASG-K8S-005 | BLOCKED | waiting |\n")
    checker.results.clear()
    checker.check_documents()
    assert checker.results[0][0] == checker.PASS  # completeness is not readiness
    checklist.write_text("| ASG-K8S-005 | PASS | done |\n" * 2)
    checker.results.clear()
    checker.check_documents()
    assert checker.results[0][0] == checker.FAIL

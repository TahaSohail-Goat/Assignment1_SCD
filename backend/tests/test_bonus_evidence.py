"""Guard factual claims made by the committed optional-bonus evidence."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("capture", ["baseline50", "adjusted50", "bonus128-20260929"])
def test_zero_downtime_load_capture_has_no_failed_requests(capture: str) -> None:
    evidence = ROOT / "docs" / "evidence" / f"k8s-load-{capture}"
    summary = json.loads((evidence / "summary.json").read_text(encoding="utf-8"))["metrics"]

    assert summary["http_reqs"]["count"] == 9559
    assert summary["http_req_failed"]["value"] == 0
    assert summary["dropped_iterations"]["count"] == 0
    assert summary["checks"]["value"] == 1
    assert (evidence / "set-image.txt").read_text(encoding="utf-8").strip() == (
        "deployment.apps/backend image updated"
    )
    assert (evidence / "rollout-status.txt").read_text(encoding="utf-8").strip() == (
        'deployment "backend" successfully rolled out'
    )

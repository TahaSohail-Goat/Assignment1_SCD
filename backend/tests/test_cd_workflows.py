"""Guard publishing boundaries; runner success remains separate deployment evidence."""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("filename", ["cd.yml", "release.yml"])
def test_publishing_follows_the_full_read_only_ci_gate(filename: str) -> None:
    workflow = yaml.safe_load((ROOT / ".github/workflows" / filename).read_text())
    jobs = workflow["jobs"]
    assert workflow["permissions"] == {"contents": "read"}
    assert jobs["test"]["uses"] == "./.github/workflows/ci.yml"
    assert jobs["build-push"]["needs"] == "test"
    for name, job in jobs.items():
        if name != "test":
            assert job["needs"]
            assert job["timeout-minutes"] <= 15
        for step in job.get("steps", []):
            if "uses" in step:
                assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", step["uses"])


def test_cd_deploys_sha_images_and_creates_the_secret_before_workloads() -> None:
    workflow = yaml.safe_load((ROOT / ".github/workflows/cd.yml").read_text())
    assert workflow[True] == {"push": {"branches": ["main"]}}
    deploy = workflow["jobs"]["deploy-k8s"]
    assert deploy["needs"] == "build-push"
    steps = deploy["steps"]
    names = [step.get("name", "") for step in steps]
    assert names.index("Create namespace and real Secret before applying workloads") < names.index(
        "Apply production overlay using the merged SHA"
    )
    text = "\n".join(step.get("run", "") for step in steps)
    assert ":latest" not in text
    assert "REPLACE_WITH_COMMIT_SHA/$GITHUB_SHA" in text
    assert "rollout status deployment/backend" in text
    assert "Host: civicpulse.local" in text
    assert "port-forward service/ingress-nginx-controller" in text
    assert "get hpa" in text
    assert "git push" not in text


def test_production_compose_pulls_the_same_registry_namespace() -> None:
    compose = yaml.safe_load((ROOT / "compose.prod.yaml").read_text())
    for service in ["backend", "migrate", "frontend"]:
        image = compose["services"][service]["image"]
        assert image.startswith("ghcr.io/tahasohail-goat/civicpulse-")
        assert "${IMAGE_TAG:?" in image


def test_ingress_readiness_does_not_depend_on_a_garbage_collected_job() -> None:
    workflow = yaml.safe_load((ROOT / ".github/workflows/cd.yml").read_text())
    steps = workflow["jobs"]["deploy-k8s"]["steps"]
    install = next(
        s["run"] for s in steps if s.get("name") == "Install ingress and autoscaling prerequisites"
    )
    # The pinned upstream manifests set ttlSecondsAfterFinished=0. Its persistent
    # webhook CA configuration is observable even after the admission Job disappears.
    assert "wait --for=condition=complete job/ingress-nginx-admission-patch" not in install
    assert "wait --for=jsonpath='{.webhooks[0].clientConfig.caBundle}'" in install
    assert "validatingwebhookconfiguration/ingress-nginx-admission" in install

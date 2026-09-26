"""Static checks of the Kubernetes manifests in k8s/base and k8s/overlays (ASG-K8S-003..022).

They read the YAML: the rendering (`kustomize build`) and the schema check (`kubeconform`) are the
`manifests` job of ci.yml, and that the pods really start is what the deployment demonstrates.
"""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

K8S = Path(__file__).resolve().parents[2] / "k8s"
BASE = K8S / "base"


def _load(path: Path) -> list[dict[str, Any]]:
    return [doc for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")) if doc]


OBJECTS: list[dict[str, Any]] = [
    doc
    for path in sorted(BASE.glob("*.yaml"))
    if path.name != "kustomization.yaml"
    for doc in _load(path)
]


def _one(kind: str, name: str) -> dict[str, Any]:
    matches = [o for o in OBJECTS if o["kind"] == kind and o["metadata"]["name"] == name]
    assert len(matches) == 1, f"{kind}/{name}: {len(matches)} found"
    return matches[0]


def _containers(workload: dict[str, Any]) -> list[dict[str, Any]]:
    spec = workload["spec"]["template"]["spec"]
    return [*spec.get("initContainers", []), *spec["containers"]]


def test_backend_hpa_uses_assignment_cpu_target_and_stabilization_windows() -> None:
    hpa = _one("HorizontalPodAutoscaler", "backend-hpa")
    assert hpa["apiVersion"] == "autoscaling/v2"
    spec = hpa["spec"]
    assert spec["scaleTargetRef"] == {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "name": "backend",
    }
    assert (spec["minReplicas"], spec["maxReplicas"]) == (2, 10)
    assert spec["metrics"][0]["resource"] == {
        "name": "cpu",
        "target": {"type": "Utilization", "averageUtilization": 60},
    }
    assert spec["behavior"]["scaleDown"]["stabilizationWindowSeconds"] == 300
    assert spec["behavior"]["scaleUp"]["stabilizationWindowSeconds"] == 0


def test_vpa_recommends_without_automatically_changing_hpa_cpu_denominator() -> None:
    vpa = _one("VerticalPodAutoscaler", "backend-vpa")
    assert vpa["spec"]["targetRef"]["name"] == "backend"
    assert vpa["spec"]["updatePolicy"]["updateMode"] == "Off"


def test_everything_lives_in_the_civicpulse_namespace() -> None:
    namespaced = [o for o in OBJECTS if o["kind"] != "Namespace"]

    assert _one("Namespace", "civicpulse")
    assert namespaced
    assert {o["metadata"]["namespace"] for o in namespaced} == {"civicpulse"}


def test_backend_and_frontend_are_deployments_with_at_least_two_replicas() -> None:
    for name in ("backend", "frontend"):
        assert _one("Deployment", name)["spec"]["replicas"] >= 2


def test_postgres_is_a_stateful_set_with_a_volume_claim_template_and_no_deployment() -> None:
    database = _one("StatefulSet", "database")

    assert database["spec"]["volumeClaimTemplates"]
    assert database["spec"]["serviceName"] == "database"
    deployment_images = [
        c["image"] for o in OBJECTS if o["kind"] == "Deployment" for c in _containers(o)
    ]
    assert not [image for image in deployment_images if image.startswith("postgres")]


def test_redis_is_a_deployment_with_a_persistent_volume_claim() -> None:
    cache = _one("Deployment", "cache")
    volumes = cache["spec"]["template"]["spec"]["volumes"]

    claim = volumes[0]["persistentVolumeClaim"]["claimName"]
    assert _one("PersistentVolumeClaim", claim)
    assert cache["spec"]["strategy"]["type"] == "Recreate"  # a ReadWriteOnce claim


def test_there_are_four_services_and_all_are_cluster_ip() -> None:
    services = [o for o in OBJECTS if o["kind"] == "Service"]

    assert sorted(s["metadata"]["name"] for s in services) == [
        "backend",
        "cache",
        "database",
        "frontend",
    ]
    assert {s["spec"]["type"] for s in services} == {"ClusterIP"}


def test_the_ingress_routes_slash_to_the_frontend_and_api_to_the_backend_on_one_host() -> None:
    rules = _one("Ingress", "civicpulse")["spec"]["rules"]

    assert len(rules) == 1
    routes = {p["path"]: p["backend"]["service"]["name"] for p in rules[0]["http"]["paths"]}
    assert routes == {"/api": "backend", "/": "frontend"}


def test_the_backend_has_the_three_probes_with_the_semantics_of_the_assignment() -> None:
    container = _one("Deployment", "backend")["spec"]["template"]["spec"]["containers"][0]

    assert container["startupProbe"]["httpGet"] == {"path": "/health", "port": 8000}
    assert container["startupProbe"]["failureThreshold"] == 30
    assert container["startupProbe"]["periodSeconds"] == 2
    assert container["livenessProbe"]["httpGet"]["path"] == "/health"  # not the database
    assert container["readinessProbe"]["httpGet"]["path"] == "/ready"  # the dependencies


def test_the_backend_rolls_out_without_losing_capacity_and_leaves_the_endpoints_first() -> None:
    deployment = _one("Deployment", "backend")
    strategy = deployment["spec"]["strategy"]["rollingUpdate"]
    pod = deployment["spec"]["template"]["spec"]
    container = pod["containers"][0]

    assert strategy == {"maxSurge": 1, "maxUnavailable": 0}
    assert pod["terminationGracePeriodSeconds"] > 10
    assert container["lifecycle"]["preStop"]["exec"]["command"][0] == "sleep"


def test_the_backend_pod_disruption_budget_keeps_one_pod() -> None:
    budget = _one("PodDisruptionBudget", "backend")["spec"]

    assert budget["minAvailable"] == 1
    assert budget["selector"]["matchLabels"] == {"app.kubernetes.io/name": "backend"}


@pytest.mark.parametrize(
    ("kind", "name"),
    [
        ("Deployment", "backend"),
        ("Deployment", "frontend"),
        ("Deployment", "cache"),
        ("StatefulSet", "database"),
    ],
)
def test_every_container_has_cpu_and_memory_requests_and_limits(kind: str, name: str) -> None:
    for container in _containers(_one(kind, name)):
        resources = container["resources"]
        assert resources["requests"]["cpu"] and resources["requests"]["memory"]
        assert resources["limits"]["cpu"] and resources["limits"]["memory"]


def test_the_backend_runs_as_a_non_root_user_with_a_read_only_filesystem() -> None:
    pod = _one("Deployment", "backend")["spec"]["template"]["spec"]

    assert pod["securityContext"]["runAsNonRoot"] is True
    assert pod["securityContext"]["runAsUser"] == 10001
    for container in _containers(_one("Deployment", "backend")):
        assert container["securityContext"]["readOnlyRootFilesystem"] is True
        assert container["securityContext"]["allowPrivilegeEscalation"] is False


def test_migrations_run_before_the_api_starts_from_the_same_image() -> None:
    pod = _one("Deployment", "backend")["spec"]["template"]["spec"]
    init = pod["initContainers"][0]

    assert init["command"] == ["alembic", "upgrade", "head"]
    assert init["image"] == pod["containers"][0]["image"]


def test_the_secret_holds_placeholders_only() -> None:
    secret = _one("Secret", "civicpulse-secrets")

    assert set(secret["stringData"]) == {"POSTGRES_PASSWORD", "GROQ_API_KEY"}
    assert set(secret["stringData"].values()) == {"REPLACE_ME"}
    assert "data" not in secret  # no base64 value either (ASG-DED-002)


def test_no_manifest_carries_a_credential() -> None:
    text = "\n".join(
        line
        for path in K8S.rglob("*.yaml")
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("#")  # comments explain the rule and may name it
    )

    assert not re.search(r"gsk_[A-Za-z0-9]{10,}", text)  # a Groq key
    assert not re.search(r"(?i)sk-[A-Za-z0-9]{20,}", text)
    assert not re.search(r"postgresql\+psycopg://[^$\s:]+:[^$\s@]+@", text)  # URL with a password
    assert "localhost" not in text and "127.0.0.1" not in text


def test_the_configuration_uses_service_names_and_no_secret_value() -> None:
    config = _one("ConfigMap", "civicpulse-config")["data"]

    assert config["REDIS_URL"] == "redis://cache:6379/0"
    assert not any("PASSWORD" in key or "KEY" in key for key in config)


def test_the_base_kustomization_lists_every_manifest_file() -> None:
    listed = set(yaml.safe_load((BASE / "kustomization.yaml").read_text())["resources"])
    present = {p.name for p in BASE.glob("*.yaml") if p.name != "kustomization.yaml"}

    assert listed == present


@pytest.mark.parametrize("overlay", ["dev", "prod"])
def test_each_overlay_extends_the_base_and_removes_the_placeholder_secret(overlay: str) -> None:
    kustomization = yaml.safe_load((K8S / "overlays" / overlay / "kustomization.yaml").read_text())

    assert kustomization["resources"] == ["../../base"]
    assert "$patch: delete" in kustomization["patches"][0]["patch"]
    assert {image["name"] for image in kustomization["images"]} == {
        "civicpulse-backend",
        "civicpulse-frontend",
    }


def test_the_prod_overlay_never_deploys_latest_and_pulls_from_ghcr() -> None:
    kustomization = yaml.safe_load((K8S / "overlays" / "prod" / "kustomization.yaml").read_text())

    for image in kustomization["images"]:
        assert image["newTag"] != "latest"
        assert image["newName"].startswith("ghcr.io/")

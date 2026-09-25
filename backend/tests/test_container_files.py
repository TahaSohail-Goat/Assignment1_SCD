"""Static checks of the Dockerfile, .dockerignore, compose.yaml and .env.example.

Docker is not needed to run these: they read the files. They do not prove that the images build or
that the stack starts; the CI job that runs ``docker compose up`` does (issue #51).
"""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

REPOSITORY = Path(__file__).resolve().parents[2]
DOCKERFILE = (REPOSITORY / "backend" / "Dockerfile").read_text(encoding="utf-8")
DOCKERIGNORE = (REPOSITORY / "backend" / ".dockerignore").read_text(encoding="utf-8").split()
COMPOSE_TEXT = (REPOSITORY / "compose.yaml").read_text(encoding="utf-8")
COMPOSE: dict[str, Any] = yaml.safe_load(COMPOSE_TEXT)
SERVICES: dict[str, dict[str, Any]] = COMPOSE["services"]
ENV_EXAMPLE = (REPOSITORY / ".env.example").read_text(encoding="utf-8")
GITIGNORE = (REPOSITORY / ".gitignore").read_text(encoding="utf-8").splitlines()


def _instructions(text: str) -> list[tuple[str, str]]:
    """(INSTRUCTION, arguments) for each Dockerfile instruction, continuation lines joined."""
    joined = re.sub(r"\\\r?\n", " ", text)
    pairs = []
    for line in joined.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            keyword, _, rest = line.partition(" ")
            pairs.append((keyword.upper(), rest.strip()))
    return pairs


INSTRUCTIONS = _instructions(DOCKERFILE)


# ---- the backend image (ASG-DEVOPS-001..007) ---------------------------------------------


def test_the_image_is_multi_stage_on_a_pinned_python_312_slim() -> None:
    bases = [args for keyword, args in INSTRUCTIONS if keyword == "FROM"]

    assert len(bases) == 2
    for base in bases:
        assert re.match(r"python:3\.12\.\d+-slim(-\w+)? AS \w+$", base), base


def test_dependencies_are_installed_in_the_builder_stage_only() -> None:
    stage = ""
    installs = []
    for keyword, args in INSTRUCTIONS:
        if keyword == "FROM":
            stage = args.split()[-1]
        if keyword == "RUN" and "pip install" in args:
            installs.append(stage)

    assert installs == ["builder"]


def test_requirements_are_copied_before_the_source() -> None:
    copies = [args for keyword, args in INSTRUCTIONS if keyword == "COPY"]
    requirements = next(i for i, args in enumerate(copies) if "requirements.txt" in args)
    source = next(i for i, args in enumerate(copies) if args.endswith("./app"))

    assert requirements < source


def test_the_image_runs_as_a_non_root_user() -> None:
    users = [args for keyword, args in INSTRUCTIONS if keyword == "USER"]

    assert users
    assert users[-1] not in {"root", "0"}
    assert INSTRUCTIONS.index(("USER", users[-1])) > max(
        i for i, (keyword, _) in enumerate(INSTRUCTIONS) if keyword == "COPY"
    )


def test_cmd_is_in_exec_form_and_starts_uvicorn_without_a_shell() -> None:
    commands = [args for keyword, args in INSTRUCTIONS if keyword == "CMD"]

    assert len(commands) == 1
    assert commands[0].startswith('["uvicorn"')
    assert "--no-access-log" in commands[0]


def test_the_image_declares_a_healthcheck() -> None:
    assert any(keyword == "HEALTHCHECK" for keyword, _ in INSTRUCTIONS)


def test_the_context_excludes_what_must_not_reach_the_image() -> None:
    for entry in (".git", ".env", ".venv", "node_modules", "__pycache__", "tests"):
        assert entry in DOCKERIGNORE


# ---- compose.yaml (ASG-DEVOPS-013..027) --------------------------------------------------


def test_the_two_networks_are_bridges_and_only_internal_is_internal() -> None:
    networks = COMPOSE["networks"]

    assert networks["edge"] == {"driver": "bridge"}
    assert networks["internal"] == {"driver": "bridge", "internal": True}


def test_backend_is_on_both_networks_and_the_data_services_on_internal_only() -> None:
    assert set(SERVICES["backend"]["networks"]) == {"edge", "internal"}
    assert list(SERVICES["database"]["networks"]) == ["internal"]
    assert list(SERVICES["cache"]["networks"]) == ["internal"]
    bridging = [n for n, s in SERVICES.items() if {"edge", "internal"} <= set(s["networks"])]
    assert bridging == ["backend"]


def test_the_data_services_publish_no_port() -> None:
    assert "ports" not in SERVICES["database"]
    assert "ports" not in SERVICES["cache"]


def test_the_named_volumes_exist_and_are_used_where_expected() -> None:
    assert set(COMPOSE["volumes"]) == {"pgdata", "redisdata", "ollama_models"}
    assert any(v.startswith("pgdata:") for v in SERVICES["database"]["volumes"])
    assert any(v.startswith("redisdata:") for v in SERVICES["cache"]["volumes"])


def test_redis_persists_with_the_append_only_file() -> None:
    command = SERVICES["cache"]["command"]

    assert command[command.index("--appendonly") + 1] == "yes"


def test_the_source_is_bind_mounted_into_the_backend_for_hot_reload() -> None:
    mounts = SERVICES["backend"]["volumes"]

    assert any(mount.startswith("./backend/app:") for mount in mounts)
    assert "--reload" in SERVICES["backend"]["command"]


@pytest.mark.parametrize("name", sorted(SERVICES))
def test_every_service_restarts_and_has_limits(name: str) -> None:
    service = SERVICES[name]

    assert service["restart"] in {"unless-stopped", "no"}
    if name != "migrate":  # the one-shot migration must not restart in a loop
        assert service["restart"] == "unless-stopped"
    limits = service["deploy"]["resources"]["limits"]
    assert limits["cpus"] and limits["memory"]


@pytest.mark.parametrize("name", ["database", "cache", "backend"])
def test_every_long_running_service_has_a_healthcheck(name: str) -> None:
    assert SERVICES[name]["healthcheck"]["test"]


def test_the_backend_waits_for_healthy_dependencies_and_finished_migrations() -> None:
    depends = SERVICES["backend"]["depends_on"]

    assert depends["database"]["condition"] == "service_healthy"
    assert depends["cache"]["condition"] == "service_healthy"
    assert depends["migrate"]["condition"] == "service_completed_successfully"
    assert SERVICES["migrate"]["depends_on"]["database"]["condition"] == "service_healthy"


def test_every_image_tag_is_pinned() -> None:
    images = [s["image"] for s in SERVICES.values() if "build" not in s]

    assert images
    for image in images:
        _, _, tag = image.partition(":")
        assert tag and tag != "latest", image


def test_credentials_come_from_the_environment_not_from_the_file() -> None:
    assert "${POSTGRES_PASSWORD}" in COMPOSE_TEXT
    assert "${POSTGRES_USER}" in COMPOSE_TEXT
    assert not re.search(r"(?i)password:\s*(?!\$\{)\S", COMPOSE_TEXT)


def test_services_reach_each_other_by_service_name_never_localhost() -> None:
    for service in SERVICES.values():
        for value in (service.get("environment") or {}).values():
            assert "localhost" not in str(value)
            assert "127.0.0.1" not in str(value)


def test_every_variable_the_compose_file_needs_is_in_the_example() -> None:
    needed = set(re.findall(r"\$\{(\w+)", COMPOSE_TEXT))
    example = {
        line.split("=")[0] for line in ENV_EXAMPLE.splitlines() if "=" in line and line[0] != "#"
    }

    assert needed <= example


def test_env_is_ignored_and_the_example_is_not() -> None:
    assert ".env" in GITIGNORE
    assert "!.env.example" in GITIGNORE

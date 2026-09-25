#!/usr/bin/env python3
"""Pre-submission lint for CivicPulse (assignment section 5.8, ASG-SUB-007).

A lint, not a grader: it catches the mechanical failures behind the automatic deductions of section
5.3 and the missing files of section 5.7. A clean run does not guarantee a good mark.

    python scripts/check_submission.py            # from the repository root
    python scripts/check_submission.py --strict   # warnings also fail the run

Standard library only (Python 3.9+), so it runs on a fresh clone. Exit code 0 when nothing FAILED.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results: list[tuple[str, str, str]] = []  # (status, check, detail)


def record(status: str, check: str, detail: str = "") -> None:
    results.append((status, check, detail))


def git(*args: str) -> str:
    try:
        completed = subprocess.run(  # noqa: S603
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False, encoding="utf-8"
        )
    except OSError:
        return ""
    return completed.stdout if completed.returncode == 0 else ""


def tracked() -> list[str]:
    return [line for line in git("ls-files").splitlines() if line]


def read(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))


FILES = tracked()
K8S = [f for f in FILES if f.startswith("k8s/") and f.endswith((".yaml", ".yml"))]
COMPOSE = [f for f in FILES if re.fullmatch(r"compose[\w.-]*\.ya?ml", f)]
DOCKERFILES = [f for f in FILES if f.endswith("Dockerfile")]
WORKFLOWS = [f for f in FILES if f.startswith(".github/workflows/") and f.endswith((".yml", ".yaml"))]

# ---- 5.7: the repository layout ------------------------------------------------------------

REQUIRED = [
    "backend/Dockerfile", "backend/.dockerignore", "backend/pyproject.toml", "backend/tests",
    "backend/alembic/versions", "backend/app/routes", "backend/app/services",
    "backend/app/repositories", "backend/app/providers/triage/base.py",
    "backend/app/providers/triage/llm.py", "backend/app/providers/triage/ollama.py",
    "backend/app/providers/triage/rules.py", "backend/app/providers/triage/simulated.py",
    "backend/app/providers/triage/factory.py",
    "frontend/Dockerfile", "frontend/.dockerignore", "frontend/nginx.conf", "frontend/package.json",
    "frontend/src/components", "frontend/src/pages", "frontend/src/api", "frontend/tests",
    "k8s/base/namespace.yaml", "k8s/base/backend.yaml", "k8s/base/frontend.yaml",
    "k8s/base/postgres.yaml", "k8s/base/redis.yaml", "k8s/base/ingress.yaml",
    "k8s/base/configmap.yaml", "k8s/base/secret.yaml", "k8s/base/hpa.yaml", "k8s/base/vpa.yaml",
    "k8s/base/pdb.yaml", "k8s/base/kustomization.yaml", "k8s/overlays/dev/kustomization.yaml",
    "k8s/overlays/prod/kustomization.yaml", "load/k6-script.js",
    "docs/ENGINEERING-NOTES.md", "docs/RUNBOOK.md", "docs/AI-USAGE.md", "docs/TRIAGE.md",
    "docs/adr/0001-provider-interface.md", "docs/adr/0004-pii-and-data-governance.md",
    "docs/evidence", "scripts/check_submission.py",
    ".github/workflows/ci.yml", ".github/workflows/cd.yml", ".github/workflows/release.yml",
    "compose.yaml", "compose.prod.yaml", ".env.example", ".gitignore", "README.md", "LICENSE",
]


def check_layout() -> None:
    have = set(FILES)
    missing = [
        p for p in REQUIRED
        if p not in have and not any(f.startswith(p.rstrip("/") + "/") for f in have)
    ]
    if missing:
        record(FAIL, "5.7 repository layout", "missing: " + ", ".join(missing))
    else:
        record(PASS, "5.7 repository layout", f"{len(REQUIRED)} required paths present")


# ---- 5.3 deductions ---------------------------------------------------------------------------

SECRET_NAMES = re.compile(
    r"(^|/)(\.env(\.(?!example$)[^/]+)?|id_rsa[^/]*|id_ed25519[^/]*|[^/]+\.(pem|key|p12|pfx|jks)|"
    r"kubeconfig[^/]*|credentials\.json|[^/]+\.secret\.ya?ml)$"
)
SECRET_CONTENT = re.compile(
    r"gsk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|"
    r"github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"
)


def check_secrets() -> None:  # ASG-DED-001, -20
    bad = [f for f in FILES if SECRET_NAMES.search(f)]
    record(FAIL if bad else PASS, "DED-001 no .env / key file tracked", ", ".join(bad))
    hits = []
    for f in FILES:
        if f.endswith((".png", ".jpg", ".pdf", ".gif", ".webp", ".lock")) or f == Path(__file__).name:
            continue
        if f.endswith("check_submission.py"):
            continue
        if SECRET_CONTENT.search(read(f)):
            hits.append(f)
    record(FAIL if hits else PASS, "DED-001 no credential pattern in tracked files", ", ".join(hits))
    history = [
        line.split("\t")[-1]
        for line in git("log", "--all", "--name-only", "--pretty=format:").splitlines()
        if line and SECRET_NAMES.search(line)
    ]
    record(
        FAIL if history else PASS,
        "DED-001 no .env / key file anywhere in Git history",
        ", ".join(sorted(set(history))),
    )
    if (ROOT / ".git").exists():
        leaked = git("log", "--all", "--oneline", "-G", SECRET_CONTENT.pattern, "--", ".",
                     ":(exclude)scripts/check_submission.py", ":(exclude)*.md",
                     ":(exclude)backend/tests")
        record(
            FAIL if leaked.strip() else PASS,
            "DED-001 no credential pattern in Git history (code, config)",
            leaked.strip().replace("\n", "; ")[:300],
        )
    ignore = read(".gitignore").splitlines()
    ok = ".env" in ignore and "!.env.example" in ignore and Path(ROOT, ".env.example").exists()
    record(PASS if ok else FAIL, "DEVOPS-024 .env ignored, .env.example committed")


def check_k8s_secrets() -> None:  # ASG-DED-002, -15
    problems = []
    for f in K8S:
        text = read(f)
        if SECRET_CONTENT.search(text):
            problems.append(f"{f}: credential pattern")
        if re.search(r"^kind:\s*Secret\s*$", text, re.M):
            body = strip_comments(text)
            if re.search(r"^data:", body, re.M):
                problems.append(f"{f}: Secret has a data: block (base64 counts as committed)")
            values = re.findall(r"^\s{2,}[A-Z_]+:\s*(\S+)\s*$", body.split("stringData:", 1)[-1], re.M)
            if any(v.strip("\"'") != "REPLACE_ME" for v in values):
                problems.append(f"{f}: Secret value is not the REPLACE_ME placeholder")
    record(FAIL if problems else PASS, "DED-002 no key or secret value in Kubernetes manifests",
           "; ".join(problems))


def image_refs() -> list[tuple[str, str]]:
    refs = []
    for f in COMPOSE + K8S:
        for match in re.finditer(r"^\s*(?:-\s*)?image:\s*(\S+)", strip_comments(read(f)), re.M):
            refs.append((f, match.group(1).strip("\"'")))
    for f in DOCKERFILES:
        for match in re.finditer(r"^FROM\s+(\S+)", read(f), re.M | re.I):
            if match.group(1).lower() != "scratch":
                refs.append((f, match.group(1)))
    return refs


def check_pinned_images() -> None:  # ASG-DED-003, -8
    unpinned: list[str] = []
    # A base manifest may name an image without a tag when every overlay sets it with `images:`.
    overlays = [strip_comments(read(f)) for f in K8S if "/overlays/" in f]
    tagged_by_overlay = {
        name
        for text in overlays
        for name, block in re.findall(r"-\s*name:\s*(\S+)\n((?:[ \t]+\w+:.*\n?)+)", text)
        if "newTag:" in block
    }
    stages = {m.group(1) for f in DOCKERFILES for m in re.finditer(r"\bAS\s+(\w+)", read(f), re.I)}
    for f, ref in image_refs():
        if ref in stages or "${" in ref or ref in tagged_by_overlay:  # a build stage name, or a value set at deploy time
            continue
        name = ref.split("@")[0]
        tag = name.rsplit(":", 1)[1] if ":" in name.rsplit("/", 1)[-1] else ""
        if "@sha256:" in ref:
            continue
        if not tag or tag == "latest":
            unpinned.append(f"{f}: {ref}")
    record(FAIL if unpinned else PASS, "DED-003 every image tag pinned",
           "; ".join(sorted(set(unpinned))))


def check_localhost() -> None:  # ASG-DED-004, -8
    hits = []
    for f in COMPOSE + K8S + WORKFLOWS:
        if f.endswith("ci.yml"):
            continue  # the CI job talks to the published port from the runner, not service to service
        for line in strip_comments(read(f)).splitlines():
            # a container probing its own port (healthcheck) is not service-to-service traffic
            if re.search(r"localhost|127\.0\.0\.1", line) and "urlopen(" not in line:
                hits.append(f)
                break
    record(FAIL if hits else PASS, "DED-004 no localhost between services (compose, k8s)", ", ".join(hits))


def check_compose_prod() -> None:  # ASG-DED-006 / DEVOPS-028, 029
    text = strip_comments(read("compose.prod.yaml"))
    if not text.strip():
        record(FAIL, "DED-006 compose.prod.yaml", "file missing")
        return
    problems = []
    if re.search(r"^\s*build:", text, re.M):
        problems.append("has a build: key")
    if "${IMAGE_TAG}" not in text:
        problems.append("does not use ${IMAGE_TAG}")
    if re.search(r"^\s*-?\s*\"?\d*:?\d+:(5432|6379)\"?", text, re.M) or re.search(
        r"(database|cache|postgres|redis):(?:(?!\n\S).)*?\bports:", text, re.S
    ):
        problems.append("publishes a database or cache port")
    record(FAIL if problems else PASS, "DED-006 compose.prod.yaml deploys images, no data port",
           "; ".join(problems))


def check_k8s_services() -> None:  # ASG-DED-006, ASG-DED-009
    bad = []
    for f in K8S:
        text = strip_comments(read(f))
        for doc in text.split("\n---"):
            if re.search(r"^kind:\s*Service\s*$", doc, re.M) and re.search(
                r"type:\s*(NodePort|LoadBalancer)", doc
            ):
                bad.append(f)
    record(FAIL if bad else PASS, "DED-006 no NodePort/LoadBalancer Service", ", ".join(bad))
    pg = read("k8s/base/postgres.yaml")
    ok = bool(re.search(r"^kind:\s*StatefulSet", pg, re.M)) and "volumeClaimTemplates" in pg
    record(PASS if ok else FAIL, "DED-009 PostgreSQL is a StatefulSet with volumeClaimTemplates")


def check_workflows() -> None:  # ASG-DED-007, -008, CICD-022, 025, 026
    if not WORKFLOWS:
        record(FAIL, "CICD workflows", "no workflow files")
        return
    no_perm, unpinned, latest, ungated = [], [], [], []
    for f in WORKFLOWS:
        text = read(f)
        body = strip_comments(text)
        if not re.search(r"^permissions:", body, re.M):
            no_perm.append(f)
        for ref in re.findall(r"^\s*-?\s*uses:\s*(\S+)", body, re.M):
            if ref.startswith("./"):
                continue
            version = ref.split("@", 1)[1] if "@" in ref else ""
            if not version:
                unpinned.append(f"{f}: {ref}")
        if re.search(r"deploy[^\n]*:latest|:latest[^\n]*deploy|newTag:\s*latest", body, re.I):
            latest.append(f)
        if f.endswith(("cd.yml", "release.yml")):
            for job, block in re.findall(r"^  ([\w-]+):\n((?:    .*\n|\n)+)", body + "\n", re.M):
                publishes = re.search(r"push:\s*true|docker push|kubectl (apply|set image)", block)
                if publishes and not re.search(r"^    needs:", block, re.M):
                    ungated.append(f"{f}:{job}")
    record(FAIL if no_perm else PASS, "CICD-025 every workflow has a permissions block", ", ".join(no_perm))
    record(FAIL if unpinned else PASS, "CICD-026 every action has a version", "; ".join(unpinned))
    record(FAIL if ungated else PASS, "DED-007 publishing/deploying jobs use needs:", ", ".join(ungated))
    prod = strip_comments(read("k8s/overlays/prod/kustomization.yaml"))
    prod_latest = re.search(r"newTag:\s*latest", prod) is not None
    record(FAIL if latest or prod_latest else PASS, "DED-008 :latest is never deployed",
           ", ".join(latest) + (" prod overlay" if prod_latest else ""))
    names = {Path(f).name for f in WORKFLOWS}
    record(PASS if {"ci.yml", "cd.yml", "release.yml"} <= names else FAIL,
           "CICD-001 ci.yml, cd.yml and release.yml exist")


def check_deploy_reference() -> None:  # CICD-023
    tag = re.findall(r"newTag:\s*(\S+)", strip_comments(read("k8s/overlays/prod/kustomization.yaml")))
    placeholder = [t for t in tag if not re.fullmatch(r"[0-9a-f]{7,40}|sha-[0-9a-f]{7,40}|v?\d+\.\d+\.\d+", t)]
    if not tag:
        record(FAIL, "CICD-023 prod overlay names an image tag")
    elif placeholder:
        record(WARN, "CICD-023 prod overlay still has a placeholder tag",
               "set by cd.yml with the commit SHA before submission: " + ", ".join(placeholder))
    else:
        record(PASS, "CICD-023 prod overlay deploys an immutable tag", ", ".join(tag))


def check_direct_commits() -> None:  # ASG-DED-010, -5
    main = "origin/main" if git("rev-parse", "--verify", "origin/main").strip() else "main"
    log = git("log", main, "--first-parent", "--pretty=format:%h %p|%s")
    if not log:
        record(WARN, "DED-010 no direct commits to main", "cannot read main; fetch first")
        return
    direct = [
        line for line in log.splitlines()
        if len(line.split("|")[0].split()) == 2  # hash + one parent: not a merge commit
    ]
    if len(direct) <= 1:
        record(PASS, "DED-010 no direct commits to main", "only the initial commit is not a merge")
    else:
        record(WARN, "DED-010 commits on main that are not merges",
               f"{len(direct)}: check each came from a PR (" + "; ".join(direct[:4]) + ")")


def check_documents() -> None:
    readme = read("README.md")
    record(PASS if len(readme) > 1500 else FAIL, "README exists and is not a stub")
    template_markers = ("Answer the assignment's eight questions", "Populate from implemented")
    for f, minimum in (("docs/ENGINEERING-NOTES.md", 3000), ("docs/RUNBOOK.md", 1500),
                       ("docs/TRIAGE.md", 500)):
        text = read(f)
        stub = any(m in text for m in template_markers) or len(text) < minimum
        record(FAIL if stub else PASS, f"{f} is filled in")
    adrs = [f for f in FILES if re.fullmatch(r"docs/adr/000[1-4]-.*\.md", f)]
    record(PASS if len(adrs) >= 4 else FAIL, "ADRs 0001-0004 exist", f"found {len(adrs)}")
    evidence = [f for f in FILES if f.startswith("docs/evidence/")]
    wanted = {"protection": "ruleset", "conflict": "conflict", "blocked merge": "ci-red",
              "hpa -w": "hpa", "scaling chart": "chart"}
    missing = [k for k, v in wanted.items() if not any(v in Path(f).name.lower() for f in evidence)]
    record(FAIL if missing else PASS, "docs/evidence has the captures of 5.7",
           "missing: " + ", ".join(missing) if missing else f"{len(evidence)} files")
    usage = read("docs/AI-USAGE.md")
    record(PASS if usage.count("| 2026-") >= 10 else WARN, "AI-USAGE has entries for both contributors")


def check_authorship() -> None:
    out = git("shortlog", "-sn", "--all", "--no-merges")
    authors = [line.split("\t", 1)[1] for line in out.splitlines() if "\t" in line]
    record(PASS if len(authors) >= 2 else WARN, "both contributors have commits",
           "; ".join(out.strip().splitlines()[:4]))


def check_placeholders() -> None:
    hits = []
    for f in FILES:
        if f.startswith("docs/") or f.endswith((".png", ".pdf", ".jpg")) or "check_submission" in f:
            continue
        if re.search(r"\bTODO\b|\bFIXME\b|\bXXX\b", read(f)):
            hits.append(f)
    record(WARN if hits else PASS, "no TODO/FIXME left in code and config", ", ".join(hits[:8]))


def main() -> int:
    strict = "--strict" in sys.argv
    if not (ROOT / ".git").exists():
        print("Run this from a git checkout of the repository.")
        return 2
    for check in (check_layout, check_secrets, check_k8s_secrets, check_pinned_images, check_localhost,
                  check_compose_prod, check_k8s_services, check_workflows, check_deploy_reference,
                  check_direct_commits, check_documents, check_authorship, check_placeholders):
        check()
    width = max(len(name) for _, name, _ in results)
    for status, name, detail in results:
        print(f"{status:<4}  {name:<{width}}  {detail}".rstrip())
    counts = {s: sum(1 for r in results if r[0] == s) for s in (PASS, WARN, FAIL)}
    print(f"\n{counts[PASS]} passed, {counts[WARN]} warnings, {counts[FAIL]} failed")
    failed = counts[FAIL] > 0 or (strict and counts[WARN] > 0)
    print("NOT ready to submit." if failed else "Mechanical checks clean. This is a lint, not a grade.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

# CivicPulse

[![CI](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/workflows/ci.yml)
[![CD](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/workflows/cd.yml)

CivicPulse is a civic-issue reporting and triage service. Citizens submit a complaint and
location; the service validates it, assigns a category and priority, stores it, and exposes it
to operators through a dashboard and statistics view.

Built for CS4032 Assignment 1 by **TahaSohail-Goat** and **Artfever** with React, TypeScript,
FastAPI, PostgreSQL, Redis, Docker and Kubernetes.

## Contents

- [What CivicPulse provides](#what-civicpulse-provides)
- [Quick start](#quick-start)
- [Configure triage](#configure-triage)
- [Architecture](#architecture)
- [Repository layout](#repository-layout)
- [API](#api)
- [Operations and observability](#operations-and-observability)
- [Kubernetes](#kubernetes)
- [CI, delivery and security](#ci-delivery-and-security)
- [Screenshots and evidence](#screenshots-and-evidence)
- [Demo and submission](#demo-and-submission)
- [Documentation, contribution and license](#documentation-contribution-and-license)

## What CivicPulse provides

| Area | Capability |
|---|---|
| Citizen workflow | Submit a complaint with a location and optional contact details. |
| Triage | Rule-based default, optional Groq hosted provider, optional local Ollama, schema validation and safe fallback. |
| Operations | Filtered dashboard, status transitions, paginated history, category/priority statistics and cache state. |
| Reliability | PostgreSQL persistence, Redis cache/rate limit, health/readiness probes, retry/timeout/fallback handling. |
| Deployment | Docker Compose for local use; Kubernetes manifests, HPA/VPA/PDB and a gated GitHub Actions delivery workflow. |
| Evidence | CI, deployment, load, rollback, provider-comparison, observability and submission evidence under `docs/evidence/`. |

The backend is the sole authority for validation, status transitions and triage results. The
frontend never connects to PostgreSQL or Redis.

## Quick start

### Prerequisites

| Tool | Why it is needed |
|---|---|
| Git | Clone the repository. |
| Docker Desktop using Linux containers | Runs the local services and supplies Node 22/Python 3.12 inside images. |
| Docker Compose with `up --wait` | Starts only after service health checks pass. |
| PowerShell 5.1+ on Windows, or a POSIX shell on macOS/Linux | Runs the commands below. |

The first build downloads container images and dependencies. No host Node or Python installation
is required for the standard Compose path.

### Start the local stack

Clone the repository and enter it:

```powershell
git clone https://github.com/TahaSohail-Goat/Assignment1_SCD.git
cd Assignment1_SCD
```

On Windows PowerShell, run this once from the repository root. It creates a gitignored `.env`
with a generated local database password when missing, then builds, migrates, seeds and waits for
healthy services. Existing `.env` values are left unchanged.

```powershell
& {
    $ErrorActionPreference = 'Stop'
    if (-not (Test-Path .env)) {
        $example = [IO.File]::ReadAllText((Join-Path (Get-Location) '.env.example'))
        [IO.File]::WriteAllText(
            (Join-Path (Get-Location) '.env'),
            $example.Replace('change-me-locally', [guid]::NewGuid().ToString('N'))
        )
    }
    docker compose up -d --build --wait
    if ($LASTEXITCODE -ne 0) { throw 'Compose startup failed' }
}
```

On macOS or Linux, use:

```bash
cp .env.example .env && docker compose up -d --build --wait
```

The Compose integration job runs that POSIX command from a clean checkout on every pull request.

### Open the application

| Service | URL | Purpose |
|---|---|---|
| CivicPulse web app | http://localhost:8080 | Submit, Dashboard and Stats views. |
| OpenAPI documentation | http://localhost:8000/docs | Interactive API reference. |
| Health endpoint | http://localhost:8000/health | Process liveness. |
| Readiness endpoint | http://localhost:8000/ready | PostgreSQL and Redis readiness. |

The default `rules` provider needs neither a key nor model download. The standard stack runs the
frontend, backend, PostgreSQL and Redis, plus the completed migration/seed job. It creates 30
synthetic seed complaints.

### Common local commands

```powershell
docker compose ps -a
docker compose logs --tail 50 backend
docker compose run --rm migrate python -m app.seed
docker compose down
```

`docker compose down` retains the database and Redis volumes. Add `--volumes` only when you want
to erase local data. If ports are busy, set `$env:FRONTEND_PORT='18080'` and
`$env:BACKEND_PORT='18000'` before starting the stack.

## Configure triage

All provider settings live in the ignored `.env` file. Never commit that file or a key.

| Mode | `.env` setting | Start command | Notes |
|---|---|---|---|
| Rules (default) | `TRIAGE_PROVIDER=rules` | `docker compose up -d --build --wait` | Deterministic and fully local. |
| Groq | `TRIAGE_PROVIDER=llm` plus `GROQ_API_KEY` | `docker compose up -d --build --wait` | Sends text and location to the configured hosted provider; use synthetic data for demos. |
| Ollama | `TRIAGE_PROVIDER=ollama` | `docker compose --profile offline up -d --build --wait` | Downloads `gemma3:1b` into a named volume; allow additional disk, time and memory. |

The service uses a 10-second provider cutoff, one jittered retry for timeout/429/5xx failures,
Pydantic output validation, a 24-hour content-hash cache and `rules:fallback` if the provider
cannot produce a safe result. Read [provider behavior and data limits](docs/AI.md) before using
a hosted provider.

## Architecture

```mermaid
flowchart LR
    browser[Citizen or operator browser] --> frontend[React served by nginx]
    subgraph edge[Edge network]
        frontend -->|same-origin /api proxy| backend[FastAPI services and validated triage]
    end
    subgraph internal[Internal network]
        backend -->|repositories| postgres[(PostgreSQL 16)]
        backend --> redis[(Redis cache and rate limiter)]
        backend --> ollama[Optional Ollama]
        migrate[Migration and seed] --> postgres
    end
    backend -->|optional HTTPS| hosted[Hosted LLM]
```

Only the backend bridges the Compose `edge` and `internal` networks. PostgreSQL and Redis have no
published production data ports, provider output is validated before storage, and business rules
stay in backend services. [Architecture details](docs/ARCHITECTURE.md) and the four ADRs explain
the design choices.

## Repository layout

```text
backend/       FastAPI application, Alembic migrations, repositories and tests
frontend/      React/Vite user interface, typed API client and component tests
k8s/           Base manifests plus dev and production overlays
observability/ Prometheus and Grafana provisioning
scripts/       Kubernetes, GitOps and submission helpers
docs/          Assignment traceability, runbooks, ADRs and authentic evidence
.github/       CI, CD, release and Kubernetes quickstart workflows
```

The required repository inventory is maintained in [REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md).

## API

| Method | Path | Behavior |
|---|---|---|
| POST | `/api/complaints` | Validate, triage and store; returns 201 and a Location header. |
| GET | `/api/complaints` | Filter by category/priority/status and paginate stored complaints. |
| GET | `/api/complaints/{id}` | Return one complaint or 404. |
| PATCH | `/api/complaints/{id}/status` | Update status; invalid transition is 409 and unknown ID is 404. |
| GET | `/api/stats` | Category/priority totals with a 30-second Redis cache and `X-Cache`. |
| GET | `/api/meta/providers` | Active provider and recent stored provider outcomes. |
| GET | `/health` | Process liveness. |
| GET | `/ready` | PostgreSQL/Redis readiness; names failed dependencies on 503. |
| GET | `/metrics` | Prometheus-format metrics. |

`POST /api/complaints` accepts `text` (10-2000 characters), `location` (3-200) and optional
`reporter_contact`. `PATCH /api/complaints/{id}/status` accepts `{"status":"in_progress"}`.
Allowed transitions are `open` to `in_progress`/`rejected` and `in_progress` to
`resolved`/`rejected`. [API design](docs/API_DESIGN.md) records response-shape decisions.

## Operations and observability

### Prometheus and Grafana

Set `GRAFANA_ADMIN_PASSWORD` in `.env`, then start the optional profile:

```powershell
docker compose --profile observability up -d --build --wait
```

Prometheus is available at http://127.0.0.1:9090 and Grafana at
http://127.0.0.1:3000/d/civicpulse/civicpulse-operations. The profile is local-only. See the
[operations runbook](docs/RUNBOOK.md#16-optional-prometheus-and-grafana-asg-bonus-004) and the
[authentic Grafana capture](docs/evidence/observability-grafana-dashboard.png).

### OpenTelemetry and Jaeger

Use the optional tracing profile to inspect browser, API and provider spans locally:

```powershell
$env:OTEL_EXPORTER_OTLP_TRACES_ENDPOINT='http://jaeger:4318/v1/traces'
$env:VITE_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT='http://127.0.0.1:4318/v1/traces'
docker compose --profile tracing up -d --build --wait
```

Submit synthetic data, then open http://127.0.0.1:16686. The collector and viewer bind only to
loopback, and trace attributes exclude complaint content, contact details, provider payloads and
credentials. See the [captured browser-to-provider trace](docs/evidence/otel-trace.png) and
[tracing runbook](docs/RUNBOOK.md#17-optional-opentelemetry-tracing-asg-bonus-005).

## Kubernetes

### Prerequisites

Install `kind` and `kubectl`, keep Docker running, and build the Compose images first. The local
cluster is named `civicpulse-demo`; it is separate from the Compose stack.

### Deploy and verify

On macOS/Linux, or from Git Bash/WSL on Windows, run the maintained deployment command:

```bash
bash scripts/k8s-up.sh
```

The script creates the cluster, installs ingress/metrics/VPA prerequisites, loads the local images,
creates the runtime Secret outside Git, deploys the dev overlay, waits for probes and seeds data.
It is exercised by the [k8s-quickstart workflow](.github/workflows/k8s-quickstart.yml).

Expose the Ingress in another terminal:

```powershell
kubectl --context kind-civicpulse-demo -n ingress-nginx port-forward service/ingress-nginx-controller 8090:80
```

Browse http://civicpulse.local:8090 after adding `127.0.0.1 civicpulse.local` to your hosts file,
or query without a hosts-file edit:

```powershell
Invoke-RestMethod -Headers @{Host='civicpulse.local'} http://127.0.0.1:8090/api/stats
```

PostgreSQL uses a StatefulSet/PVC. Both app Deployments have two replicas, probes and rolling
updates; Services are ClusterIP. HPA controls 2-10 backend replicas and VPA runs in recommendation
mode. Detailed setup, rollback and limitations are in [RUNBOOK.md](docs/RUNBOOK.md).

### Optional GitOps

After the Kubernetes quickstart, install the local Argo CD demonstration:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/argocd-gitops-demo.ps1
```

It reconciles the repository's `dev` overlay with automated prune and self-heal while keeping the
runtime Secret outside Git. [GitOps evidence and limits](docs/evidence/argocd-gitops-README.md).

## CI, delivery and security

Pull requests run linting, type checking, backend/frontend tests, image builds, vulnerability
scans, manifest validation and Compose integration. Pushes to protected `main` run the same gates,
publish immutable GHCR images, produce SBOMs, keylessly sign and verify image digests, deploy to an
ephemeral kind cluster and perform an Ingress smoke test.

Latest main [CD 36554371413](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36554371413)
passed those gates at `77cc1e0`. The workflow deletes its cluster after the smoke test; this is
deployment evidence, not a persistent public hosting service.

Security controls include ignored environment files, non-root pinned images, network segmentation,
schema validation, rate limiting, signed immutable deployment references and protected branches.
Read the [security baseline](docs/SECURITY.md), [CI/CD guide](docs/CICD.md) and
[Cosign verification evidence](docs/evidence/cosign-verification.md).

## Screenshots and evidence

The screenshots below show the animated interface (issue #142): a three.js city backdrop, a 3D stats
chart and Motion transitions. They were captured from a separate Compose project with empty volumes,
real PostgreSQL, Redis and rules triage: 30 seed complaints plus one submission, with no mocked
browser responses. Without WebGL, on software rendering or with reduced motion, the same views use
a static background. The [capture details](docs/evidence/screenshots-README.md) and the original
[verification transcript](docs/evidence/screenshots-clean-clone-log.txt) describe the setup.

### Submit

![Successful complaint submission, rules classification and the high-priority pulse in the 3D city](docs/evidence/screenshots-submit.png)

### Dashboard

![Dashboard filters and stored complaints with category and priority badges](docs/evidence/screenshots-dashboard.png)

### Stats

![31 complaints, a real Redis cache HIT and the 3D category chart](docs/evidence/screenshots-stats.png)

Additional evidence includes [load and rolling updates](docs/evidence/k8s-load-README.md),
[rollback](docs/evidence/k8s-rollback-index.md), [PVC persistence](docs/evidence/k8s-pg-persistence.txt),
[provider comparison](docs/evidence/provider-comparison-README.md), and
[engineering notes](docs/ENGINEERING-NOTES.md).

## Demo and submission

- [YouTube demo (unlisted)](https://youtu.be/bExMGzoHYow)
- [Google Drive backup](https://drive.google.com/file/d/1uNGCvKnzy_vpxxolNp6qQp8R4ht3Ip58/view?usp=drive_link)
- [Submission package and links](docs/SUBMISSION.md)
- [Video verification and scope](docs/evidence/submission-final-README.md)

The video is 4:38 and demonstrates fresh-clone startup, hosted triage, fallback, network
isolation, HPA scaling and both rollback methods. Historical rubric caveats remain recorded in the
[final checklist](docs/FINAL_SUBMISSION_CHECKLIST.md).

## Documentation, contribution and license

Start with the [document index](docs/DOCUMENT_INDEX.md), then consult
[assignment traceability](docs/ASSIGNMENT_TRACEABILITY.md), [runbook](docs/RUNBOOK.md),
[team contribution agreement](docs/TEAM_CONTRIBUTION.md), [AI usage disclosure](docs/AI-USAGE.md)
and [GitHub workflow](docs/GITHUB_WORKFLOW.md).

Changes follow issue to feature branch to partner-reviewed PR into `dev`, followed by a
merge-commit promotion to protected `main`. The project is licensed under the
[MIT License](LICENSE).
# Non-Functional Requirements

The measurable and testable obligations of the assignment, one row each. Every statement and every number comes from [`docx/ASSIGNMENT.md`](../docx/ASSIGNMENT.md) through [`ASSIGNMENT_TRACEABILITY.md`](ASSIGNMENT_TRACEABILITY.md); where the assignment gives no number the row says so. Nothing here sets a target the assignment does not set.

**Categories:** Security · Reliability · Performance · Availability · Maintainability · Testability · Observability · Portability · Deployability. A row can carry two.

**Verification:** unit test · integration test · CI job · inspection / lint · config check · demo · measurement · document review (the codes of the matrix, spelled out).

## 1. The non-functional requirements (`ASG-NFR-001…017`)

| ID | Category | Requirement (from the matrix) | Measure | Verification | Source |
|---|---|---|---|---|---|
| ASG-NFR-001 | Maintainability | Backend is FastAPI + Pydantic v2 (recommended) or Flask (permitted; must be stated in README) | FastAPI + Pydantic v2 named in `backend/pyproject.toml`; if Flask is used instead, the README says so | inspection / lint | §2.2 p5 |
| ASG-NFR-002 | Maintainability | Four layers `routes/ services/ repositories/ providers/`; dependency arrows point one way only | four packages `routes/ services/ repositories/ providers/`; imports point one way only | inspection / lint | §2.2 p5 |
| ASG-NFR-003 | Maintainability | `routes/`: HTTP only — parse, validate, serialise, status codes; no business rules | no business rule in `routes/` (HTTP parsing, validation, serialisation and status codes only) | inspection / lint | §2.2 p5 |
| ASG-NFR-004 | Maintainability | `services/`: business rules — triage orchestration, state machine, statistics | triage orchestration, the state machine and statistics live in `services/` | inspection / lint | §2.2 p5 |
| ASG-NFR-005 | Maintainability | `repositories/`: all SQL lives here and nowhere else | 0 SQL statements outside `repositories/` (grep check) | inspection / lint, CI job | §2.2 p5 |
| ASG-NFR-006 | Maintainability, Portability | `providers/`: outbound integrations (LLM, cache) behind interfaces | every outbound integration (LLM, cache) sits behind an interface in `providers/` | inspection / lint | §2.2 p5 |
| ASG-NFR-007 | Maintainability | A route must not open a database session | 0 database sessions opened in `routes/` | inspection / lint | §2.2 p5 |
| ASG-NFR-008 | Reliability, Availability | Graceful shutdown on SIGTERM: stop accepting new requests, finish in-flight, close pool connections, exit | on SIGTERM: stop accepting requests, finish in-flight ones, close pool connections, exit. No time bound: no numeric target in the assignment | integration test, demo | §2.2 p7 |
| ASG-NFR-009 | Observability | Structured logging: JSON to stdout, never to a file | 100% of log output is JSON on stdout; 0 log files | unit test, inspection / lint | §2.2 p7 |
| ASG-NFR-010 | Observability | Every log line carries `request_id` propagated from the `X-Request-ID` header (generate one if absent) | every log line carries `request_id`, taken from `X-Request-ID` or generated when absent | unit test | §2.2 p7 |
| ASG-NFR-011 | Observability, Reliability | One WARNING per triage fallback with the complaint id, the provider and the error class | exactly 1 WARNING per triage fallback, with the complaint id, the provider and the error class | unit test | §2.2 p7 |
| ASG-NFR-012 | Testability | ≥ 14 backend tests, unit and integration, deterministic | ≥ 14 backend tests (unit and integration), deterministic | CI job | §4 C p20 |
| ASG-NFR-013 | Testability | Backend coverage ≥ 65% on `app/` | backend coverage ≥ 65% on `app/` | CI job | §3.4 p17; §4 C p20 |
| ASG-NFR-014 | Testability | ≥ 5 meaningful frontend component tests (Vitest) passing in CI | ≥ 5 meaningful frontend component tests (Vitest), passing in CI | CI job | §3.4 p17; §4 B p19 |
| ASG-NFR-015 | Testability, Reliability | Test suite is green on every run; no `time.sleep()` and no re-runs to get a pass — determinism by design | 0 `time.sleep()` in tests; 0 re-runs to get a pass; green on every run | CI job | §2.5 p11–12 |
| ASG-NFR-016 | Security, Portability | No `localhost` for service-to-service communication (containers/pods use service names) | 0 uses of `localhost` for service-to-service communication (service names instead) | inspection / lint, CI job | §5.3 p24; §3.4 p17 |
| ASG-NFR-017 | Security | Anything in the browser bundle is public: no credentials/keys in build output ("it's minified" is not a defence) | 0 credentials or keys in the browser bundle (build output) | inspection / lint | §2.1 p5 |

## 2. Measurable constraints inside the other requirement groups

These are the numbers and limits the assignment states inside the data, cache, AI, image, Kubernetes and CI/CD requirements. Each appears once here, under its own ID.

| ID | Category | Requirement (from the matrix) | Measure | Verification | Source |
|---|---|---|---|---|---|
| ASG-DATA-001 | Portability | PostgreSQL 16 | PostgreSQL 16 | config check | §2.3 p7 |
| ASG-DATA-006 | Data | `text`: 10–2000 chars, enforced in the DB (constraint) as well as the app | `text` 10–2000 characters, enforced in the database (constraint) as well as in the application | integration test | §2.3 p7 |
| ASG-DATA-007 | Data | `location`: 3–200 chars | `location` 3–200 characters | integration test | §2.3 p7 |
| ASG-CACHE-001 | Portability | Redis 7 | Redis 7 | config check | §2.4 p8 |
| ASG-AI-006 | Portability, Performance | `OllamaTriage`: fully offline path; Ollama runs as a container in the Compose stack (1B-parameter model); same interface | Ollama runs a 1B-parameter model as a container in the Compose stack | unit test, demo | §2.5 p9–10 |
| ASG-DEVOPS-002 | Deployability, Security | Backend base is `python:3.12-slim` | backend base image `python:3.12-slim` (pinned tag) | inspection / lint | §3.1 p12 |
| ASG-DEVOPS-008 | Deployability, Security | Frontend builds with `node:22-alpine` and serves with `nginx:1.27-alpine` | frontend builds with `node:22-alpine` and serves with `nginx:1.27-alpine` (pinned tags) | inspection / lint | §3.1 p12 |
| ASG-K8S-014 | Performance, Availability | HPA behavior: scaleDown `stabilizationWindowSeconds: 300`; scaleUp `stabilizationWindowSeconds: 0` | HPA behavior: scaleDown `stabilizationWindowSeconds: 300`, scaleUp `stabilizationWindowSeconds: 0` | inspection / lint | §3.3 p15 |
| ASG-K8S-015 | Availability | PodDisruptionBudget `minAvailable: 1` on the backend | PodDisruptionBudget `minAvailable: 1` on the backend | inspection / lint | §3.3 p14 |
| ASG-K8S-016 | Reliability, Availability | `startupProbe`: httpGet `/health` port 8000, `failureThreshold: 30`, `periodSeconds: 2` | `startupProbe` on `/health`, port 8000, `failureThreshold: 30`, `periodSeconds: 2` | inspection / lint | §3.3 p15 |
| ASG-K8S-019 | Availability, Deployability | Rolling update `maxSurge: 1`, `maxUnavailable: 0` | rolling update `maxSurge: 1`, `maxUnavailable: 0` | inspection / lint | §3.3 p15 |
| ASG-K8S-021 | Availability, Deployability | Demonstrate a zero-downtime rollout: load generator during `kubectl set image`, zero failed requests (scored as bonus — see ASG-BONUS-001) | 0 failed requests while a load generator runs during `kubectl set image` (a demonstration; scored as bonus) | demo | §3.3 p15 |
| ASG-DATA-012 | Data | `ai_summary`: nullable, one line, ≤ 140 chars | `ai_summary` is one line, ≤ 140 characters, nullable | integration test | §2.3 p7 |
| ASG-DATA-019 | Data, Deployability | Idempotent seed command loading ≥ 30 realistic complaints | idempotent seed command loading ≥ 30 realistic complaints | integration test | §2.3 p8 |
| ASG-CACHE-003 | Performance | Stats cache TTL is 30 s | stats cache TTL = 30 s | integration test | §2.4 p8 |
| ASG-AI-001 | Reliability | `TriageResult` Pydantic model: `category: Category`, `priority: Priority`, `summary: str` (max 140), `confidence: float` (0.0–1.0) | `summary` max 140 characters; `confidence` between 0.0 and 1.0 | unit test | §2.5 p9 |
| ASG-AI-003 | Availability, Reliability | Implementations `LLMTriage`, `OllamaTriage`, `RuleBasedTriage`, `SimulatedTriage` (at least 3 working) | at least 3 of the 4 triage implementations work | unit test | §2.5 p9; §4 F p20 |
| ASG-AI-013 | Reliability, Performance | Hard timeout of 10 seconds on every LLM call | hard timeout of 10 seconds on every LLM call | unit test | §2.5 p11 |
| ASG-AI-014 | Reliability | Retry once with jitter — on timeout, 429 and 5xx only; never retry a 400 | retry once, with jitter, on timeout, 429 and 5xx only; never retry a 400 | unit test | §2.5 p11 |
| ASG-AI-016 | Performance | Cache triage results by content hash in Redis, 24 h TTL | triage results cached by content hash in Redis, 24 h TTL | integration test | §2.5 p11 |
| ASG-DEVOPS-010 | Deployability, Performance | Report both stage sizes; a frontend image over ~60 MB indicates the multi-stage split is not working | frontend image over about 60 MB indicates the multi-stage split is not working; report both stage sizes | measurement | §3.1 p12 |
| ASG-K8S-004 | Availability | `backend` Deployment with ≥ 2 replicas | `backend` Deployment with ≥ 2 replicas | CI job | §3.3 p14 |
| ASG-K8S-005 | Availability | `frontend` Deployment with ≥ 2 replicas | `frontend` Deployment with ≥ 2 replicas | CI job | §3.3 p14 |
| ASG-K8S-013 | Performance, Availability | HPA: `minReplicas: 2`, `maxReplicas: 10`, CPU Utilization target 60% | HPA: `minReplicas: 2`, `maxReplicas: 10`, CPU utilization target 60% | inspection / lint | §3.3 p15 |
| ASG-CICD-005 | Testability | `test-backend`: pytest with coverage ≥ 65% on `app/`, `TRIAGE_PROVIDER=simulated` | `test-backend`: coverage ≥ 65% on `app/` with `TRIAGE_PROVIDER=simulated` (the CI form of ASG-NFR-013) | CI job | §3.4 p17 |
| ASG-CICD-006 | Testability | `test-frontend`: Vitest component tests, ≥ 5 meaningful tests | `test-frontend`: ≥ 5 meaningful Vitest tests (the CI form of ASG-NFR-014) | CI job | §3.4 p17 |
| ASG-CICD-026 | Security, Maintainability | Actions pinned — `@v4` at minimum (commit SHA for the bonus) | GitHub Actions pinned at `@v4` at minimum (commit SHA for the bonus) | inspection / lint | §3.4 p18 |
| ASG-CICD-031 | Deployability, Availability | A bad deploy can be undone in thirty seconds | a bad deploy can be undone in thirty seconds | measurement | §1.4 p3 |

## 3. Release-blocking deductions (`ASG-DED-001…011`)

The eleven automatic deductions of assignment §5.3 are release-blocking security and reliability constraints. Each is guarded by the requirements named in the last columns; a violation is a defect to fix before merging, not a task for later.

| ID | Deduction (release-blocking) | Points | Source | Guarded by | Verification |
|---|---|---|---|---|---|
| ASG-DED-001 | A `.env`, key, token or password anywhere in Git history (plus rotate and write an incident note) | −20 | §5.3 p24 | `.gitignore`, secret scan on every commit/PR, ASG-DEVOPS-023/024 | inspection / lint, CI job |
| ASG-DED-002 | An LLM API key in a committed Kubernetes manifest, even base64-encoded | −15 | §5.3 p24 | ASG-K8S-011 | inspection / lint, CI job |
| ASG-DED-003 | Unpinned base image, or postgres / redis / node without a tag | −8 | §5.3 p24 | ASG-DEVOPS-001/025 | inspection / lint, CI job |
| ASG-DED-004 | `localhost` used for service-to-service communication | −8 | §5.3 p24 | ASG-NFR-016 | inspection / lint, CI job |
| ASG-DED-005 | Frontend able to reach the database (network segmentation not implemented) | −8 | §5.3 p24 | ASG-DEVOPS-013…017 | demo |
| ASG-DED-006 | Published database/cache port in `compose.prod.yaml`, or NodePort/LoadBalancer Service on the database | −8 | §5.3 p24 | ASG-DEVOPS-028, ASG-K8S-008 | config check, CI job |
| ASG-DED-007 | Publishing or deploying job not gated by `needs:` | −8 | §5.3 p24 | ASG-CICD-022 | inspection / lint |
| ASG-DED-008 | Deploying `:latest` anywhere | −8 | §5.3 p24 | ASG-CICD-023 | inspection / lint, CI job |
| ASG-DED-009 | PostgreSQL as a Deployment with no PVC | −8 | §5.3 p24 | ASG-K8S-006 | CI job |
| ASG-DED-010 | Commits pushed directly to main | −5 | §5.3 p24 | ASG-GH-001/002; `AGENTS.md` §6 | inspection / lint |
| ASG-DED-011 | README quickstart that does not work from a clean clone | −5 | §5.3 p24 | ASG-DOC-004, ASG-GEN-007 | demo |

## 4. Not specified by the assignment

The assignment states **no numeric target** for these, so this catalog sets none:

| Topic | What the assignment says |
|---|---|
| Request latency budget (for example a p95) | Only that `/metrics` exposes a request-latency histogram and that triage latency is recorded (`ASG-AI-*`); no threshold |
| Availability percentage or SLO | None; availability is expressed as ≥ 2 replicas, probes and a rollout that keeps serving |
| Rate-limit threshold and window | The limiter must return 429 with `Retry-After` when exceeded; the limit and window are not given (the source only notes that the free LLM tier allows "on the order of tens of requests per minute") |

## 5. Coverage

| Group | Rows | IDs |
|---|---|---|
| Non-functional requirements | 17 | `ASG-NFR-001…017` |
| Measurable constraints | 28 | see section 2 |
| Deductions cross-referenced | 11 | `ASG-DED-001…011` |

`ASG-CACHE-006` (explain at the viva why TTL and explicit invalidation are both used) and `ASG-CICD-017` (the kind/k3d deploy job) are requirements without a number, and length rules for documents (for example `ASG-K8S-027`: 3–5 sentences) belong to the documentation requirements; all of them stay in their own catalogs.

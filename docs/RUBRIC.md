# Rubric, Deductions, Bonus and Viva

Extracted from `docx/ASSIGNMENT.md` §4 (p19–22), §5.1 (p23), §5.3 (p24) and §5.4 (p24–25). Marks are copied exactly. Each rubric item maps to the requirement IDs in [`ASSIGNMENT_TRACEABILITY.md`](ASSIGNMENT_TRACEABILITY.md) so no line can be forgotten.

> **Source inconsistency (do not silently correct).** The header and §4 state **150 marks**. The rubric lines below sum to **175**. The instructor said (verbally, 2026-09-25) that the rubric is left as it is and managed by the teaching assistant (decisions table in [`SUBMISSION.md`](SUBMISSION.md)), so every line is treated as worth its stated marks and all mandatory lines are pursued.

## 1. Arithmetic check

| Part | Title | Stated section total | Sum of item marks | Match |
|---|---|---|---|---|
| A | Collaboration and version control | 15 | 3+2+4+3+3 = 15 | yes |
| B | Frontend | 18 | 5+5+3+3+2 = 18 | yes |
| C | Backend | 25 | 7+4+3+3+3+2+3 = 25 | yes |
| D | Data layer | 12 | 4+3+2+3 = 12 | yes |
| E | Cache layer | 10 | 3+2+4+1 = 10 | yes |
| F | AI layer | 25 | 5+5+6+3+3+2+1 = 25 | yes |
| G | Docker and Compose | 15 | 4+2+4+2+2+1 = 15 | yes |
| H | Kubernetes | 20 | 5+2+4+2+4+3 = 20 | yes |
| I | CI/CD | 20 | 4+3+3+4+3+2+1 = 20 | yes |
| J | Documentation, portfolio and reflection | 15 | 4+4+2+3+2 = 15 | yes |
| | **Total (A–J)** | **150 stated** | **175 computed** | **no (+25)** |
| | Parts A–G | "110 marks" (§5.1 p23) | 120 computed | no (+10) |
| | Parts H–J | not stated | 55 computed | — |
| | Bonus | "capped at +15" | 4+4+3+2+2 = 15 | yes |

## 2. Rubric items → requirement IDs

Item codes (`A1` … `J5`) are Phase 00 labels for easy reference; they are not part of the source.

### A · Collaboration and version control — 15

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| A1 | 3 | main protected: no direct push, PR required, CI required, ≥ 1 approval; screenshot in `docs/evidence/` | ASG-GH-001, ASG-CICD-011 |
| A2 | 2 | Two-branch model with dev plus feature branches; no work committed directly to main | ASG-GH-002, ASG-CICD-002 |
| A3 | 4 | ≥ 5 merged PRs, each linked to an Issue, each with a substantive partner review comment | ASG-GH-003, ASG-GH-004, ASG-GH-005 |
| A4 | 3 | ≥ 35 commits, conventional prefixes, neither partner below 35% by `git shortlog -sn` | ASG-GH-006, ASG-GH-007, ASG-GH-008 |
| A5 | 3 | One deliberate merge conflict on real code, resolved, with markers/resolution/merge evidence and 2–4 sentences on why that version won | ASG-GH-009, ASG-GH-010, ASG-GH-011 |

### B · Frontend — 18

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| B1 | 5 | Submit view: validation, honest loading state, renders category, priority, AI summary and provider | ASG-FR-004, -005, -006, -007 |
| B2 | 5 | Dashboard: pagination, filters, status transitions, server's 409 message surfaced verbatim | ASG-FR-008, -009, -010 |
| B3 | 3 | Stats view rendering aggregates and cache-hit state from X-Cache | ASG-FR-011, -012 |
| B4 | 3 | Runtime configuration — no baked-in API URL; one image runs in any environment | ASG-FR-016, -017 |
| B5 | 2 | ≥ 5 meaningful component tests passing in CI | ASG-NFR-014, ASG-CICD-006 |

### C · Backend — 25

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| C1 | 7 | All ten endpoints to contract, correct status codes, field-level validation errors | ASG-FR-020 … -033, ASG-FR-036 (nine listed; the instructor confirmed there is no tenth) |
| C2 | 4 | Four-layer separation: no SQL outside repositories, no business rules in routes | ASG-NFR-002 … -007 |
| C3 | 3 | Status state machine as an explicit transition table; invalid transitions 409 | ASG-FR-027, -028, -034, -035 |
| C4 | 3 | /health and /ready correctly distinguished; /health does not touch the database | ASG-FR-031, -032, ASG-K8S-017, -018 |
| C5 | 3 | Structured JSON logging to stdout with a propagated request_id | ASG-NFR-009, -010, -011 |
| C6 | 2 | SIGTERM handled: in-flight requests drain before exit | ASG-NFR-008 |
| C7 | 3 | ≥ 14 backend tests, unit and integration, deterministic, coverage ≥ 65% | ASG-NFR-012, -013, -015, ASG-CICD-005 |

### D · Data layer — 12

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| D1 | 4 | Alembic migrations; zero schema DDL in application startup code | ASG-DATA-002, -003, -004 |
| D2 | 3 | Schema complete including `triaged_by`, `ai_summary`, `triage_latency_ms`, timestamptz | ASG-DATA-005 … -015 |
| D3 | 2 | Two indexes, each justified by a named query in your notes | ASG-DATA-016, -017, -018 |
| D4 | 3 | Idempotent seed of ≥ 30 realistic complaints; running it twice changes nothing | ASG-DATA-019, -020, -021 |

### E · Cache layer — 10

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| E1 | 3 | `/api/stats` read-through cache, 30 s TTL, correct X-Cache header | ASG-CACHE-002, -003, -004 |
| E2 | 2 | Cache invalidated on write, not left to expire | ASG-CACHE-005 |
| E3 | 4 | Distributed Redis rate limiter on `POST /api/complaints`, 429 with Retry-After | ASG-CACHE-007 … -010, ASG-FR-022 |
| E4 | 1 | Redis AOF on a named volume, with your justification written down | ASG-CACHE-011, -012 |

### F · AI layer — 25

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| F1 | 5 | `TriageProvider` interface with ≥ 3 working implementations selected by environment variable | ASG-AI-002 … -008 |
| F2 | 5 | Structured output requested and validated against a Pydantic schema; malformed output rejected safely | ASG-AI-001, -010, -011, -012 |
| F3 | 6 | Timeout, single jittered retry on retryable errors only, fallback to rules, `triaged_by` recorded | ASG-AI-013, -014, -015, -022 |
| F4 | 3 | Content-hash caching of triage results with a measured, reported hit rate | ASG-AI-016, -017 |
| F5 | 3 | Prompt-injection guardrail plus a test that submits an injection attempt | ASG-AI-019, -020 |
| F6 | 2 | `triage_latency_ms` recorded and surfaced through `/api/meta/providers` | ASG-AI-023, ASG-DATA-014, ASG-FR-030 |
| F7 | 1 | PII/data-governance ADR: what leaves your machine, to whom, and why that is acceptable | ASG-AI-024, ASG-DOC-011 |

### G · Docker and Compose — 15

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| G1 | 4 | Both images multi-stage, pinned base, non-root USER, exec-form CMD, cache-correct layer order | ASG-DEVOPS-001 … -009 |
| G2 | 2 | `.dockerignore` per build context, with before/after context sizes reported | ASG-DEVOPS-010, -011, -012 |
| G3 | 4 | Two networks with `internal: true`; frontend provably cannot reach the database | ASG-DEVOPS-013 … -017 |
| G4 | 2 | Three named volumes, each justified; dev bind mount present and absent from prod | ASG-DEVOPS-019, -020 |
| G5 | 2 | Healthchecks on all services with `depends_on: condition: service_healthy` | ASG-DEVOPS-021, -022 |
| G6 | 1 | `compose.prod.yaml` uses `image: ${IMAGE_TAG}`, no `build:`, no published DB or cache port | ASG-DEVOPS-028, -029 |

### H · Kubernetes — 20

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| H1 | 5 | Namespace, Deployments, StatefulSet + PVC for Postgres, ClusterIP Services, Ingress routing `/` and `/api` | ASG-K8S-003 … -009 |
| H2 | 2 | ConfigMap and Secret separated; committed manifests carry placeholders only | ASG-K8S-010, -011 |
| H3 | 4 | All three probes correct: liveness independent of the database, readiness dependent on it | ASG-K8S-016, -017, -018 |
| H4 | 2 | `resources.requests` and `limits` set on every container | ASG-K8S-022 |
| H5 | 4 | HPA v2 with tuned behavior, plus captured `kubectl get hpa -w` output and a replicas-vs-load chart from a real load test | ASG-K8S-012 … -014, -023 … -026 |
| H6 | 3 | VPA in recommender mode, recommendations committed, requests updated in response, HPA/VPA conflict explained | ASG-K8S-028, -029, -030 |

### I · CI/CD — 20

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| I1 | 4 | `ci.yml` running lint, type check, backend and frontend tests on every PR, configured as required checks | ASG-CICD-003 … -006, -011 |
| I2 | 3 | Compose integration smoke job asserting a real request path end to end | ASG-CICD-010 |
| I3 | 3 | Trivy image scan and kubeconform manifest validation in CI | ASG-CICD-008, -009 |
| I4 | 4 | `cd.yml` with `needs:` gating publish, images pushed to GHCR tagged by commit SHA | ASG-CICD-012 … -014, -022, -023 |
| I5 | 3 | Kubernetes deploy job on an ephemeral cluster, waiting on rollout status and smoke-testing the Ingress | ASG-CICD-017 … -020 |
| I6 | 2 | Secrets from GitHub Secrets with a scoped token and a least-privilege `permissions:` block | ASG-CICD-024, -025 |
| I7 | 1 | Evidence of a red pipeline blocking a merge, then green | ASG-CICD-027 |

### J · Documentation, portfolio and reflection — 15

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| J1 | 4 | `README.md`: problem statement, badges, Mermaid architecture diagram, working one-command quickstart, API table, screenshots | ASG-DOC-001 … -006 |
| J2 | 4 | Four ADRs: provider interface; frontend runtime config; deploy-by-SHA; PII/data governance | ASG-DOC-008 … -011 |
| J3 | 2 | `docs/RUNBOOK.md`: how to deploy, roll back, read logs, and what to do when triage starts failing | ASG-DOC-013 |
| J4 | 3 | Demo video ≤ 5 minutes, both partners speaking, covering clean clone → running system, AI triage, fallback, network isolation failing, HPA scaling, rollback | ASG-DOC-014, -015 |
| J5 | 2 | `docs/ENGINEERING-NOTES.md` answering all eight questions in §5.2 with file-and-line references | ASG-DOC-016 … -024 |

### Bonus — capped at +15

| Code | Marks | Rubric line | Requirement IDs |
|---|---|---|---|
| BON1 | +4 | Zero-downtime rolling update demonstrated under live load with zero failed requests | ASG-BONUS-001, ASG-K8S-021 |
| BON2 | +4 | GitOps: Argo CD or Flux reconciling the cluster from the repository | ASG-BONUS-002 |
| BON3 | +3 | Deploy by image digest rather than tag, with Cosign signing and verification in CI | ASG-BONUS-003, -006, -007 |
| BON4 | +2 | Prometheus scraping `/metrics` plus a Grafana dashboard, screenshot committed | ASG-BONUS-004 |
| BON5 | +2 | OpenTelemetry tracing across frontend → backend → LLM call | ASG-BONUS-005 |

Bonus work is **never** started before every mandatory item in its area passes (project rule: no overbuilding).

## 3. Automatic deductions

| Points | Deduction (source §5.3 p24) | ID |
|---|---|---|
| −20 | A `.env`, key, token or password anywhere in Git history — plus rotate the credential and write an incident note | ASG-DED-001 |
| −15 | An LLM API key in a committed Kubernetes manifest, even base64-encoded | ASG-DED-002 |
| −8 | Unpinned base image, or postgres / redis / node without a tag | ASG-DED-003 |
| −8 | `localhost` used for service-to-service communication | ASG-DED-004 |
| −8 | Frontend able to reach the database — network segmentation not implemented | ASG-DED-005 |
| −8 | Published database or cache port in `compose.prod.yaml`, or a NodePort/LoadBalancer Service on the database | ASG-DED-006 |
| −8 | Publishing or deploying job not gated by `needs:` | ASG-DED-007 |
| −8 | Deploying `:latest` anywhere | ASG-DED-008 |
| −8 | PostgreSQL as a Deployment with no PVC | ASG-DED-009 |
| −5 | Commits pushed directly to main | ASG-DED-010 |
| −5 | README quickstart that does not work from a clean clone | ASG-DED-011 |

Maximum stated deductions: 20 + 15 + 8×7 + 5 + 5 = **101**. Treat every one as a release blocker.

## 4. Viva (multiplies the individual mark)

`Individual mark = team mark × viva factor` — 1.0 explains any part of the submission; 0.75 solid on own work, shaky on partner's; 0.5 describes what the code does but not why and cannot modify it live; 0.0 cannot explain the submission. Ten minutes each, individually, repository open, including questions on the partner's code. Requirement IDs: ASG-SUB-009, -010, -011.

Consequence for the workflow: every substantial piece of work must be explainable by **both** members (see [`TEAM_CONTRIBUTION.md`](TEAM_CONTRIBUTION.md) and [`AGENTS.md`](../AGENTS.md) §1).

## 5. Priority order when time is short (source §5.1)

F (AI layer) > C (backend) > I (CI/CD) > H (Kubernetes). "Never skip the fallback test" — ASG-AI-022.

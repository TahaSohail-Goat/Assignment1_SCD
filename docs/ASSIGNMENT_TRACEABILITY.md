# Assignment Traceability

Living index mapping **every obligation in the assignment** to a stable ID, an owner, an issue, an artifact, a verification method and evidence. Built in Phase 00 from the complete [`docx/ASSIGNMENT.md`](../docx/ASSIGNMENT.md) (transcription of `docx/ASSIGNMENT_SOURCE.pdf`).

- Source references are `§section pPDF-page`.
- Nothing here is invented. Where the source is unclear the row points at an extraction note (`EN-xx` in [`docx/EXTRACTION_NOTES.md`](../docx/EXTRACTION_NOTES.md)) or at the decisions table of [`SUBMISSION.md`](SUBMISSION.md).
- **Owner** and **Issue** come from the Phase 02–12 allocation in issue #18 (`docs/TEAM_CONTRIBUTION.md`): the issue is the work package that implements or evidences the row, the owner is that package's owner (the other person reviews). Rows still `TBD` have no implementing package: bonus items, policy and informational rows.
- Rubric marks and their mapping to these IDs live in [`RUBRIC.md`](RUBRIC.md); submission/viva/engineering-note items are expanded in [`SUBMISSION.md`](SUBMISSION.md).

## ID families

The pack's required families are used unchanged. Phase 00 adds four families for source content that has no home in them (recorded as an engineering decision; no assignment content is altered):

| Family | Covers | Origin |
|---|---|---|
| `ASG-GEN-*` | Team, scope, "what done means", meta-constraints | added in Phase 00 |
| `ASG-FR-*` | Functional behaviour: frontend views, API contract, domain rules | pack |
| `ASG-NFR-*` | Layering, logging, shutdown, testing, security constraints | pack |
| `ASG-DATA-*` | PostgreSQL, Alembic, schema, seed, persistence | pack |
| `ASG-CACHE-*` | Redis cache and rate limiter | pack |
| `ASG-AI-*` | Triage interface, providers, safeguards | pack |
| `ASG-DEVOPS-*` | Images, Compose, networks, volumes | pack |
| `ASG-K8S-*` | Kubernetes, HPA, VPA | pack |
| `ASG-CICD-*` | GitHub Actions, registry, rollback | pack |
| `ASG-GH-*` | Collaboration and version control | pack |
| `ASG-DOC-*` | README, ADRs, RUNBOOK, notes, video, evidence | pack |
| `ASG-BONUS-*` | Optional bonus work (capped) | pack |
| `ASG-DED-*` | Automatic deductions (release blockers) | added in Phase 00 |
| `ASG-SUB-*` | Submission, viva, policy | added in Phase 00 |
| `ASG-REPO-*` | Repository layout of §5.7 | added in Phase 00 |

## Legends

- **Type:** `Mandatory` · `Recommended` (source says recommended/permitted) · `Constraint` · `Evidence` (must be demonstrated/captured) · `Bonus` · `Policy` · `Advisory` (context, no test) · `Deduction`.
- **Verification:** `UT` unit test · `IT` integration test · `CI` CI job · `INS` inspection/lint · `CFG` config check · `DEMO` live/video demo · `MEAS` measurement · `DOC` document review.
- **Status:** `Not started` · `Skeleton` (directory placeholder only) · `Blocked` (waiting on a decision, see `SUBMISSION.md`) · `Info` (no implementation; tracked for awareness). `Implemented (P0x-Sxx, #issue)` (merged with tests or captures as evidence).

Columns follow the pack contract: `ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status`.

---

## ASG-GEN — General

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-GEN-001 | header p1 | Team of 2 members | Constraint | TBD | TBD | — | INS | `docs/TEAM_CONTRIBUTION.md` | Info |
| ASG-GEN-002 | header p1; §5.1 p23 | Duration stated as "2 Weeks" but §5.1 says four weeks; no deadline date given | Advisory | TBD | TBD | — | DOC | — | Info (deadline: `SUBMISSION.md`) |
| ASG-GEN-003 | header p1; §4 p19 | Total marks stated as 150; rubric sums to 175 | Advisory | TBD | TBD | — | DOC | `docs/RUBRIC.md` | Info (rubric left to the TA: `SUBMISSION.md`) |
| ASG-GEN-004 | §1.2 p2 | Product may be renamed; the contracts in §2 must be kept — they are what gets tested | Constraint | TBD | TBD | — | INS | — | Info |
| ASG-GEN-005 | §1.2 p2 | Whole system runs as five cooperating containers on a laptop with one command | Mandatory | Artfever | #55 | `compose.yaml` | DEMO | `docs/evidence/`, `ci.yml` integration job, `compose.yaml`, `docs/evidence/screenshots-clean-clone-log.txt` | Implemented; CI-run stack (database, cache, backend, frontend; Ollama behind `--profile offline`); demo video pending |
| ASG-GEN-006 | §1.2 p2 | System also runs as a scaled, probed, auto-scaling workload on a Kubernetes cluster in CI | Mandatory | Artfever | #55 | `k8s/`, `.github/workflows/cd.yml` | CI | CI run link, `k8s-quickstart.yml`, cd run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941, CD run 36230267941; `docs/evidence/k8s-load-README.md` | Implemented; CI-proven: `k8s-quickstart` workflow and `cd.yml` deploy (probed, HPA present) |
| ASG-GEN-007 | §1.4 p3 | A stranger clones the repository and, with one command, has the whole system running with seeded data | Mandatory | Artfever | #55 | `README.md`, `compose.yaml` | DEMO | clean-clone log, `README.md`, `ci.yml` integration job, `docs/evidence/screenshots-clean-clone-log.txt` | Implemented; the macOS/Linux command in the README is what the CI integration job runs on a clean runner, and the PowerShell block was verified on a clean clone (#100); clean-clone video pending |
| ASG-GEN-008 | §1.4 p3 | A second command puts the system on a Kubernetes cluster | Mandatory | Artfever | #55 | `k8s/`, `README.md` | DEMO | `docs/evidence/`, `scripts/k8s-up.sh`, `k8s-quickstart.yml`, `docs/evidence/screenshots-kubernetes-output.txt` | Implemented; `bash scripts/k8s-up.sh` runs on a clean runner in the `k8s-quickstart` workflow |
| ASG-GEN-009 | §1.4 p3 | A push to main tests it, builds signed and scanned images, deploys them, and can be undone in thirty seconds | Mandatory | Artfever | #55 | `.github/workflows/cd.yml` | CI, DEMO | CI run, rollback capture, `cd.yml`, `docs/evidence/cd-local-rollback.txt`, CD run 36230267941; `docs/evidence/k8s-rollback-index.md` | Implemented; cd run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 tested, published by SHA, scanned in CI, deployed; both rollbacks in `docs/RUNBOOK.md` (signing not required: `SUBMISSION.md`) |
| ASG-GEN-010 | §1.4 p3 | Every claim in the README can be demonstrated | Mandatory | Artfever | #55 | `README.md` | INS | `README.md`, `backend/tests/test_readme.py`, `docs/evidence/screenshots-README.md`; linked source/evidence | Implemented; README has a 'What is not shown' section and `test_readme.py` checks every link |
| ASG-GEN-011 | §5.1 p23 | Applicable configuration is "as written, teams of 2" (5 merged PRs, 35% commit floor); teams-of-3 and split-assignment variants do not apply | Constraint | TBD | TBD | — | DOC | — | Info |
| ASG-GEN-012 | §5.1 p23 | Priority order if behind: F (AI) > C (backend) > I (CI/CD) > H (Kubernetes); never skip the fallback test | Advisory | TBD | TBD | — | — | — | Info |
| ASG-GEN-013 | §1.3 p2 | Frontend must be an origin that is not localhost and needs CORS/build-step/runtime-config handling | Advisory | TBD | TBD | — | INS | — | Info |

## ASG-FR — Functional requirements

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-FR-001 | §2.1 p4 | Frontend stack is React 18 + Vite + TypeScript | Mandatory | Artfever | #34 | `frontend/package.json` | INS | `frontend/package.json` | Implemented (#34) |
| ASG-FR-002 | §2.1 p4 | Frontend presents only a submission form and an operations dashboard (plus stats view) — presentation and interaction; no business rules | Mandatory | Artfever | #35 | `frontend/src/` | INS | `frontend/src/App.tsx`, `frontend/src/pages/Stats.tsx` | Three views implemented (#35/#36) |
| ASG-FR-003 | §2.1 p4 | Category, priority and valid status transitions are decided by the backend and rendered by the frontend — never duplicated (no list of valid transitions in React) | Mandatory | Artfever | #35 | `frontend/src/` | INS, UT | `frontend/src/pages/Dashboard.tsx`, `frontend/tests/views.test.tsx` | Implemented (#35/#36) |
| ASG-FR-004 | §2.1 p4 | Submit view: free-text complaint, location, optional contact | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/src/pages/Submit.tsx`, `frontend/tests/views.test.tsx` | Implemented (#35/#36) |
| ASG-FR-005 | §2.1 p4 | Submit view: client-side validation that mirrors server rules without replacing them | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/src/pages/Submit.tsx`, `frontend/tests/views.test.tsx` | Implemented (#35/#36) |
| ASG-FR-006 | §2.1 p4 | Submit view shows the returned category, priority, AI summary and which provider produced it | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/src/pages/Submit.tsx`, `frontend/tests/views.test.tsx` | Implemented (#35); covered by the component tests |
| ASG-FR-007 | §2.1 p4 | Submit view renders the loading state honestly (AI calls take seconds) | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/tests/views.test.tsx` | Implemented (#35/#36); delayed request and 429 `Retry-After` tests pass |
| ASG-FR-008 | §2.1 p4; §4 B p19 | Dashboard: paginated, filterable list (category, priority, status) | Mandatory | Artfever | #35, #102 | `frontend/src/pages/` | UT | `frontend/src/pages/Dashboard.tsx`, `frontend/tests/views.test.tsx` | Implemented (#35, #36); #102 adds tested stale-row clearing, retry and last-page recovery (review pending) |
| ASG-FR-009 | §2.1 p4 | Dashboard: operator can advance status | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/src/pages/Dashboard.tsx`, `frontend/tests/views.test.tsx`, `docs/evidence/issue-35-409.png` | Implemented (#35/#36); forbidden transition captured |
| ASG-FR-010 | §2.1 p4; §4 B p19 | An invalid transition surfaces the server's 409 message (verbatim), not a generic "error" | Mandatory | Artfever | #35 | `frontend/src/pages/` | UT | `frontend/tests/views.test.tsx`, `docs/evidence/issue-35-409.png` | Component test passed (#36); screenshot captured (#35) |
| ASG-FR-011 | §2.1 p4 | Stats view: aggregate counts by category and priority | Mandatory | Artfever | #36 | `frontend/src/pages/` | UT | `frontend/tests/views.test.tsx`, `docs/evidence/issue-36-stats-hit.png` | Implemented (#36); screenshot captured |
| ASG-FR-012 | §2.1 p4 | Stats view displays whether the response was a cache hit, from the X-Cache header | Mandatory | Artfever | #36 | `frontend/src/pages/` | UT | `frontend/tests/views.test.tsx`, `docs/evidence/issue-36-stats-hit.png` | Implemented (#36); HIT/MISS/missing tested; screenshot captured |
| ASG-FR-013 | §2.1 p5 | Typed API client generated from or checked against the backend's OpenAPI schema | Mandatory | Artfever | #34 | `frontend/src/api/` | CI, INS | `frontend/src/api/check-contract.mjs`, `backend/tests/test_contract.py` | Implemented (#34, #39): `check:api-contract` and `test_contract.py` compare the snapshot with the served OpenAPI |
| ASG-FR-014 | §2.1 p5 | Frontend has an error boundary | Mandatory | Artfever | #36 | `frontend/src/components/` | UT | `frontend/tests/views.test.tsx` | Implemented (#36) |
| ASG-FR-015 | §2.1 p5 | No secrets in frontend code (everything in a browser bundle is public) | Mandatory | Artfever | #34 | `frontend/` | INS | bundle scan, `frontend/src/`, `docs/adr/0002-frontend-runtime-config.md` | Implemented (#34): no key or secret in `frontend/src`; the API is same-origin |
| ASG-FR-016 | §2.1 p4; §4 B p19 | Runtime configuration: no baked-in API URL; one image runs in any environment (build-once-deploy-many) | Mandatory | Artfever | #34 | `frontend/nginx.conf`, entrypoint | DEMO | two-env run, `frontend/nginx.conf`, ADR 0002 | Implemented (#34, #48): relative `/api` calls, nginx proxy; one image for every environment |
| ASG-FR-017 | §2.1 p4 | Mechanism is `/config.js` generated at container start from env vars **or** nginx proxy of `/api`; the choice is stated in an ADR | Mandatory | Artfever | #34 | `docs/adr/0002-frontend-runtime-config.md` | DOC | `docs/adr/0002-frontend-runtime-config.md` | Implemented (#34, #48): the nginx-proxy option, stated in ADR 0002 |
| ASG-FR-020 | §2.2 p5 | `POST /api/complaints`: validate → triage → persist; respond 201 | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented for validate and persist (P04-S02, #38); triage in #44, limiter in #43 |
| ASG-FR-021 | §2.2 p5 | `POST /api/complaints` returns 400 with a field-level error body on invalid input | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-022 | §2.2 p5 | `POST /api/complaints` returns 429 when the caller exceeds the rate limit (mechanism: ASG-CACHE-007…009) | Mandatory | Artfever | #43 | `backend/app/routes/` | IT | `backend/tests/test_rate_limit.py`, `ci.yml` integration job | Implemented (#43); a real Redis 429 with `Retry-After` is checked by the CI integration job (RUNBOOK section 8) |
| ASG-FR-023 | §2.2 p5 | `GET /api/complaints/{id}` returns 200 or 404 | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-024 | §2.2 p6 | `GET /api/complaints` filters by category, priority, status | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-025 | §2.2 p6 | `GET /api/complaints` paginates with `page` and `page_size` (≤ 100) | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-026 | §2.2 p6 | `GET /api/complaints` returns `total` | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-027 | §2.2 p6 | `PATCH /api/complaints/{id}/status` enforces the state machine | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/`, `services/` | IT | `backend/tests/test_complaints_api.py`, `backend/tests/test_state_machine.py` | Implemented (P04-S02, #38) |
| ASG-FR-028 | §2.2 p6 | Invalid transition returns 409 naming the attempted transition | Mandatory | TahaSohail-Goat | #38 | `backend/app/services/` | UT, IT | `backend/tests/test_complaints_api.py` | Implemented (P04-S02, #38) |
| ASG-FR-029 | §2.2 p6 | `GET /api/stats` returns aggregates (counts by category and priority per ASG-FR-011); caching per ASG-CACHE-002…005 | Mandatory | TahaSohail-Goat | #42 | `backend/app/services/` | IT | `backend/tests/test_stats_api.py`, `backend/tests/test_stats_service.py` | Implemented (P06-S01, #42) |
| ASG-FR-030 | §2.2 p6 | `GET /api/meta/providers` returns which triage provider is active and the last 20 triage outcomes (provider, latency ms, fallback y/n) | Mandatory | Artfever | #46 | `backend/app/routes/` | IT | `backend/tests/test_meta.py` | Implemented (#46) |
| ASG-FR-031 | §2.2 p6 | `GET /health` is liveness: process is alive; must not touch the database | Mandatory | TahaSohail-Goat | #37 | `backend/app/routes/` | UT, IT | `backend/tests/test_health.py` | Implemented (P04-S01, #37) |
| ASG-FR-032 | §2.2 p6 | `GET /ready` returns 200 only if Postgres and Redis are both reachable; 503 naming the failed dependency | Mandatory | TahaSohail-Goat | #37 | `backend/app/routes/` | IT | `backend/tests/test_ready.py` | Implemented (P04-S01, #37) |
| ASG-FR-033 | §2.2 p6 | `GET /metrics` exposes Prometheus text format: request count, request latency histogram, triage latency, fallback counter | Mandatory | TahaSohail-Goat | #37 | `backend/app/routes/` | IT | `backend/tests/test_metrics.py` | Implemented (P04-S01, #37) |
| ASG-FR-034 | §2.2 p6 | Status state machine: open→in_progress→resolved; open→rejected; in_progress→rejected; resolved and rejected are terminal; everything else is 409 | Mandatory | TahaSohail-Goat | #38 | `backend/app/services/` | UT | `backend/tests/test_state_machine.py` | Implemented (P04-S02, #38) |
| ASG-FR-035 | §2.2 p6 | The state machine is an explicit transition table, not a chain of ifs | Mandatory | TahaSohail-Goat | #38 | `backend/app/services/` | INS, UT | `backend/tests/test_state_machine.py` | Implemented (P04-S02, #38) |
| ASG-FR-036 | §4 C p19 | All endpoints in the API contract are implemented to contract with correct status codes (rubric says "ten"; the table lists nine) | Mandatory | TahaSohail-Goat | #39 | `backend/app/routes/` | IT | `backend/tests/test_contract.py` | Implemented for eight of nine endpoints (P04-S03, #39); GET /api/meta/providers is enforced once #46 merges |
| ASG-FR-037 | §1.2 p2 | End-to-end intake flow: citizen submits → system validates → triages (category, priority, one-line summary) → persists durably → shown on live operations dashboard with aggregate statistics | Mandatory | TahaSohail-Goat | #53 | whole system | IT, DEMO | demo video, `ci.yml` integration job, `frontend/tests/views.test.tsx` | Implemented (#38, #46, #35); the CI integration job creates and reads a complaint end to end; demo video pending |

## ASG-NFR — Non-functional requirements

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-NFR-001 | §2.2 p5 | Backend is FastAPI + Pydantic v2 (recommended) or Flask (permitted; must be stated in README) | Recommended | TahaSohail-Goat | #37 | `backend/pyproject.toml` | INS | `backend/pyproject.toml` | Implemented (P04-S01, #37) |
| ASG-NFR-002 | §2.2 p5 | Four layers `routes/ services/ repositories/ providers/`; dependency arrows point one way only | Mandatory | TahaSohail-Goat | #38 | `backend/app/` | INS | `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-003 | §2.2 p5 | `routes/`: HTTP only — parse, validate, serialise, status codes; no business rules | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | INS | `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-004 | §2.2 p5 | `services/`: business rules — triage orchestration, state machine, statistics | Mandatory | TahaSohail-Goat | #38 | `backend/app/services/` | INS | `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-005 | §2.2 p5 | `repositories/`: all SQL lives here and nowhere else | Mandatory | TahaSohail-Goat | #38 | `backend/app/repositories/` | INS, CI | `backend/tests/test_no_ddl_in_app.py`, `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-006 | §2.2 p5 | `providers/`: outbound integrations (LLM, cache) behind interfaces | Mandatory | TahaSohail-Goat | #38 | `backend/app/providers/` | INS | `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-007 | §2.2 p5 | A route must not open a database session | Mandatory | TahaSohail-Goat | #38 | `backend/app/routes/` | INS | `backend/tests/test_layering.py` | Implemented (P04-S02, #38) |
| ASG-NFR-008 | §2.2 p7 | Graceful shutdown on SIGTERM: stop accepting new requests, finish in-flight, close pool connections, exit | Mandatory | TahaSohail-Goat | #37 | `backend/app/` | IT, DEMO | `backend/tests/test_graceful_shutdown.py` | Implemented (P04-S01, #37) |
| ASG-NFR-009 | §2.2 p7 | Structured logging: JSON to stdout, never to a file | Mandatory | TahaSohail-Goat | #37 | `backend/app/` | UT, INS | `backend/tests/test_logging.py` | Implemented (P04-S01, #37) |
| ASG-NFR-010 | §2.2 p7 | Every log line carries `request_id` propagated from the `X-Request-ID` header (generate one if absent) | Mandatory | TahaSohail-Goat | #37 | `backend/app/` | UT | `backend/tests/test_request_context.py`, `backend/tests/test_logging.py` | Implemented (P04-S01, #37) |
| ASG-NFR-011 | §2.2 p7 | One WARNING per triage fallback with the complaint id, the provider and the error class | Mandatory | TahaSohail-Goat | #44 | `backend/app/services/` | UT | `backend/tests/test_triage_service.py` | Implemented (P07-S01, #44) |
| ASG-NFR-012 | §4 C p20 | ≥ 14 backend tests, unit and integration, deterministic | Mandatory | TahaSohail-Goat | #39 | `backend/tests/` | CI | `backend/tests/` (249 tests) | Implemented (P04-S03, #39) |
| ASG-NFR-013 | §3.4 p17; §4 C p20 | Backend coverage ≥ 65% on `app/` | Mandatory | TahaSohail-Goat | #39 | `backend/pyproject.toml` | CI | `backend/pyproject.toml` (`--cov-fail-under=65`), coverage 97% | Implemented (P04-S03, #39) |
| ASG-NFR-014 | §3.4 p17; §4 B p19 | ≥ 5 meaningful frontend component tests (Vitest) passing in CI | Mandatory | Artfever | #36, #102 | `frontend/tests/` | CI | `frontend/tests/views.test.tsx` (13 passing locally) | Implemented (#36); #102 adds two reproduced Dashboard regressions; CI/review pending on follow-up |
| ASG-NFR-015 | §2.5 p11–12 | Test suite is green on every run; no `time.sleep()` and no re-runs to get a pass — determinism by design | Mandatory | TahaSohail-Goat | #39 | `backend/tests/` | CI | `backend/tests/test_determinism.py`, ten green runs in a row | Implemented (P04-S03, #39) |
| ASG-NFR-016 | §5.3 p24; §3.4 p17 | No `localhost` for service-to-service communication (containers/pods use service names) | Constraint | TahaSohail-Goat | #47 | `compose*.yaml`, `k8s/` | INS, CI | integration job, `backend/tests/test_container_files.py`, `scripts/check_submission.py` | Implemented (#47, #49, #91): service names in Compose and Kubernetes; `check_submission.py` scans both |
| ASG-NFR-017 | §2.1 p5 | Anything in the browser bundle is public: no credentials/keys in build output ("it's minified" is not a defence) | Constraint | Artfever | #34 | `frontend/` | INS | bundle scan, `scripts/check_submission.py` | Implemented (#34): no credential in the bundle; `check_submission.py` scans for key patterns |

## ASG-DATA — Data layer

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-DATA-001 | §2.3 p7 | PostgreSQL 16 | Mandatory | TahaSohail-Goat | #40 | `compose.yaml`, `k8s/base/postgres.yaml` | CFG | `compose.yaml`, `k8s/base/postgres.yaml` | Implemented (#40, #47): `postgres:16.10-alpine` in Compose, CI and Kubernetes |
| ASG-DATA-002 | §2.3 p7 | Schema managed by Alembic migrations | Mandatory | TahaSohail-Goat | #40 | `backend/alembic/versions/` | INS, IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-003 | §2.3 p7; §4 D p20 | No `CREATE TABLE` / schema DDL in application startup code, ever | Mandatory | TahaSohail-Goat | #40 | `backend/app/` | INS, CI | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-004 | §2.3 p7 | Migrations are versioned, reviewable and reversible (upgrade and downgrade) | Mandatory | TahaSohail-Goat | #40 | `backend/alembic/versions/` | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-005 | §2.3 p7 | `id`: UUID, server-generated | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-006 | §2.3 p7 | `text`: 10–2000 chars, enforced in the DB (constraint) as well as the app | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-007 | §2.3 p7 | `location`: 3–200 chars | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-008 | §2.3 p7 | `reporter_contact`: nullable | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-009 | §2.3 p7 | `category` enum: water, electricity, sanitation, roads, streetlights, other | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-010 | §2.3 p7 | `priority` enum: high, normal, low | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-011 | §2.3 p7 | `status` enum: open, in_progress, resolved, rejected; default open | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-012 | §2.3 p7 | `ai_summary`: nullable, one line, ≤ 140 chars | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-013 | §2.3 p7 | `triaged_by`: llm:groq, llm:ollama, rules, rules:fallback (values for simulated/other hosted providers unspecified) | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-014 | §2.3 p8 | `triage_latency_ms`: integer | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-015 | §2.3 p8 | `created_at` / `updated_at`: timestamptz, UTC | Mandatory | TahaSohail-Goat | #40 | migration | IT | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-016 | §2.3 p8 | Index on `(status, priority)` | Mandatory | TahaSohail-Goat | #40 | migration | INS | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-017 | §2.3 p8 | Index on `created_at` | Mandatory | TahaSohail-Goat | #40 | migration | INS | `backend/alembic/versions/0001_create_complaints.py`, `backend/tests/test_migrations.py` | Implemented (P05-S01, #40) |
| ASG-DATA-018 | §2.3 p8; §4 D p20 | Engineering notes state, per index, which query it serves | Evidence | TahaSohail-Goat | #40 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/DATA_MODEL.md` | Implemented (P05-S01, #40) |
| ASG-DATA-019 | §2.3 p8 | Idempotent seed command loading ≥ 30 realistic complaints | Mandatory | Artfever | #41 | `backend/` seed | IT | `backend/app/seed.py`, `backend/tests/test_seed.py` | Implemented (#41); PostgreSQL CI passed on PR #79 |
| ASG-DATA-020 | §2.3 p8 | Seed complaints are in Urdu-influenced English, spread across categories | Mandatory | Artfever | #41 | seed data | INS | `backend/app/seed.py` | Implemented (#41) |
| ASG-DATA-021 | §2.3 p8 | Running the seed twice does not duplicate rows | Mandatory | Artfever | #41 | seed | IT | `backend/tests/test_seed.py` | Implemented (#41); PostgreSQL CI passed on PR #79 |
| ASG-DATA-022 | §2.3 p8 | `docker compose down` then `up` preserves every row | Evidence | TahaSohail-Goat | #53 | `compose.yaml` (`pgdata`) | DEMO | `docs/evidence/`, `ci.yml` step | CI evidence (P11, #53): rows survive `down` then `up`, run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36189116384; video demo pending |
| ASG-DATA-023 | §2.3 p8 | On Kubernetes, deleting the Postgres pod preserves every row | Evidence | Artfever | #54 | `k8s/base/postgres.yaml` | DEMO | `docs/evidence/k8s-pg-persistence.txt`, `k8s-quickstart.yml` | Done: 30 rows and a full-row fingerprint preserved when `database-0` is deleted (local capture, reviewed in #96; repeated on a clean runner by `k8s-quickstart`) |

## ASG-CACHE — Cache layer

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-CACHE-001 | §2.4 p8 | Redis 7 | Mandatory | TahaSohail-Goat | #42 | `compose.yaml`, `k8s/base/redis.yaml` | CFG | `compose.yaml`, `k8s/base/redis.yaml` | Implemented (#42, #47): `redis:7.4.11-alpine` |
| ASG-CACHE-002 | §2.4 p8 | Job 1: read-through cache for `/api/stats` | Mandatory | TahaSohail-Goat | #42 | `backend/app/services/` | IT | `backend/tests/test_stats_service.py` | Implemented (P06-S01, #42) |
| ASG-CACHE-003 | §2.4 p8 | Stats cache TTL is 30 s | Mandatory | TahaSohail-Goat | #42 | `backend/app/` | IT | `backend/tests/test_redis_cache.py`, `backend/tests/test_stats_service.py` | Implemented (P06-S01, #42) |
| ASG-CACHE-004 | §2.4 p8 | `/api/stats` responds with `X-Cache: HIT` or `MISS` | Mandatory | TahaSohail-Goat | #42 | `backend/app/routes/` | IT | `backend/tests/test_stats_api.py` | Implemented (P06-S01, #42) |
| ASG-CACHE-005 | §2.4 p8 | Cache is invalidated on write, so a new complaint appears in stats immediately | Mandatory | TahaSohail-Goat | #42 | `backend/app/services/` | IT | `backend/tests/test_stats_service.py`, `backend/tests/test_stats_api.py` | Implemented (P06-S01, #42) |
| ASG-CACHE-006 | §2.4 p8 | Be able to explain at viva why TTL **and** explicit invalidation are both used | Evidence | TahaSohail-Goat | #42 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/CACHE.md`, `backend/tests/test_stats_service.py` | Implemented (P06-S01, #42) |
| ASG-CACHE-007 | §2.4 p8 | Job 2: distributed rate limiter (fixed-window or token-bucket) in Redis, keyed by client IP | Mandatory | Artfever | #43 | `backend/app/` | IT | `backend/tests/test_rate_limit.py`, `ci.yml` | Implemented (#43); checked against a real Redis in the CI integration job |
| ASG-CACHE-008 | §2.4 p8 | Rate limiter protects `POST /api/complaints` | Mandatory | Artfever | #43 | `backend/app/routes/` | IT | `backend/tests/test_rate_limit.py` | Implemented (#43) |
| ASG-CACHE-009 | §2.4 p8 | When exceeded: 429 with a `Retry-After` header | Mandatory | Artfever | #43 | `backend/app/` | IT | `backend/tests/test_rate_limit.py`, `ci.yml` | Implemented (#43); the CI integration job prints the 429 and its `Retry-After` |
| ASG-CACHE-010 | §2.4 p8 | Limiter is distributed (Redis), not an in-process dictionary (holds under HPA scale-out) | Constraint | Artfever | #43 | `backend/app/` | INS | `backend/tests/test_rate_limit.py` (two app instances), `k8s-quickstart.yml` | Implemented (#43); `k8s-quickstart` sends requests through the Ingress to two backend replicas and sees the shared limit answer 429 |
| ASG-CACHE-011 | §2.4 p9 | Redis AOF enabled on a named volume | Mandatory | TahaSohail-Goat | #47 | `compose.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); restart check in #53 |
| ASG-CACHE-012 | §2.4 p9 | Written justification: why the cache needs a volume although a cache can be rebuilt | Evidence | Artfever | #43 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/CACHE.md`, `docs/ENGINEERING-NOTES.md` | Decision recorded (#43) |

## ASG-AI — AI layer

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-AI-001 | §2.5 p9 | `TriageResult` Pydantic model: `category: Category`, `priority: Priority`, `summary: str` (max 140), `confidence: float` (0.0–1.0) | Mandatory | TahaSohail-Goat | #44 | `backend/app/providers/triage/base.py` | UT | `backend/tests/test_triage_providers.py` | Implemented (P07-S01, #44) |
| ASG-AI-002 | §2.5 p9 | `TriageProvider` Protocol: `name: str`; `triage(text, location) -> TriageResult` | Mandatory | TahaSohail-Goat | #44 | `backend/app/providers/triage/base.py` | UT | `backend/tests/test_triage_providers.py` | Implemented (P07-S01, #44) |
| ASG-AI-003 | §2.5 p9; §4 F p20 | Implementations `LLMTriage`, `OllamaTriage`, `RuleBasedTriage`, `SimulatedTriage` (at least 3 working) | Mandatory | TahaSohail-Goat | #44 | `backend/app/providers/triage/` | UT | `backend/tests/test_triage_providers.py`, `backend/tests/test_remote_triage.py` | All four implemented across #44/#45; live paths pending |
| ASG-AI-004 | §2.5 p9 | Provider is selected by the `TRIAGE_PROVIDER` environment variable | Mandatory | TahaSohail-Goat | #44 | `.../triage/factory.py` | UT | `backend/tests/test_triage_providers.py`, `backend/tests/test_remote_triage.py` | Implemented for all four providers (#44/#45) |
| ASG-AI-005 | §2.5 p9–10 | `LLMTriage`: production path calling a free-tier hosted model (Groq recommended primary; Gemini recommended alternative; OpenRouter / Cloudflare Workers AI / Hugging Face acceptable if free and documented) | Mandatory | Artfever | #45 | `.../triage/llm.py` | UT (mocked), DEMO | `backend/tests/test_remote_triage.py`, `docs/ENGINEERING-NOTES.md` | Implemented (#45); live call pending |
| ASG-AI-006 | §2.5 p9–10 | `OllamaTriage`: fully offline path; Ollama runs as a container in the Compose stack (1B-parameter model); same interface | Mandatory | Artfever | #45 | `.../triage/ollama.py`, `compose.yaml` | UT (mocked), DEMO | `backend/tests/test_remote_triage.py`, `compose.yaml` | Implemented (#45, #48): the Ollama service and the model preload are in Compose (`--profile offline`); not exercised end to end in CI |
| ASG-AI-007 | §2.5 p9 | `RuleBasedTriage`: deterministic keyword fallback; always available; never fails | Mandatory | TahaSohail-Goat | #44 | `.../triage/rules.py` | UT | `backend/tests/test_triage_providers.py` | Implemented (P07-S01, #44) |
| ASG-AI-008 | §2.5 p9 | `SimulatedTriage`: deterministic fake for CI — seeded, no network, configurable failure injection | Mandatory | TahaSohail-Goat | #44 | `.../triage/simulated.py` | UT | `backend/tests/test_triage_providers.py` | Implemented (P07-S01, #44) |
| ASG-AI-009 | §2.5 p10 | Chosen hosted provider is free and documented; cite the live limits actually observed in the notes | Evidence | Artfever | #45 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/ENGINEERING-NOTES.md` (published limits and source) | Published limits checked (#45); account-specific live check pending |
| ASG-AI-010 | §2.5 p11 | Structured output is requested from the model (JSON mode, tool calling, or response schema) | Mandatory | Artfever | #45 | `.../triage/llm.py` | UT | `backend/tests/test_remote_triage.py` | Implemented (#45) |
| ASG-AI-011 | §2.5 p11 | The response is validated against the Pydantic model regardless; malformed output (prose, code fence, out-of-enum category, over-long summary) is rejected safely | Mandatory | Artfever | #45 | `.../triage/` | UT | `backend/tests/test_remote_triage.py` | Implemented (#45) |
| ASG-AI-012 | §2.5 p11 | Never `eval` model output; never build SQL from model output | Constraint | Artfever | #45 | `backend/app/` | INS | `backend/app/providers/triage/llm.py` | Inspected (#45) |
| ASG-AI-013 | §2.5 p11 | Hard timeout of 10 seconds on every LLM call | Mandatory | Artfever | #45 | `.../triage/llm.py` | UT | `backend/tests/test_triage_service.py`, `backend/tests/test_remote_triage.py` | Orchestration and HTTP call timeouts implemented (#44/#45) |
| ASG-AI-014 | §2.5 p11 | Retry once with jitter — on timeout, 429 and 5xx only; never retry a 400 | Mandatory | Artfever | #45 | `.../triage/` | UT | `backend/tests/test_triage_service.py` | Implemented (P07-S01, #44) |
| ASG-AI-015 | §2.5 p11 | Fall back to `RuleBasedTriage` and record `triaged_by = "rules:fallback"`; a user never sees a 500 because a third party was rate-limited | Mandatory | TahaSohail-Goat | #44 | `backend/app/services/` | UT, IT | `backend/tests/test_triage_service.py`, `backend/tests/test_complaints_api.py` | Implemented (P07-S01, #44) |
| ASG-AI-016 | §2.5 p11 | Cache triage results by content hash in Redis, 24 h TTL | Mandatory | Artfever | #46 | `backend/app/services/` | IT | `backend/tests/test_injection_cache.py` | Implemented with in-memory store (#46); real Redis verification pending |
| ASG-AI-017 | §2.5 p11 | Report the measured hit rate of the content-hash cache | Evidence | Artfever | #46 | `docs/ENGINEERING-NOTES.md` | MEAS | `docs/TRIAGE.md` (1 hit / 2 requests, in-memory) | Test interval measured (#46); real Redis workload pending |
| ASG-AI-018 | §2.5 p11 | Never log the API key; it comes from the environment / Kubernetes Secret / GitHub Secrets, never from a file in the repository | Constraint | Artfever | #45 | `backend/app/`, `k8s/`, workflows | INS, UT | `backend/tests/test_remote_triage.py` | Provider checked (#45); deployment secrets pending |
| ASG-AI-019 | §2.5 p11 | Prompt-injection guardrail: complaint text is untrusted data — delimit it clearly, constrain output to the enum, reject anything outside it | Mandatory | Artfever | #46 | `.../triage/` | UT | `backend/tests/test_injection_cache.py`; hosted delimiter in #45 | Implemented across #45/#46 |
| ASG-AI-020 | §2.5 p11 | One test submits an injection attempt and asserts the category is still decided by the schema | Mandatory | Artfever | #46 | `backend/tests/` | UT | `test_injection_attempt_cannot_override_schema_category` | Implemented (#46) |
| ASG-AI-021 | §2.5 p12 | CI is pinned to `SimulatedTriage`; a provider that always raises tests the fallback; a provider returning malformed JSON tests the validator | Mandatory | TahaSohail-Goat | #44 | `backend/tests/`, `ci.yml` | UT, CI | `backend/tests/test_triage_service.py` | Implemented (P07-S01, #44) |
| ASG-AI-022 | §2.5 p12 | Test: given a provider that always raises, `POST /api/complaints` still returns 201 and `triaged_by == "rules:fallback"` | Mandatory | TahaSohail-Goat | #44 | `backend/tests/` | IT | `backend/tests/test_complaints_api.py`, `backend/tests/test_complaints_integration.py` | Implemented (P07-S01, #44) |
| ASG-AI-023 | §2.3 p8; §4 F p20 | `triage_latency_ms` is recorded per complaint and surfaced through `/api/meta/providers` | Mandatory | Artfever | #46 | `backend/app/` | IT | `backend/tests/test_meta.py`, `backend/tests/test_injection_cache.py` | Implemented (#46) |
| ASG-AI-024 | §2.5 p10; §4 F p21 | PII / data-governance decision recorded in an ADR: what leaves the machine, to whom, and why that is acceptable (redact, send body only, or accept and document) | Mandatory | Artfever | #46 | `docs/adr/0004-pii-and-data-governance.md` | DOC | `docs/adr/0004-pii-and-data-governance.md` | Decision recorded (#46); deployment check pending |
| ASG-AI-025 | §2.5 p10 | Measure (not assert) the hosted-vs-Ollama trade-off: quality and latency of the offline path | Recommended | Artfever | #45 | `docs/ENGINEERING-NOTES.md` | MEAS | measurement log | Not done: needs a live hosted key and an Ollama model; stated in the README and `docs/ENGINEERING-NOTES.md` |

## ASG-DEVOPS — Images and Compose

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-DEVOPS-001 | §3.1 p12 | Two images (backend, frontend), both multi-stage, pinned, non-root | Mandatory | TahaSohail-Goat | #47 | `*/Dockerfile` | INS, CI | `backend/tests/test_container_files.py`, `backend/Dockerfile`, `frontend/Dockerfile` | Implemented (#47, #48): both images multi-stage, pinned, non-root |
| ASG-DEVOPS-002 | §3.1 p12 | Backend base is `python:3.12-slim` | Mandatory | TahaSohail-Goat | #47 | `backend/Dockerfile` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-003 | §3.1 p12 | Backend dependencies installed in a builder stage | Mandatory | TahaSohail-Goat | #47 | `backend/Dockerfile` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-004 | §3.1 p12 | Cache-friendly COPY order (requirements before source) | Mandatory | TahaSohail-Goat | #47 | `backend/Dockerfile` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-005 | §3.1 p12 | Backend runs as a non-root `USER` | Mandatory | TahaSohail-Goat | #47 | `backend/Dockerfile` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-006 | §3.1 p12 | Backend `CMD` in exec form | Mandatory | TahaSohail-Goat | #47 | `backend/Dockerfile` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-007 | §3.1 p12 | `HEALTHCHECK` declared | Mandatory | TahaSohail-Goat | #47 | `*/Dockerfile` | INS | `backend/tests/test_container_files.py`, `backend/Dockerfile`, `frontend/Dockerfile` | Implemented (#47, #48): `HEALTHCHECK` in both Dockerfiles |
| ASG-DEVOPS-008 | §3.1 p12 | Frontend builds with `node:22-alpine` and serves with `nginx:1.27-alpine` | Mandatory | Artfever | #48 | `frontend/Dockerfile` | INS | — | Built in CI (#91, 2936f8a); pinned Node 22 and nginx 1.27, non-root runtime |
| ASG-DEVOPS-009 | §3.1 p12 | Final frontend image contains no Node, no `node_modules`, no source | Mandatory | Artfever | #48 | `frontend/Dockerfile` | INS | `docker history` | CI (#91, 2936f8a) checked runtime has no Node, node_modules or source |
| ASG-DEVOPS-010 | §3.1 p12 | Report both stage sizes; a frontend image over ~60 MB indicates the multi-stage split is not working | Evidence | TahaSohail-Goat | #53 | `README.md` / notes | MEAS | size capture, `docs/evidence/container-sizes.md` | CI (#91, 2936f8a): builder 288 MB, security-updated runtime 60.1 MB (~60 MB guide) |
| ASG-DEVOPS-011 | §3.1 p12 | `.dockerignore` in each build context excluding `.git`, `node_modules`, `.venv`, `__pycache__`, `.env`, test fixtures | Mandatory | TahaSohail-Goat | #47 | `backend/.dockerignore`, `frontend/.dockerignore` | INS | `backend/tests/test_container_files.py` | Frontend ignore measured in CI (#91, 2936f8a) |
| ASG-DEVOPS-012 | §3.1 p12 | Report build-context size before and after `.dockerignore`, with numbers | Evidence | TahaSohail-Goat | #53 | notes | MEAS | size capture, `docs/evidence/container-sizes.md` | CI (#91, 2936f8a): frontend context 105.95 MB without ignore, 160.17 kB with ignore |
| ASG-DEVOPS-013 | §3.2 p12–13 | Two Compose networks: `edge` (bridge) and `internal` (bridge, `internal: true`) | Mandatory | TahaSohail-Goat | #47 | `compose.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-014 | §3.2 p13 | frontend joins `edge` only | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | — | Frontend edge-only in both Compose files; CI integration green (#91, 2936f8a) |
| ASG-DEVOPS-015 | §3.2 p13 | backend joins both networks — the only service that bridges them | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-016 | §3.2 p13 | database and cache join `internal` only | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-017 | §3.2 p13 | `docker compose exec frontend ping database` must fail; demonstrate the failure in the video | Evidence | Artfever | #48 | — | DEMO | video + capture | CI (#91, 2936f8a): ping failed with bad address database; video pending |
| ASG-DEVOPS-018 | §3.2 p13 | Resolve and document where the hosted-LLM caller lives given `internal: true` (more than one defensible design) | Evidence | Artfever | #32 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/ENGINEERING-NOTES.md` | Implemented (#32, #54): answered in `docs/ENGINEERING-NOTES.md` Q7 and `docs/ARCHITECTURE.md` |
| ASG-DEVOPS-019 | §3.2 p13 | Three named volumes `pgdata`, `redisdata`, `ollama_models`, each justified | Mandatory | TahaSohail-Goat | #47 | `compose.yaml` | CFG, DOC | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-020 | §3.2 p13 | Development-only bind mount of source into the backend for hot reload; present in `compose.yaml`, absent from `compose.prod.yaml`; one sentence on why | Mandatory | TahaSohail-Goat | #47 | `compose.yaml` | CFG, DOC | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-021 | §3.2 p13 | Healthchecks on every service | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-022 | §3.2 p13 | `depends_on` with `condition: service_healthy` | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-023 | §3.2 p13 | All credentials via `${...}` from `.env` | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-024 | §3.2 p13 | `.env.example` committed; `.env` gitignored | Mandatory | TahaSohail-Goat | #47 | `.env.example`, `.gitignore` | INS | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-025 | §3.2 p13 | Every image tag pinned | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml`, Dockerfiles | INS, CI | `backend/tests/test_container_files.py`, `scripts/check_submission.py` | Implemented: every image tag pinned; the backend base image is also pinned by digest |
| ASG-DEVOPS-026 | §3.2 p13 | `restart: unless-stopped` | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-027 | §3.2 p13 | Resource limits under `deploy.resources` | Mandatory | TahaSohail-Goat | #47 | `compose*.yaml` | CFG | `backend/tests/test_container_files.py` | Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-028 | §3.2 p13 | No published port on database or cache in the production file | Mandatory | Artfever | #48 | `compose.prod.yaml` | CFG, CI | — | Production Compose has no database/cache ports; static check and CI green (#91, 2936f8a) |
| ASG-DEVOPS-029 | §3.2 p14 | Two files: `compose.yaml` (dev, `build:`) and `compose.prod.yaml` (deploy, `image:` with `${IMAGE_TAG}`, no `build:` key anywhere) | Mandatory | Artfever | #48 | `compose.yaml`, `compose.prod.yaml` | CFG, CI | — | Standalone image-only production Compose added; static check and CI green (#91, 2936f8a) |

## ASG-K8S — Kubernetes

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-K8S-001 | §3.3 p14 | Local cluster is k3d or kind (managed cloud not required, earns no extra marks) | Mandatory | TahaSohail-Goat | #49 | — | DEMO | `scripts/k8s-up.sh` | Implemented: kind, in `scripts/k8s-up.sh`, `k8s-quickstart.yml` and `cd.yml` |
| ASG-K8S-002 | §3.3 p14 | Manifests organised with Kustomize (`base/` + `overlays/dev` + `overlays/prod`); Helm acceptable with an ADR | Mandatory | TahaSohail-Goat | #49 | `k8s/` | CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-003 | §3.3 p14 | Everything in namespace `civicpulse`, never `default` | Mandatory | TahaSohail-Goat | #49 | `k8s/base/namespace.yaml` | INS, CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-004 | §3.3 p14 | `backend` Deployment with ≥ 2 replicas | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-005 | §3.3 p14 | `frontend` Deployment with ≥ 2 replicas | Mandatory | TahaSohail-Goat | #49 | `k8s/base/frontend.yaml` | CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-006 | §3.3 p14 | `postgres` is a StatefulSet with `volumeClaimTemplates` → PVC; be ready to explain why a Deployment is wrong | Mandatory | TahaSohail-Goat | #49 | `k8s/base/postgres.yaml` | CI, DOC | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-007 | §3.3 p14 | `redis` is a Deployment with a PVC | Mandatory | TahaSohail-Goat | #49 | `k8s/base/redis.yaml` | CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-008 | §3.3 p14 | Four Services, all ClusterIP; the database is never NodePort or LoadBalancer | Mandatory | TahaSohail-Goat | #49 | `k8s/base/` | CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-009 | §3.3 p14 | Ingress routes `/` → frontend and `/api` → backend on one host | Mandatory | TahaSohail-Goat | #49 | `k8s/base/ingress.yaml` | DEMO | smoke test, `backend/tests/test_k8s_manifests.py`, `k8s-quickstart.yml` | Implemented (#49); `/` and `/api/stats` answered through the Ingress in cd run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 and in `k8s-quickstart` |
| ASG-K8S-010 | §3.3 p14 | ConfigMap holds non-secret configuration | Mandatory | TahaSohail-Goat | #49 | `k8s/base/configmap.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-011 | §3.3 p14 | Secret for DB password and LLM API key; committed manifests contain placeholders only | Mandatory | TahaSohail-Goat | #49 | `k8s/base/secret.yaml` | INS, CI | secret scan, `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-012 | §3.3 p15 | HorizontalPodAutoscaler (autoscaling/v2) on the backend | Mandatory | Artfever | #50 | `k8s/base/hpa.yaml` | CI | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-013 | §3.3 p15 | HPA: `minReplicas: 2`, `maxReplicas: 10`, CPU Utilization target 60% | Mandatory | Artfever | #50 | `k8s/base/hpa.yaml` | INS | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-014 | §3.3 p15 | HPA behavior: scaleDown `stabilizationWindowSeconds: 300`; scaleUp `stabilizationWindowSeconds: 0` | Mandatory | Artfever | #50 | `k8s/base/hpa.yaml` | INS | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-015 | §3.3 p14 | PodDisruptionBudget `minAvailable: 1` on the backend | Mandatory | TahaSohail-Goat | #49 | `k8s/base/pdb.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-016 | §3.3 p15 | `startupProbe`: httpGet `/health` port 8000, `failureThreshold: 30`, `periodSeconds: 2` | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-017 | §3.3 p15 | `livenessProbe`: httpGet `/health`; must NOT depend on the database | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-018 | §3.3 p15 | `readinessProbe`: httpGet `/ready`; SHOULD depend on the database | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-019 | §3.3 p15 | Rolling update `maxSurge: 1`, `maxUnavailable: 0` | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-020 | §3.3 p15 | `terminationGracePeriodSeconds` and a `preStop` sleep so the pod leaves Service endpoints before it stops accepting connections | Mandatory | TahaSohail-Goat | #49 | `k8s/base/backend.yaml` | INS | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-021 | §3.3 p15 | Demonstrate a zero-downtime rollout: load generator during `kubectl set image`, zero failed requests (scored as bonus — see ASG-BONUS-001) | Evidence | Artfever | #50 | `load/k6-script.js` | DEMO | `docs/evidence/k8s-load-README.md` | Zero failed requests in both captures; video pending |
| ASG-K8S-022 | §3.3 p16; §4 H p21 | `resources.requests` (incl. `cpu`) and `limits` set on every container — the HPA needs the request as denominator | Mandatory | TahaSohail-Goat | #49 | `k8s/base/` | INS, CI | `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-023 | §3.3 p16 | metrics-server installed | Mandatory | Artfever | #50 | docs / overlay | DEMO | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-024 | §3.3 p16 | Generate load with k6 or hey and capture the scale-out | Evidence | Artfever | #50 | `load/k6-script.js` | DEMO, MEAS | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-025 | §3.3 p16; §5.8 p26 | Commit `kubectl get hpa -w` output showing replicas rising | Evidence | Artfever | #50 | `docs/evidence/` | DOC | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-026 | §3.3 p16; §5.8 p26 | Commit a chart of replicas against offered load over time | Evidence | Artfever | #50 | `docs/evidence/` | DOC | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-027 | §3.3 p16 | 3–5 sentences on the lag between load arriving and capacity arriving | Evidence | Artfever | #50 | `docs/evidence/k8s-load-README.md` (engineering notes integration: #54) | DOC | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-028 | §3.3 p16 | Vertical Pod Autoscaler installed and run on the backend in recommender mode (`updateMode: "Off"`) | Mandatory | Artfever | #50 | `k8s/base/vpa.yaml` | INS, DEMO | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-029 | §3.3 p16 | VPA loop: record guessed requests → run load test → commit Target / Lower Bound / Upper Bound from `kubectl describe vpa backend-vpa` → update requests → re-run the load test and report the HPA change | Evidence | Artfever | #50 | `docs/evidence/` | DOC | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |
| ASG-K8S-030 | §3.3 p16–17 | Explain why VPA runs in Off mode: the HPA/VPA feedback conflict when both act on CPU | Evidence | Artfever | #50 | `docs/evidence/k8s-load-README.md` (engineering notes integration: #54) | DOC | `docs/evidence/k8s-load-README.md` | Implemented; measured locally; reviewed (#93) |

## ASG-CICD — Pipeline

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-CICD-001 | §3.4 p17 | Three workflows: `ci.yml`, `cd.yml`, `release.yml` | Mandatory | TahaSohail-Goat | #51 | `.github/workflows/` | INS | `backend/tests/test_ci_workflow.py` | Done: `ci.yml`, `cd.yml`, `release.yml` (and `k8s-quickstart.yml`) |
| ASG-CICD-002 | §3.4 p17 | Two branches: `dev` for work, `main` for deployable software; main protected with required checks and one approval | Mandatory | TahaSohail-Goat | #51 | repo settings | DEMO | `docs/evidence/ruleset-main.json`, `docs/evidence/ci-gate.md` | Done: `main` and `dev` protected by rulesets with the ten required checks (exports and the red-then-green demonstration) |
| ASG-CICD-003 | §3.4 p17 | `ci.yml` runs on pull request to main and on push to dev | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-004 | §3.4 p17 | `lint-and-type`: ruff + mypy (backend); eslint + `tsc --noEmit` (frontend) | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-005 | §3.4 p17 | `test-backend`: pytest with coverage ≥ 65% on `app/`, `TRIAGE_PROVIDER=simulated` | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-006 | §3.4 p17 | `test-frontend`: Vitest component tests, ≥ 5 meaningful tests | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-007 | §3.4 p17 | `build`: build both images; do not push; a PR must not publish artifacts | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-008 | §3.4 p17 | `scan`: Trivy on both images, failing on HIGH/CRITICAL with a fixed version available | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-009 | §3.4 p17 | `manifests`: `kustomize build overlays/prod` piped to `kubeconform` | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-010 | §3.4 p17 | `integration`: `docker compose up -d`, wait for `/ready`, POST a complaint, GET it back, assert the category, check `X-Cache` goes MISS → HIT, `docker compose down -v` | Mandatory | TahaSohail-Goat | #51 | `ci.yml` | CI | `backend/tests/test_ci_workflow.py` | Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-011 | §4 I p21 | `ci.yml` checks configured as required checks on main | Mandatory | TahaSohail-Goat | #51 | repo settings | DEMO | screenshot | Done: ten required checks on `main` and `dev`; blocking shown in `docs/evidence/ci-gate.md` |
| ASG-CICD-012 | §3.4 p18 | `cd.yml` runs on push to main | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-013 | §3.4 p18 | `test`: the full suite again on the merged result | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-014 | §3.4 p18 | `build-push` (`needs: test`): build both images, push to GHCR tagged `${{ github.sha }}` and `latest` | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-015 | §3.4 p18 | Emit an SBOM with Syft | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-016 | §3.4 p18 | Capture the image digest as a job output | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-017 | §3.4 p18 | `deploy-k8s` (`needs: build-push`): spin up a kind/k3d cluster in the runner and apply `overlays/prod` with the SHA tag | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-018 | §3.4 p18 | Wait for `kubectl rollout status` | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-019 | §3.4 p18 | Run a smoke test against the Ingress | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-020 | §3.4 p18 | Print `kubectl get hpa` | Mandatory | Artfever | #52 | `cd.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-021 | §3.4 p18 | `release.yml` on tag `v*`: build, push semver tags, generate release notes | Mandatory | Artfever | #52 | `release.yml` | CI | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-022 | §3.4 p18 | `needs:` on every publishing and deploying job | Mandatory | Artfever | #52 | all workflows | INS | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-023 | §3.4 p18 | Deploy by immutable reference (commit SHA; digest for bonus); `:latest` may be pushed but never deployed; "what is production running?" has a one-word answer usable in `git show` | Mandatory | Artfever | #52 | `cd.yml`, `k8s/overlays/prod` | INS | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-024 | §3.4 p18 | All credentials from GitHub Secrets; a scoped, revocable registry token (never an account password); `GITHUB_TOKEN` with `packages: write` for GHCR | Mandatory | TahaSohail-Goat | #51 | workflows | INS | `backend/tests/test_ci_workflow.py` | Done: credentials only from GitHub Secrets and `GITHUB_TOKEN` (`packages: write` only in the publishing job) |
| ASG-CICD-025 | §3.4 p18 | Least-privilege `permissions:` block on every workflow | Mandatory | TahaSohail-Goat | #51 | workflows | INS | `backend/tests/test_ci_workflow.py` | Done: explicit least-privilege `permissions:` in every workflow |
| ASG-CICD-026 | §3.4 p18 | Actions pinned — `@v4` at minimum (commit SHA for the bonus) | Mandatory | TahaSohail-Goat | #51 | workflows | INS | `backend/tests/test_ci_workflow.py` | Done: every third-party action pinned to a commit SHA in every workflow |
| ASG-CICD-027 | §3.4 p18 | Evidence the gate works: PR with a deliberately failing test — screenshot of the red check and blocked merge button; fixed in the same PR; screenshot of green | Evidence | TahaSohail-Goat | #51 | `docs/evidence/` | DEMO | `docs/evidence/ci-gate.md`, `ci-red-check.png`, `ci-red-blocked.png`, `ci-green.png` | Done (P10-S01, #51): PR #90 red then green |
| ASG-CICD-028 | §3.4 p18 | Rollback mechanism 1: `kubectl rollout undo deployment/backend -n civicpulse` | Mandatory | Artfever | #52 | `docs/RUNBOOK.md` | DEMO | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-029 | §3.4 p18–19 | Rollback mechanism 2: re-apply the previous overlay with the previous SHA | Mandatory | Artfever | #52 | `docs/RUNBOOK.md` | DEMO | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-030 | §3.4 p19 | Both rollbacks demonstrated on video, with an explanation of when to use each | Evidence | Artfever | #52 | `docs/RUNBOOK.md` | DEMO | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-031 | §1.4 p3 | A bad deploy can be undone in thirty seconds | Mandatory | Artfever | #52 | `docs/RUNBOOK.md` | MEAS | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |

## ASG-GH — Collaboration and version control

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-GH-001 | §4 A p19 | `main` protected: no direct push, PR required, CI required, ≥ 1 approval | Mandatory | TahaSohail-Goat | #56 | repo settings | DEMO | `docs/evidence/` screenshot, `docs/evidence/ruleset-main.json`, `docs/evidence/ci-gate.md` | Done: rulesets on `main` and `dev` with PR, approvals and the ten required checks; evidence is the exports and the red-then-green demonstration |
| ASG-GH-002 | §4 A p19 | Two-branch model: `dev` plus feature branches; no work committed directly to main | Mandatory | TahaSohail-Goat | #56 | branches | INS | branch list, `docs/GITHUB_WORKFLOW.md` | Done: `dev` and `feature/<n>-<slug>` branches; the six commits on `main` before the rulesets are the Phase 00 baseline (`SUBMISSION.md`) |
| ASG-GH-003 | §4 A p19 | ≥ 5 merged PRs | Mandatory | TahaSohail-Goat | #56 | GitHub | INS | PR list, GitHub pull requests | Done: 44 merged pull requests, 21 of them with a substantive partner review (threshold 5) |
| ASG-GH-004 | §4 A p19 | Each merged PR is linked to an Issue | Mandatory | TahaSohail-Goat | #56 | GitHub | INS | PR list, GitHub pull requests | Done: every merged PR names its issue (`Related issue` or `Closes`) |
| ASG-GH-005 | §4 A p19 | Each merged PR has a substantive review comment from the partner | Mandatory | TahaSohail-Goat | #56 | GitHub | INS | PR reviews, GitHub pull requests | Partial: 21 of 44 merged PRs carry a substantive partner review; the others are mostly small follow-ups (CI, evidence, docs) and the earliest baseline PR. Post-merge partner reviews of the remaining PRs are still welcome |
| ASG-GH-006 | §4 A p19 | ≥ 35 commits | Mandatory | TahaSohail-Goat | #56 | git history | MEAS | `git shortlog -sn` | Done: 111 commits by `git shortlog` (no merges), threshold 35 |
| ASG-GH-007 | §4 A p19 | Commits use conventional prefixes (`feat:`, `fix:`, `docs:` …) | Mandatory | TahaSohail-Goat | #56 | git history | INS | `git log` | Done: 105 of 111 commit subjects use a conventional prefix; six do not (one initial commit, five early frontend commits) |
| ASG-GH-008 | §4 A p19 | Neither partner below 35% by `git shortlog -sn` | Mandatory | TahaSohail-Goat | #56 | git history | MEAS | `git shortlog -sn` | At risk: `git shortlog -sn --no-merges` gives 80 / 31 (Artfever 28 %), threshold 35 %. Genuine remaining work should be authored by the second contributor; no artificial commits |
| ASG-GH-009 | §4 A p19 | One deliberate merge conflict on real code, resolved | Mandatory | TahaSohail-Goat | #56 | git history | INS | merge commit, `docs/evidence/issue-46-triage-conflict.txt` | Done: a real add/add conflict in `backend/app/services/triage.py` between #44 and #46, resolved in #70 |
| ASG-GH-010 | §4 A p19 | Conflict evidence: markers, resolution and merge shown | Evidence | TahaSohail-Goat | #56 | `docs/evidence/` | DOC | screenshots, `docs/evidence/issue-46-triage-conflict.txt` | Done: markers, resolution and merge in the evidence file |
| ASG-GH-011 | §4 A p19 | 2–4 sentences on why the winning version won | Evidence | TahaSohail-Goat | #56 | `docs/evidence/` / notes | DOC | `docs/evidence/issue-46-triage-conflict.txt` | Done: the resolution paragraph of the evidence file explains why the kept version won |

## ASG-DOC — Documentation, portfolio and reflection

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-DOC-001 | §4 J p22 | `README.md`: problem statement | Mandatory | Artfever | #55 | `README.md` | DOC | `README.md`, `README.md` introduction | Implemented (#55) |
| ASG-DOC-002 | §4 J p22 | `README.md`: badges | Mandatory | Artfever | #55 | `README.md` | DOC | `README.md`, `README.md` CI/CD badges | Implemented (#55) |
| ASG-DOC-003 | §4 J p22 | `README.md`: Mermaid architecture diagram | Mandatory | Artfever | #55 | `README.md` | DOC | `README.md`, `README.md` Mermaid; `docs/ARCHITECTURE.md` | Implemented (#55) |
| ASG-DOC-004 | §4 J p22 | `README.md`: working one-command quickstart | Mandatory | Artfever | #55 | `README.md` | DEMO | clean-clone run, `README.md`, `ci.yml`, `docs/evidence/screenshots-clean-clone-log.txt` | Implemented (#55, #100); the PowerShell block was verified on a clean clone, and the equivalent command is exercised by the CI integration job |
| ASG-DOC-005 | §4 J p22 | `README.md`: API table | Mandatory | Artfever | #55 | `README.md` | DOC | `README.md`, `README.md`; running OpenAPI comparison (nine pairs) | Implemented (#55) |
| ASG-DOC-006 | §4 J p22 | `README.md`: screenshots | Mandatory | Artfever | #55 | `README.md`, `docs/evidence/` | DOC | `README.md`, `docs/evidence/`, `docs/evidence/screenshots-{submit,dashboard,stats}.png` | Implemented (#55, #100): three real application screenshots (Submit, Dashboard, Stats) plus the CI-gate and HPA captures |
| ASG-DOC-007 | §2.2 p5 | If Flask is used, the README says so | Mandatory | Artfever | #55 | `README.md` | DOC | `README.md`, `README.md`; `backend/app/main.py` | Implemented (#55): the README states FastAPI, not Flask |
| ASG-DOC-008 | §4 J p22 | ADR 0001: provider interface | Mandatory | Artfever | #46 | `docs/adr/0001-provider-interface.md` | DOC | `docs/adr/0001-provider-interface.md` | Implemented (#46) |
| ASG-DOC-009 | §2.1 p4; §4 J p22 | ADR 0002: frontend runtime config (states the `/config.js` vs nginx-proxy choice) | Mandatory | Artfever | #34 | `docs/adr/0002-frontend-runtime-config.md` | DOC | `docs/adr/0002-frontend-runtime-config.md` | Implemented (#34, #48): the nginx-proxy choice is stated |
| ASG-DOC-010 | §4 J p22 | ADR 0003: deploy-by-SHA | Mandatory | Artfever | #52 | `docs/adr/0003-deploy-by-sha.md` | DOC | `docs/evidence/cd-local-rollback.txt`; cd run 36230267941 | Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-DOC-011 | §4 J p22 | ADR 0004: PII / data governance | Mandatory | Artfever | #46 | `docs/adr/0004-pii-and-data-governance.md` | DOC | `docs/adr/0004-pii-and-data-governance.md` | Implemented (#46) |
| ASG-DOC-012 | §3.3 p14 | ADR for the choice of Helm — only if Helm replaces Kustomize | Recommended | TBD | TBD | `docs/adr/` | DOC | — | Info |
| ASG-DOC-013 | §4 J p22 | `docs/RUNBOOK.md`: how to deploy, roll back, read logs, and what to do when triage starts failing | Mandatory | TahaSohail-Goat | #53 | `docs/RUNBOOK.md` | DOC | `docs/RUNBOOK.md` | Implemented (#53): every section written; sections 1-10 and 11-12 are run in CI; rollback measured |
| ASG-DOC-014 | §4 J p22 | Demo video ≤ 5 minutes with both partners speaking | Mandatory | Artfever | #55 | video link | DEMO | link, `README.md` recording plan only | Pending: the demo video is recorded by the two contributors (script: `docs/DEMO_SCRIPT.md`) |
| ASG-DOC-015 | §4 J p22 | Video covers: clean clone → running system; AI triage; fallback; network isolation failing; HPA scaling; rollback | Mandatory | Artfever | #55 | video | DEMO | link, `README.md` recording plan only | Pending: the demo video (script: `docs/DEMO_SCRIPT.md`) |
| ASG-DOC-016 | §4 J p22; §5.2 p23 | `docs/ENGINEERING-NOTES.md` answers all eight questions with references to the team's own files and lines (generic answers score zero) | Mandatory | Artfever | #54 | `docs/ENGINEERING-NOTES.md` | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96); the more-than-one-hour duration is confirmed by Artfever |
| ASG-DOC-017 | §5.2 p23 | EN-Q1: three laptop-vs-CI differences and the exact Dockerfile/manifest line freezing each | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-018 | §5.2 p23 | EN-Q2: position on the CI/CD maturity ladder (Lecture 03, slide 32); justify the rung; name the next rung and what it buys | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-019 | §5.2 p23 | EN-Q3: the exact line guaranteeing build-once-deploy-many and what breaks without it | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-020 | §5.2 p23 | EN-Q4: what "correct" means for a probabilistic LLM component and how CI stays deterministic (Lecture 01, slide 34) | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-021 | §5.2 p23 | EN-Q5: measured HPA lag in seconds; where the time went; what would reduce it | Evidence | Artfever | #54 | notes | MEAS | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-022 | §5.2 p24 | EN-Q6: why VPA is Off; failure mode of running it in Auto alongside HPA | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-023 | §5.2 p24 | EN-Q7: where the hosted-LLM caller lives given `internal: true`, and how it was resolved | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96) |
| ASG-DOC-024 | §5.2 p24 | EN-Q8: a failure that cost > 1 hour — symptoms, wrong first belief, the exact command/log line that revealed the truth | Evidence | Artfever | #54 | notes | DOC | `docs/ENGINEERING-NOTES.md` | Done; reviewed (#96); the more-than-one-hour duration is confirmed by Artfever |
| ASG-DOC-025 | §5.5 p25 | `docs/AI-USAGE.md`: tools named, which parts they wrote or shaped, what was changed afterwards and why | Mandatory | TahaSohail-Goat | #56 | `docs/AI-USAGE.md` | DOC | `docs/AI-USAGE.md` | Implemented: one row per pull request for both contributors |
| ASG-DOC-026 | §5.7 p26 | `docs/TRIAGE.md` exists in the layout; its content is not specified | Advisory | Artfever | #46 | `docs/TRIAGE.md` | DOC | `docs/TRIAGE.md` | Implemented as operations/evidence guide (#46) |
| ASG-DOC-027 | §5.7 p26; §4 A p19 | `docs/evidence/` holds screenshots: protection, conflict, blocked merge, `hpa -w`, scaling chart | Evidence | TahaSohail-Goat | #53 | `docs/evidence/` | DOC | `docs/evidence/` | Implemented: conflict, blocked merge, `hpa -w`, scaling chart, ruleset exports and the CI gate demonstration |
| ASG-DOC-028 | §5.3 p24 | If a credential ever lands in history: rotate it and write an incident note | Policy | TBD | TBD | `docs/SECURITY.md` | DOC | — | Info |

## ASG-BONUS — Optional (capped at +15)

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-BONUS-001 | §4 p22; §3.3 p15 | Zero-downtime rolling update demonstrated under live load with zero failed requests — +4 | Bonus | TBD | TBD | `load/k6-script.js` | DEMO | capture, `docs/evidence/k8s-zero-downtime-index.md` | Measured: zero failed requests during a rolling replacement under k6 load (two runs); the video is pending |
| ASG-BONUS-002 | §4 p22 | GitOps: Argo CD or Flux reconciling the cluster from the repository — +4 | Bonus | TBD | TBD | `k8s/` | DEMO | capture | Not started |
| ASG-BONUS-003 | §4 p22 | Deploy by image digest rather than tag, with Cosign signing and verification in CI — +3 | Bonus | TBD | TBD | `cd.yml` | CI | `.github/workflows/cd.yml` | Partial: images are deployed by digest under the SHA tag (`cd.yml`); Cosign signing and verification are not done |
| ASG-BONUS-004 | §4 p22 | Prometheus scraping `/metrics` plus a Grafana dashboard, screenshot committed — +2 | Bonus | TBD | TBD | `docs/evidence/` | DEMO | screenshot | Not started |
| ASG-BONUS-005 | §4 p22 | OpenTelemetry tracing across frontend → backend → LLM call — +2 | Bonus | TBD | TBD | app code | DEMO | trace capture | Not started |
| ASG-BONUS-006 | §3.1 p12 | Pin the backend base image by digest (called out "for the bonus") | Bonus | TBD | TBD | `backend/Dockerfile` | INS | `backend/Dockerfile` | Done: both stages of `backend/Dockerfile` pin `python:3.12.14-slim-bookworm` by sha256 digest |
| ASG-BONUS-007 | §3.4 p18 | Pin Actions by commit SHA (called out "for the bonus") | Bonus | TBD | TBD | workflows | INS | `.github/workflows/` | Done: every third-party action in `ci.yml`, `cd.yml`, `release.yml` and `k8s-quickstart.yml` is pinned to a commit SHA |
| ASG-BONUS-008 | §4 p22 | Bonus total is capped at +15 (items above sum to exactly 15) | Constraint | TBD | TBD | — | DOC | — | Info |

## ASG-DED — Automatic deductions (release blockers)

Each deduction is a **guard**: the repository must never enter that state. See [`AGENTS.md`](../AGENTS.md) §9 and [`SECURITY.md`](SECURITY.md). The guards are verified in the final audit, P12-S02 (#56, `TahaSohail-Goat`); each guard's implementing packages are the owners of the IDs named in its *Guarded by* column.

| ID | Source | Deduction | Points | Guarded by | Verification | Status |
|---|---|---|---|---|---|---|
| ASG-DED-001 | §5.3 p24 | A `.env`, key, token or password anywhere in Git history (plus rotate and write an incident note) | −20 | `.gitignore`, secret scan on every commit/PR, ASG-DEVOPS-023/024 | INS, CI | Guard active (`.gitignore` added in Phase 00) |
| ASG-DED-002 | §5.3 p24 | An LLM API key in a committed Kubernetes manifest, even base64-encoded | −15 | ASG-K8S-011 | INS, CI, `scripts/check_submission.py` | Clear: `check_submission.py` and a manifest test find no key; the Secret holds placeholders |
| ASG-DED-003 | §5.3 p24 | Unpinned base image, or postgres / redis / node without a tag | −8 | ASG-DEVOPS-001/025 | INS, CI, `scripts/check_submission.py` | Clear: every image tag pinned |
| ASG-DED-004 | §5.3 p24 | `localhost` used for service-to-service communication | −8 | ASG-NFR-016 | INS, CI, `scripts/check_submission.py` | Clear: service names only |
| ASG-DED-005 | §5.3 p24 | Frontend able to reach the database (network segmentation not implemented) | −8 | ASG-DEVOPS-013…017 | DEMO, `ci.yml` | Clear: the CI integration job shows the frontend cannot resolve `database` |
| ASG-DED-006 | §5.3 p24 | Published database/cache port in `compose.prod.yaml`, or NodePort/LoadBalancer Service on the database | −8 | ASG-DEVOPS-028, ASG-K8S-008 | CFG, CI, `scripts/check_submission.py` | Clear: no data port in `compose.prod.yaml`, all Services ClusterIP |
| ASG-DED-007 | §5.3 p24 | Publishing or deploying job not gated by `needs:` | −8 | ASG-CICD-022 | INS, `.github/workflows/cd.yml` | Clear: every publishing or deploying job has `needs:` |
| ASG-DED-008 | §5.3 p24 | Deploying `:latest` anywhere | −8 | ASG-CICD-023 | INS, CI, `.github/workflows/cd.yml` | Clear: `:latest` is pushed but never deployed |
| ASG-DED-009 | §5.3 p24 | PostgreSQL as a Deployment with no PVC | −8 | ASG-K8S-006 | CI, `k8s/base/postgres.yaml` | Clear: PostgreSQL is a StatefulSet with a volumeClaimTemplate |
| ASG-DED-010 | §5.3 p24 | Commits pushed directly to main | −5 | ASG-GH-001/002; `AGENTS.md` §6 | INS | Guard active (rulesets); initial commit: `SUBMISSION.md` |
| ASG-DED-011 | §5.3 p24 | README quickstart that does not work from a clean clone | −5 | ASG-DOC-004, ASG-GEN-007 | DEMO, `README.md` | Clear: the quickstart is what the CI integration job and `k8s-quickstart` run on clean runners |

## ASG-SUB — Submission, viva and policy

| ID | Source | Requirement | Type | Owner | Issue | Code/Artifact | Verification | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| ASG-SUB-001 | §5.8 p26 | GitHub repository URL — public, or private with both instructors added | Mandatory | TahaSohail-Goat | #56 | repo | INS | URL | Info (repo is public) |
| ASG-SUB-002 | §5.8 p26 | Link to a successful `cd.yml` run that tested, published and deployed | Evidence | TahaSohail-Goat | #56 | Actions | DEMO | link, https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 | Ready: successful `cd.yml` run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 |
| ASG-SUB-003 | §5.8 p26 | Link to both images in GHCR, showing SHA tags | Evidence | TahaSohail-Goat | #56 | GHCR | DEMO | link, `docs/SUBMISSION.md` | Ready: both images are public in GHCR with SHA tags (`ghcr.io/tahasohail-goat/civicpulse-backend` and `-frontend`) |
| ASG-SUB-004 | §5.8 p26 | Demo video link (unlisted) | Evidence | Artfever | #55 | video | DEMO | link, No video link yet | Pending: the demo video link |
| ASG-SUB-005 | §5.8 p26 | `git shortlog -sn` output, pasted | Evidence | TahaSohail-Goat | #56 | terminal | MEAS | output, `docs/SUBMISSION.md` | Recorded in `docs/SUBMISSION.md` (refresh before submitting) |
| ASG-SUB-006 | §5.8 p26 | `kubectl get hpa -w` capture and replicas-vs-load chart | Evidence | TahaSohail-Goat | #56 | `docs/evidence/` | DOC | files, `docs/evidence/` | Ready: `docs/evidence/k8s-load-baseline50/hpa-watch.txt` and `k8s-load-comparison.png` |
| ASG-SUB-007 | §5.8 p26 | Run `python scripts/check_submission.py` from the repository root before submitting (a lint, not a grader) | Mandatory | TahaSohail-Goat | #56 | `scripts/check_submission.py` | CI | output | Script written (P12-S02, #56); final run and its output recorded at submission |
| ASG-SUB-008 | §5.3 p24 | Late submissions are not accepted and there is no retake (course policy); no deadline date is given | Policy | TBD | TBD | — | — | — | Info (deadline: `SUBMISSION.md`) |
| ASG-SUB-009 | §5.4 p24 | Viva: individual, 10 minutes each, repository open, including questions on the partner's code | Policy | TBD | TBD | — | — | — | Info |
| ASG-SUB-010 | §5.4 p25 | Individual mark = team mark × viva factor: 1.0 explains any part; 0.75 solid on own work / shaky on partner's; 0.5 describes what but not why, cannot modify live; 0.0 cannot explain the submission | Policy | TBD | TBD | — | — | — | Info |
| ASG-SUB-011 | §5.4 p25 | If a partner is not contributing, say so in week 1, not week 5 | Policy | TBD | TBD | `docs/TEAM_CONTRIBUTION.md` | — | — | Info |
| ASG-SUB-012 | §5.5 p25 | AI use is permitted with honest attribution; presenting AI-generated work as original is plagiarism; the viva only cares whether the line can be defended | Policy | TBD | TBD | `docs/AI-USAGE.md` | DOC | — | Info |

## ASG-REPO — Repository layout (§5.7 p25–26)

The layout root is named `civicpulse/` in the source; the product may be renamed (ASG-GEN-004) so the repository root name is not significant. Directory placeholders (`.gitkeep`) were created in Phase 00; files arrive in the phase shown in [`REPOSITORY_STRUCTURE.md`](REPOSITORY_STRUCTURE.md).

| ID | Source | Required path(s) | Type | Owner | Issue | Verification | Status |
|---|---|---|---|---|---|---|---|
| ASG-REPO-001 | §5.7 | `backend/app/{routes,services,repositories,providers}/` | Mandatory | TahaSohail-Goat | #37 | INS, `backend/app/` | Implemented |
| ASG-REPO-002 | §5.7 | `backend/app/providers/triage/{base,llm,ollama,rules,simulated,factory}.py` | Mandatory | TahaSohail-Goat | #44 | INS, `backend/app/providers/triage/` | Implemented |
| ASG-REPO-003 | §5.7 | `backend/alembic/versions/` | Mandatory | TahaSohail-Goat | #40 | INS | Implemented (P05-S01, #40) |
| ASG-REPO-004 | §5.7 | `backend/tests/` | Mandatory | TahaSohail-Goat | #39 | INS | Implemented (P04-S03, #39) |
| ASG-REPO-005 | §5.7 | `backend/Dockerfile`, `backend/.dockerignore`, `backend/pyproject.toml` | Mandatory | TahaSohail-Goat | #37 | INS, `backend/Dockerfile` | Implemented (#47) |
| ASG-REPO-006 | §5.7 | `frontend/src/{components,pages,api}/` | Mandatory | Artfever | #34 | INS, `frontend/src/` | Implemented (#34-#36) |
| ASG-REPO-007 | §5.7 | `frontend/tests/` | Mandatory | Artfever | #36 | `frontend/tests/views.test.tsx` | Implemented (#36) |
| ASG-REPO-008 | §5.7 | `frontend/Dockerfile`, `frontend/.dockerignore`, `frontend/nginx.conf`, `frontend/package.json` | Mandatory | Artfever | #34 | INS, `frontend/Dockerfile` | Implemented (#48) |
| ASG-REPO-009 | §5.7 | `k8s/base/{namespace,backend,frontend,postgres,redis,ingress,configmap,secret}.yaml` | Mandatory | TahaSohail-Goat | #49 | INS, `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49) |
| ASG-REPO-010 | §5.7 | `k8s/base/{hpa,vpa,pdb}.yaml`, `k8s/base/kustomization.yaml` | Mandatory | TahaSohail-Goat | #49 | INS, `backend/tests/test_k8s_manifests.py` | Implemented (#49, #50) |
| ASG-REPO-011 | §5.7 | `k8s/overlays/{dev,prod}/kustomization.yaml` | Mandatory | TahaSohail-Goat | #49 | INS, `backend/tests/test_k8s_manifests.py` | Implemented (P09-S01, #49) |
| ASG-REPO-012 | §5.7 | `load/k6-script.js` | Mandatory | Artfever | #50 | INS | Implemented: `load/k6-script.js`; two real captures in `docs/evidence/k8s-load-README.md` |
| ASG-REPO-013 | §5.7 | `docs/{ENGINEERING-NOTES,RUNBOOK,AI-USAGE,TRIAGE}.md` | Mandatory | Artfever | #54 | INS, `docs/` | Implemented (#54, #55): all four documents are written |
| ASG-REPO-014 | §5.7 | `docs/adr/0001-provider-interface.md` … `0004-pii-and-data-governance.md` | Mandatory | TahaSohail-Goat | #56 | INS, `docs/adr/` | Implemented: ADRs 0001-0004 |
| ASG-REPO-015 | §5.7 | `docs/evidence/` | Mandatory | TahaSohail-Goat | #53 | INS, `docs/evidence/` | Implemented |
| ASG-REPO-016 | §5.7 | `scripts/check_submission.py` | Mandatory | TahaSohail-Goat | #56 | INS, `scripts/check_submission.py` | Implemented (#56) |
| ASG-REPO-017 | §5.7 | `.github/workflows/{ci.yml,cd.yml,release.yml}` | Mandatory | TahaSohail-Goat | #51 | INS | Implemented (#51, #52) |
| ASG-REPO-018 | §5.7 | `compose.yaml`, `compose.prod.yaml`, `.env.example`, `.gitignore` | Mandatory | TahaSohail-Goat | #47 | INS, `backend/tests/test_container_files.py` | Implemented (#47, #48) |
| ASG-REPO-019 | §5.7 | `README.md`, `LICENSE` | Mandatory | Artfever | #55 | INS | Implemented: `README.md` written (#55, #100), `LICENSE` is MIT (#99) |

---

## Coverage summary

Counts are checked mechanically (see the Phase 00 PR). Every ID above is unique; every rubric item in [`RUBRIC.md`](RUBRIC.md) maps to at least one ID; every automatic deduction has an `ASG-DED-*` guard.

| Family | IDs |
|---|---|
| ASG-GEN | 13 |
| ASG-FR | 35 |
| ASG-NFR | 17 |
| ASG-DATA | 23 |
| ASG-CACHE | 12 |
| ASG-AI | 25 |
| ASG-DEVOPS | 29 |
| ASG-K8S | 30 |
| ASG-CICD | 31 |
| ASG-GH | 11 |
| ASG-DOC | 28 |
| ASG-BONUS | 8 |
| ASG-DED | 11 |
| ASG-SUB | 12 |
| ASG-REPO | 19 |
| **Total** | **304** |

> `ASG-FR-018` and `ASG-FR-019` are intentionally unused: frontend rows (001–017) and backend/API rows (020–037) are separated by a gap so later phases can add rows to either group without renumbering. IDs are never reused or renumbered.

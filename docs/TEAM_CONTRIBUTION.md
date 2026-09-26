# Team Contribution

## Purpose
Maintain genuine, balanced ownership between the two students. Both must be able to explain every part of the submission at the individual viva (`docs/SUBMISSION.md` §4).

## Members
| Member | GitHub | Repository permission | Sessions |
|---|---|---|---|
| Member A | `TahaSohail-Goat` | admin (owner) | own login, own clone/worktree |
| Member B | `Artfever` | write (collaborator since 2026-09-25) | own login, own clone/worktree; runbook: `docs/PARTNER_RUNBOOK.md` |

## Working agreement — two real accounts, two sessions
1. **Each person acts only as themself.** Before any GitHub write, `gh auth status` must show the acting person's own account. Nobody — person or AI session — uses the other's login, token, password or SSH key, commits under the other's name, or posts a review, approval or comment for them.
2. **Two sessions, in parallel** (`AGENTS.md` §7): each person runs their own AI session (Contributor A: Claude Code; Contributor B: Codex) on their own machine login, in their own clone or `git worktree`, on their own issues, on disjoint files. A session never edits a file owned by an open issue of the other person.
3. **Git identity per clone, and one disclosure trailer per AI-assisted commit:** `git config user.name` / `user.email` are the person's own. Every AI-assisted commit ends with exactly one trailer naming the tool, in the form that tool's identity supports:
   - Contributor A (Claude Code): `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` — the form that session is configured to emit.
   - Contributor B (Codex): `Assisted-by: OpenAI Codex` — Codex has no verified co-author address, and this repository does not invent identities or e-mail addresses for tools.
   The trailer discloses; it never changes authorship. `git shortlog -sn` counts the commit's **author**, so rubric A4 is unaffected. Both forms satisfy the disclosure duty of assignment §5.5 together with the `docs/AI-USAGE.md` entry.
4. **Cross-review:** every PR by Member A is reviewed by Member B and vice versa. `main` requires one approval from the other member (the author cannot approve their own PR); `dev` no longer blocks a merge on review state (owner decision 2026-09-25, `docs/GITHUB_WORKFLOW.md`), so cross-review is a rule of the team.
5. **What counts as a review:** the six-point standard in `docs/GITHUB_WORKFLOW.md` ("Required Partner Review"), including one "why" question per PR whose answer stays in the thread.
6. **AI assistance is allowed and must be disclosed:** each person may use their own AI session for authoring *and* for reviewing, but only after reading the change themselves; every use is logged in `docs/AI-USAGE.md`. The viva measures whether each person can defend the code, whoever typed it.
7. **No manufactured numbers:** no artificial commits, no split commits to inflate counts, no staged conflicts. The deliberate merge conflict (rubric A5) must be a real conflict on real code between two genuine branches (planned below).

## Allocation — Phase 01 (effort points)
| Issue | Work | Owner | Reviewer | Points |
|---|---|---|---|---|
| #13 P01-S01 | PRD | `TahaSohail-Goat` | `Artfever` | 3 |
| #15 P01-S03 | FR catalog: API and domain | `TahaSohail-Goat` | `Artfever` | 6 |
| #18 P01-S06 | Traceability and allocation of Phases 02–12 | `TahaSohail-Goat` | `Artfever` | 6 |
| #14 P01-S02 | FR catalog: frontend | `TahaSohail-Goat` | `Artfever` | 4 |
| #16 P01-S04 | NFR catalog | `TahaSohail-Goat` | `Artfever` | 6 |
| #17 P01-S05 | Use cases | `TahaSohail-Goat` | `Artfever` | 5 |
| | **Total** | 30 | 0 | 30 |

Parent issue: #12. **Owner decision (2026-09-25):** to save time, `TahaSohail-Goat` writes all of Phase 01, including #14, #16 and #17 that were first allocated to `Artfever`; `Artfever` reviews them and takes his own issues from Phase 02 on. The effort balance is restored in Phases 02–12 (70 points each) and, more importantly for rubric A4, in commits: `Artfever` owns 13 of the 25 packages. The allocation of Phases 02–12 follows below (decided in #18).

## Allocation — Phases 02–12 (effort points)

Decided in issue #18; **both members must accept it in the PR thread**. The parent issue of each phase (#21–#31) carries the same table. Every package has one owner and the other person as reviewer.

| Issue | Work | Owner | Reviewer | Points |
|---|---|---|---|---|
| #32 P02-S01 | Architecture document with diagrams; verify repository layout against section 5.7 | `Artfever` | `TahaSohail-Goat` | 5 |
| #33 P02-S02 | API design document: answer the design questions DQ-API-01..18 | `TahaSohail-Goat` | `Artfever` | 6 |
| #34 P03-S01 | Frontend scaffold, typed API client, runtime configuration and ADR 0002 | `Artfever` | `TahaSohail-Goat` | 5 |
| #35 P03-S02 | Submit view and Dashboard | `Artfever` | `TahaSohail-Goat` | 6 |
| #36 P03-S03 | Stats view, error boundary and at least five component tests | `Artfever` | `TahaSohail-Goat` | 4 |
| #37 P04-S01 | Backend skeleton: settings, JSON logging with request_id, health/ready/metrics, graceful SIGTERM | `TahaSohail-Goat` | `Artfever` | 6 |
| #38 P04-S02 | Complaint API: routes, services, state machine, validation and error responses | `TahaSohail-Goat` | `Artfever` | 7 |
| #39 P04-S03 | Backend test suite: at least 14 deterministic tests and coverage >= 65% | `TahaSohail-Goat` | `Artfever` | 4 |
| #40 P05-S01 | Alembic migrations, schema, indexes and repositories | `TahaSohail-Goat` | `Artfever` | 6 |
| #41 P05-S02 | Idempotent seed of at least 30 realistic complaints in Urdu-influenced English | `Artfever` | `TahaSohail-Goat` | 4 |
| #42 P06-S01 | Stats read-through cache: TTL 30 s, X-Cache header, invalidation on write | `TahaSohail-Goat` | `Artfever` | 4 |
| #43 P06-S02 | Distributed Redis rate limiter with 429 + Retry-After, and the AOF justification | `Artfever` | `TahaSohail-Goat` | 4 |
| #44 P07-S01 | TriageProvider interface, RuleBasedTriage, SimulatedTriage, factory and fallback orchestration | `TahaSohail-Goat` | `Artfever` | 7 |
| #45 P07-S02 | LLMTriage (hosted) and OllamaTriage: structured output, 10 s timeout, one jittered retry | `Artfever` | `TahaSohail-Goat` | 7 |
| #46 P07-S03 | Content-hash triage cache, prompt-injection guardrail, latency recording, /api/meta/providers and ADRs 0001 and 0004 | `Artfever` | `TahaSohail-Goat` | 5 |
| #47 P08-S01 | Backend image and compose.yaml core | `TahaSohail-Goat` | `Artfever` | 6 |
| #48 P08-S02 | Frontend image, nginx, Ollama service, compose.prod.yaml and the network-isolation proof | `Artfever` | `TahaSohail-Goat` | 6 |
| #49 P09-S01 | Kustomize base and overlays: namespace, Deployments, StatefulSet, Services, Ingress, ConfigMap/Secret placeholders, probes, PDB | `TahaSohail-Goat` | `Artfever` | 7 |
| #50 P09-S02 | HPA v2, VPA (Off), metrics-server, k6 load test and scale-out evidence | `Artfever` | `TahaSohail-Goat` | 7 |
| #51 P10-S01 | ci.yml: lint/type, tests, build, Trivy, kubeconform, Compose integration; required checks; red-to-green evidence | `TahaSohail-Goat` | `Artfever` | 7 |
| #52 P10-S02 | cd.yml and release.yml: gated build/push to GHCR by SHA, SBOM, digest, ephemeral-cluster deploy, rollback procedures | `Artfever` | `TahaSohail-Goat` | 7 |
| #53 P11-S01 | Compose-side evidence and the RUNBOOK | `TahaSohail-Goat` | `Artfever` | 5 |
| #54 P11-S02 | Kubernetes-side evidence and ENGINEERING-NOTES (eight questions, file-and-line references) | `Artfever` | `TahaSohail-Goat` | 5 |
| #55 P12-S01 | README (badges, Mermaid architecture, one-command quickstart, API table, screenshots) and the demo video | `Artfever` | `TahaSohail-Goat` | 5 |
| #56 P12-S02 | check_submission.py, final audit checklist and the submission package | `TahaSohail-Goat` | `Artfever` | 5 |

### Totals

| Phase | Parent | `TahaSohail-Goat` | `Artfever` | Total |
|---|---|---|---|---|
| 02 Architecture & Repository Structure | #21 | 6 | 5 | 11 |
| 03 Frontend | #22 | 0 | 15 | 15 |
| 04 Backend & Domain Layer | #23 | 17 | 0 | 17 |
| 05 Data Layer | #24 | 6 | 4 | 10 |
| 06 Cache, Rate Limiting & Reliability | #25 | 4 | 4 | 8 |
| 07 AI Layer | #26 | 7 | 12 | 19 |
| 08 Docker & Compose | #27 | 6 | 6 | 12 |
| 09 Kubernetes | #28 | 7 | 7 | 14 |
| 10 CI/CD | #29 | 7 | 7 | 14 |
| 11 Quality Assurance, Evidence & Reflection | #30 | 5 | 5 | 10 |
| 12 Final Assignment Audit & Submission | #31 | 5 | 5 | 10 |
| **02–12 total** | | **70** | **70** | **140** |
| **With Phase 01 (30 + 0)** | | **100** (58.8%) | **70** (41.2%) | **170** |

**How the split was made.** Points are **relative effort** (a 7-point package is about 1.75 times a 4-point one), not hours and not commit counts; the assignment's own estimate for the whole project is roughly 35–45 hours per student (§5.1), and the points are used only to balance the two halves. The halves were balanced to the point, then checked against three rules:

1. **Vertical lanes keep the sessions conflict-free.** `TahaSohail-Goat` owns the backend contract path (API design, backend, migrations, cache invalidation, the provider interface and fallback, the backend image, the Kubernetes base, `ci.yml`, the compose-side evidence, the final audit). `Artfever` owns the frontend, the LLM and Ollama providers with the triage cache and guardrail, the rate limiter, the seed, the frontend image and production Compose, HPA/VPA and load testing, `cd.yml`/`release.yml`, the Kubernetes-side evidence and notes, and the README and video.
2. **Both touch almost every phase.** The only phases where one person owns everything are Phase 03 (frontend, `Artfever`) and Phase 04 (backend, `TahaSohail-Goat`); they run at the same time, so nobody waits. The two halves meet at the API design (P02-S02), which `Artfever` must confirm works for the frontend before it merges.
3. **The highest-value areas are split** (rubric priority F > C > I > H, assignment §5.1): the AI layer is 7 points for `TahaSohail-Goat` and 12 for `Artfever`; CI/CD, Kubernetes and Docker are split evenly.

Because each person also **reviews every package of the other**, both read all of the code. The individual viva asks about the partner's code (assignment §5.4); see *Explain-back and viva readiness* below.

### Sequencing

Owner decision (2026-09-25): keep the process light. `TahaSohail-Goat` finishes Phases 00 and 01 first; after that **both work in parallel on their own issues** and only a real dependency makes someone wait. Flow: issue → `feature/<n>-<slug>` from `dev` → PR into `dev` → the other contributor reviews → merge; one `dev` → `main` PR per coherent block (`main` needs one approval, as the assignment requires).

Dependencies that do make one package wait for another (from the issues' Dependencies lines): #41 after #40 (Phase 05); #43 after #42 (Phase 06, both write `docs/CACHE.md`); #45 after #44 (Phase 07); #48 after #47 (Phase 08); #50 after #49 (Phase 09); #52 after #51 (Phase 10); #56 after everything else (Phase 12). Everything else can run at the same time, in particular Phase 03 (frontend, `Artfever`) next to Phase 04 (backend, `TahaSohail-Goat`). Phase 07 runs #44 and #46 in parallel by design (see the planned merge conflict below), with #45 after #44. The team target is to be done by Sunday 27 Sep 2026; the Google Classroom deadline is "next Tuesday" (`docs/SUBMISSION.md`).

### File ownership and serialization

Each package lists the files it owns; a session never edits a file owned by an open package of the other person. The lists:

- **#32 P02-S01** (`Artfever`): `docs/ARCHITECTURE.md`; `docs/REPOSITORY_STRUCTURE.md`
- **#33 P02-S02** (`TahaSohail-Goat`): `docs/API_DESIGN.md`; `docs/frs/api.md (DQ answer column only)`; `docs/SUBMISSION.md (the open decisions rows only)`
- **#34 P03-S01** (`Artfever`): `frontend/package.json`; `frontend/package-lock.json`; `frontend/vite.config.ts`; `frontend/tsconfig*.json`; `frontend/eslint config`; `frontend/src/api/**`; `frontend/src/main.tsx`; `frontend/src/App.tsx`; `docs/adr/0002-frontend-runtime-config.md`
- **#35 P03-S02** (`Artfever`): `frontend/src/pages/Submit*`; `frontend/src/pages/Dashboard*`; `frontend/src/components/** (except ErrorBoundary*)`
- **#36 P03-S03** (`Artfever`): `frontend/src/pages/Stats*`; `frontend/src/components/ErrorBoundary*`; `frontend/tests/**`
- **#37 P04-S01** (`TahaSohail-Goat`): `backend/pyproject.toml`; `backend/app/main.py`; `backend/app/config.py`; `backend/app/logging.py`; `backend/app/middleware.py`; `backend/app/routes/health.py`; `backend/app/routes/metrics.py` — *pyproject.toml and the lockfile are conflict-heavy: dependency additions by the other contributor go through this owner or a one-line PR.*
- **#38 P04-S02** (`TahaSohail-Goat`): `backend/app/routes/complaints.py`; `backend/app/services/complaints.py`; `backend/app/services/state_machine.py`; `backend/app/schemas/**`; `backend/app/errors.py` — *The create-complaint service is touched again by #42 (cache invalidation); the planned real merge conflict is in `backend/app/services/triage.py` (#44 and #46).*
- **#39 P04-S03** (`TahaSohail-Goat`): `backend/tests/**`; `backend coverage configuration`
- **#40 P05-S01** (`TahaSohail-Goat`): `backend/alembic/**`; `backend/alembic.ini`; `backend/app/repositories/**`; `docs/DATA_MODEL.md` — *Migration heads are conflict-heavy: only this owner adds migrations.*
- **#41 P05-S02** (`Artfever`): `backend/app/seed/**`; `backend seed data file`; `seed test`
- **#42 P06-S01** (`TahaSohail-Goat`): `backend/app/services/stats.py`; `backend/app/providers/cache.py`; `docs/CACHE.md (stats section)` — *Touches the create-complaint service only to invalidate the cache.*
- **#43 P06-S02** (`Artfever`): `backend/app/services/rate_limit.py`; `docs/CACHE.md (rate-limit and AOF sections)` — *docs/CACHE.md is edited by P06-S01 and P06-S02: P06-S01 merges first, P06-S02 rebases.*
- **#44 P07-S01** (`TahaSohail-Goat`): `backend/app/providers/triage/base.py`; `backend/app/providers/triage/rules.py`; `backend/app/providers/triage/simulated.py`; `backend/app/providers/triage/factory.py`; `backend/app/services/triage.py`
- **#45 P07-S02** (`Artfever`): `backend/app/providers/triage/llm.py`; `backend/app/providers/triage/ollama.py`; `docs/AI.md (provider section)` — *New Python dependencies (for example the OpenAI SDK) go through the P04-S01 owner or a one-line PR.*
- **#46 P07-S03** (`Artfever`): `backend/app/services/triage_cache.py`; `backend/app/services/triage.py (cache and latency hooks only; shared with #44)`; `backend/app/routes/meta.py`; `docs/adr/0001-provider-interface.md`; `docs/adr/0004-pii-and-data-governance.md`; `docs/TRIAGE.md`; `backend/tests/test_injection*.py` — *Touches `backend/app/services/triage.py`: planned real merge conflict with #44.*
- **#47 P08-S01** (`TahaSohail-Goat`): `backend/Dockerfile`; `backend/.dockerignore`; `compose.yaml`; `.env.example` — *compose.yaml is conflict-heavy: this owner first; P08-S02 adds frontend and Ollama only after this merges.*
- **#48 P08-S02** (`Artfever`): `frontend/Dockerfile`; `frontend/.dockerignore`; `frontend/nginx.conf`; `compose.prod.yaml`; `compose.yaml (frontend and ollama services only)`
- **#49 P09-S01** (`TahaSohail-Goat`): `k8s/base/{namespace,backend,frontend,postgres,redis,ingress,configmap,secret,pdb}.yaml`; `k8s/base/kustomization.yaml`; `k8s/overlays/**` — *k8s/base/kustomization.yaml is conflict-heavy: this owner first; P09-S02 adds its entries after.*
- **#50 P09-S02** (`Artfever`): `k8s/base/hpa.yaml`; `k8s/base/vpa.yaml`; `load/k6-script.js`; `docs/evidence/k8s-hpa-*`; `docs/evidence/k8s-vpa-*`; `docs/evidence/k8s-load-*`
- **#51 P10-S01** (`TahaSohail-Goat`): `.github/workflows/ci.yml`; `docs/evidence/ci-*`
- **#52 P10-S02** (`Artfever`): `.github/workflows/cd.yml`; `.github/workflows/release.yml`; `docs/adr/0003-deploy-by-sha.md`
- **#53 P11-S01** (`TahaSohail-Goat`): `docs/evidence/compose-*`; `docs/RUNBOOK.md`
- **#54 P11-S02** (`Artfever`): `docs/evidence/k8s-pg-*`; `docs/evidence/k8s-rollback-*`; `docs/evidence/k8s-zero-downtime-*`; `docs/ENGINEERING-NOTES.md`
- **#55 P12-S01** (`Artfever`): `README.md`; `docs/evidence/screenshots-*`
- **#56 P12-S02** (`TahaSohail-Goat`): `scripts/check_submission.py`; `docs/FINAL_SUBMISSION_CHECKLIST.md`; `LICENSE`; `docs/PHASE_STATUS.md`; `docs/evidence/protection-*`

Files that two packages both touch are **serialized** (one after the other) or **append-only**:

| File | Rule |
|---|---|
| `docs/CACHE.md` | P06-S01 merges first (stats section); P06-S02 rebases (rate-limit and AOF sections) |
| `backend/app/services/triage.py` | #44 (fallback orchestration) and #46 (cache and latency hooks) are developed in parallel from the same `dev` commit; the second to merge resolves the real conflict (see below) |
| `compose.yaml` | P08-S01 first; P08-S02 adds frontend and Ollama services after it merges |
| `k8s/base/kustomization.yaml` | P09-S01 first; P09-S02 adds its entries after it merges |
| `docs/SUBMISSION.md` (decisions table) | edits to the owner's own rows |

Other conflict-heavy files: migrations (only #40 adds them); `backend/pyproject.toml` and lockfiles (the owner of #37 adds dependencies, or the other person opens a one-line PR); `.github/workflows` (`ci.yml` is #51, `cd.yml` and `release.yml` are #52: disjoint files, same conventions); `docs/evidence/` (distinct filename prefixes per package: `compose-*`, `ci-*`, `k8s-hpa-*`, `k8s-vpa-*`, `k8s-load-*`, `k8s-pg-*`, `k8s-rollback-*`, `k8s-zero-downtime-*`, `protection-*`, `screenshots-*`, `conflict-*`); `docs/AI-USAGE.md` (one table per contributor).

### Planned real merge conflict (rubric A5, `ASG-GH-009…011`)

The rubric wants "one deliberate merge conflict on real code, resolved". It must be **real** — produced by genuine, required changes on two genuine branches, never by editing lines just to collide. Because phases run one at a time (`AGENTS.md` §11), both branches must belong to the same phase.

- **The overlap (Phase 07):** #44 (`TahaSohail-Goat`: the fallback orchestration — on provider failure use the rules provider, record `triaged_by = "rules:fallback"`, log the WARNING) and #46 (`Artfever`: the content-hash triage cache and latency recording) both have to change the triage orchestration in `backend/app/services/triage.py`.
- **How it happens:** both branches are cut from the same `dev` commit (after Phase 06 is complete) and developed independently. #46 does not wait for #44 to merge: it codes against the `TriageProvider` interface that the assignment itself defines (§2.5), and #45 (LLM and Ollama providers) is the package that waits for #44. The second of #44 and #46 to merge resolves the conflict on their own branch.
- **Evidence** (`docs/evidence/conflict-*`): the conflict markers, the resolution, the merge/rebase result, and 2–4 sentences on why that version won — written by the person who resolved it and understood by both.
- **If git merges the two branches cleanly**, no conflict is manufactured. The next genuine overlap in the same phase is used instead (for example two open packages editing the same function), and the reason is recorded.

### Demo video speaking split (rubric J4: ≤ 5 minutes, both partners speaking)

A plan to rehearse; the real timings come from the recording.

| Time | Segment | Speaker |
|---|---|---|
| 0:00–0:20 | The problem and what CivicPulse is | both |
| 0:20–1:10 | Clean clone → one command → running, seeded system; Dashboard and Stats tour | `TahaSohail-Goat` |
| 1:10–2:00 | AI triage; fallback when the provider fails (`rules:fallback`, still 201); prompt-injection example | `Artfever` |
| 2:00–2:30 | Network isolation: `docker compose exec frontend ping database` fails | `TahaSohail-Goat` |
| 2:30–3:30 | HPA scaling under load (`kubectl get hpa -w`, chart); VPA in recommender mode | `Artfever` |
| 3:30–4:30 | Rollback both ways (`kubectl rollout undo`; re-applying the previous overlay/SHA) and when to use each | `TahaSohail-Goat` |
| 4:30–5:00 | CI/CD gates and `git shortlog -sn` | both |

### Explain-back and viva readiness (assignment §5.4)

The individual mark is the team mark × a viva factor (1.0 / 0.75 / 0.5 / 0.0), and the viva includes questions on the partner's code. So:

- Every PR description ends with three "ask me at the viva" questions; the reviewer asks at least one "why" question in the thread (`docs/GITHUB_WORKFLOW.md`).
- Before each phase's `dev` → `main` integration PR, each contributor gives the other a 10-minute walkthrough of their largest package in that phase; the integration PR notes that it happened.
- Anyone who cannot explain a package of the other after review says so in the PR thread, and the author explains it again — silence is not approval.

## Balance tracking (rubric A3/A4)
Targets: ≥ 35 commits, neither partner below 35% by `git shortlog -sn`, ≥ 5 merged PRs each linked to an issue and each reviewed by the other person. Snapshot at the end of every phase:

| Date | Phase | Commits A / B | PRs authored A / B | PRs reviewed A / B | Note |
|---|---|---|---|---|---|
| 2026-09-25 | 00 | 6 / 0 | 1 (+1 open) / 0 | 0 / 0 | Phase 00 was authored before the partner joined; PR #9 has no partner review and cannot count toward `ASG-GH-005`. |

Commands: `git shortlog -sn --no-merges origin/main`, `gh pr list --state merged --json number,author,reviews`.

## Conflict-heavy Files
These are owned by one session at a time; the concrete rules per file are in *File ownership and serialization* above:
- migrations
- `compose.yaml` and `compose.prod.yaml`
- shared K8s base (`k8s/base/kustomization.yaml`)
- `.github/workflows`
- lockfiles and `backend/pyproject.toml`
- root package/config files

## Review
Each merged PR needs a meaningful review from the other person. A review that only says "LGTM" does not count.

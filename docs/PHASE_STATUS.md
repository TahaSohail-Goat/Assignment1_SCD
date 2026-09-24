# Phase Status

Updated at the end of every phase. A phase is **Complete** only when its gate in `docs/phases/PHASE-NN-*.md` is satisfied and its PR is merged under the branch-protection rules. The next permitted phase is the first one that is not Complete.

| Phase | Name | Issue | Branch | PR | Status |
|---|---|---|---|---|---|
| 00 | Assignment Baseline & Governance | #1 (sub-issues #2–#8, follow-up #10) | `dev/1-phase-00-baseline` (retired, deleted after merge) · `feature/10-branching-model-and-review-decisions` | #9 merged to `main` 2026-09-25 (rebase-merge, no partner review) · #11 open into `dev` | Baseline merged. Follow-up #10/#11 applies the owner's review decisions; hold its merge for the partner's review. Parent #1 closes when #11 lands |
| 01 | Requirements Engineering | — | — | — | Not started |
| 02 | Architecture & Repository Structure | — | — | — | Not started |
| 03 | Frontend | — | — | — | Not started |
| 04 | Backend & Domain Layer | — | — | — | Not started |
| 05 | Data Layer | — | — | — | Not started |
| 06 | Cache, Rate Limiting & Reliability | — | — | — | Not started |
| 07 | AI Layer | — | — | — | Not started |
| 08 | Docker & Compose | — | — | — | Not started (needs Docker, B-017) |
| 09 | Kubernetes | — | — | — | Not started (needs Docker + kubectl + kind/k3d) |
| 10 | CI/CD | — | — | — | Not started |
| 11 | QA, Evidence & Reflection | — | — | — | Not started |
| 12 | Final Assignment Audit & Submission | — | — | — | Not started |

## Next permitted phase

**Phase 01 — Requirements Engineering**, planned to start on **2026-09-26** when the second member becomes a collaborator (owner decision; B-010). Phase 01 also allocates the future work between the two real collaborators, so it must not start before the partner exists.

Preconditions:
1. The partner is a repository collaborator using their own GitHub login (B-010).
2. PR #11 (branch-model documentation) is reviewed by the partner and merged into `dev`; Phase 01 branches are cut from `dev` as `feature/<issue-number>-<slug>`.
3. Protection is enabled on `main` (B-011) — an admin action right after the partner is added.

Open items that do **not** block Phase 01: B-002/B-003 (deferred by the owner), B-006 (`triaged_by` values — decide in Phase 05/07), B-001, B-007, B-008, B-013–B-016. Resolved: B-004 (nine endpoints), B-009 (`dev` + `feature/*`).

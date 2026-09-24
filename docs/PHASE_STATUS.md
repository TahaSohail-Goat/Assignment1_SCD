# Phase Status

Updated at the end of every phase. A phase is **Complete** only when its gate in `docs/phases/PHASE-NN-*.md` is satisfied and its PR is merged under the branch-protection rules. The next permitted phase is the first one that is not Complete.

| Phase | Name | Issue | Branch | PR | Status |
|---|---|---|---|---|---|
| 00 | Assignment Baseline & Governance | #1 (sub-issues #2–#8) | `dev/1-phase-00-baseline` | Phase 00 PR (open, **not merged**) | Work complete; awaiting review and merge decision (B-009, B-010, B-011) |
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

**Phase 01 — Requirements Engineering**, after the Phase 00 PR has been reviewed (documentation PRs are not merged until the repository review is complete — `START_HERE.md` §6) and the team has answered or consciously deferred the open items in `docs/BLOCKERS.md` that affect Phase 01: B-004 (endpoint count), B-006 (`triaged_by` values) and B-009 (branch model).

If the merge is deferred, Phase 01 is branched from `dev/1-phase-00-baseline` (a stacked PR) rather than from `main`, because it edits the Phase 00 documents.

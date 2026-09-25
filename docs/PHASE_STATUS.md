# Phase Status

Snapshot of 2026-09-25. Team target: everything done by Sunday 27 Sep 2026 (the Google Classroom deadline is "next Tuesday"; see [`SUBMISSION.md`](SUBMISSION.md)).

| Phase | Name | Issue | Branch | PR | Status |
|---|---|---|---|---|---|
| 00 | Assignment Baseline & Governance | #1 (sub-issues #2–#8, #10, #58, #59) | `feature/10-…` (merged) · `feature/58-…` · `feature/59-…` | #9 and #11 merged; #60, #61 open into `dev` | Nearly done: #60 and #61 merge, then `dev` goes to `main` |
| 01 | Requirements Engineering | #12 (sub-issues #13–#18) | `feature/<n>-<slug>` per issue | #19, #20, #57 open into `dev`; #14, #16, #17 still to write | In progress: `TahaSohail-Goat` finishes Phases 00–01 |
| 02 | Architecture & Repository Structure | — | — | — | Not started |
| 03 | Frontend | — | — | — | Not started |
| 04 | Backend & Domain Layer | — | — | — | Not started |
| 05 | Data Layer | — | — | — | Not started |
| 06 | Cache, Rate Limiting & Reliability | — | — | — | Not started |
| 07 | AI Layer | — | — | — | Not started |
| 08 | Docker & Compose | — | — | — | Not started (needs Docker) |
| 09 | Kubernetes | — | — | — | Not started (needs Docker + kubectl + kind/k3d) |
| 10 | CI/CD | — | — | — | Not started |
| 11 | QA, Evidence & Reflection | — | — | — | Not started |
| 12 | Final Assignment Audit & Submission | — | — | — | Not started |

## How we work now

- **Phases 00 and 01 are finished first, by `TahaSohail-Goat` (Claude Code)**, including the three Phase 01 packages that were first allocated to `Artfever` (#14, #16, #17). `Artfever` reviews them.
- **From Phase 02 both work in parallel** on their own issues as allocated in `docs/TEAM_CONTRIBUTION.md`. Where one package needs the other's merged code, that package waits; otherwise nobody waits.
- **Flow:** issue → `feature/<n>-<slug>` from `dev` → PR into `dev` → the other contributor reviews and approves → merge. The reviewer approves unless there is a real defect (broken build, missing requirement, secret, invented requirement); wording nits are comments, not change requests.
- **`dev` → `main`:** one integration PR when a coherent block is done. `main` is protected (PR, one approval, CI once it exists): that is what the assignment requires.

Instructor answers, open decisions and the deadline are in the decisions table of [`SUBMISSION.md`](SUBMISSION.md).

Remaining for full protection evidence: the ruleset screenshot in `docs/evidence/` and required status checks with `ci.yml` (Phase 10).

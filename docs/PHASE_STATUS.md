# Phase Status

Snapshot of 2026-09-26. Team target: everything done by Sunday 27 Sep 2026 (see [`SUBMISSION.md`](SUBMISSION.md)).

| Phase | Name | Issue | Branch | PR | Status |
|---|---|---|---|---|---|
| 00 | Assignment Baseline & Governance | #1 (all issues #2–#8, #10, #58, #59 closed) | `feature/58-ai-session-protocol` · `feature/59-record-instructor-answers` | #9, #11, #60 and #61 merged into `dev` | **Complete**; the `dev` → `main` integration PR carries it to `main` |
| 01 | Requirements Engineering | #12 (sub-issues #13–#18) | `feature/<n>-<slug>` per issue | #19, #20, #57 and the packages #14, #16, #17 merged | **Complete** on `dev`; on `main` with the same integration PR |
| 02 | Architecture & Repository Structure | #21 (packages #32, #33) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 03 | Frontend | #22 (packages #34, #35, #36) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever |
| 04 | Backend & Domain Layer | #23 (packages #37, #38, #39) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: TahaSohail-Goat |
| 05 | Data Layer | #24 (packages #40, #41) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 06 | Cache, Rate Limiting & Reliability | #25 (packages #42, #43) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 07 | AI Layer | #26 (packages #44, #45, #46) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 08 | Docker & Compose | #27 (packages #47, #48) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat (needs Docker) |
| 09 | Kubernetes | #28 (packages #49, #50) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat (needs Docker + kubectl + kind/k3d) |
| 10 | CI/CD | #29 (packages #51, #52) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 11 | QA, Evidence & Reflection | #30 (packages #53, #54) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |
| 12 | Final Assignment Audit & Submission | #31 (packages #55, #56) | `feature/<n>-<slug>` per package | — | Not started — issues created; owners: Artfever, TahaSohail-Goat |

## Next permitted phase

## How we work now

- **Phases 00 and 01 are finished first, by `TahaSohail-Goat` (Claude Code)**, including #14, #16 and #17, which were first allocated to `Artfever`. `Artfever` reviews them.
- **From Phase 02 both work in parallel** on their own issues as allocated in `docs/TEAM_CONTRIBUTION.md`. A package waits only for a package it depends on (listed in its issue).
- **Flow:** issue → `feature/<n>-<slug>` from `dev` → PR into `dev` → the other contributor reviews → merge. The reviewer approves unless there is a real defect (broken build, missing requirement, secret, invented requirement); wording nits are comments, not change requests.
- **`dev` → `main`:** one integration PR when a coherent block is done. `main` is protected (PR, one approval, CI once it exists): that is what the assignment requires.

Instructor answers, open decisions and the deadline are in the decisions table of [`SUBMISSION.md`](SUBMISSION.md).

Protection evidence: the ruleset exports and the CI gate demonstration in `docs/evidence/`.

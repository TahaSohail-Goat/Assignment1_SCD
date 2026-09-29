# Phase Status

Snapshot of 2026-09-26. Team target: everything done by Sunday 27 Sep 2026 (see [`SUBMISSION.md`](SUBMISSION.md)).

| Phase | Name | Issue | Branch | PR | Status |
|---|---|---|---|---|---|
| 00 | Assignment Baseline & Governance | #1 (all issues #2–#8, #10, #58, #59 closed) | `feature/58-ai-session-protocol` · `feature/59-record-instructor-answers` | #9, #11, #60 and #61 merged into `dev` | **Complete**; the `dev` → `main` integration PR carries it to `main` |
| 01 | Requirements Engineering | #12 (sub-issues #13–#18) | `feature/<n>-<slug>` per issue | #19, #20, #57 and the packages #14, #16, #17 merged | **Complete** on `dev`; on `main` with the same integration PR |
| 02 | Architecture & Repository Structure | #21 (packages #32, #33) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 03 | Frontend | #22 (packages #34, #35, #36) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. Dashboard #103 and theme #106 reached main in #111. |
| 04 | Backend & Domain Layer | #23 (packages #37, #38, #39) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 05 | Data Layer | #24 (packages #40, #41) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 06 | Cache, Rate Limiting & Reliability | #25 (packages #42, #43) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 07 | AI Layer | #26 (packages #44, #45, #46) | `feature/<n>-<slug>` per package | — | Implementation merged; live Groq/Ollama comparison measured in #112. The live-path fixes and evidence reached main in #114. |
| 08 | Docker & Compose | #27 (packages #47, #48) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 09 | Kubernetes | #28 (packages #49, #50) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 10 | CI/CD | #29 (packages #51, #52) | `feature/<n>-<slug>` per package | — | Implementation merged to main in the reviewed promotion history; see traceability for evidence. |
| 11 | QA, Evidence & Reflection | #30 (packages #53, #54) | `feature/<n>-<slug>` per package | — | Operational evidence merged; live provider comparison captured in #112 and promoted in #114. |
| 12 | Final Assignment Audit & Submission | #31 (packages #55, #56) | `feature/<n>-<slug>` per package | — | Submission package delivered through #118/#119; both video voices confirmed by Artfever. Final sign-off correction and successful main CD gate issue closure; historical caveats remain disclosed. |

## Current work

Video and backup links are in [SUBMISSION.md](SUBMISSION.md), with verification in
[evidence/submission-final-README.md](evidence/submission-final-README.md).
#113/#114 merged the live provider work; #116/#117 merged the successful release evidence.
Latest main `77cc1e0` passed CD 36554371413 after the final bonus promotion. All repository
deliverables, evidence and capped bonus implementations are on `main`. This status does not
claim a Classroom submission or erase historical rubric caveats.

## How we work now

- **Phases 00 and 01 are finished first, by `TahaSohail-Goat` (Claude Code)**, including #14, #16 and #17, which were first allocated to `Artfever`. `Artfever` reviews them.
- **From Phase 02 both work in parallel** on their own issues as allocated in `docs/TEAM_CONTRIBUTION.md`. A package waits only for a package it depends on (listed in its issue).
- **Flow:** issue → `feature/<n>-<slug>` from `dev` → PR into `dev` → the other contributor reviews → merge. The reviewer approves unless there is a real defect (broken build, missing requirement, secret, invented requirement); wording nits are comments, not change requests.
- **`dev` → `main`:** one integration PR when a coherent block is done. `main` is protected (PR, one approval, CI once it exists): that is what the assignment requires.

Instructor answers, open decisions and the deadline are in the decisions table of [`SUBMISSION.md`](SUBMISSION.md).

Protection evidence: the ruleset exports and the CI gate demonstration in `docs/evidence/`.

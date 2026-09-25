# Phase Execution Protocol

Every phase uses the same loop. **One phase at a time** (`AGENTS.md` §11): step 0 must be true before step 1 starts, and step 14 must be done before the next phase's step 0.

## 0. Gate
The previous phase is Complete: its issues are closed, its PRs are merged into `dev`, its gate is checked, its integration PR is merged into `main`, and `docs/PHASE_STATUS.md` says so. See `docs/AI_SESSIONS.md` section 6.

## 1. Read
Use the phase prompt + document index.

## 2. Plan
Build a short task checklist and identify dependencies.

## 3. Inspect
Inspect current files and existing implementation.

## 4. Issue
Ensure parent/sub-issues exist with requirement IDs.

## 5. Branch
Create `feature/<issue-number>-<slug>` from `dev`.

## 6. Implement
Make small, coherent commits.

## 7. Verify
Run tests/checks/evidence.

## 8. Document
Update docs, ADRs, evidence, traceability.

## 9. PR
Open/update the PR into `dev`. When the phase gate is met, open the `dev` → `main` integration PR (merge commit).

## 10. Review
Partner review must be substantive.

## 11. Rebase
Rebase the feature branch on `origin/dev` before merge when required. `dev` and `main` are never rebased.

## 12. Merge
Only after branch protection and CI.

## 13. Close
Update issue and phase status.

## 14. Integrate
Open the phase's `dev` → `main` integration PR (its body lists `Closes #…` for every issue of the phase), get the other contributor's approval, merge with a **merge commit**, and mark the phase Complete in `docs/PHASE_STATUS.md`.

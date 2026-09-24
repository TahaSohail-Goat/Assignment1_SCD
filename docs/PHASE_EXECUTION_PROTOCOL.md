# Phase Execution Protocol

Every phase uses the same loop:

## 1. Read
Use the phase prompt + document index.

## 2. Plan
Build a short task checklist and identify dependencies.

## 3. Inspect
Inspect current files and existing implementation.

## 4. Issue
Ensure parent/sub-issues exist with requirement IDs.

## 5. Branch
Create `dev/<issue-number>-<slug>`.

## 6. Implement
Make small, coherent commits.

## 7. Verify
Run tests/checks/evidence.

## 8. Document
Update docs, ADRs, evidence, traceability.

## 9. PR
Open/update PR.

## 10. Review
Partner review must be substantive.

## 11. Rebase
Before merge when required.

## 12. Merge
Only after branch protection and CI.

## 13. Close
Update issue and phase status.

# Final Submission Checklist

## Snapshot and interpretation

Audit follow-up #109, 2026-09-26, Artfever. Verified dev `39fca0c`, main `c5f5e38`.
This is an in-progress final audit, not a declaration that the assignment is complete.
PASS means the stated verification has supporting evidence; FAIL means a known unmet
condition; BLOCKED means final verification is held or not completed. Unverified does
not mean unimplemented. Optional/advisory rows do not create mandatory work.

Owner direction: video and live Groq/Ollama comparison are on hold until the end.
Ruleset/instructor screenshots and exact-deadline confirmation are removed from the task
list; existing ruleset exports remain. No screenshot is claimed captured. No local Ollama
service was started. Keep #55, #56 and #31 open.

## Commands and evidence

- `git shortlog -sn origin/dev`: 109 Taha Sohail, 70 Artfever (39.1%) at 39fca0c.
- `git shortlog -sn origin/main`: 109 Taha Sohail, 42 Artfever at c5f5e38.
- `python scripts/check_submission.py --ref origin/dev`: contribution floor PASS on dev; historical
  non-merge warning remains. No credential-pattern hit in any tracked path's history.
  Pattern matching cannot prove the absence of arbitrary secrets.
- Frontend: 21 tests passed, including minimum/maximum Unicode regression cases.
- Backend on merged dev CI run 36243422641: **363 passed, 94.42% coverage**, with PostgreSQL 16. Four checker regressions pass using temporary Git repos. All ten CI jobs pass. The earlier local run skipped 33 PostgreSQL tests; CI supplies that missing evidence.
- Initial scan: local Markdown file targets resolve; anchors/external URLs were not tested.
- Latest main CD [36235766515](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36235766515)
  succeeded at c5f5e38. Its cluster is ephemeral; dev-only work needs promotion.
- Historical warning: PR #9 was rebase-merged (349fe86). A linear first-parent commit is
  not proof of a direct push. All six linear first-parent commit subjects match PR #9 (first 60 characters); captured review explains the rebase merge. This reconciles the mechanical warning, not an immutable audit of every historical push event.

## Requirement verification

All 304 IDs appear once. Existing matrix claims are context, not automatic PASS verdicts.
Evidence sources and command summaries: [final-audit-index.md](evidence/final-audit-index.md). PASS entries apply to this verified snapshot; re-run on final main.

| ID | Status | Evidence and remaining verification |
|---|---|---|
| ASG-GEN-001 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-002 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-003 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-004 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-005 | BLOCKED | Owner HOLD: default Compose runs four long-lived services; optional offline profile with the fifth Ollama service has not been exercised live. |
| ASG-GEN-006 | PASS | README and screenshots-README.md document actual startup and limits; CI 36243422641 verifies Compose, main CD 36235766515 verifies ephemeral Kubernetes deployment. Signing exception is recorded in SUBMISSION.md; video remains separately held. |
| ASG-GEN-007 | PASS | README and screenshots-README.md document actual startup and limits; CI 36243422641 verifies Compose, main CD 36235766515 verifies ephemeral Kubernetes deployment. Signing exception is recorded in SUBMISSION.md; video remains separately held. |
| ASG-GEN-008 | PASS | README and screenshots-README.md document actual startup and limits; CI 36243422641 verifies Compose, main CD 36235766515 verifies ephemeral Kubernetes deployment. Signing exception is recorded in SUBMISSION.md; video remains separately held. |
| ASG-GEN-009 | PASS | README and screenshots-README.md document actual startup and limits; CI 36243422641 verifies Compose, main CD 36235766515 verifies ephemeral Kubernetes deployment. Signing exception is recorded in SUBMISSION.md; video remains separately held. |
| ASG-GEN-010 | PASS | README and screenshots-README.md document actual startup and limits; CI 36243422641 verifies Compose, main CD 36235766515 verifies ephemeral Kubernetes deployment. Signing exception is recorded in SUBMISSION.md; video remains separately held. |
| ASG-GEN-011 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-012 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-GEN-013 | PASS | Source constraints/ambiguities recorded in docx/ASSIGNMENT.md, RUBRIC.md and SUBMISSION.md; two-person project and backend contract preserved. Informational guidance is not a claim of completed live evidence. |
| ASG-FR-001 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-002 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-003 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-004 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-005 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-006 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-007 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-008 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-009 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-010 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-011 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-012 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-013 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-014 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-015 | PASS | frontend/src and final-audit-bundle.json: no recognized credential patterns in the running compiled asset. Browser configuration is public; arbitrary-secret absence cannot be proven by regex. |
| ASG-FR-016 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-017 | PASS | frontend/nginx.conf proxies /api to backend; docs/adr/0002-frontend-runtime-config.md records this permitted mechanism. |
| ASG-FR-020 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-021 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-022 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-023 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-024 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-025 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-026 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-027 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-028 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-029 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-030 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-031 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-032 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-033 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-034 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-035 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-036 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-FR-037 | PASS | frontend/tests/views.test.tsx, theme.test.tsx; backend/tests/test_contract.py, test_complaints_api.py, test_meta.py, test_state_machine.py; API snapshot check. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-001 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-002 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-003 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-004 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-005 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-006 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-007 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-008 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-009 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-010 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-011 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-012 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-013 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-014 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-015 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-016 | PASS | backend/tests/test_layering.py, test_no_ddl_in_app.py, test_graceful_shutdown.py, test_logging.py, test_request_context.py, test_determinism.py; backend/app/main.py. Merged-dev CI 36243422641 at 39fca0c: all ten jobs pass (363 backend tests, 94.42% coverage, 21 frontend tests). |
| ASG-NFR-017 | PASS | docs/evidence/final-audit-bundle.json records SHA256 and no recognized credential pattern in the actual running compiled JavaScript. |
| ASG-DATA-001 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-002 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-003 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-004 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-005 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-006 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-007 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-008 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-009 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-010 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-011 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-012 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-013 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-014 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-015 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-016 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-017 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-018 | PASS | docs/DATA_MODEL.md and ENGINEERING-NOTES.md justify both named indexes; backend/app/seed.py has 30 synthetic Urdu-influenced English rows. test_seed.py passes in PostgreSQL CI. |
| ASG-DATA-019 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-020 | PASS | docs/DATA_MODEL.md and ENGINEERING-NOTES.md justify both named indexes; backend/app/seed.py has 30 synthetic Urdu-influenced English rows. test_seed.py passes in PostgreSQL CI. |
| ASG-DATA-021 | PASS | backend/tests/test_migrations.py, test_complaint_repository.py, test_seed.py; backend/alembic/versions/0001_create_complaints.py. PostgreSQL integration passes in CI 36243422641. |
| ASG-DATA-022 | PASS | CI integration at 39fca0c exercises Compose down/up persistence; source steps in ci.yml and prior capture indexed in RUNBOOK. |
| ASG-DATA-023 | PASS | docs/evidence/k8s-pg-persistence.txt: 30 rows, identical full-row fingerprint, different pod UID and unchanged PVC UID; reviewed capture retained. |
| ASG-CACHE-001 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-002 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-003 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-004 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-005 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-006 | PASS | docs/CACHE.md and ENGINEERING-NOTES.md explain TTL plus invalidation; tests demonstrate lost invalidation bound. Human viva performance is not claimed. |
| ASG-CACHE-007 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-008 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-009 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-010 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-011 | PASS | backend/tests/test_stats_service.py, test_stats_api.py, test_rate_limit.py; compose.yaml and docs/CACHE.md. Real Redis integration in CI 36243422641; distributed ingress evidence in scripts/k8s-up.sh and prior quickstart CI. |
| ASG-CACHE-012 | PASS | docs/ENGINEERING-NOTES.md Redis volume decision explains AOF counter durability and one-second crash window. |
| ASG-AI-001 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-002 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-003 | BLOCKED | Owner HOLD on live hosted/Ollama comparison and account limits. Implementations and mocked tests exist; live hosted/offline operation and quality are not claimed. |
| ASG-AI-004 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-005 | BLOCKED | Owner HOLD on live hosted/Ollama comparison and account limits. Implementations and mocked tests exist; live hosted/offline operation and quality are not claimed. |
| ASG-AI-006 | BLOCKED | Owner HOLD on live hosted/Ollama comparison and account limits. Implementations and mocked tests exist; live hosted/offline operation and quality are not claimed. |
| ASG-AI-007 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-008 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-009 | BLOCKED | Owner HOLD on live hosted/Ollama comparison and account limits. Implementations and mocked tests exist; live hosted/offline operation and quality are not claimed. |
| ASG-AI-010 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-011 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-012 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-013 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-014 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-015 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-016 | PASS | docs/evidence/final-audit-cache.py and .json: real Redis 7.4.11; 2 synthetic service calls, 1 miss, 1 hit, 1 provider call, TTL 86400 s. Hit rate 50% for this interval only; no database writes. |
| ASG-AI-017 | PASS | docs/evidence/final-audit-cache.py and .json: real Redis 7.4.11; 2 synthetic service calls, 1 miss, 1 hit, 1 provider call, TTL 86400 s. Hit rate 50% for this interval only; no database writes. |
| ASG-AI-018 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-019 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-020 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-021 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-022 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-023 | PASS | backend/tests/test_remote_triage.py, test_triage_service.py, test_injection_cache.py, test_meta.py; backend/app/providers/triage/. Controlled HTTP/schema/fallback tests pass in CI 36243422641; does not establish live model quality. |
| ASG-AI-024 | PASS | docs/adr/0004-pii-and-data-governance.md records data flow, synthetic-data restriction and dated provider terms. Runtime tests are separate. |
| ASG-AI-025 | BLOCKED | Owner HOLD on live hosted/Ollama comparison and account limits. Implementations and mocked tests exist; live hosted/offline operation and quality are not claimed. |
| ASG-DEVOPS-001 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-002 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-003 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-004 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-005 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-006 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-007 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-008 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-009 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-010 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-011 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-012 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-013 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-014 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-015 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-016 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-017 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-018 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-019 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-020 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-021 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-022 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-023 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-024 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-025 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-026 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-027 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-028 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-DEVOPS-029 | PASS | backend/tests/test_container_files.py; both Dockerfiles, compose.yaml and compose.prod.yaml; CI 36243422641 build/scan/context-and-image-size/integration jobs pass. Optional Ollama runtime remains unverified. |
| ASG-K8S-001 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-002 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-003 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-004 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-005 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-006 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-007 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-008 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-009 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-010 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-011 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-012 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-013 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-014 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-015 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-016 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-017 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-018 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-019 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-020 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-021 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-022 | PASS | backend/tests/test_k8s_manifests.py; k8s/base and overlays; CI manifest validation; main CD 36235766515 and docs/evidence/k8s-load-README.md, k8s-pg-persistence.txt. Existing real cluster captures, not a new load run. |
| ASG-K8S-023 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-024 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-025 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-026 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-027 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-028 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-029 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-K8S-030 | PASS | docs/evidence/k8s-load-README.md and baseline50/adjusted50 raw captures: 9559 requests each, zero failures; HPA 2 to 3 baseline, VPA target 182m/250Mi applied, adjusted desired replicas 2; measured lag and Off-mode rationale documented. |
| ASG-CICD-001 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-002 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-003 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-004 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-005 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-006 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-007 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-008 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-009 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-010 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-011 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-012 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-013 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-014 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-015 | PASS | Main CD 36235766515 emits both Syft SBOMs; .github/workflows/cd.yml has the generation/upload steps. |
| ASG-CICD-016 | PASS | cd.yml exposes both build digests as job outputs and deploys those bytes under SHA tags; main CD 36235766515 succeeds. |
| ASG-CICD-017 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-018 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-019 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-020 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-021 | BLOCKED | release.yml and regression tests exist, but no successful tag-triggered release run is recorded. Final release remains to be exercised. |
| ASG-CICD-022 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-023 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-024 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-025 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-026 | PASS | backend/tests/test_ci_workflow.py and test_cd_workflows.py; .github/workflows/; CI 36243422641 and main CD 36235766515; docs/evidence/final-audit-github.json. |
| ASG-CICD-027 | PASS | docs/evidence/ci-gate.md and ci-red-check.png, ci-red-blocked.png, ci-green.png show PR #90 failing then fixed; current main rules captured in final-audit-github.json. |
| ASG-CICD-028 | PASS | docs/evidence/k8s-rollback-index.md and cd-local-rollback.txt: undo 0.18 s, overlay restore 0.94 s in rejected-rollout scenario with old replicas healthy. Not a general outage-recovery guarantee. |
| ASG-CICD-029 | PASS | docs/evidence/k8s-rollback-index.md and cd-local-rollback.txt: undo 0.18 s, overlay restore 0.94 s in rejected-rollout scenario with old replicas healthy. Not a general outage-recovery guarantee. |
| ASG-CICD-030 | BLOCKED | Owner HOLD: both rollback methods still need the required video. |
| ASG-CICD-031 | PASS | docs/evidence/k8s-rollback-index.md and cd-local-rollback.txt: undo 0.18 s, overlay restore 0.94 s in rejected-rollout scenario with old replicas healthy. Not a general outage-recovery guarantee. |
| ASG-GH-001 | BLOCKED | Protection settings verified in final-audit-github.json. Owner removed the separate ruleset screenshot task; no screenshot or instructor waiver is claimed. Original rubric evidence caveat remains. |
| ASG-GH-002 | PASS | docs/evidence/final-audit-github.json: current main PR+approval+ten-check rules; five merged, issue-linked PRs with substantive partner reviews. git history and docs/GITHUB_WORKFLOW.md. |
| ASG-GH-003 | PASS | docs/evidence/final-audit-github.json: current main PR+approval+ten-check rules; five merged, issue-linked PRs with substantive partner reviews. git history and docs/GITHUB_WORKFLOW.md. |
| ASG-GH-004 | PASS | docs/evidence/final-audit-github.json: current main PR+approval+ten-check rules; five merged, issue-linked PRs with substantive partner reviews. git history and docs/GITHUB_WORKFLOW.md. |
| ASG-GH-005 | PASS | docs/evidence/final-audit-github.json: current main PR+approval+ten-check rules; five merged, issue-linked PRs with substantive partner reviews. git history and docs/GITHUB_WORKFLOW.md. |
| ASG-GH-006 | PASS | git shortlog -sn origin/dev at 39fca0c: Artfever 70/179 (39.1%), Taha 109/179 (60.9%). Both exceed 35%; refresh on final main. |
| ASG-GH-007 | FAIL | Six historical non-merge subjects do not match the conventional-prefix pattern (including bootstrap first commit and one leading BOM). Exact commits are recorded in evidence/final-audit-index.md; shared history is preserved. |
| ASG-GH-008 | PASS | git shortlog -sn origin/dev at 39fca0c: Artfever 70/179 (39.1%), Taha 109/179 (60.9%). Both exceed 35%; refresh on final main. |
| ASG-GH-009 | PASS | docs/evidence/issue-46-triage-conflict.txt contains raw add/add markers and four-sentence resolution rationale. PR #70 merged as 61e129a; backend/app/services/triage.py retains orchestration with cache hooks. |
| ASG-GH-010 | PASS | docs/evidence/issue-46-triage-conflict.txt contains raw add/add markers and four-sentence resolution rationale. PR #70 merged as 61e129a; backend/app/services/triage.py retains orchestration with cache hooks. |
| ASG-GH-011 | PASS | docs/evidence/issue-46-triage-conflict.txt contains raw add/add markers and four-sentence resolution rationale. PR #70 merged as 61e129a; backend/app/services/triage.py retains orchestration with cache hooks. |
| ASG-DOC-001 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-002 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-003 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-004 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-005 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-006 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-007 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-008 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-009 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-010 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-011 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-012 | PASS | Conditional requirement does not apply: project uses Kustomize, not Helm. |
| ASG-DOC-013 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-014 | BLOCKED | Owner HOLD: unlisted video, both partners speaking, at most five minutes. |
| ASG-DOC-015 | BLOCKED | Owner HOLD: unlisted video, both partners speaking, at most five minutes. |
| ASG-DOC-016 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-017 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-018 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-019 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-020 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-021 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-022 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-023 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-024 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-025 | PASS | README.md, docs/adr/0001..0004, docs/RUNBOOK.md, docs/ENGINEERING-NOTES.md and docs/AI-USAGE.md; docs/evidence/screenshots-README.md. Source/document inspection plus test_readme.py in CI 36243422641. |
| ASG-DOC-026 | PASS | docs/TRIAGE.md exists and explains provider operation and measurement scope; assignment does not prescribe its contents. |
| ASG-DOC-027 | BLOCKED | Existing conflict/CI/HPA/chart evidence is present; owner removed the separate ruleset screenshot task. Original screenshot clause remains a disclosed rubric caveat, not a new active task. |
| ASG-DOC-028 | PASS | Conditional incident policy recorded in SECURITY.md. No credential-pattern match found in current full-history scan; no credential incident is invented. |
| ASG-BONUS-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Measured: zero failed requests during a rolling replacement under k6 load (two runs); the video is pending |
| ASG-BONUS-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Partial: images are deployed by digest under the SHA tag (`cd.yml`); Cosign signing and verification are not done |
| ASG-BONUS-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-006 | PASS | Backend Dockerfile pins both stages by digest; third-party Actions are SHA-pinned; bonus cap is documented in RUBRIC.md. These are component checks, not a claim of full signing bonus. |
| ASG-BONUS-007 | PASS | Backend Dockerfile pins both stages by digest; third-party Actions are SHA-pinned; bonus cap is documented in RUBRIC.md. These are component checks, not a claim of full signing bonus. |
| ASG-BONUS-008 | PASS | Backend Dockerfile pins both stages by digest; third-party Actions are SHA-pinned; bonus cap is documented in RUBRIC.md. These are component checks, not a claim of full signing bonus. |
| ASG-DED-001 | PASS | Submission lint at 39fca0c scans tracked files and every history path for recognized credential patterns and secret filenames; no matches. Pattern scan limitation documented. |
| ASG-DED-002 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-003 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-004 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-005 | PASS | CI 36243422641 integration negative frontend/database DNS check passes; prior actual local output in screenshots-compose-output.txt. |
| ASG-DED-006 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-007 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-008 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-009 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-010 | PASS | Current main requires PR/approval/checks. All six linear first-parent subjects match PR #9 rebase-merge history; see final-audit-index.md. Mechanical warning is retained. |
| ASG-DED-011 | PASS | README clean-clone capture screenshots-README.md; current dev CI integration passes startup/persistence paths. Kubernetes quickstart has prior clean-runner evidence; no new cold-build timing claim. |
| ASG-SUB-001 | PASS | gh repo view confirms PUBLIC; URL in SUBMISSION.md. |
| ASG-SUB-002 | PASS | Main CD run 36235766515 succeeded at c5f5e38. Refresh after final promotion. |
| ASG-SUB-003 | PASS | Both GHCR c5f5e38 full-SHA tags resolve via docker buildx imagetools inspect; manifest digests captured in evidence/final-audit-github.json. |
| ASG-SUB-004 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-SUB-005 | PASS | Command, revision and shortlog snapshot recorded in SUBMISSION.md; refresh final main. |
| ASG-SUB-006 | PASS | docs/evidence/k8s-load-baseline50/hpa-watch.txt and k8s-load-comparison.png exist; load method and findings checked against k8s-load-README.md. |
| ASG-SUB-007 | PASS | Submission lint executed on origin/dev 39fca0c; actual output in evidence/final-audit-index.md. Must repeat after final promotion. |
| ASG-SUB-008 | PASS | Policy recorded in SUBMISSION.md and AI-USAGE.md. No claim of future submission timing or human viva performance; deadline confirmation is not an active owner task. |
| ASG-SUB-009 | PASS | Policy recorded in SUBMISSION.md and AI-USAGE.md. No claim of future submission timing or human viva performance; deadline confirmation is not an active owner task. |
| ASG-SUB-010 | PASS | Policy recorded in SUBMISSION.md and AI-USAGE.md. No claim of future submission timing or human viva performance; deadline confirmation is not an active owner task. |
| ASG-SUB-011 | PASS | Policy recorded in SUBMISSION.md and AI-USAGE.md. No claim of future submission timing or human viva performance; deadline confirmation is not an active owner task. |
| ASG-SUB-012 | PASS | Policy recorded in SUBMISSION.md and AI-USAGE.md. No claim of future submission timing or human viva performance; deadline confirmation is not an active owner task. |
| ASG-REPO-001 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `backend/app/{routes,services,repositories,providers}/` |
| ASG-REPO-002 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `backend/app/providers/triage/{base,llm,ollama,rules,simulated,factory}.py` |
| ASG-REPO-003 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `backend/alembic/versions/` |
| ASG-REPO-004 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `backend/tests/` |
| ASG-REPO-005 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `backend/Dockerfile`, `backend/.dockerignore`, `backend/pyproject.toml` |
| ASG-REPO-006 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `frontend/src/{components,pages,api}/` |
| ASG-REPO-007 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `frontend/tests/` |
| ASG-REPO-008 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `frontend/Dockerfile`, `frontend/.dockerignore`, `frontend/nginx.conf`, `frontend/package.json` |
| ASG-REPO-009 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `k8s/base/{namespace,backend,frontend,postgres,redis,ingress,configmap,secret}.yaml` |
| ASG-REPO-010 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `k8s/base/{hpa,vpa,pdb}.yaml`, `k8s/base/kustomization.yaml` |
| ASG-REPO-011 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `k8s/overlays/{dev,prod}/kustomization.yaml` |
| ASG-REPO-012 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `load/k6-script.js` |
| ASG-REPO-013 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `docs/{ENGINEERING-NOTES,RUNBOOK,AI-USAGE,TRIAGE}.md` |
| ASG-REPO-014 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `docs/adr/0001-provider-interface.md` … `0004-pii-and-data-governance.md` |
| ASG-REPO-015 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `docs/evidence/` |
| ASG-REPO-016 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `scripts/check_submission.py` |
| ASG-REPO-017 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `.github/workflows/{ci.yml,cd.yml,release.yml}` |
| ASG-REPO-018 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `compose.yaml`, `compose.prod.yaml`, `.env.example`, `.gitignore` |
| ASG-REPO-019 | PASS | Tracked layout verified by git ls-files and the 54-path checker. `README.md`, `LICENSE` |

## Rubric lines

Mappings and marks: [RUBRIC.md](RUBRIC.md).

| Rubric | Status | Evidence / remaining verification |
|---|---|---|
| A1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| A2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| A3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| A4 | FAIL | Count/share thresholds pass on dev; historical conventional-prefix exceptions remain (ASG-GH-007). |
| A5 | PASS | Raw markers, four-sentence resolution and PR #70 merge evidence are linked in ASG-GH-009..011. |
| B1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| B2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| B3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| B4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| B5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C6 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| C7 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| D1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| D2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| D3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| D4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| E1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| E2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| E3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| E4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F6 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| F7 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| G1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| G2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| G3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| G4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| G5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G6 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| H6 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I4 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I6 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| I7 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| J1 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| J2 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| J3 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| J4 | BLOCKED | Owner HOLD: both-partner unlisted video. |
| J5 | PASS | Mapped requirement evidence above; CI/captures indexed in evidence/final-audit-index.md. Scope limits in those rows apply. |
| BON1 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON2 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON3 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON4 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON5 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |

## Final handoff

1. Partner reviews #109 evidence update; #108 is merged. Promotion of reviewed dev needs a separate approval.
2. Refresh contribution counts on dev and main; exclude unrelated/unmerged branches.
3. Finish per-ID and rubric evidence review, including PostgreSQL integration on final head.
4. Resume held comparison/video when Artfever directs it; add actual results and video link.
5. Promote reviewed dev changes; verify new main CD and refresh submission references.
6. Close #55/#56/#31 only when their acceptance criteria are met.

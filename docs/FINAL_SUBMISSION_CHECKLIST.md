# Final Submission Checklist

## Snapshot and interpretation

Audit follow-up #107, 2026-09-26, Artfever. Baseline dev `a4cd0b9`, main `c5f5e38`.
This is an in-progress final audit, not a declaration that the assignment is complete.
PASS means the stated verification has supporting evidence; FAIL means a known unmet
condition; BLOCKED means final verification is held or not completed. Unverified does
not mean unimplemented. Optional/advisory rows do not create mandatory work.

Owner direction: video and live Groq/Ollama comparison are on hold until the end.
Ruleset/instructor screenshots and exact-deadline confirmation are removed from the task
list; existing ruleset exports remain. No screenshot is claimed captured. No local Ollama
service was started. Keep #55, #56 and #31 open.

## Commands and evidence

- `git shortlog -sn origin/dev`: 109 Taha Sohail, 47 Artfever (30.1%) at a4cd0b9.
- `git shortlog -sn origin/main`: 109 Taha Sohail, 42 Artfever at c5f5e38.
- `python scripts/check_submission.py --ref origin/dev`: contribution floor FAIL; historical
  non-merge warning remains. No credential-pattern hit in any tracked path's history.
  Pattern matching cannot prove the absence of arbitrary secrets.
- Frontend: 21 tests passed, including minimum/maximum Unicode regression cases.
- Backend with checker regressions: 330 passed, 33 skipped without TEST_DATABASE_URL. This does not
  re-prove PostgreSQL integration or coverage. Four checker regression cases pass using temporary Git repos. Backend lint and mypy, frontend lint/typecheck/build pass.
- Initial scan: local Markdown file targets resolve; anchors/external URLs were not tested.
- Latest main CD [36235766515](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36235766515)
  succeeded at c5f5e38. Its cluster is ephemeral; dev-only work needs promotion.
- Historical warning: PR #9 was rebase-merged (349fe86). A linear first-parent commit is
  not proof of a direct push. Final reviewer must reconcile the complete main history.

## Requirement verification

All 304 IDs appear once. Existing matrix claims are context, not automatic PASS verdicts.
BLOCKED rows require final evidence review, not necessarily new code. Re-run on final main.

| ID | Status | Evidence and remaining verification |
|---|---|---|
| ASG-GEN-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-GEN-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Info (deadline: `SUBMISSION.md`) |
| ASG-GEN-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Info (rubric left to the TA: `SUBMISSION.md`) |
| ASG-GEN-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-GEN-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; CI-run stack (database, cache, backend, frontend; Ollama behind `--profile offline`); demo video pending |
| ASG-GEN-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; CI-proven: `k8s-quickstart` workflow and `cd.yml` deploy (probed, HPA present) |
| ASG-GEN-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; the macOS/Linux command in the README is what the CI integration job runs on a clean runner, and the PowerShell block was verified on a clean clone (#100); clean-clone video pending |
| ASG-GEN-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; `bash scripts/k8s-up.sh` runs on a clean runner in the `k8s-quickstart` workflow |
| ASG-GEN-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; cd run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 tested, published by SHA, scanned in CI, deployed; both rollbacks in `docs/RUNBOOK.md` (signing not required: `SUBMISSION.md`) |
| ASG-GEN-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; README has a 'Demo video and remaining handover' section and `test_readme.py` checks every link |
| ASG-GEN-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-GEN-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-GEN-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-FR-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34) |
| ASG-FR-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Three views implemented (#35/#36) |
| ASG-FR-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35/#36) |
| ASG-FR-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35/#36) |
| ASG-FR-005 | PASS | frontend/src/pages/Submit.tsx; frontend/tests/views.test.tsx: Unicode boundaries verified; 21 frontend tests pass. PR review pending. |
| ASG-FR-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35); covered by the component tests |
| ASG-FR-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35/#36); delayed request and 429 `Retry-After` tests pass |
| ASG-FR-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35, #36); #102 adds tested stale-row clearing, retry and last-page recovery (merged in PR #103; awaiting promotion) |
| ASG-FR-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#35/#36); forbidden transition captured |
| ASG-FR-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Component test passed (#36); screenshot captured (#35) |
| ASG-FR-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#36); screenshot captured |
| ASG-FR-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#36); HIT/MISS/missing tested; screenshot captured |
| ASG-FR-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34, #39): `check:api-contract` and `test_contract.py` compare the snapshot with the served OpenAPI |
| ASG-FR-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#36) |
| ASG-FR-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34): no key or secret in `frontend/src`; the API is same-origin |
| ASG-FR-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34, #48): relative `/api` calls, nginx proxy; one image for every environment |
| ASG-FR-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34, #48): the nginx-proxy option, stated in ADR 0002 |
| ASG-FR-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented for validate and persist (P04-S02, #38); triage in #44, limiter in #43 |
| ASG-FR-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#43); a real Redis 429 with `Retry-After` is checked by the CI integration job (RUNBOOK section 8) |
| ASG-FR-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-025 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-026 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-027 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-028 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-029 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-FR-030 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#46) |
| ASG-FR-031 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-FR-032 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-FR-033 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-FR-034 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-035 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-FR-036 | BLOCKED | Final source/evidence review outstanding. Matrix: All nine endpoints implemented; #46 merged. Contract and metadata tests pass; see backend/tests/test_contract.py and test_meta.py |
| ASG-FR-037 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#38, #46, #35); the CI integration job creates and reads a complaint end to end; demo video pending |
| ASG-NFR-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-NFR-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S02, #38) |
| ASG-NFR-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-NFR-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-NFR-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S01, #37) |
| ASG-NFR-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-NFR-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S03, #39) |
| ASG-NFR-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S03, #39) |
| ASG-NFR-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#36); #102 adds two reproduced Dashboard regressions; CI/review pending on follow-up |
| ASG-NFR-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P04-S03, #39) |
| ASG-NFR-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#47, #49, #91): service names in Compose and Kubernetes; `check_submission.py` scans both |
| ASG-NFR-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34): no credential in the bundle; `check_submission.py` scans for key patterns |
| ASG-DATA-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#40, #47): `postgres:16.10-alpine` in Compose, CI and Kubernetes |
| ASG-DATA-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P05-S01, #40) |
| ASG-DATA-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#41); PostgreSQL CI passed on PR #79 |
| ASG-DATA-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#41) |
| ASG-DATA-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#41); PostgreSQL CI passed on PR #79 |
| ASG-DATA-022 | BLOCKED | Final source/evidence review outstanding. Matrix: CI evidence (P11, #53): rows survive `down` then `up`, run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36189116384; video demo pending |
| ASG-DATA-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: 30 rows and a full-row fingerprint preserved when `database-0` is deleted (local capture, reviewed in #96; repeated on a clean runner by `k8s-quickstart`) |
| ASG-CACHE-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#42, #47): `redis:7.4.11-alpine` |
| ASG-CACHE-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-CACHE-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-CACHE-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-CACHE-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-CACHE-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P06-S01, #42) |
| ASG-CACHE-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#43); checked against a real Redis in the CI integration job |
| ASG-CACHE-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#43) |
| ASG-CACHE-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#43); the CI integration job prints the 429 and its `Retry-After` |
| ASG-CACHE-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#43); `k8s-quickstart` sends requests through the Ingress to two backend replicas and sees the shared limit answer 429 |
| ASG-CACHE-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); restart check in #53 |
| ASG-CACHE-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Decision recorded (#43) |
| ASG-AI-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-003 | BLOCKED | Final source/evidence review outstanding. Matrix: All four implemented across #44/#45; live paths pending |
| ASG-AI-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented for all four providers (#44/#45) |
| ASG-AI-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#45); live call pending |
| ASG-AI-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#45, #48): the Ollama service and the model preload are in Compose (`--profile offline`); not exercised end to end in CI |
| ASG-AI-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Published limits checked (#45); account-specific live check pending |
| ASG-AI-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#45) |
| ASG-AI-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#45) |
| ASG-AI-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Inspected (#45) |
| ASG-AI-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Orchestration and HTTP call timeouts implemented (#44/#45) |
| ASG-AI-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented with in-memory store (#46); real Redis verification pending |
| ASG-AI-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Test interval measured (#46); real Redis workload pending |
| ASG-AI-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Provider checked (#45); deployment secrets pending |
| ASG-AI-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented across #45/#46 |
| ASG-AI-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#46) |
| ASG-AI-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P07-S01, #44) |
| ASG-AI-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#46) |
| ASG-AI-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Decision recorded (#46); deployment check pending |
| ASG-AI-025 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-DEVOPS-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#47, #48): both images multi-stage, pinned, non-root |
| ASG-DEVOPS-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#47, #48): `HEALTHCHECK` in both Dockerfiles |
| ASG-DEVOPS-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Built in CI (#91, 2936f8a); pinned Node 22 and nginx 1.27, non-root runtime |
| ASG-DEVOPS-009 | BLOCKED | Final source/evidence review outstanding. Matrix: CI (#91, 2936f8a) checked runtime has no Node, node_modules or source |
| ASG-DEVOPS-010 | BLOCKED | Final source/evidence review outstanding. Matrix: CI (#91, 2936f8a): builder 288 MB, security-updated runtime 60.1 MB (~60 MB guide) |
| ASG-DEVOPS-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Frontend ignore measured in CI (#91, 2936f8a) |
| ASG-DEVOPS-012 | BLOCKED | Final source/evidence review outstanding. Matrix: CI (#91, 2936f8a): frontend context 105.95 MB without ignore, 160.17 kB with ignore |
| ASG-DEVOPS-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Frontend edge-only in both Compose files; CI integration green (#91, 2936f8a) |
| ASG-DEVOPS-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-017 | BLOCKED | Final source/evidence review outstanding. Matrix: CI (#91, 2936f8a): ping failed with bad address database; video pending |
| ASG-DEVOPS-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#32, #54): answered in `docs/ENGINEERING-NOTES.md` Q7 and `docs/ARCHITECTURE.md` |
| ASG-DEVOPS-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-025 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented: every image tag pinned; the backend base image is also pinned by digest |
| ASG-DEVOPS-026 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-027 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P08-S01, #47); built and started in CI: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-DEVOPS-028 | BLOCKED | Final source/evidence review outstanding. Matrix: Production Compose has no database/cache ports; static check and CI green (#91, 2936f8a) |
| ASG-DEVOPS-029 | BLOCKED | Final source/evidence review outstanding. Matrix: Standalone image-only production Compose added; static check and CI green (#91, 2936f8a) |
| ASG-K8S-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented: kind, in `scripts/k8s-up.sh`, `k8s-quickstart.yml` and `cd.yml` |
| ASG-K8S-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#49); `/` and `/api/stats` answered through the Ingress in cd run https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 and in `k8s-quickstart` |
| ASG-K8S-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Zero failed requests in both captures; video pending |
| ASG-K8S-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P09-S01, #49); rendered and schema-checked by CI, not yet deployed to a cluster |
| ASG-K8S-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-025 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-026 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-027 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-028 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-029 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-K8S-030 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; measured locally; reviewed (#93) |
| ASG-CICD-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: `ci.yml`, `cd.yml`, `release.yml` (and `k8s-quickstart.yml`) |
| ASG-CICD-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: `main` and `dev` protected by rulesets with the ten required checks (exports and the red-then-green demonstration) |
| ASG-CICD-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (P10-S01, #51); green run: https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36164848945 |
| ASG-CICD-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: ten required checks on `main` and `dev`; blocking shown in `docs/evidence/ci-gate.md` |
| ASG-CICD-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-014 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-015 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: credentials only from GitHub Secrets and `GITHUB_TOKEN` (`packages: write` only in the publishing job) |
| ASG-CICD-025 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: explicit least-privilege `permissions:` in every workflow |
| ASG-CICD-026 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: every third-party action pinned to a commit SHA in every workflow |
| ASG-CICD-027 | BLOCKED | Final source/evidence review outstanding. Matrix: Done (P10-S01, #51): PR #90 red then green |
| ASG-CICD-028 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-029 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-CICD-030 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-CICD-031 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-GH-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: rulesets on `main` and `dev` with PR, approvals and the ten required checks; evidence is the exports and the red-then-green demonstration |
| ASG-GH-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: `dev` and `feature/<n>-<slug>` branches; the six commits on `main` before the rulesets are the Phase 00 baseline (`SUBMISSION.md`) |
| ASG-GH-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: 44 merged pull requests, 21 of them with a substantive partner review (threshold 5) |
| ASG-GH-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: every merged PR names its issue (`Related issue` or `Closes`) |
| ASG-GH-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Partial: 21 of 44 merged PRs carry a substantive partner review; the others are mostly small follow-ups (CI, evidence, docs) and the earliest baseline PR. Post-merge partner reviews of the remaining PRs are still welcome |
| ASG-GH-006 | PASS | 156 commits at origin/dev a4cd0b9 (threshold 35). |
| ASG-GH-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: 105 of 111 commit subjects use a conventional prefix; six do not (one initial commit, five early frontend commits) |
| ASG-GH-008 | FAIL | 47/156 = 30.1% Artfever at a4cd0b9; minimum 35% required on final revision. |
| ASG-GH-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: a real add/add conflict in `backend/app/services/triage.py` between #44 and #46, resolved in #70 |
| ASG-GH-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: markers, resolution and merge in the evidence file |
| ASG-GH-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: the resolution paragraph of the evidence file explains why the kept version won |
| ASG-DOC-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55) |
| ASG-DOC-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55) |
| ASG-DOC-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55) |
| ASG-DOC-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55, #100); the PowerShell block was verified on a clean clone, and the equivalent command is exercised by the CI integration job |
| ASG-DOC-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55) |
| ASG-DOC-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55, #100): three real application screenshots (Submit, Dashboard, Stats) plus the CI-gate and HPA captures |
| ASG-DOC-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#55): the README states FastAPI, not Flask |
| ASG-DOC-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#46) |
| ASG-DOC-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#34, #48): the nginx-proxy choice is stated |
| ASG-DOC-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented; local checks/rehearsal; main CD run 36230267941 succeeded; video pending |
| ASG-DOC-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#46) |
| ASG-DOC-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-DOC-013 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented (#53): every section written; sections 1-10 and 11-12 are run in CI; rollback measured |
| ASG-DOC-014 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-DOC-015 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-DOC-016 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96); the more-than-one-hour duration is confirmed by Artfever |
| ASG-DOC-017 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-018 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-019 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-020 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-021 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-022 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-023 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96) |
| ASG-DOC-024 | BLOCKED | Final source/evidence review outstanding. Matrix: Done; reviewed (#96); the more-than-one-hour duration is confirmed by Artfever |
| ASG-DOC-025 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented: one row per pull request for both contributors |
| ASG-DOC-026 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented as operations/evidence guide (#46) |
| ASG-DOC-027 | BLOCKED | Final source/evidence review outstanding. Matrix: Implemented: conflict, blocked merge, `hpa -w`, scaling chart, ruleset exports and the CI gate demonstration |
| ASG-DOC-028 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-BONUS-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Measured: zero failed requests during a rolling replacement under k6 load (two runs); the video is pending |
| ASG-BONUS-002 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Partial: images are deployed by digest under the SHA tag (`cd.yml`); Cosign signing and verification are not done |
| ASG-BONUS-004 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Not started |
| ASG-BONUS-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: both stages of `backend/Dockerfile` pin `python:3.12.14-slim-bookworm` by sha256 digest |
| ASG-BONUS-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Done: every third-party action in `ci.yml`, `cd.yml`, `release.yml` and `k8s-quickstart.yml` is pinned to a commit SHA |
| ASG-BONUS-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-DED-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Guard active (`.gitignore` added in Phase 00) |
| ASG-DED-002 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-003 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-004 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-005 | BLOCKED | Final source/evidence review outstanding. Matrix: Clear: the CI integration job shows the frontend cannot resolve `database` |
| ASG-DED-006 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-007 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-008 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-009 | PASS | Static guard checked by scripts/check_submission.py and existing container/Kubernetes/workflow tests. Recheck final revision. |
| ASG-DED-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Guard active (rulesets); initial commit: `SUBMISSION.md` |
| ASG-DED-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Clear: the quickstart is what the CI integration job and `k8s-quickstart` run on clean runners |
| ASG-SUB-001 | BLOCKED | Final source/evidence review outstanding. Matrix: Info (repo is public) |
| ASG-SUB-002 | PASS | Main CD run 36235766515 succeeded at c5f5e38. Refresh after final promotion. |
| ASG-SUB-003 | BLOCKED | Final source/evidence review outstanding. Matrix: Ready: both images are public in GHCR with SHA tags (`ghcr.io/tahasohail-goat/civicpulse-backend` and `-frontend`) |
| ASG-SUB-004 | BLOCKED | Owner HOLD: video or live comparison. Implementation does not replace actual evidence. |
| ASG-SUB-005 | PASS | Command, revision and shortlog snapshot recorded in SUBMISSION.md; refresh final main. |
| ASG-SUB-006 | BLOCKED | Final source/evidence review outstanding. Matrix: Ready: `docs/evidence/k8s-load-baseline50/hpa-watch.txt` and `k8s-load-comparison.png` |
| ASG-SUB-007 | BLOCKED | Final source/evidence review outstanding. Matrix: Script written (P12-S02, #56); final run and its output recorded at submission |
| ASG-SUB-008 | BLOCKED | Final source/evidence review outstanding. Matrix: Info (deadline: `SUBMISSION.md`) |
| ASG-SUB-009 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-SUB-010 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-SUB-011 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
| ASG-SUB-012 | BLOCKED | Final source/evidence review outstanding. Matrix: Info |
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
| A2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| A3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| A4 | FAIL | Contribution floor unmet at baseline; ASG-GH-008. |
| A5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| B1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| B2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| B3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| B4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| B5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C6 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| C7 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| D1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| D2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| D3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| D4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| E1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| E2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| E3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| E4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F6 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| F7 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| G6 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| H6 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I4 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I6 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| I7 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| J1 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| J2 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| J3 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| J4 | BLOCKED | Owner HOLD: both-partner unlisted video. |
| J5 | BLOCKED | Reconcile all mapped requirement evidence before final sign-off. |
| BON1 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON2 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON3 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON4 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |
| BON5 | BLOCKED | Optional bonus; assess only actual evidence. Not a mandatory blocker. |

## Final handoff

1. Partner reviews #107 and CI, then Artfever merges after approval.
2. Refresh contribution counts on dev and main; exclude unrelated/unmerged branches.
3. Finish per-ID and rubric evidence review, including PostgreSQL integration on final head.
4. Resume held comparison/video when Artfever directs it; add actual results and video link.
5. Promote reviewed dev changes; verify new main CD and refresh submission references.
6. Close #55/#56/#31 only when their acceptance criteria are met.

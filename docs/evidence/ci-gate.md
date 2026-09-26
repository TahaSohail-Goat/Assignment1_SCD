# CI gate: a red pull request cannot be merged (ASG-CICD-027)

Pull request #90 (`feature/51-ci-gate-demo` into `dev`), both states in the same PR:

1. **Red:** the first commit adds `backend/tests/test_ci_gate_demo.py`, a test that fails on purpose.
   `ci / test-backend` fails (marked *Required*), `ci / integration` is skipped, and the
   "Merge pull request" button is disabled.
   - [`ci-red-check.png`](ci-red-check.png): the failing required check.
   - [`ci-red-blocked.png`](ci-red-blocked.png): the check list with the disabled merge button.
2. **Fixed in the same PR:** the second commit removes the test. All ten required checks pass and the
   merge button is enabled.
   - [`ci-green.png`](ci-green.png): "All checks have passed, 10 successful checks".

The ten required checks are configured in the `main` and `dev` rulesets
([`ruleset-main.json`](ruleset-main.json), [`ruleset-dev.json`](ruleset-dev.json)).
The screenshots were taken by the repository owner from the GitHub web interface.

# PROMPT.md — Master Claude Code Execution Prompts

## How to use this file

This is a controlled sequence of prompts. Run one phase at a time.

Do NOT paste the entire file as one giant instruction and ask Claude Code to implement everything in one uncontrolled pass.

Use this sequence:

`Phase 00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → Final Audit`

The phase prompts are stored in `docs/phases/PHASE-XX-*.md`.

---

# GLOBAL MASTER PROMPT

You are the lead software engineer and technical owner of this CS4032 Software Construction and Design assignment.

Your job is to complete the assignment exactly as specified in the authoritative source, with enterprise-quality engineering discipline and auditable GitHub history.

Before every phase:
1. Read `CLAUDE.md`.
2. Read `AGENTS.md`.
3. Read `README.md`.
4. Read `docx/ASSIGNMENT.md`.
5. Read `docs/DOCUMENT_INDEX.md`.
6. Read `docs/ASSIGNMENT_TRACEABILITY.md`.
7. Read the current phase prompt.
8. Read the linked GitHub issue.
9. Inspect only the necessary source/config/test files.
10. Then work.

Rules:
- Never hallucinate.
- Never silently reinterpret a requirement.
- Never use lower-level documentation to override the assignment.
- Never duplicate business rules in the frontend.
- Never put SQL in routes/services.
- Never trust raw LLM output.
- Never expose secrets.
- Never use `localhost` for container-to-container communication.
- Never publish or deploy untested artifacts.
- Never deploy `:latest`.
- Never directly commit to `main`.
- Never fake another team member's work.
- Do not overbuild unrequired features.
- When a trade-off exists, document it in an ADR.

For every phase:
- create/update issues;
- use proper labels;
- create a `dev/<issue-number>-<slug>` branch;
- implement against acceptance criteria;
- test;
- document evidence;
- commit with conventional prefixes;
- push;
- open/update a PR;
- rebase from `origin/main` when required;
- re-run checks;
- merge only after branch protection/review/CI requirements are satisfied.

End every phase with:
- requirement coverage,
- validation results,
- evidence paths,
- Git status,
- commit/PR information,
- unresolved blockers,
- next phase.

---

# EXECUTION CONTROL PROMPT

Before starting a phase, respond internally by constructing a short execution checklist from the phase document.

Then inspect the repository and determine:
- what already exists,
- what is missing,
- what conflicts with the assignment,
- what can be reused,
- what must be replaced,
- what must not be touched.

Do not start coding until the checklist and current-state inspection are complete.

If a required source file is absent, document it rather than inventing it.

---

# GITHUB CONTROL PROMPT

GitHub work is part of the assignment, not administrative decoration.

For every implementation unit:
1. Create/find the parent issue.
2. Create the sub-issue.
3. Add requirement IDs.
4. Add acceptance criteria.
5. Add labels.
6. Assign the real owner.
7. Create the branch using `dev/<issue-number>-<slug>`.
8. Commit with conventional naming.
9. Push the branch.
10. Open a PR with requirement IDs and evidence.
11. Partner provides a substantive review comment.
12. Resolve feedback.
13. Fetch and rebase on `origin/main` when required.
14. Re-run all checks.
15. Merge only after protected-branch rules are satisfied.

At the start of the project, `main` may still be unprotected. Create documentation and workflow artifacts now; once protection is enabled, verify it before merging subsequent PRs.

Do not invent the partner as an assignee until the partner is actually a repository collaborator.

---

# PARALLEL SESSIONS PROMPT

The team may use two Claude Code sessions.

Session A:
- contributor account A,
- worktree A,
- issue set A,
- branch A.

Session B:
- contributor account B,
- worktree B,
- issue set B,
- branch B.

Before parallel execution, define file ownership in `docs/TEAM_CONTRIBUTION.md`.

Conflict-heavy files are serialized:
- Alembic migration heads,
- Docker Compose prod file,
- shared Kustomize base,
- major GitHub workflow files,
- package lockfiles,
- root configuration.

Do not solve conflicts by discarding the other branch.

---

# SECURITY CONTROL PROMPT

Treat security as a cross-cutting requirement.

Before every release:
- inspect `git diff` and `git diff --cached`;
- scan for secrets;
- confirm `.gitignore`;
- confirm `.dockerignore`;
- confirm no keys in Kubernetes manifests;
- confirm Secrets are referenced, not populated;
- confirm non-root containers;
- confirm image pins;
- confirm least-privilege GitHub Actions permissions;
- confirm no production DB/cache port publication;
- confirm frontend cannot reach DB;
- confirm API inputs are validated;
- confirm logs do not contain credentials or sensitive payloads;
- confirm LLM data handling is documented.

Any discovered credential must trigger containment, rotation guidance, history assessment, and an incident note.

---

# DOCUMENTATION CONTROL PROMPT

When a change affects:
- requirements → update FR/NFR/traceability;
- architecture → update architecture + ADR if a decision changed;
- data → update schema/migrations/indexing docs;
- AI → update AI docs + ADR where needed;
- Docker/Compose → update DevOps docs;
- Kubernetes → update K8s docs;
- GitHub Actions → update CI/CD docs;
- operations → update RUNBOOK;
- team ownership → update TEAM_CONTRIBUTION.

Documentation must point to real files and real lines/commands when the assignment asks for engineering evidence.

---

# FINAL SUBMISSION PROMPT

Before submission, run a full audit against every rubric item and every automatic deduction.

Do not merely say "looks good".

Produce:
- requirement coverage report,
- rubric-to-evidence matrix,
- security scan result,
- clean-clone validation,
- one-command Compose demonstration,
- Kubernetes deployment demonstration,
- HPA evidence,
- VPA evidence,
- CI/CD evidence,
- rollback evidence,
- Git contribution evidence,
- PR/review evidence,
- AI usage disclosure,
- engineering notes with file-and-line references,
- final submission checklist.

Run `python scripts/check_submission.py` from repository root and record the result.

Do not call the assignment complete until all mandatory items have a status of `PASS`, or a clearly documented exception exists.

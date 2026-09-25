# AGENTS.md — Permanent Engineering Contract

## 1. Scope
This repository is an academic but portfolio-grade implementation of the CivicPulse assignment. All work must remain auditable and explainable by both team members.

## 2. Mandatory Behaviors
- Read documentation before coding.
- Inspect existing files before changing them.
- Trace every substantial implementation to assignment requirement IDs.
- Keep mandatory work, optional enhancements, and future ideas separate.
- Never use fabricated evidence.
- Never expose secrets in code, history, logs, screenshots, manifests, or CI.
- Never make the frontend a second business-rule authority.
- Never put SQL outside repository/data-access boundaries.
- Never allow AI output to bypass schema validation.
- Never treat a passing build as proof that the assignment is complete.

## 3. Documentation-First Workflow

### Global read order
`CLAUDE.md`
→ `AGENTS.md`
→ `README.md`
→ `docx/ASSIGNMENT.md`
→ `docs/DOCUMENT_INDEX.md`
→ `docs/ASSIGNMENT_TRACEABILITY.md`
→ current phase prompt
→ issue
→ affected source/tests/config
→ implementation.

### Phase completion order
1. Implement.
2. Test.
3. Verify against assignment.
4. Update documentation.
5. Capture evidence.
6. Update issue.
7. Commit.
8. Push issue branch.
9. Open/update PR.
10. Rebase when the workflow requires it.
11. Re-run checks.
12. Merge only when protected-branch conditions are satisfied.

## 4. Token-Efficient Reading
Do not load every document on every task after the initial baseline.

Use:
- `docs/DOCUMENT_INDEX.md` to identify the minimum required documents;
- exact searches/targeted reads for the relevant assignment clauses;
- phase documents for scope;
- ADRs only when making or revisiting their decisions.

When touching architecture, security, data, CI/CD, or Kubernetes, expand the read set accordingly.

## 5. No-Hallucination Rule
If you cannot prove a requirement from:
- `docx/ASSIGNMENT.md`,
- approved architecture docs,
- an ADR,
- or the current issue,

do not implement it as a mandatory assignment requirement.

Write the uncertainty into `docs/BLOCKERS.md` or `docs/adr/`.

## 6. Git Safety
- No direct commits to `main`. No direct commits to `dev` either: work happens on `feature/<issue-number>-<slug>` branches cut from `dev` and reaches `dev` by pull request; `dev` reaches `main` by a merge-commit pull request (`docs/GITHUB_WORKFLOW.md`).
- No force push to shared branches (`main`, `dev`).
- No `--no-verify` to hide failures.
- Use `--force-with-lease` only after an intentional rebase on your own issue branch.
- Never rewrite another contributor's work.
- Never commit `.env`, keys, tokens, certificates, passwords, kubeconfig files, or credentials.
- Verify GitHub identity before any remote action.

## 7. Two-Session Collaboration
Two AI-assisted sessions — one per contributor, each with that person's own tool (for example Claude Code for one, Codex for the other) — may run in parallel only when:
- each session has a separate issue,
- each session has its own branch/worktree,
- file ownership is disjoint (the single recorded exception, the planned merge conflict of Phase 07 for rubric A5, is in `docs/AI_SESSIONS.md` section 3),
- both GitHub identities are real authenticated accounts,
- neither session edits the same migration/workflow/manifest concurrently.

Never impersonate the partner's identity.
Never fabricate commits, review comments, approvals, or contribution.

Use actual separate GitHub authentication/worktrees for both contributors. The operating manual for both sessions — parallel versus handoff work, the phase-by-phase table and paste-ready prompts — is `docs/AI_SESSIONS.md`. Each contributor's session authenticates as that contributor (browser login done by the person, never by pasting a token or password into an AI session) and follows `docs/PARTNER_RUNBOOK.md` for the step-by-step routine.

Any AI agent that reads this file (Codex reads `AGENTS.md` natively; Claude Code also loads `CLAUDE.md`) is bound by it. Where a repository document says "Claude Code", read "the contributor's AI session".

## 8. Contribution Balance
The assignment requires `git shortlog -sn` to show neither partner below 35%.

Therefore each contributor's AI session must maintain a contribution plan based on estimated effort and real authorship. Do not optimize for artificial commit counts. Favor meaningful, reviewable work.

## 9. Assignment-Specific Security
The assignment has severe automatic deductions for:
- credentials in history,
- keys in Kubernetes manifests,
- unpinned images,
- localhost service-to-service communication,
- frontend-to-database access,
- exposed DB/cache production ports,
- ungated publishing/deployment,
- deploying `:latest`,
- PostgreSQL as a Deployment without PVC,
- direct commits to main,
- broken clean-clone README.

These are release blockers, not cleanup tasks.

## 10. Required End-of-Task Report
Report:
- what changed,
- requirement IDs,
- files changed,
- tests/checks,
- evidence captured,
- branch,
- commit,
- PR,
- blockers,
- next phase allowed.

## 11. One Phase at a Time
Owner decision (2026-09-25): **completely finish one phase before starting another.**

A phase is complete only when, in this order: every issue of the phase has its acceptance boxes ticked and is named in the integration PR's `Closes` line; every PR of the phase is merged into `dev` with a substantive review from the other contributor (one historical exception, PR #9 of Phase 00, is recorded in `docs/AI_SESSIONS.md` section 2); the phase gate in `docs/phases/PHASE-NN-*.md` is checked with evidence; the phase row in `docs/PHASE_STATUS.md` says Complete on `dev`, set by a status PR merged before the integration PR is opened; and the phase's `dev` → `main` integration PR (merge commit, one approval) is merged. A phase is complete **on `main`**: the row counts only once `git show origin/main:docs/PHASE_STATUS.md` shows it, and the next phase starts only then.

Until phase N is complete on `main`, do **not** create branches, commits, PRs or issue edits for a later phase. Allowed while a phase is open: work inside it, answering reviews, reading, and planning that the phase's own prompt requires. If a step would need a later phase or an unmerged dependency, stop and say so.

The definitions of parallel work, handoffs and solo phases, the phase-start and phase-close checklists and the prompt library are in `docs/AI_SESSIONS.md`.

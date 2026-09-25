# AI Usage Disclosure

The course explicitly requires honest disclosure of AI assistance (assignment §5.5).

Maintain a factual record of:
- tool used,
- date/phase,
- what the tool generated or shaped,
- what the students changed,
- why the changes were made.

Do not claim hand-written authorship for generated work.

Each contributor keeps a **separate table** below (so the two never edit the same lines and never conflict). Add a row in the same PR as the work it describes.

## Log — Contributor A (`TahaSohail-Goat`, Claude Code)

| Date | Phase | Tool / model | What it generated or shaped | What the students changed, and why |
|---|---|---|---|---|
| 2026-09-25 | 00 | Claude Code (Anthropic), model `claude-sonnet-5`, driven by the repository owner | Transcribed `docx/ASSIGNMENT_SOURCE.pdf` into `docx/ASSIGNMENT.md`; wrote `docx/EXTRACTION_NOTES.md`; extracted 304 requirement IDs into `docs/ASSIGNMENT_TRACEABILITY.md`; wrote `docs/RUBRIC.md`, `docs/SUBMISSION.md`, `docs/REPOSITORY_STRUCTURE.md`, `docs/ENVIRONMENT_PREREQUISITES.md`, `docs/BLOCKERS.md`, `docs/PHASE_STATUS.md`; created labels, issues, the `.gitignore`/`.gitattributes` files, issue templates and the directory skeleton; ran host tool detection. The governance prompt pack (`CLAUDE.md`, `AGENTS.md`, `PROMPT.md`, `docs/…` stubs, phase prompts) was supplied to the session as input. | The repository owner merged PR #9 on 2026-09-25 with no change to its content (merged tree identical to the branch tip); no written review exists. *Record here, with reasons, every correction the students make from now on.* |
| 2026-09-25 | 00 (follow-up #10) | Claude Code (Anthropic), model `claude-sonnet-5`, driven by the repository owner | Applied the owner's review decisions: retired the `dev/<n>-<slug>` convention, created the literal `dev` branch, rewrote the branch model / PR flow / merge-strategy rules in `docs/GITHUB_WORKFLOW.md`, and updated `PROMPT.md`, `AGENTS.md`, `docs/PHASE_EXECUTION_PROTOCOL.md`, `docs/CICD.md`, the PR template, `docs/BLOCKERS.md`, `docs/ASSIGNMENT_TRACEABILITY.md`, `docs/PHASE_STATUS.md`, `docs/TEAM_CONTRIBUTION.md`. | *Pending* — awaiting the partner's review of the PR. |
| 2026-09-25 | 00 (follow-up #10) / 01 setup | Claude Code (Anthropic), model `claude-sonnet-5`, in the session and GitHub account of `TahaSohail-Goat` only | Tightened the `main` ruleset and created the `dev` ruleset (1 approval, no bypass, merge methods), disabled squash merge, exported the rulesets to `docs/evidence/`, wrote the two-account working agreement and review standard, created the Phase 01 issues #12–#18 with a 15/15 effort split. No action was taken as, or with the credentials of, `Artfever`. | *Pending* — both members to confirm the split and the settings in the PR thread. |
| 2026-09-25 | 00 (#58) | Claude Code (Anthropic), model `claude-sonnet-5`, in the session and GitHub account of `TahaSohail-Goat` | Audited the open Phase 00 and Phase 01 issues, PRs and branches after the owner's review; created the two missing Phase 00 issues (#58 session protocol, #59 open instructor and team questions); wrote `docs/AI_SESSIONS.md` (phase gating, parallel versus handoff versus solo, the phase-by-phase table, handoff protocol, checklists and a paste-ready prompt library for both sessions); updated `AGENTS.md`, `CLAUDE.md`, `docs/PHASE_EXECUTION_PROTOCOL.md`, `docs/PARTNER_RUNBOOK.md` and `docs/DOCUMENT_INDEX.md`; added a `merge=union` rule for this log to `.gitattributes` after testing it in a scratch repository. | Owner decision applied: complete one phase fully before starting another (2026-09-25). No hand edits to these documents by the students are recorded. |

## Log — Contributor B (`Artfever`, Codex)

| Date | Phase | Tool / model | What it generated or shaped | What the student changed, and why |
|---|---|---|---|---|
| — | — | — | *No entries yet. Contributor B adds a row per PR, in that PR.* | — |

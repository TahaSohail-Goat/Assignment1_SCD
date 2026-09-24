# AI Usage Disclosure

The course explicitly requires honest disclosure of AI assistance (assignment §5.5).

Maintain a factual record of:
- tool used,
- date/phase,
- what the tool generated or shaped,
- what the students changed,
- why the changes were made.

Do not claim hand-written authorship for generated work.

## Log

| Date | Phase | Tool / model | What it generated or shaped | What the students changed, and why |
|---|---|---|---|---|
| 2026-09-25 | 00 | Claude Code (Anthropic), model `claude-sonnet-5`, driven by the repository owner | Transcribed `docx/ASSIGNMENT_SOURCE.pdf` into `docx/ASSIGNMENT.md`; wrote `docx/EXTRACTION_NOTES.md`; extracted 304 requirement IDs into `docs/ASSIGNMENT_TRACEABILITY.md`; wrote `docs/RUBRIC.md`, `docs/SUBMISSION.md`, `docs/REPOSITORY_STRUCTURE.md`, `docs/ENVIRONMENT_PREREQUISITES.md`, `docs/BLOCKERS.md`, `docs/PHASE_STATUS.md`; created labels, issues, the `.gitignore`/`.gitattributes` files, issue templates and the directory skeleton; ran host tool detection. The governance prompt pack (`CLAUDE.md`, `AGENTS.md`, `PROMPT.md`, `docs/…` stubs, phase prompts) was supplied to the session as input. | The repository owner merged PR #9 on 2026-09-25 with no change to its content (merged tree identical to the branch tip); no written review exists. *Record here, with reasons, every correction the students make from now on.* |
| 2026-09-25 | 00 (follow-up #10) | Claude Code (Anthropic), model `claude-sonnet-5`, driven by the repository owner | Applied the owner's review decisions: retired the `dev/<n>-<slug>` convention, created the literal `dev` branch, rewrote the branch model / PR flow / merge-strategy rules in `docs/GITHUB_WORKFLOW.md`, and updated `PROMPT.md`, `AGENTS.md`, `docs/PHASE_EXECUTION_PROTOCOL.md`, `docs/CICD.md`, the PR template, `docs/BLOCKERS.md`, `docs/ASSIGNMENT_TRACEABILITY.md`, `docs/PHASE_STATUS.md`, `docs/TEAM_CONTRIBUTION.md`. | *Pending* — awaiting the partner's review of the PR. |

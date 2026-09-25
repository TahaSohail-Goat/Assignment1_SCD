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
| 2026-09-25 | 01 (#13, PR #19) | Claude Code (Anthropic), model `claude-sonnet-5`, in the session and GitHub account of `TahaSohail-Goat` | Wrote `docs/PRD.md` from `docx/ASSIGNMENT.md` (13 sections, a sequence diagram and a state diagram) and ran the checks on it (requirement IDs, blocker references, links, table lint, Mermaid parse). After Contributor B's review of the first version: linked `USE_CASES.md` from the workflow, functional-requirements and traceability sections and split section 3 into users, supporting systems and stakeholders (commit "link the use-case catalog and group actors by role"); drafted the reply that answers the reviewer's "why" question. | Owner decision applied: the nine endpoints listed in the assignment are the contract (B-004). No hand edits to this document by the students are recorded; all changes, including those after review, were made in this session. The two review findings were raised by Contributor B and applied as described. |

## Log — Contributor B (`Artfever`, Codex)

| Date | Phase | Tool / model | What it generated or shaped | What the student changed, and why |
|---|---|---|---|---|
| — | — | — | *No entries yet. Contributor B adds a row per PR, in that PR.* | — |

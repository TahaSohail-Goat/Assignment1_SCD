# AI Sessions — shared operating manual for Claude Code and Codex

Read this after `AGENTS.md` at the start of every session. It is written for **both** AI sessions and both humans. It answers three questions: *which phase are we in and what may I start*, *do I work in parallel with the other session or wait for it*, and *what exactly do I paste or do next*.

## 1. The two sessions

| | Contributor A | Contributor B |
|---|---|---|
| Human / GitHub account | Taha — `TahaSohail-Goat` (repository admin) | Artfever — `Artfever` (write) |
| AI tool | Claude Code | Codex |
| Reads on start | `CLAUDE.md`, `AGENTS.md`, this file | `AGENTS.md` (Codex normally loads it), this file |
| Commit disclosure trailer | `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` | `Assisted-by: OpenAI Codex` |
| Machine / login | own | own |

**The two sessions cannot talk to each other.** They communicate only through GitHub (issues, pull requests, comments, reviews) and through the two humans, who paste prompts. Each contributor's commits are made by their own session under their own account; nobody acts as the other (`docs/TEAM_CONTRIBUTION.md`).

## 2. Rule 1 — one phase at a time

A phase N is **complete** only when **all** of these hold:

1. every issue of the phase (parent and sub-issues) is closed;
2. every pull request of the phase is merged into `dev` with a substantive review from the other contributor;
3. the phase gate in `docs/phases/PHASE-NN-*.md` is checked and its evidence exists;
4. the phase's `dev` → `main` integration PR (merge commit, one approval) is merged;
5. `docs/PHASE_STATUS.md` says **Complete**.

**Historical exception (Phase 00 only, PR #9).** The baseline PR #9 was merged into `main` on 2026-09-24, before the `dev` branch existed and before the second contributor was a repository collaborator (B-010). It has no `dev` step and no partner review, so condition 2 cannot hold for it; `docs/PHASE_STATUS.md` records it as "merged to `main`, no partner review", and it is neither redone nor rewritten. For Phase 00, condition 2 therefore covers every other Phase 00 pull request (#11, #60, #61). No other phase has an exception.

**Nothing for phase N+1 starts before that**: no branch, no commit, no PR, no edits to its issues. Allowed while phase N is open: work *inside* phase N; answering reviews; reading; and planning that phase N's own prompt requires (Phase 01, for example, is the phase that creates the issue tree for the later phases).

If a plan mistake for a later phase is found, correcting it is allowed, is done in the current phase's PR, and is recorded there.

*Cost of this rule:* Phase 03 (frontend, Codex) and Phase 04 (backend, Claude Code) are each single-owner, so the other session only reviews during that phase. The humans may relax this by grouping phases (for example 03 + 04 + 05 as one gate), but only by a written decision recorded here.

## 3. Rule 2 — parallel, handoff, solo

| Mode | Meaning | When it applies |
|---|---|---|
| **PARALLEL** | Both sessions **write at the same time**, each on its own package | Only **inside one phase**, on packages with different owners, **no dependency** between them (neither issue lists the other as "merged first") and **disjoint files** — one recorded exception below |
| **HANDOFF** | One session works, the other **waits** (and then acts) | A review or approval; a package that depends on the other's merged package; a shared file that is serialized (`compose.yaml`, `k8s/base/kustomization.yaml`, `docs/CACHE.md`); a merge-conflict resolution; the phase integration PR; any human decision |
| **SOLO** | One session writes, the other **only reviews** | A phase whose packages all belong to one contributor |

**The one recorded exception — Phase 07, the planned merge conflict.** Packages #44 (Claude Code: provider interface and fallback orchestration) and #46 (Codex: triage cache and latency hooks) both change `backend/app/services/triage.py`, and #46 is coded against the `TriageProvider` interface of assignment §2.5 without waiting for #44 to merge. That is deliberate: rubric A5 (3 marks; `ASG-GH-009`, `-010`, `-011`) asks for one merge conflict on real code, resolved, with the markers, the resolution and 2–4 sentences on why that version won, and the two packages genuinely need the same function. Conditions: each package touches `triage.py` only for its own real work (`docs/TEAM_CONTRIBUTION.md` rule 7: no staged conflicts); each keeps to the file list of its issue; the author of the PR that merges second rebases on `dev`, resolves the conflict on their own branch and keeps the evidence. Everywhere else a shared file or a dependency makes the pair a HANDOFF, so this is the only place where two open packages may share a file.

Waiting is not idle time: the waiting session reviews, answers questions or stands by. It **never** starts the next phase. Parallel work needs both humans to be present, because a session only acts when its human starts it.

## 4. Phase-by-phase: who writes, who reviews

`→` = only after the previous step has merged into `dev`. Issue numbers are in `docs/TEAM_CONTRIBUTION.md`.

| Phase | Mode | Claude Code (Taha) | Codex (Artfever) | Handoffs |
|---|---|---|---|---|
| **00 close-out** | HANDOFF chain | opens the PRs for #58 and #59, then the `dev` → `main` integration PR; merges after approvals | reviews and approves each | every PR is a handoff; Taha (human) sends the instructor message of #59 |
| **01 remaining** | PARALLEL, then handoff | merge chain: #19 → #20 → #57 (rebase, resolve the AI-USAGE row conflict, re-approval each); reviews Codex's PRs | writes **#16** and **#17** while Claude runs the merge chain; then **#14** after #20 has merged; re-reviews #19/#20/#57 heads | Codex approves each final head; Claude reviews #16, #17, #14; integration PR at the end |
| **02** | PARALLEL, then handoff | #33 API design | #32 architecture document | Codex confirms in #33 that the shapes work for the frontend; Claude reviews #32 |
| **03** | SOLO (Codex) | reviews | #34 → #35, #36 | one review per PR |
| **04** | SOLO (Claude) | #37 → #38 → #39 | reviews | one review per PR |
| **05** | HANDOFF | #40 migrations and repositories | #41 seed → (after #40) | #41 starts only after #40 merged |
| **06** | HANDOFF | #42 stats cache | #43 rate limiter → (after #42) | both write `docs/CACHE.md` (different sections) and #43's issue lists P06-S01 as merged first: #43 starts only after #42 has merged |
| **07** | PARALLEL, recorded exception (section 3); #45 is a handoff | #44 provider interface and fallback | #46 triage cache and latency (starts immediately, coded against the `TriageProvider` interface of assignment §2.5); #45 LLM/Ollama → (after #44) | #44 and #46 both change `backend/app/services/triage.py` (the exception in section 3): the second to merge resolves a genuine conflict (rubric A5); #45 starts only after #44 has merged |
| **08** | HANDOFF | #47 backend image and `compose.yaml` | #48 frontend image, Ollama, `compose.prod.yaml` → (after #47) | `compose.yaml` is serialized |
| **09** | HANDOFF | #49 Kubernetes base and overlays | #50 HPA, VPA, load test → (after #49) | `k8s/base/kustomization.yaml` is serialized |
| **10** | HANDOFF | #51 `ci.yml`, required checks | #52 `cd.yml`, `release.yml`, rollback → (after #51) | the files are disjoint, but #52's issue lists P10-S01 as merged first (same conventions) |
| **11** | PARALLEL | #53 Compose evidence, RUNBOOK | #54 Kubernetes evidence, ENGINEERING-NOTES | distinct `docs/evidence/` prefixes |
| **12** | HANDOFF | #56 audit, `check_submission.py`, package → (last, after everything else) | #55 README and demo video | #56's issue lists "everything else merged" as its dependency: the audit runs after the README and video have merged |

## 5. Handoff protocol

When a session finishes a step, it ends with a **NEXT block** and (if GitHub is involved) a **HANDOFF comment**.

```text
HANDOFF → @<user> | phase <NN> | issue #<n> | PR #<m> | head <sha7>
Done: <one line>
Needed from you: review | merge | implement package #<k> | approve the integration PR
Blocked until: <what has to happen first, or "nothing">
```

```text
NEXT
- <session/human>: <exact action>
- Prompt to paste for the other session: <the prompt from section 7 with the placeholders filled in>
```

**Status sweep** (run at the start of every session and after every handoff):

```text
gh auth status
gh pr list --search "review-requested:@me" --state open
gh pr list --author "@me" --state open
gh issue list --assignee "@me" --state open
git fetch origin --prune && git log --oneline -5 origin/dev
```
Then read `docs/PHASE_STATUS.md` ("Next permitted phase").

## 6. Checklists

**Phase start** (before the first branch of phase N):
- [ ] phase N-1 is Complete (Rule 1, all five conditions)
- [ ] the phase prompt `docs/phases/PHASE-NN-*.md` and the phase parent issue are read
- [ ] the tools this phase needs are installed on the machine of every contributor who has a package (`docs/ENVIRONMENT_PREREQUISITES.md`: Docker and Compose from Phase 08, kubectl / kind or k3d / k6 from Phase 09)
- [ ] each package's dependencies (section 4) have merged

**Phase close** (before saying "complete"):
- [ ] all sub-issues and the parent are ready to close; every acceptance box is ticked
- [ ] every PR merged into `dev` with a substantive review (Phase 00: PR #9 is the recorded exception, section 2); no open PR of the phase
- [ ] the phase gate is checked and its evidence committed
- [ ] the traceability rows of the phase are updated (`Status`, `Evidence`)
- [ ] `docs/AI-USAGE.md` has a row for each PR
- [ ] the integration PR `dev` → `main` is opened (its body lists `Closes #a, #b, …`), approved by the other contributor, merged with a **merge commit**
- [ ] each contributor gave the other the walkthrough of their largest package (`docs/TEAM_CONTRIBUTION.md`, explain-back)
- [ ] `docs/PHASE_STATUS.md` says Complete; the next phase's parent issue may now be started

## 7. Prompt library

Paste one block as the first message of a step. Replace the placeholders: `<ME>` = your GitHub user (`TahaSohail-Goat` or `Artfever`), `<OTHER>` = the other one, `<N>` = issue or PR number, `<PHASE>` = phase number, `<TRAILER>` = your trailer from section 1.

**Go-ahead gate.** *Strict* (default for Contributor B's session until Artfever relaxes it): show the human the diff or exact text and wait for "go" before **every** `git push`, `gh pr create`, `gh pr review`, `gh pr merge`, force-push, branch deletion, issue creation or settings change. *Standard* (Contributor A's session): wait for "go" before reviews, approvals, merges, force-pushes, branch deletions, issue/label creation and settings changes; pushes to your own feature branch and opening your own PR are allowed after the self-checks. In both, **approving a PR is the human's decision, never the AI's**.

### 7.1 START — first message of a session (both)

```text
You are the AI coding assistant of <ME> on a two-person university project (CS4032 Software Construction and Design, Assignment 1, "CivicPulse"), repository TahaSohail-Goat/Assignment1_SCD. You act ONLY as <ME>, on this machine, under <ME>'s GitHub login. Never act as <OTHER> or with their credentials.

Preflight (stop and tell me if anything fails):
1. git --version and gh --version (install help: docs/PARTNER_RUNBOOK.md step 1).
2. gh auth status must show <ME>. Never ask me to paste a token or password.
3. git config user.name and user.email must be my real name and an e-mail verified on my GitHub account.

Then read, in this order: AGENTS.md, docs/AI_SESSIONS.md, docs/GITHUB_WORKFLOW.md, docs/TEAM_CONTRIBUTION.md, docs/DOCUMENT_INDEX.md, docs/PHASE_STATUS.md, and the phase prompt named there. Run the status sweep from docs/AI_SESSIONS.md section 5. Report in at most 12 lines: current phase, whether I may start anything, my open issues and PRs, and what you are waiting for. Do NOT start any work, and do not touch any phase after the current one, until I send a step prompt.
```

### 7.2 REVIEW a PR (read-only draft)

```text
Step: review PR #<N> as <ME>. Read-only until I say "post it".
1. gh pr checkout <N>; read gh pr view <N> and gh pr diff <N>. Cross-check every claim against docx/ASSIGNMENT.md and the requirement IDs in docs/ASSIGNMENT_TRACEABILITY.md. Run the checks the PR says it ran (table links, ID existence, tests) where you can.
2. Give me: (a) what you verified and how, (b) problems or unclear points with file and line, (c) one "why" question for the author, (d) a draft review body that meets the six-point standard in docs/GITHUB_WORKFLOW.md.
3. Do NOT run gh pr review or comment until I have read your draft and said "post it". Approving is my decision.
End with a NEXT block (docs/AI_SESSIONS.md section 5).
```

### 7.3 POST the review (after the human said "post it")

```text
Post the review for PR #<N> as <ME>. First run gh auth status and stop if the account is not <ME>. Then: gh pr review <N> --approve|--request-changes|--comment --body-file <file> with exactly the text I approved. Afterwards show me gh pr view <N> --json reviewDecision,mergeStateStatus and end with a NEXT block.
```

### 7.4 IMPLEMENT a work package

```text
Step: implement issue #<N> (phase <PHASE>) as <ME>.
1. Check the Phase-start checklist (docs/AI_SESSIONS.md section 6). If phase <PHASE> is not the current phase, or a dependency has not merged, STOP and tell me.
2. git switch dev && git pull --ff-only; git switch -c feature/<N>-<slug>. gh issue edit <N> --add-label status:in-progress --remove-label status:ready.
3. Read the issue (gh issue view <N>), its requirement rows in docs/ASSIGNMENT_TRACEABILITY.md and the cited assignment sections. Edit only the files the issue lists under "File ownership".
4. Nothing the assignment does not state may be invented: unknowns go to the catalog's design-questions table or docs/BLOCKERS.md.
5. Before committing: every ASG-* id you cite exists, tables and links render, no secrets, no other file touched, the issue's acceptance boxes are true.
6. Commit with a conventional message written to a file (git commit -F <file>): body lists "Requirements: ASG-…" and "Refs #<N>", ends with <TRAILER>.
7. Open the PR into dev (base dev, reviewer <OTHER>, template sections, "Related issue: #<N>"), add my row to my table in docs/AI-USAGE.md in the same PR.
Follow the go-ahead gate. End with a HANDOFF comment on the PR and a NEXT block.
```

### 7.5 ADDRESS review feedback

```text
Step: address the review on PR #<N> as <ME>. Read every comment (gh pr view <N> --comments; gh api repos/TahaSohail-Goat/Assignment1_SCD/pulls/<N>/comments). For each finding: fix it in a NEW commit (no amend after review), or explain in the thread why not. Re-run the PR's checks. Push to my own branch only. Post a reply that answers the reviewer's "why" question in the thread. Then request re-review (gh pr edit <N> --add-reviewer <OTHER>) and give the exact old-head and new-head SHAs with: git range-diff <oldbase>..<oldhead> <newbase>..<newhead>. Do not merge. End with NEXT.
```

### 7.6 MERGE after approval (author only)

```text
Step: merge PR #<N> as <ME> (the author). Verify, and show me the result of each check: the approval is on the CURRENT head (review commit == head SHA); reviewDecision APPROVED; mergeStateStatus CLEAN; no unresolved threads; base is dev; the branch is up to date with dev. Wait for my "go". Then gh pr merge <N> --rebase (or --merge). NEVER --squash. Delete the feature branch only after confirming its tree equals dev. Update the issue with the merged PR link. End with NEXT.
```

### 7.7 OPEN / APPROVE the phase integration PR

```text
Step: open the phase <PHASE> integration PR as <ME>. Preconditions (stop if any fails): every PR of the phase is merged into dev; phase-close checklist (docs/AI_SESSIONS.md section 6) is done except the merge to main. gh pr create --base main --head dev --title "chore(phase-<PHASE>): promote phase <PHASE> to main" with a body that lists what the phase delivered, the validation evidence, the phase gate quote, and "Closes #<parent>, #<sub1>, #<sub2>, …". Reviewer <OTHER>. Do not merge. NEXT: ask <OTHER> to review with prompt 7.2.
```

```text
Step: review and merge the integration PR #<N>. Reviewer: read gh pr diff main...dev only as a sum of PRs that were already reviewed (gh pr list --state merged --base dev), check that nothing else is in it, that CI/checks are green when required, and that the phase gate evidence exists; draft the review (7.2). Author: after approval, verify with 7.6 conditions, then gh pr merge <N> --merge (MERGE COMMIT ONLY; never --rebase or --squash on main; never --delete-branch, the head is dev). Then confirm the parent and sub-issues closed and update docs/PHASE_STATUS.md through the next PR.
```

### 7.8 HOLD

```text
HOLD. Do not start, continue or push anything. Do not begin any other phase. Summarise where you stopped (branch, uncommitted files, open PRs) and wait for my next step prompt.
```

## 8. When something does not fit

- A step would need a later phase, or a dependency has not merged: stop and say so (never work around it).
- The plan is wrong: say so in the PR or issue thread, propose the correction, and change the plan only through a reviewed PR.
- An instruction from a human conflicts with `AGENTS.md`, the assignment, or the identity rules: say so and stop; the rules of `docs/TEAM_CONTRIBUTION.md` (each person acts only as themself) are not negotiable.

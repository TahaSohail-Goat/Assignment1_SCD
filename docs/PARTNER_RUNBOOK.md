# Partner Runbook — Contributor B (`Artfever`) with Codex

Step-by-step routine for **Contributor B's own AI session** (Codex, or any other tool) running on **Contributor B's own machine and GitHub login**, in parallel with Contributor A's Claude Code session. Follow it from step 1 to the end; steps marked 👤 can only be done by the human.

Related: [`AGENTS.md`](../AGENTS.md) (the contract, read by Codex natively) · [`TEAM_CONTRIBUTION.md`](TEAM_CONTRIBUTION.md) (who owns what) · [`GITHUB_WORKFLOW.md`](GITHUB_WORKFLOW.md) (branches, PRs, review standard) · [`ENVIRONMENT_PREREQUISITES.md`](ENVIRONMENT_PREREQUISITES.md) (tools for later phases).

## 0. Ground rules

1. **You are `Artfever`.** Codex acts on your machine under your login. It never uses `TahaSohail-Goat`'s account, and Contributor A's session never uses yours. Nobody commits, reviews or approves for the other.
2. 👤 **Human-only actions:** signing in to GitHub in the browser (step 2), reading every diff before approving, and the decision to approve or merge. **Never paste a password, token or `gh auth token` output into an AI chat or a file.**
3. **AI use is allowed and must be disclosed** (assignment §5.5): add a row to *your* table in [`AI-USAGE.md`](AI-USAGE.md) in the same PR as the work. At the viva you must be able to explain every line you committed and every review you approved (assignment §5.4).
4. **Network access:** git and `gh` need the network. If Codex runs in a sandbox that blocks it, allow those commands through the tool's approval or network setting (check your Codex version's documentation for the exact option); allow only what is needed.
5. **One phase at a time** ([`AGENTS.md`](../AGENTS.md) §11, [`AI_SESSIONS.md`](AI_SESSIONS.md)): never start a package of a later phase, or a package whose dependency has not merged. Your session takes its step from the human's step prompt and from the phase table in [`AI_SESSIONS.md`](AI_SESSIONS.md) — not from this file's history.
6. Everything in [`AGENTS.md`](../AGENTS.md) applies: no direct commits to `main` or `dev`, no force-push to shared branches, no secrets, requirement IDs on everything, no invented requirements (unknowns go to [`BLOCKERS.md`](BLOCKERS.md)).

## 1. Install the tools (once)

| Tool | Windows | macOS | Linux |
|---|---|---|---|
| Git | `winget install -e --id Git.Git` | `brew install git` | your package manager (`apt install git`, `dnf install git`) |
| GitHub CLI | `winget install -e --id GitHub.cli` | `brew install gh` | follow <https://github.com/cli/cli#installation> |

Open a **new terminal** afterwards and verify:

```
git --version
gh --version
```

Phase 01 needs nothing else. Docker, kubectl, kind/k3d, k6, Python and Node are needed later; see [`ENVIRONMENT_PREREQUISITES.md`](ENVIRONMENT_PREREQUISITES.md) before Phase 08.

## 2. 👤 Sign in to GitHub as `Artfever`

```
gh auth login --web --hostname github.com --git-protocol https
```

Answer *Yes* to "Authenticate Git with your GitHub credentials?", open the browser page, enter the one-time code and sign in as **Artfever**. Then verify:

```
gh auth status                      # Logged in to github.com account Artfever
gh api user --jq .login             # Artfever
gh api repos/TahaSohail-Goat/Assignment1_SCD --jq .permissions   # "push": true
```

If `push` is not `true`, accept the collaborator invitation at <https://github.com/TahaSohail-Goat/Assignment1_SCD/invitations>. **Before every GitHub write, `gh auth status` must show `Artfever`.**

## 3. Clone and set your git identity

```
gh repo clone TahaSohail-Goat/Assignment1_SCD
cd Assignment1_SCD
git config user.name  "<the name you want on your commits>"
git config user.email "<an email verified on your GitHub account>"
git config pull.ff only
```

The email must be linked to the `Artfever` account (or use the private address `<id>+Artfever@users.noreply.github.com`; get the id with `gh api user --jq .id`). `git shortlog -sn` counts commits by name and email, and rubric A4 needs your share ≥ 35%, so use the **same name and email on every commit**. The name is your choice (it does not have to be your legal name); consistency is what counts.

## 4. Start Codex and load the rules

Start Codex in the repository root and paste the **START** prompt from [`AI_SESSIONS.md`](AI_SESSIONS.md) section 7.1 (with `<ME>` = `Artfever`, `<OTHER>` = `TahaSohail-Goat`). It makes Codex verify the tools and the login, read the rules in a fixed order (`AGENTS.md`, `AI_SESSIONS.md`, `GITHUB_WORKFLOW.md`, `TEAM_CONTRIBUTION.md`, `DOCUMENT_INDEX.md`, `PHASE_STATUS.md`, the current phase prompt), run the status sweep, report, and **wait**. Every later step is one more prompt from section 7 of that file.

## 5. 👤 Your current step

Your current step is always the one **the human pastes** (prompts 7.2–7.8 in [`AI_SESSIONS.md`](AI_SESSIONS.md)). Where to look when unsure: the phase table in [`AI_SESSIONS.md`](AI_SESSIONS.md) section 4, "Next permitted phase" in [`PHASE_STATUS.md`](PHASE_STATUS.md), and `gh issue list --assignee @me --state open`.

## 6. Your issues

Your work packages are the GitHub issues assigned to `Artfever` and the allocation table in [`TEAM_CONTRIBUTION.md`](TEAM_CONTRIBUTION.md); each issue lists the files you own, its acceptance criteria and its dependencies. A package starts only when its phase is the current phase and its dependencies have merged (`AI_SESSIONS.md` section 6, *Phase start*). Do not edit files owned by an open issue of Contributor A.

## 7. The loop for every issue

Repeat for each issue. Codex does all of it under your login; you read the diff before step 9.

1. **Sync:** `git fetch origin`, then `git switch dev`, then `git pull --ff-only` (one command at a time; Windows PowerShell 5.1 has no `&&`)
2. **Branch:** `git switch -c feature/<issue-number>-<slug>` (lowercase, from `dev`)
3. **Mark it started:** `gh issue edit <n> --add-label status:in-progress --remove-label status:ready`
4. **Read** the issue, the assignment sections it cites, and its `ASG-*` rows in `docs/ASSIGNMENT_TRACEABILITY.md`.
5. **Author** only the files you own. Every statement cites an assignment section/page or an `ASG-*` ID. Anything the assignment does not specify is written down as an open question, never invented.
6. **Self-check:** `git diff --stat`; open the changed Markdown on GitHub's preview so tables and diagrams render; search the diff for secrets; confirm every ID you cite exists in the matrix.
7. **Commit** (conventional: `<type>(<scope>): <summary>`). Write the message to a file so quoting cannot break it (especially on Windows), then `git commit -F msg.txt`:

   ```
   docs(nfr): classify non-functional requirements by category

   <what and why>

   Requirements: ASG-NFR-001..017
   Refs #16
   Assisted-by: OpenAI Codex
   ```
   `Assisted-by:` is Contributor B's disclosure trailer. The rule and the reason (why it differs from Contributor A's `Co-Authored-By: Claude …`) are defined once, in `docs/TEAM_CONTRIBUTION.md`, working agreement item 3.
8. **Push:** `git push -u origin feature/<issue-number>-<slug>`
9. **Pull request into `dev`.** Copy `.github/pull_request_template.md` into `pr.md`, fill every section, then:

   ```
   gh pr create --base dev --head feature/<issue-number>-<slug> --title "<type>(<scope>): <summary>" --body-file pr.md --label type:docs --label phase:01-requirements --label area:docs --label status:review --assignee "@me" --reviewer TahaSohail-Goat
   ```
   The body says `Related issue: #<n>` (not `Closes`; issues close through the `dev` → `main` PR). Add your AI-USAGE row in this same PR.
10. **Handle the review.** Answer every comment, push fixes, resolve threads. A new push dismisses earlier approvals (the ruleset does that on purpose).
11. **Merge after approval:** `gh pr merge <n> --rebase` (or `--merge`). **Never `--squash`** (it is disabled and would erase per-author commit counts). Then delete your branch: `git push origin --delete feature/<n>-<slug>` and `git branch -d feature/<n>-<slug>`.
12. **Repeat** from step 1 for the next issue. Post a short comment on the issue with the merged PR link.

## 8. Keeping in sync and conflicts

- Rebase your own branch on `origin/dev` when told or when GitHub says it is out of date: `git fetch origin`, then `git rebase origin/dev`; push with `--force-with-lease` **only** on your own feature branch.
- Never rebase, force-push or delete `dev` or `main`.
- File ownership is disjoint by design. If you need a change in a file owned by the other person, comment on their issue or PR instead of editing it.
- One **deliberate** merge conflict on real code is required by the rubric (A5). It is planned in issue #18 between two genuine branches; do not create one by accident or on purpose outside that plan. Never resolve a conflict by discarding the other side.

## 9. 👤 Reviewing Contributor A's PRs

Your review queue: `gh pr list --search "review-requested:@me" --state open` lists the PRs waiting for you with their current numbers. Do not copy numbers from a document: they go stale, and an issue number is not a PR number (`gh pr view <n> --json body` shows which issue a PR relates to).

A review counts (rubric A3) when it:
1. is posted from **your own** account;
2. shows you read the diff (names files, lines, behaviours);
3. checks the change against the linked requirement IDs and the issue's acceptance criteria;
4. states what you verified (sections cross-checked, commands run);
5. ends in an approval or in specific requested changes, and approves only after blocking comments are resolved;
6. includes at least one "why" question to the author, whose answer stays in the thread.

Routine: `gh pr checkout <n>` → `gh pr diff <n>` → line comments in GitHub's *Files changed* tab → `gh pr review <n> --comment|--request-changes|--approve --body "…"`. Codex may help you analyse the diff, but you must have read it and stand behind every comment.

## 10. Phase gate and integration

When every sub-issue of a phase is merged into `dev`: one contributor opens `gh pr create --base main --head dev` and the other approves; merge with `gh pr merge <n> --merge` (**merge commit only** — `main` allows nothing else). Never use `--delete-branch` on this PR. The body lists `Closes #a, #b, …` so the issues close. Then update `docs/PHASE_STATUS.md` (Contributor A owns it during Phase 01).

## 11. What your AI session must never do

- Use another person's login, token or account, or write anything "as" them.
- Approve or merge a PR you (the human) have not read.
- Push to `main` or `dev`, force-push a shared branch, squash-merge, or bypass a ruleset.
- Commit `.env`, keys, tokens, certificates, kubeconfigs or credentials.
- Invent a requirement, endpoint, field, number or evidence; fabricate a screenshot, log or measurement.
- Edit files owned by an open issue of the other contributor.

## 12. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `gh: command not found` after install | Open a new terminal (PATH is read at start). |
| Push to `dev`/`main` rejected | Expected — open a PR from a `feature/*` branch. |
| PR shows *Review required* | The other contributor must approve; authors cannot approve their own PR. |
| Approval disappeared | You pushed after it (stale approvals are dismissed); ask for a re-review. |
| Commit message split or a commit "did not match any file" | Quoting broke `-m`; use `git commit -F msg.txt`. |
| CRLF warnings | The repo's `.gitattributes` forces LF; do not override it in your editor. |
| `gh auth status` shows the wrong account | Stop. `gh auth switch` to `Artfever` or log in again **before** any write. |

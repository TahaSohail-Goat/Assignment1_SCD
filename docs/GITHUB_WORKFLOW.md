# GitHub Workflow

## Branch Model

Decision (owner, 2026-09-25): the assignment's literal two-branch model — `dev` for work, `main` for deployable software — plus short-lived feature branches (assignment §3.4, rubric A2, `ASG-GH-002`).

`main`
- protected (see "Branch protection and review")
- deployable; the only branch CD deploys from
- no direct push and no direct commit, ever (`ASG-DED-010`)
- changed only by a pull request from `dev`

`dev`
- long-lived integration branch ("dev for work")
- changed only by pull requests from feature branches — no direct commits either
- `ci.yml` runs on every push to it (`ASG-CICD-003`)
- reaches `main` only through a `dev` → `main` pull request

`feature/<issue-number>-<slug>`
- one short-lived branch per issue, cut from the current `dev`
- lowercase kebab-case slug, e.g. `feature/12-frontend-submit-form`
- used for every kind of work (code, docs, chores), merged into `dev` by pull request, then deleted

Do not create arbitrary branch names. The earlier `dev/<issue-number>-<slug>` convention is **retired**: git cannot hold a branch called `dev` and branches under `dev/` at the same time. (Phase 00 used `dev/1-phase-00-baseline` for PR #9; that branch was deleted after its merge — last commit `000d3de`, tree identical to `main`.)

## Pull-Request Flow

```
feature/<n>-<slug>  ──PR──►  dev  ──PR──►  main
```

1. **Feature PR (base `dev`).** Title `<type>(<scope>): <summary>`; body cites the requirement IDs and `Related issue: #<n>`; needs a substantive partner review before merge.
2. **Integration PR (`dev` → `main`).** Opened when a phase (or a coherent slice) is done; needs CI green and ≥ 1 approval once protection is on.
3. **Merge strategy.**
   - Feature → `dev`: *Rebase and merge* or *Create a merge commit*. **Do not squash**: rubric A4 counts commits and each partner's share (`ASG-GH-006`, `ASG-GH-008`), and squashing erases both.
   - `dev` → `main`: **Create a merge commit only.** A rebase-merge would copy `dev`'s commits onto `main` under new SHAs, `dev` would no longer contain what `main` has, and every later integration PR would show duplicate commits and conflicts.
4. **Closing issues.** GitHub closes `Closes #n` issues only when the PR lands on the *default* branch (`main`). Feature PRs therefore say `Related issue: #n`; the `dev` → `main` PR lists `Closes #a, #b, …`. An issue finished earlier than that is closed manually with a link to its merged PR.
5. **CI triggers.** Assignment §3.4 says `ci.yml` runs "on pull request to main, on push to dev". Under that literal reading a feature PR into `dev` gets no PR-triggered run. Phase 10 decides whether `ci.yml` also triggers on `pull_request` to `dev` (a superset of the requirement; recommended so feature PRs are gated before they reach `dev`).

## Issue Hierarchy

Use a parent issue for each phase.

Parent:
`[PHASE-XX] <Phase Name>`

Sub-issue:
`[PXX-SYY] <Specific Work Item>`

Each issue must include:
- Objective
- Assignment requirement IDs
- Context
- In scope
- Out of scope
- Acceptance criteria
- Test/evidence criteria
- Owner
- Dependencies
- Definition of done

## Labels

Use:
- `type:feature`
- `type:bug`
- `type:docs`
- `type:test`
- `type:infra`
- `type:refactor`
- `type:chore`
- `phase:00-foundation`, etc.
- `area:frontend`
- `area:backend`
- `area:data`
- `area:cache`
- `area:ai`
- `area:devops`
- `area:kubernetes`
- `area:cicd`
- `area:testing`
- `status:ready`
- `status:in-progress`
- `status:review`
- `status:blocked`

## Assignment of Work

Initially, documentation issues can be assigned to the primary contributor while the second member is not yet a collaborator.

Once the second member is a real collaborator:
- create a balanced work allocation based on effort;
- ensure both members own substantial implementation;
- maintain ≥35% contribution each;
- do not manufacture commits.

## Commit Convention

`<type>(<scope>): <imperative summary>`

Allowed examples:
- `docs(requirements): establish assignment traceability`
- `feat(api): implement complaint status transition`
- `test(ai): verify malformed provider output fallback`
- `ci(actions): add gated container scan`
- `fix(cache): invalidate stats after complaint insert`

## PR Convention

Title:
`<type>(<scope>): <summary>`

PR body:
- Summary
- Requirement IDs
- Changes
- Validation
- Evidence
- Risks / Notes
- Reviewer checklist
- Related issue

## Required Partner Review

The assignment requires substantive partner review comments (rubric A3, `ASG-GH-005`). A review must discuss code/documentation behavior or evidence. "LGTM" alone is not sufficient evidence of substantive review.

A review counts when it:
1. is posted by the **other contributor's own GitHub account** (never by the author, never on someone's behalf);
2. shows the diff was actually read — it names files, lines or behaviours;
3. checks the change against the linked requirement IDs and the issue's acceptance criteria;
4. states what was verified (commands run, assignment sections cross-checked);
5. ends in an approval or in specific requested changes, and approves only once blocking comments are resolved;
6. includes at least one "why" question to the author whose answer stays in the thread (viva preparation, `ASG-SUB-009`).

Reviewer routine (each person runs it under their own login):

```
gh auth status                         # confirm you are acting as yourself
gh pr checkout <n>                     # get the actual branch
gh pr diff <n>                         # read the change
gh pr review <n> --comment -b "…"      # substantive comment (line comments in the Files tab are better)
gh pr review <n> --request-changes -b "…"
gh pr review <n> --approve -b "Verified: … Checked against: ASG-… Question answered: …"
```

AI assistance in a review is allowed only in the reviewer's **own** session and account, after the reviewer has read the change and can defend every comment; it is logged in `docs/AI-USAGE.md`. A review the reviewer has not read is not a review.

## Rebase / Merge

Before merging a **feature** PR:
1. `git fetch origin`
2. `git rebase origin/dev`
3. resolve conflicts
4. run full required checks
5. push using `--force-with-lease` only to your own feature branch
6. wait for CI
7. obtain required approval
8. merge via PR into `dev`

`dev` is never rebased or force-pushed. If `main` ever contains something `dev` lacks, merge `main` into `dev` through a PR rather than rewriting `dev`.

Never bypass protection.

## Deliberate Merge Conflict

A real code conflict must be created, resolved, documented, and preserved as evidence.

Do this with two genuine branches and real code changes. Never fake conflict screenshots.

## Repository State and Phase 00 Conventions

Recorded 2026-09-25 when governance was established. Repository: `TahaSohail-Goat/Assignment1_SCD` (public).

### Labels created (35)
Documented set plus the phase labels. Two labels were **added** in Phase 00 because documentation and security work fit no documented `area:` label: `area:docs`, `area:security`. The ten default GitHub labels (`bug`, `documentation`, `enhancement`, …) were left untouched; prefer the namespaced labels below.

| Group | Labels |
|---|---|
| `type:` | `feature` · `bug` · `docs` · `test` · `infra` · `refactor` · `chore` |
| `phase:` | `00-foundation` · `01-requirements` · `02-architecture` · `03-frontend` · `04-backend` · `05-data` · `06-cache` · `07-ai` · `08-devops` · `09-kubernetes` · `10-cicd` · `11-qa-evidence` · `12-final-audit` |
| `area:` | `frontend` · `backend` · `data` · `cache` · `ai` · `devops` · `kubernetes` · `cicd` · `testing` · `docs` (added) · `security` (added) |
| `status:` | `ready` · `in-progress` · `review` · `blocked` |

### Issue and branch numbering
- One parent issue per phase; sub-issues are linked as GitHub sub-issues and listed in the parent body.
- One branch per issue: `feature/<issue-number>-<slug>`, cut from `dev` (see "Branch Model"). Where several small sub-issues form one reviewable change, one branch may carry them; the PR then names every issue.
- Phase 00 (history): parent #1, sub-issues #2–#8, PR #9 from `dev/1-phase-00-baseline` (rebase-merged by the owner on 2026-09-25, without a partner review because the partner was not yet a collaborator — it therefore does not count toward `ASG-GH-005`). Follow-up #10 applies the review decisions.
- Branch-model decision recorded in `docs/SUBMISSION.md` (decisions table).

### Issue templates
`.github/ISSUE_TEMPLATE/` provides `phase.yml` (parent), `feature.yml`, `docs.yml` and `bug.yml`. Every template carries the sections required above (objective, requirement IDs, context, in/out of scope, acceptance criteria, test/evidence criteria, owner, dependencies, definition of done). The pull-request template is `.github/pull_request_template.md`.

### Branch protection and review (configured 2026-09-25, relaxed the same day)
Both members are collaborators (`TahaSohail-Goat` admin, `Artfever` write). Protection is implemented as two repository **rulesets** (Settings → Rules → Rulesets); the exported JSON is in `docs/evidence/`.

| Setting | `main` (ruleset 23990471) | `dev` (ruleset 23990939) |
|---|---|---|
| Deletion | blocked | blocked |
| Force-push / non-fast-forward | blocked | blocked |
| Pull request required | yes | yes |
| Approvals required | **1** (the author cannot approve their own PR) | **0** |
| Stale approvals dismissed on new push | no | no |
| Review threads must be resolved | no | no |
| Bypass actors | none (admin included) | none |
| Allowed merge methods | **merge commit only** | rebase or merge commit |
| Required status checks | the ten `ci.yml` jobs (rubric I1): `lint-and-type`, `test-backend`, `test-frontend`, `build (backend)`, `build (frontend)`, `scan (backend)`, `scan (frontend)`, `manifests`, `integration`, `context-and-image-size` | the same ten |

**Owner decision (2026-09-25): keep the process light.** `dev` was relaxed so that a merge is never blocked by review state, and `main` keeps exactly what the assignment requires (§3.4 p17, rubric A1): a pull request, one approval and, once `ci.yml` exists, the required checks. One thing GitHub still enforces on both branches: a review that **requests changes** blocks the merge until its author approves or dismisses it, so reviewers request changes only for real defects.

Repository level: **squash merge is disabled** (it would erase the per-author commit counts rubric A4 measures); *delete branch on merge* stays **off** (it would try to delete `dev` after every `dev` → `main` merge); auto-merge is off.

Evidence: `docs/evidence/ruleset-main.json` and `ruleset-dev.json` (exports of the live rules, including the required checks) and `docs/evidence/ci-gate.md` (a red pull request blocked, then green). Still open for `ASG-GH-001`: a screenshot of the ruleset page itself (`docs/evidence/protection-*`, taken by the repository owner in the browser; a CLI cannot take one).

Ask for a partner review on every PR: rubric A3 counts merged PRs that carry a substantive partner review ("≥ 5 merged PRs"), and a review comment on a merged PR still counts. `dev` no longer enforces it, so a PR may be merged when time forces it, but an unreviewed merge does not help that rubric line.

### Requirement IDs in issues
Every issue and PR cites `ASG-*` IDs from `docs/ASSIGNMENT_TRACEABILITY.md`. When a PR completes an ID, update that row's Owner/Issue/Artifact/Evidence/Status in the same PR.

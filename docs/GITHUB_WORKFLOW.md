# GitHub Workflow

## Branch Model

Decision **B-009** (owner, 2026-09-25): the assignment's literal two-branch model — `dev` for work, `main` for deployable software — plus short-lived feature branches (assignment §3.4, rubric A2, `ASG-GH-002`).

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

The assignment requires substantive partner review comments. A review must discuss code/documentation behavior or evidence. "LGTM" alone is not sufficient evidence of substantive review.

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
- Branch-model decision recorded as `docs/BLOCKERS.md` **B-009** (resolved).

### Issue templates
`.github/ISSUE_TEMPLATE/` provides `phase.yml` (parent), `feature.yml`, `docs.yml` and `bug.yml`. Every template carries the sections required above (objective, requirement IDs, context, in/out of scope, acceptance criteria, test/evidence criteria, owner, dependencies, definition of done). The pull-request template is `.github/pull_request_template.md`.

### Branch protection and review
`main` is not protected yet, and the second member becomes a collaborator on 2026-09-26 (`docs/BLOCKERS.md` B-010, B-011). Until then every change still goes through a PR. Once the partner is a collaborator: enable protection on `main` (require a PR, ≥ 1 approval, required status checks once `ci.yml` exists, no force-push, no deletion) and capture the settings screenshot for `docs/evidence/` (`ASG-GH-001`). Protecting `dev` is optional; the convention is still "PRs only, no direct commits".

Merge only PRs that have a substantive partner review — an unreviewed merge cannot count toward the "≥ 5 merged PRs with partner review" rubric line.

### Requirement IDs in issues
Every issue and PR cites `ASG-*` IDs from `docs/ASSIGNMENT_TRACEABILITY.md`. When a PR completes an ID, update that row's Owner/Issue/Artifact/Evidence/Status in the same PR.

# GitHub Workflow

## Branch Model

`main`
- protected
- deployable
- no direct push

`dev/<issue-number>-<slug>`
- developer integration branch for the specific issue
- this is the branch named by the assignment's dev/feature workflow

Do not create arbitrary branch names.

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

Before merge:
1. `git fetch origin`
2. `git rebase origin/main`
3. resolve conflicts
4. run full required checks
5. push using `--force-with-lease` only to your own branch
6. wait for CI
7. obtain required approval
8. merge via PR

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
- One branch per issue: `dev/<issue-number>-<slug>`. Phase 00 uses `dev/1-phase-00-baseline` (parent issue #1), and one PR covers sub-issues #2–#8.
- The branch-name convention conflicts with the assignment's literal "dev" branch wording; see `docs/BLOCKERS.md` **B-009**. Decide before the second PR.

### Issue templates
`.github/ISSUE_TEMPLATE/` provides `phase.yml` (parent), `feature.yml`, `docs.yml` and `bug.yml`. Every template carries the sections required above (objective, requirement IDs, context, in/out of scope, acceptance criteria, test/evidence criteria, owner, dependencies, definition of done). The pull-request template is `.github/pull_request_template.md`.

### Branch protection and review
`main` is not protected yet and the second collaborator does not exist yet (`docs/BLOCKERS.md` B-010, B-011). Until both are resolved every change goes through a PR **and no PR is merged**.

### Requirement IDs in issues
Every issue and PR cites `ASG-*` IDs from `docs/ASSIGNMENT_TRACEABILITY.md`. When a PR completes an ID, update that row's Owner/Issue/Artifact/Evidence/Status in the same PR.

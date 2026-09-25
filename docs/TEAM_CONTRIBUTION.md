# Team Contribution

## Purpose
Maintain genuine, balanced ownership between the two students. Both must be able to explain every part of the submission at the individual viva (`docs/SUBMISSION.md` §4).

## Members
| Member | GitHub | Repository permission | Sessions |
|---|---|---|---|
| Member A | `TahaSohail-Goat` | admin (owner) | own login, own clone/worktree |
| Member B | `Artfever` | write (collaborator since 2026-09-25) | own login, own clone/worktree |

## Working agreement — two real accounts, two sessions
1. **Each person acts only as themself.** Before any GitHub write, `gh auth status` must show the acting person's own account. Nobody — person or AI session — uses the other's login, token, password or SSH key, commits under the other's name, or posts a review, approval or comment for them.
2. **Two sessions, in parallel** (`AGENTS.md` §7): each person runs their own Claude Code session on their own machine login, in their own clone or `git worktree`, on their own issues, on disjoint files. A session never edits a file owned by an open issue of the other person.
3. **Git identity per clone:** `git config user.name` / `user.email` are the person's own. AI-assisted commits keep the `Co-Authored-By` trailer.
4. **Cross-review:** every PR by Member A is reviewed by Member B and vice versa. The rulesets enforce this mechanically (1 approval, the author cannot approve, stale approvals dismissed, threads resolved — `docs/GITHUB_WORKFLOW.md`).
5. **What counts as a review:** the six-point standard in `docs/GITHUB_WORKFLOW.md` ("Required Partner Review"), including one "why" question per PR whose answer stays in the thread.
6. **AI assistance is allowed and must be disclosed:** each person may use their own AI session for authoring *and* for reviewing, but only after reading the change themselves; every use is logged in `docs/AI-USAGE.md`. The viva measures whether each person can defend the code, whoever typed it.
7. **No manufactured numbers:** no artificial commits, no split commits to inflate counts, no staged conflicts. The deliberate merge conflict (rubric A5) must be a real conflict on real code between two genuine branches (planned in issue #18).

## Allocation — Phase 01 (effort points)
| Issue | Work | Owner | Reviewer | Points |
|---|---|---|---|---|
| #13 P01-S01 | PRD | `TahaSohail-Goat` | `Artfever` | 3 |
| #15 P01-S03 | FR catalog: API and domain | `TahaSohail-Goat` | `Artfever` | 6 |
| #18 P01-S06 | Traceability and allocation of Phases 02–12 | `TahaSohail-Goat` | `Artfever` | 6 |
| #14 P01-S02 | FR catalog: frontend | `Artfever` | `TahaSohail-Goat` | 4 |
| #16 P01-S04 | NFR catalog | `Artfever` | `TahaSohail-Goat` | 6 |
| #17 P01-S05 | Use cases | `Artfever` | `TahaSohail-Goat` | 5 |
| | **Total** | 15 | 15 | 30 |

Parent issue: #12. Allocation of Phases 02–12 is decided in #18 and recorded here; it must be accepted by both members in the PR thread.

## Balance tracking (rubric A3/A4)
Targets: ≥ 35 commits, neither partner below 35% by `git shortlog -sn`, ≥ 5 merged PRs each linked to an issue and each reviewed by the other person. Snapshot at the end of every phase:

| Date | Phase | Commits A / B | PRs authored A / B | PRs reviewed A / B | Note |
|---|---|---|---|---|---|
| 2026-09-25 | 00 | 6 / 0 | 1 (+1 open) / 0 | 0 / 0 | Phase 00 was authored before the partner joined; PR #9 has no partner review and cannot count toward `ASG-GH-005`. |

Commands: `git shortlog -sn --no-merges origin/main`, `gh pr list --state merged --json number,author,reviews`.

## Conflict-heavy Files
These should normally be owned by one session at a time:
- migrations
- `compose.prod.yaml`
- shared K8s base
- `.github/workflows`
- lockfiles
- root package/config files

## Review
Each merged PR needs a meaningful review from the other person. A review that only says "LGTM" does not count.

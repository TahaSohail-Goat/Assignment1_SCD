# Team Contribution

## Purpose
Maintain genuine, balanced ownership between the two students.

## Rules
- Only record real work.
- Do not create artificial commits.
- Do not ask one account to impersonate the other.
- Use separate Claude Code sessions/worktrees when parallelizing.
- Record issue ownership here.

## Allocation Table
| Contributor | GitHub handle | Area | Issues | Target contribution |
|---|---|---|---|---|
| Member A | `TahaSohail-Goat` (repository owner/admin) | Phase 00 governance and documentation baseline; remaining areas allocated in Phase 01 | #1 – #8 (Phase 00) | ≥35% |
| Member B | **not yet a collaborator — handle unknown** (B-010) | TBD in Phase 01 | none | ≥35% |

Only Member A exists on GitHub today. No work is assigned to Member B, and no Member B commits, reviews or approvals may be recorded until that person is a real collaborator using their own login (`AGENTS.md` §7).

## Contribution balance (assignment §4 A4)
`git shortlog -sn` must show neither partner below 35%, ≥ 35 commits in total, conventional prefixes. Phase 01 allocates future phases by **estimated effort**, not by commit count. Both members must be able to explain every part of the submission at the individual viva (`docs/SUBMISSION.md` §4).

## Conflict-heavy Files
These should normally be owned by one session at a time:
- migrations
- `compose.prod.yaml`
- shared K8s base
- `.github/workflows`
- lockfiles
- root package/config files

## Review
Each merged PR requiring partner review must have a meaningful partner review comment. A review that only says "LGTM" does not count (`docs/GITHUB_WORKFLOW.md`).

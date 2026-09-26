# Final audit evidence - issue #109

Verified 2026-09-26 as Artfever. Source snapshot: dev `39fca0c`, main `c5f5e38`.
This audit records actual checks and prior captures; no held video/live-provider evidence
is claimed. Review the [final checklist](../FINAL_SUBMISSION_CHECKLIST.md) for all 304 IDs.

## CI and contribution

[CI run 36243422641](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36243422641)
passes all ten jobs on merged dev `39fca0c`. Its backend log records **363 passed** and
**94.42% coverage**, using PostgreSQL 16. Frontend has **21 passing tests**. Lint, formatting,
type checks, API snapshot, image builds/scans/sizes, manifest validation and Compose integration
all pass. This supersedes the local run that skipped 33 PostgreSQL tests.

[GitHub capture](final-audit-github.json) contains exact job URLs/conclusions, current main
rules, and five merged issue-linked PRs with substantive Taha reviews: #79, #81, #91, #100,
#103. Main requires one approval, the ten checks, no force push/deletion, and merge commits.
The owner removed the separate settings screenshot task; an instructor waiver is not claimed.

`git shortlog -sn origin/dev` at 39fca0c:

```text
109 Taha Sohail
70  Artfever
```

Artfever: **70/179 = 39.1%**. Main still has 42 Artfever and 109 Taha until promotion.
These are snapshot counts, not counts of unmerged feature work.

Both published full-SHA image tags for main c5f5e38 resolve via `docker buildx imagetools inspect`; index and platform digests are retained in final-audit-github.json. PR #105 received a retrospective Artfever review of its seven documentation diffs before promotion; the screenshot caveat remains explicit.

## History exceptions

`git log origin/main --first-parent --format=%H %P|%s` finds six linear commits besides
the root. All six subjects match PR #9's original commits (first 60 characters): 349fe86,
e4279b9, fe960f7, dfffc1c, a9ceaa2, 5cb659b. `gh pr view 9 --json mergedAt,mergeCommit,commits`
confirms a rebase merge ending at 349fe86. The lint warning is preserved; linear history
alone does not demonstrate direct pushes.

The conventional-prefix check of non-merge subjects uses
`^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?: `.
It finds these actual exceptions; shared history was not rewritten:

| Commit | Subject |
|---|---|
| `5af1fdc` | [leading BOM] feat(k8s): capture HPA scaling and apply measured VPA requests |
| `99a2fca` | Abort superseded dashboard list requests |
| `6da3963` | Record frontend container and network CI evidence |
| `2936f8a` | Fix CI timeout and refresh nginx runtime packages |
| `947141e` | Add frontend and production Compose stack |
| `f16977d` | first commit |

The count/share portions of rubric A4 pass; its prefix clause retains this finding.
Git-generated merge subjects are excluded from the prefix check and included in shortlog.

## Real Redis triage-cache interval

[Executable capture](final-audit-cache.py) and [unaltered JSON output](final-audit-cache.json)
use the running Compose backend and real Redis 7.4.11. Run in PowerShell:

```powershell
Get-Content -Raw docs/evidence/final-audit-cache.py | docker compose exec -T backend python -
```

Two calls with the same unique synthetic text/location produced one miss, one hit, one rules
provider call and a Redis TTL of 86400 seconds. Hit rate is **1/2 = 50%** for this interval.
Observed service latencies were 3 ms then 0 ms (integer rounding); this is not an LLM latency
benchmark. A counting wrapper delegates to the unchanged rules provider and real TriageCache.
The script makes no database writes and deletes only its own unique cache key in finally.
It neither starts Ollama nor calls Groq. CI still provides malformed/fallback/injection cases.

## Compiled frontend

[Bundle capture](final-audit-bundle.json) identifies the actual served JavaScript by SHA256,
with no match for the submission checker's recognized credential patterns. It was fetched
from localhost:8080 after the e15766d frontend build, whose application tree equals dev 39fca0c.
This is a targeted pattern scan, not a proof against every possible secret representation.

## Existing operational evidence rechecked

- [Clean-clone provenance](screenshots-README.md): real Compose startup, 30 seed rows,
  ready checks, negative database DNS, actual browser POST/GET and screenshots; build cache
  was available. Current dev CI repeats startup and persistence checks.
- [Load/VPA evidence](k8s-load-README.md): both 9559-request runs have zero failures;
  baseline desired replicas 2 to 3; target 182m/250Mi applied; adjusted desired replicas 2.
  About 38 seconds to third Ready pod, subject to sampling uncertainty.
- [Persistence](k8s-pg-persistence.txt): 30 rows and matching full-row fingerprint after
  replacement of database pod; PVC UID unchanged.
- [Rollback](k8s-rollback-index.md): 0.18 s undo / 0.94 s overlay restoration in the tested
  rejected-rollout scenario. Old healthy replicas remained; this is not universal outage recovery.
- [Conflict markers and resolution](issue-46-triage-conflict.txt): raw add/add conflict and
  four sentences explaining retention of Taha's orchestration plus cache hooks. PR #70
  merged as 61e129a; current triage.py retains that resolved structure.
- [Red/green merge gate](ci-gate.md): PR #90 and existing screenshots; no new screenshot claimed.

## Submission lint output

Executed on the 39fca0c baseline with the #109 documentation worktree. The checker verifies
checklist coverage, not that every verdict is PASS. New evidence file count can change after
this capture is committed. Historical warning is interpreted above.

```text
PASS  5.7 repository layout                                             54 required paths present
PASS  DED-001 no .env / key file tracked
PASS  DED-001 no credential pattern in tracked files
PASS  DED-001 no .env / key file anywhere in Git history
PASS  DED-001 no credential pattern in Git history (all tracked paths)
PASS  DEVOPS-024 .env ignored, .env.example committed
PASS  DED-002 no key or secret value in Kubernetes manifests
PASS  DED-003 every image tag pinned
PASS  DED-004 no localhost between services (compose, k8s)
PASS  DED-006 compose.prod.yaml deploys images, no data port
PASS  DED-006 no NodePort/LoadBalancer Service
PASS  DED-009 PostgreSQL is a StatefulSet with volumeClaimTemplates
PASS  CICD-025 every workflow has a permissions block
PASS  CICD-026 every action has a version
PASS  DED-007 publishing/deploying jobs use needs:
PASS  DED-008 :latest is never deployed
PASS  CICD-001 ci.yml, cd.yml and release.yml exist
PASS  CICD-023 prod overlay tag is set to the commit SHA by cd.yml      runner-only substitution (docs/adr/0003-deploy-by-sha.md); Git keeps the placeholder
WARN  DED-010 commits on main that are not merges                       6: check each came from a PR (349fe86 e4279b9|docs(status): record Phase 00 pull request number; e4279b9 fe960f7|docs(env): record detected prerequisites and setup steps; fe960f7 dfffc1c|docs(requirements): establish assignment traceability, rubric and blockers; dfffc1c a9ceaa2|docs(assignment): preserve source and add faithful transcription)
PASS  final checklist covers every requirement ID                       coverage only; held and unverified items must remain BLOCKED
PASS  README exists and is not a stub
PASS  docs/ENGINEERING-NOTES.md is filled in
PASS  docs/RUNBOOK.md is filled in
PASS  docs/TRIAGE.md is filled in
PASS  ADRs 0001-0004 exist                                              found 4
PASS  docs/evidence has the captures of 5.7                             84 files
PASS  AI-USAGE has entries for both contributors
PASS  no TODO/FIXME left in code and config
PASS  GH-008 each partner has at least 35%                              origin/dev (39fca0cdbc47): Artfever 70/179 (39.1%); Taha Sohail 109/179 (60.9%)

28 passed, 1 warnings, 0 failed
Mechanical checks clean. This is a lint, not a grade.
```

## Remaining

Video/live-provider work remains held. Tag-triggered release evidence remains outstanding.
Original screenshot clause and commit-prefix exceptions are disclosed rather than silently
waived. Final main promotion/CD and submission refresh still require completion.

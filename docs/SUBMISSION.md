# Submission, Engineering Notes, Viva and Policy Requirements

Extracted from `docx/ASSIGNMENT.md` §5 (p23–26) and the parts of §3–§4 that define deliverables. Nothing here is new: every line traces to an ID in [`ASSIGNMENT_TRACEABILITY.md`](ASSIGNMENT_TRACEABILITY.md). Marks are in [`RUBRIC.md`](RUBRIC.md).

## 1. Submission package (§5.8 p26)

| # | Item | ID | Where it will come from |
|---|---|---|---|
| 1 | GitHub repository URL — public, or private with both instructors added | ASG-SUB-001 | Current repo `https://github.com/TahaSohail-Goat/Assignment1_SCD` is **public**. |
| 2 | Link to a successful `cd.yml` run that tested, published and deployed | ASG-SUB-002 | **Ready:** https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941 (full test gate, both images to GHCR by SHA, SBOMs, deploy to an ephemeral kind cluster, Ingress smoke test) |
| 3 | Link to both images in GHCR, showing SHA tags | ASG-SUB-003 | **Ready:** <https://github.com/TahaSohail-Goat/Assignment1_SCD/pkgs/container/civicpulse-backend> and `.../civicpulse-frontend`; both public, tags `34e8402fd08c371eb191558fb615bb6fcca4f2d7` and `8074879eb7067db84dab691c74dae420a078fb3f` plus `latest` |
| 4 | Demo video link (unlisted) | ASG-SUB-004 | **Pending:** to be recorded by both contributors; script in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md). Link: _not yet_ |
| 5 | `git shortlog -sn` output, pasted | ASG-SUB-005 | Recorded below; re-run right before submitting |
| 6 | `kubectl get hpa -w` capture and replicas-vs-load chart | ASG-SUB-006 | **Ready:** [`k8s-load-baseline50/hpa-watch.txt`](evidence/k8s-load-baseline50/hpa-watch.txt) and [`k8s-load-comparison.png`](evidence/k8s-load-comparison.png) |

`git shortlog -sn --no-merges` on `dev`, 2026-09-26 (refresh before submitting):

```
80	Taha Sohail
31	Artfever
```

The rubric asks for neither partner below 35 %. At this snapshot the second contributor is at 28 %, so
the remaining genuine work (pull-request reviews, documentation, evidence and fixes) should be
authored by them; artificial commits are not an option (`docs/TEAM_CONTRIBUTION.md`, rule 7).

Before submitting, from the repository root: `python scripts/check_submission.py` (ASG-SUB-007). The source calls it "a lint, not a grader"; it "catches the mechanical failures behind most of §5.3". Its content is **not supplied** by the assignment; the instructor said to write it if we want to, and we will.

Policy: late submissions are not accepted; there is no retake ("Submit something imperfect on time"). The source gives **no calendar deadline**; the instructor said it is the Google Classroom one ("next Tuesday"). (ASG-SUB-008)

## 2. Engineering notes — the eight questions (§5.2 p23–24)

File: `docs/ENGINEERING-NOTES.md`. "With references to your own files and lines. Generic answers score zero." Rubric J5 (2 marks). Answers are written in Phase 12 from real files, real line numbers and real measurements — never drafted from assumption.

| Q | ID | Question (verbatim in `docx/ASSIGNMENT.md` §5.2) | Needs, from earlier phases |
|---|---|---|---|
| 1 | ASG-DOC-017 | Three things that differ between your laptop and a CI runner, and the exact line in a Dockerfile or manifest that freezes each | Dockerfiles, compose, manifests with pinned lines |
| 2 | ASG-DOC-018 | Position on the CI/CD maturity ladder (Lecture 03, slide 32); justify the rung; name the next rung and what it buys | Lecture material (not required by the instructor) |
| 3 | ASG-DOC-019 | The exact line guaranteeing build-once-deploy-many, and what breaks without it | Frontend runtime-config line, `${IMAGE_TAG}` / SHA tag line |
| 4 | ASG-DOC-020 | What "correct" means for a probabilistic LLM component, and how CI was kept deterministic (Lecture 01, slide 34) | `SimulatedTriage`, fallback/malformed-output tests (lecture slides not required) |
| 5 | ASG-DOC-021 | HPA lag: seconds between offered load rising and replicas rising; where the time went; what would reduce it | Real load-test capture |
| 6 | ASG-DOC-022 | Why VPA is in Off mode; failure mode of running it in Auto alongside HPA | VPA manifest and recommendations |
| 7 | ASG-DOC-023 | Where the hosted-LLM caller lives given `internal: true`, and how it was resolved | Compose network design |
| 8 | ASG-DOC-024 | A failure that cost more than an hour: symptoms, what was wrongly believed first, the exact command or log line that revealed the truth | Kept as a running log during Phases 03–11 |

Additional statements the notes must also carry (they are required by other sections):

| Statement | ID | Source |
|---|---|---|
| Which query each of the two indexes serves | ASG-DATA-018 | §2.3 p8 |
| Why TTL **and** explicit invalidation (viva-ready) | ASG-CACHE-006 | §2.4 p8 |
| Why Redis needs a volume although a cache is rebuildable | ASG-CACHE-012 | §2.4 p9 |
| Live provider limits actually observed | ASG-AI-009 | §2.5 p10 |
| Measured cache hit rate | ASG-AI-017 | §2.5 p11 |
| Hosted-vs-Ollama measured trade-off (recommended) | ASG-AI-025 | §2.5 p10 |
| Where the LLM caller lives despite `internal: true` | ASG-DEVOPS-018 | §3.2 p13 |
| Image stage sizes and build-context before/after sizes | ASG-DEVOPS-010, -012 | §3.1 p12 |
| Why the dev bind mount is right in `compose.yaml` and wrong in `compose.prod.yaml`; volume justifications | ASG-DEVOPS-019, -020 | §3.2 p13 |
| 3–5 sentences on HPA lag | ASG-K8S-027 | §3.3 p16 |
| Why VPA is Off | ASG-K8S-030 | §3.3 p16–17 |

To keep Q8 honest, record any multi-hour failure in `docs/ENGINEERING-NOTES.md` **as it happens**, with the command that exposed it.

## 3. Demo video (§4 J p22)

≤ 5 minutes, **both partners speaking** (ASG-DOC-014). Must cover (ASG-DOC-015):

1. clean clone → running system (one command);
2. AI triage;
3. fallback;
4. network isolation failing (`docker compose exec frontend ping database` must fail — ASG-DEVOPS-017);
5. HPA scaling;
6. rollback — both mechanisms and when to use each (ASG-CICD-028…030).

## 4. Viva and individual accountability (§5.4 p24–25)

Individual, ten minutes each, repository open, including questions on the partner's code (ASG-SUB-009). `Individual mark = team mark × viva factor` (ASG-SUB-010): 1.0 / 0.75 / 0.5 / 0.0 as defined in [`RUBRIC.md`](RUBRIC.md) §4. "If your partner is not contributing, say so in week 1, not week 5" (ASG-SUB-011).

Viva-specific topics the source names explicitly: why TTL **and** explicit invalidation (ASG-CACHE-006); why a Deployment for a database is wrong (ASG-K8S-006).

## 5. AI assistance (§5.5 p25)

Honest attribution, not avoidance (ASG-SUB-012, ASG-DOC-025). `docs/AI-USAGE.md` must name the tools, which parts they wrote or shaped, and what was changed afterwards and why. Specific disclosure carries no penalty; presenting AI-generated work as one's own is plagiarism under the course policy. "A line you cannot defend is worth nothing regardless of its author."

This repository is developed with Claude Code. Every phase records that in `docs/AI-USAGE.md` (Phase 00 entry included).

## 6. Pre-submission gate

Do not call the assignment complete until each mandatory ID in the traceability matrix is `PASS` or has a documented exception, all eleven `ASG-DED-*` guards are verified, and:

- [ ] `python scripts/check_submission.py` run and output recorded
- [ ] clean-clone quickstart executed on a fresh clone (ASG-DED-011)
- [ ] secret scan of full Git history (ASG-DED-001)
- [ ] `git shortlog -sn` shows neither partner below 35% (ASG-GH-008)
- [ ] ≥ 5 merged PRs, each linked to an Issue with a substantive partner review (ASG-GH-003…005)
- [ ] every rubric line in [`RUBRIC.md`](RUBRIC.md) has an evidence path in [`EVIDENCE_PLAN.md`](EVIDENCE_PLAN.md)

## Decisions and instructor answers

Answers relayed by the owner on 2026-09-25. They were **verbal**, not written.

| Topic | Decision or answer | Effect |
|---|---|---|
| Deadline | The one on Google Classroom; "next Tuesday". Team target: everything done by Sunday 27 Sep | Late work is not accepted (ASG-SUB-008) |
| Scope | The whole assignment, parts A–J | No phase or rubric part is dropped |
| Rubric totals | Left as it is; the teaching assistant manages it | Every line stays at its stated marks |
| Endpoints | Nine; there is no tenth | `ASG-FR-038` is not added |
| Image signing | Not required | Cosign stays an optional bonus (`ASG-BONUS-003`) |
| `scripts/check_submission.py` | Write it if we want to | We will (it checks the deductions mechanically) |
| Lecture slides | Not necessary | Engineering-notes questions 2 and 4 are answered from this project |
| AI use | Allowed; each of us uses an assistant under their **own** account and discloses it in `docs/AI-USAGE.md` (assignment §5.5) | Only this two-account arrangement rests on the verbal answer |
| Zero-downtime demo | Not asked | We do it anyway (§3.3, bonus +4) |
| Initial commit on `main` | Not asked | History is not rewritten |
| LICENSE | Not decided | Both members decide in Phase 12 |
| `triaged_by` for `SimulatedTriage` and other hosted providers | Not specified by the assignment | Decided in Phase 02 (API design, #33) and recorded in the design document and an ADR; the four listed values must all be accepted |
| Purpose of `docs/TRIAGE.md` | Not specified by the assignment | Triage design lives in `docs/AI.md`; decide by Phase 07 |
| Frontend image tag | §2.1 says `nginx:alpine`, §3.1 says `nginx:1.27-alpine` | The pinned tag in §3.1 governs |
| Ollama in the default stack | §1.2 says five containers | Keep Ollama in `compose.yaml` |
| Branch model | `dev` plus `feature/<n>-<slug>`, PRs into `dev`, `dev` into `main` | `docs/GITHUB_WORKFLOW.md` |
| Tool installs per machine | Python 3.12, Node 22, Docker, kubectl, kind or k3d, k6 | `docs/ENVIRONMENT_PREREQUISITES.md` §8 |

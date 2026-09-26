# Repository Structure

Current inventory at dev `a4cd0b9`, verified 2026-09-26 using `git ls-files` and the 54-path layout check in `scripts/check_submission.py`. The repository root is the assignment layout root (section 5.7). All 19 layout requirements have their files. Presence does not prove runtime behavior; see the final checklist for verification limits.

| Requirement | Paths | Inventory |
|---|---|---|
| ASG-REPO-001 | `backend/app/{routes,services,repositories,providers}/` | Present; Implemented |
| ASG-REPO-002 | `backend/app/providers/triage/{base,llm,ollama,rules,simulated,factory}.py` | Present; Implemented |
| ASG-REPO-003 | `backend/alembic/versions/` | Present; Implemented (P05-S01, #40) |
| ASG-REPO-004 | `backend/tests/` | Present; Implemented (P04-S03, #39) |
| ASG-REPO-005 | `backend/Dockerfile`, `backend/.dockerignore`, `backend/pyproject.toml` | Present; Implemented (#47) |
| ASG-REPO-006 | `frontend/src/{components,pages,api}/` | Present; Implemented (#34-#36) |
| ASG-REPO-007 | `frontend/tests/` | Present; Implemented (#36) |
| ASG-REPO-008 | `frontend/Dockerfile`, `frontend/.dockerignore`, `frontend/nginx.conf`, `frontend/package.json` | Present; Implemented (#48) |
| ASG-REPO-009 | `k8s/base/{namespace,backend,frontend,postgres,redis,ingress,configmap,secret}.yaml` | Present; Implemented (P09-S01, #49) |
| ASG-REPO-010 | `k8s/base/{hpa,vpa,pdb}.yaml`, `k8s/base/kustomization.yaml` | Present; Implemented (#49, #50) |
| ASG-REPO-011 | `k8s/overlays/{dev,prod}/kustomization.yaml` | Present; Implemented (P09-S01, #49) |
| ASG-REPO-012 | `load/k6-script.js` | Present; Implemented: `load/k6-script.js`; two real captures in `docs/evidence/k8s-load-README.md` |
| ASG-REPO-013 | `docs/{ENGINEERING-NOTES,RUNBOOK,AI-USAGE,TRIAGE}.md` | Present; Implemented (#54, #55): all four documents are written |
| ASG-REPO-014 | `docs/adr/0001-provider-interface.md` … `0004-pii-and-data-governance.md` | Present; Implemented: ADRs 0001-0004 |
| ASG-REPO-015 | `docs/evidence/` | Present; Implemented |
| ASG-REPO-016 | `scripts/check_submission.py` | Present; Implemented (#56) |
| ASG-REPO-017 | `.github/workflows/{ci.yml,cd.yml,release.yml}` | Present; Implemented (#51, #52) |
| ASG-REPO-018 | `compose.yaml`, `compose.prod.yaml`, `.env.example`, `.gitignore` | Present; Implemented (#47, #48) |
| ASG-REPO-019 | `README.md`, `LICENSE` | Present; Implemented: `README.md` written (#55, #100), `LICENSE` is MIT (#99) |

Additional implementation files include `scripts/k8s-up.sh`, `.github/workflows/k8s-quickstart.yml`, frontend theme tests, and this audit's `docs/FINAL_SUBMISSION_CHECKLIST.md`. The first two support the verified second deployment command; theme is an optional enhancement. `docx/` preserves the assignment source; governance documents record collaboration and decisions.

## Decisions recorded in Phase 00

| # | Decision | Reason |
|---|---|---|
| 1 | The prompt pack was flattened into the repository root and its wrapper folder deleted. | Requested by the repository owner; the pack's own documents (`CLAUDE.md`, `AGENTS.md`, `docs/…`) address paths relative to the repository root. |
| 2 | The existing root `README.md` (0 bytes, tracked) was replaced by the pack's `README.md`. | The original held no content; nothing was lost. |
| 3 | `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` → `.github/pull_request_template.md`. | GitHub auto-applies a single default template only from `.github/pull_request_template.md`; a file inside a `PULL_REQUEST_TEMPLATE/` directory is treated as one of several selectable templates. |
| 4 | Empty directories carry a `.gitkeep`; a `.gitkeep` is deleted in the same commit that adds the first real file to its directory. | Git does not track empty directories. |
| 5 | `.gitignore` blocks `.env*` (except `.env.example`), keys, certificates and kubeconfigs before any code exists. | The −20 deduction (ASG-DED-001) is triggered by a secret **anywhere in history**; prevention must precede the first commit that could contain one. Committed placeholder manifests such as `k8s/base/secret.yaml` remain trackable. |
| 6 | `.gitattributes` forces LF and marks the PDF and images binary. | Development is on Windows with `core.autocrlf=true`; CRLF in Dockerfiles/scripts breaks Linux containers. Also guarantees the assignment PDF cannot be rewritten by line-ending logic. This is engineering hygiene, not an assignment requirement. |
| 7 | The `docx/assets/architecture-diagram.png` derivative was added. | The diagram is not in the PDF text layer; keeping it beside the transcription makes `ASSIGNMENT.md` self-contained. It is a byte-for-byte extraction of the embedded image. |

## Rules going forward

- New top-level directories require an issue and an update to this file.
- Files the assignment lists (§5.7) must live at exactly those paths.
- The four prompt/governance files at the root (`CLAUDE.md`, `AGENTS.md`, `PROMPT.md`, `START_HERE.md`) are kept for the duration of development. Phase 12 decides whether they stay in the submitted repository; they are also AI-usage evidence (ASG-DOC-025).
- Nothing outside the §5.7 layout and `docs/`/`docx/` governance additions is added without a recorded reason.

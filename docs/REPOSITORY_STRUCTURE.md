# Repository Structure

Source of truth: assignment §5.7 (p25–26), requirement IDs `ASG-REPO-001…019`. Phase 00 created the **directory skeleton only** (`.gitkeep` placeholders); no application code exists yet. Phase 02 re-verifies this structure against the assignment before implementation begins.

## Layout

The repository root **is** the layout root (the source calls it `civicpulse/`; the product may be renamed — ASG-GEN-004). Legend: ✅ exists now · 📁 placeholder directory (`.gitkeep`) · ⏳ created by the phase shown.

```
.
├── backend/                                   ASG-REPO-001…005
│   ├── app/
│   │   ├── routes/                            📁  Phase 04   HTTP only
│   │   ├── services/                          📁  Phase 04   business rules, state machine, stats
│   │   ├── repositories/                      📁  Phase 05   all SQL, nowhere else
│   │   └── providers/
│   │       └── triage/                        📁  Phase 07   base · llm · ollama · rules · simulated · factory (.py)
│   ├── alembic/versions/                      📁  Phase 05   migrations only, no startup DDL
│   ├── tests/                                 📁  Phase 04+
│   └── Dockerfile · .dockerignore · pyproject.toml         ⏳ Phase 04 / 08
├── frontend/                                  ASG-REPO-006…008
│   ├── src/{components,pages,api}/            📁  Phase 03
│   ├── tests/                                 📁  Phase 03
│   └── Dockerfile · .dockerignore · nginx.conf · package.json   ⏳ Phase 03 / 08
├── k8s/                                       ASG-REPO-009…011
│   ├── base/                                  📁  Phase 09   namespace, backend, frontend, postgres, redis,
│   │                                                         ingress, configmap, secret, hpa, vpa, pdb, kustomization
│   └── overlays/{dev,prod}/                   📁  Phase 09   kustomization.yaml each
├── load/                                      📁  Phase 09   k6-script.js  (ASG-REPO-012)
├── scripts/                                   📁  Phase 12   check_submission.py (B-014)  (ASG-REPO-016)
├── docs/                                      ASG-REPO-013…015
│   ├── ENGINEERING-NOTES.md · RUNBOOK.md · AI-USAGE.md          ✅ stubs (final content Phase 11–12)
│   ├── TRIAGE.md                              ⏳ purpose unspecified (B-016)
│   ├── adr/0001…0004-*.md                     ✅ stubs (the four ADRs the rubric requires)
│   ├── evidence/                              📁  Phase 11   screenshots, captures, charts
│   └── …governance documents (see DOCUMENT_INDEX.md)           ✅
├── docx/                                      ✅ authoritative assignment source + transcription
│   ├── ASSIGNMENT_SOURCE.pdf                  ✅ unchanged, SHA-256 in EXTRACTION_NOTES.md
│   ├── ASSIGNMENT.md · EXTRACTION_NOTES.md    ✅ Phase 00
│   └── assets/architecture-diagram.png        ✅ extracted from PDF page 3
├── .github/
│   ├── workflows/                             📁  Phase 10   ci.yml · cd.yml · release.yml  (ASG-REPO-017)
│   ├── ISSUE_TEMPLATE/                        ✅ Phase 00
│   └── pull_request_template.md               ✅ Phase 00
├── compose.yaml · compose.prod.yaml · .env.example              ⏳ Phase 08  (ASG-REPO-018)
├── .gitignore · .gitattributes                ✅ Phase 00
├── README.md                                  ✅ placeholder; real README Phase 12   (ASG-REPO-019)
├── LICENSE                                    ⏳ type not specified (B-015)
├── CLAUDE.md · AGENTS.md · PROMPT.md · START_HERE.md            ✅ governance / execution framework
```

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

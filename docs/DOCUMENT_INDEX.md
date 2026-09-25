# Document Index

| Document | Purpose | Read When |
|---|---|---|
| `docx/ASSIGNMENT_SOURCE.pdf` | Original assignment, unchanged (SHA-256 in `docx/EXTRACTION_NOTES.md`) | Only to settle a transcription doubt |
| `docx/ASSIGNMENT.md` | Authoritative searchable assignment transcription | Always before requirement decisions |
| `docx/EXTRACTION_NOTES.md` | How the transcription was made; source anomalies (`EN-xx`) | When a source sentence looks odd or incomplete |
| `docs/ASSIGNMENT_TRACEABILITY.md` | Requirement IDs (`ASG-*`) and evidence mapping | Every phase |
| `docs/RUBRIC.md` | Rubric lines with marks → requirement IDs; deductions; bonus; viva | Planning, QA, final audit |
| `docs/SUBMISSION.md` | Submission package, engineering-notes questions, video, viva, AI policy | Phases 11–12, planning evidence |
| `docs/REPOSITORY_STRUCTURE.md` | Required layout (§5.7), what exists, which phase fills what | Any time a file is created |
| `docs/PHASE_STATUS.md` | Phase gate status and the next permitted phase | Start and end of every phase |
| `docs/PRD.md` | Product scope and actors | Requirements, frontend, backend |
| `docs/FRs.md` | Functional requirements | Feature implementation |
| `docs/NFRs.md` | Non-functional requirements | Architecture, QA, security |
| `docs/USE_CASES.md` | Behavioral flows | API/UI testing |
| `docs/ARCHITECTURE.md` | System architecture | Architecture/backend/infra |
| `docs/FRONTEND.md` | Frontend rules | Frontend |
| `docs/BACKEND.md` | Backend layering/API rules | Backend |
| `docs/DATA_MODEL.md` | Database model | Data layer |
| `docs/CACHE.md` | Redis cache/rate limiting | Cache |
| `docs/AI.md` | AI provider abstraction and safeguards | AI |
| `docs/DEVOPS.md` | Docker and Compose | DevOps |
| `docs/KUBERNETES.md` | K8s manifests and probes | Kubernetes |
| `docs/CICD.md` | GitHub Actions | CI/CD |
| `docs/SECURITY.md` | Security baseline | Every implementation/release |
| `docs/GITHUB_WORKFLOW.md` | Issues, branches, PRs, labels, review, merge | Every GitHub action |
| `docs/EVIDENCE_PLAN.md` | Evidence required for rubric | QA/release |
| `docs/TEAM_CONTRIBUTION.md` | Ownership and collaboration | Parallel work |
| `docs/AI_SESSIONS.md` | Shared manual for both AI sessions: one phase at a time, parallel vs handoff vs solo, phase-by-phase table, handoff protocol, checklists, paste-ready prompts | Start of **every** session, and at every handoff |
| `docs/PARTNER_RUNBOOK.md` | Step-by-step routine for Contributor B's own AI session (tool install → login → PR → review → merge) | Contributor B, every session |
| `docs/ENVIRONMENT_PREREQUISITES.md` | Detected tools, install steps for missing ones | Phase 00, onboarding, before Phases 08–09 |
| `docs/RUNBOOK.md` | Operational procedures | Deployment/demo |
| `docs/ENGINEERING-NOTES.md` | Answers to the assignment's eight reflection questions | Final phase (log failures as they happen) |
| `docs/AI-USAGE.md` | Honest AI-assistance disclosure | Throughout; finalize before submission |
| `docs/BLOCKERS.md` | Unresolved source/implementation questions (`B-xxx`) | Whenever something is unclear |
| `docs/PHASE_EXECUTION_PROTOCOL.md` · `docs/QUALITY_GATES.md` | Phase loop and gates | Start/end of each phase |
| `docs/adr/` | Architecture decision records (the four required ADRs plus any others) | When making or revisiting a decision |
| `docs/phases/PHASE-NN-*.md` | Scope of each phase | The current phase only |
| `PROMPT.md` · `CLAUDE.md` · `AGENTS.md` · `START_HERE.md` | Execution framework and permanent contract | Once per session (`AGENTS.md`/`CLAUDE.md`), `PROMPT.md` per phase |

## Token-Saving Rule

Do not read every document before every small edit.

Use the phase prompt and this table to determine the minimum reading set. Expand only when a change crosses domains. For a single requirement, search `docx/ASSIGNMENT.md` for the exact clause (page markers `PDF page N` help) and look up its ID in `docs/ASSIGNMENT_TRACEABILITY.md`.

## Authority Order

1. `docx/ASSIGNMENT_SOURCE.pdf` / `docx/ASSIGNMENT.md` (highest).
2. Approved ADRs and the current issue's acceptance criteria.
3. Governance and phase documents in this repository.
4. Anything else — never overrides 1–3. Conflicts and ambiguities go to `docs/BLOCKERS.md`.

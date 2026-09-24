# CivicPulse — CS4032 Software Construction and Design

This repository is developed in phases from the authoritative assignment.

## Status
**Phase 00 — assignment baseline and governance.** No application code exists yet; everything under "Core Architecture" below is what the assignment *requires*, not a claim about what runs today. This README will be rewritten with a working quickstart, badges, architecture diagram and screenshots in the final phase, and will only assert what can be demonstrated. Current phase status: [`docs/PHASE_STATUS.md`](docs/PHASE_STATUS.md).

## First Read
1. `CLAUDE.md`
2. `AGENTS.md`
3. `docx/ASSIGNMENT.md`
4. `docs/DOCUMENT_INDEX.md`
5. `PROMPT.md`

## Source of Truth
The assignment source is stored under `docx/` (`ASSIGNMENT_SOURCE.pdf`, unchanged).
The Markdown transcription (`docx/ASSIGNMENT.md`) is for searchable engineering use and must faithfully preserve the source content; anomalies found while transcribing are in `docx/EXTRACTION_NOTES.md`. Requirement IDs, rubric mapping and open questions live in `docs/ASSIGNMENT_TRACEABILITY.md`, `docs/RUBRIC.md` and `docs/BLOCKERS.md`.

## Working Principle
No requirement is implemented from memory or assumption. Requirements are mapped to traceability IDs, issues, code, tests, and evidence.

## Core Architecture Required by the Assignment
- React 18 + Vite + TypeScript frontend
- FastAPI + Pydantic v2 (Flask is permitted if explicitly documented)
- PostgreSQL 16 + Alembic
- Redis 7
- AI provider abstraction with hosted LLM, Ollama, rules fallback, and simulated CI path as required
- Docker multi-stage images
- Docker Compose with network segmentation
- Kubernetes with Kustomize (or Helm only if explicitly chosen/documented)
- GitHub Actions CI/CD
- GHCR publishing
- security/quality gates
- evidence and reflection documentation

## Current Rule
Do not claim a component is complete merely because it exists. It is complete only when its assignment contract, tests, operational behavior, and evidence are satisfied.

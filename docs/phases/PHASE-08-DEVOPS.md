# Phase 08 — Docker & Compose

## Read
- assignment DevOps section
- DEVOPS
- SECURITY
- architecture
- AI network implications

## Implement
Two multi-stage images:
- backend: pinned Python slim base
- frontend: Node build + nginx runtime

Required:
- pinned bases
- non-root
- exec CMD
- HEALTHCHECK
- cache-friendly Dockerfile order
- .dockerignore
- build-context size measurement
- Compose two-network topology
- internal network segmentation
- three named volumes
- dev bind mount only in dev
- service healthchecks
- healthy depends_on
- restart policy
- resource limits
- env-based credentials
- .env.example
- production compose uses images only
- no DB/cache port publication in prod

Demonstrate frontend→database network failure.

## Gate
Clean clone can start the complete system with the documented command.

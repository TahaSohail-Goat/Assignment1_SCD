# Phase 10 — CI/CD

## Read
- assignment CI/CD section
- CICD
- SECURITY
- Docker/K8s docs
- GitHub workflow

## Implement
`.github/workflows/ci.yml`
- PR to main
- dev push trigger as required
- backend lint/type/tests
- frontend lint/type/tests
- coverage ≥65%
- build images without push
- Trivy
- kubeconform
- Compose integration smoke
- wait for `/ready`
- post/get complaint
- assert cache MISS→HIT

`.github/workflows/cd.yml`
- main
- full test gate
- build/push GHCR
- SHA tag
- `latest` may exist as a pushed tag only if assignment permits, but deployment must never use it
- SBOM
- ephemeral kind/k3d
- rollout status
- ingress smoke
- HPA visibility

`.github/workflows/release.yml`
- `v*` tags
- semver tags
- release notes

Apply:
- `needs:`
- minimal permissions
- secrets from GitHub Secrets
- pinned action versions, ideally commit SHA where practical

## Evidence
Create a deliberate failing PR, capture red check and blocked merge state, then fix and capture green.

## Gate
Publishing/deployment cannot run when validation is red.

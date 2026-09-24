# Evidence Plan

Evidence must be real and reproducible.

## Repository / GitHub
- protected main screenshot
- issue hierarchy
- labels
- branch list
- PR list
- partner review comments
- `git shortlog -sn`
- conflict evidence

## Docker / Compose
- clean clone quickstart
- image stage sizes
- `.dockerignore` context sizes before/after
- network isolation command showing frontend cannot reach DB
- persistence demo
- cache HIT/MISS
- rate limit 429 + Retry-After

## AI
- provider metadata
- fallback case
- malformed output validation
- timeout/retry behavior
- prompt injection test
- measured cache hit rate
- measured triage latency
- PII decision ADR

## Kubernetes
- deployment state
- probes
- rollout
- HPA watch output
- replicas-vs-load chart
- VPA recommendation
- updated requests
- PostgreSQL persistence after pod deletion
- rollback

## CI/CD
- red PR check blocked
- green re-run
- image scan
- manifest validation
- Compose integration
- SHA-tagged GHCR image
- SBOM
- deployment smoke test

Store screenshots/charts under `docs/evidence/` using descriptive names.

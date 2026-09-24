# Security Baseline

## Secrets
Never commit:
- `.env`
- LLM keys
- registry tokens
- passwords
- certificates/private keys
- kubeconfig
- credentials in fixtures/logs

Use:
- `.env.example`
- environment variables
- GitHub Secrets
- Kubernetes Secret references

## Containers
- non-root users
- pinned base images
- small final images
- no development dependencies in runtime image
- healthcheck
- read-only assumptions where practical

## Network
Frontend:
- edge network only

Backend:
- edge + internal

Database:
- internal only

Redis:
- internal only

Frontend must provably fail to reach PostgreSQL.

## API
- validate every external input
- field-level errors
- rate limit complaint submission
- avoid leaking internal exception data
- propagate/request-generate request IDs
- do not log secrets
- do not log full sensitive complaint contact data unless explicitly justified

## LLM
Complaint text is untrusted data.
- delimit it
- constrain output to schema
- reject malformed output
- use timeout
- limited retry
- safe fallback
- cache by content hash
- document PII handling

## Kubernetes
- placeholders in committed secret manifests
- Secret references in workloads
- least-privilege service accounts/permissions where applicable
- resource requests/limits
- probes with correct semantics
- no DB NodePort/LoadBalancer

## GitHub Actions
Every workflow should have explicit minimal permissions.
Publishing and deployment jobs must depend on successful validation.
Never deploy `latest`.

# CI/CD Engineering Contract

Required workflows:
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- `.github/workflows/release.yml`

CI:
- PR to main
- push to `dev` (assignment §3.4)
- PR to `dev`: optional superset so feature PRs are gated before they reach `dev`; decided in Phase 10 (`docs/GITHUB_WORKFLOW.md`, "Pull-Request Flow")
- lint
- type check
- backend tests + coverage
- frontend tests
- build without push
- Trivy scan
- kubeconform
- Docker Compose integration smoke

CD:
- main only
- full test gate
- build/push GHCR
- SHA tag
- SBOM
- ephemeral kind/k3d deployment
- rollout status
- Ingress smoke test
- HPA visibility

Security:
- secrets from GitHub Secrets
- least-privilege permissions
- publishing/deploying jobs gated with `needs`
- no deploy of `latest`

Release:
- tags matching `v*`
- semver tags
- release notes

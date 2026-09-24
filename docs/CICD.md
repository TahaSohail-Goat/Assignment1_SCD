# CI/CD Engineering Contract

Required workflows:
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- `.github/workflows/release.yml`

CI:
- PR to main
- push to dev/work branches as required
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

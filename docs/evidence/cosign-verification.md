# Cosign keyless verification (ASG-BONUS-003)

`cd.yml` signs the two GHCR image digests after publishing, using GitHub Actions OIDC and no
stored signing key. Before Kubernetes resources are created, the deployment job verifies each
digest's signature against this repository's `cd.yml` workflow identity on `refs/heads/main`.

The next successful main-branch CD run is the required live evidence. Its **Keylessly sign
published image digests** and **Verify keyless signatures before deployment** steps must both
be green. Record that run URL and the two digest references here only after it succeeds.

This document intentionally contains no synthetic signature, digest, or screenshot.

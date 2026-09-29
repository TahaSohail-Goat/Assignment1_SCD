# Cosign keyless verification (ASG-BONUS-003)

`cd.yml` signs the two GHCR image digests after publishing, using GitHub Actions OIDC and no
stored signing key. Before Kubernetes resources are created, the deployment job verifies each
digest's signature against this repository's `cd.yml` workflow identity on `refs/heads/main`.

Main CD [36554371413](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36554371413)
at `77cc1e0` completed successfully on 2026-09-29. Its **Keylessly sign published image digests**
and **Verify keyless signatures before deployment** steps both passed, followed by the ephemeral
kind deployment and Ingress smoke test. The workflow summary is the authoritative record of the
two published digest references.

This document intentionally contains no synthetic signature, digest, or screenshot.

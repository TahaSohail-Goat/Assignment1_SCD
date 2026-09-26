# Kubernetes rollback evidence (#54)

The archived copy [k8s-rollback-local.txt](k8s-rollback-local.txt) is byte-identical to
the original. The original, unedited capture is [cd-local-rollback.txt](cd-local-rollback.txt), committed
with #52. Both methods were run against the real kind cluster through the actual ingress.
It records 0.18s for imperative undo and 0.94s for restoring the previous source overlay/SHA.
The intentionally missing image never displaced the old healthy replicas. These timings
are specific to that rejected rollout and are not an outage-recovery guarantee.

Commands and the choice between methods are in [RUNBOOK section 13](../RUNBOOK.md#13-rollback).
Images in this local rehearsal were built locally and loaded under SHA names; this is not a
successful GHCR/CD capture. The required both-partner video remains pending.

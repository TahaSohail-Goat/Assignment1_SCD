# Argo CD GitOps evidence (ASG-BONUS-002, issue #130)

This package records a local, live Argo CD reconciliation of CivicPulse from the public
repository. The Application targets `dev` at `k8s/overlays/dev`, names the in-cluster
`civicpulse` namespace, and enables automated prune and self-heal. The Secret is deliberately
absent from that overlay and is created out of band by the Kubernetes quickstart; neither the
manifest nor this evidence includes a secret value.

Captured on 2026-09-29 from the `kind-civicpulse` cluster:

- [`status.txt`](argocd-gitops-bonus130-20260929/status.txt) reports `sync=Synced` and
  `health=Healthy` for revision `27103d1f1175b7c1f695857f812f3d0cc7d263d8`.
- [`workloads.txt`](argocd-gitops-bonus130-20260929/workloads.txt) records two available backend
  replicas, two available frontend replicas, cache, and the corresponding Pods.
- [`argocd-pods.txt`](argocd-gitops-bonus130-20260929/argocd-pods.txt) records the running Argo CD
  components. [`hashes.txt`](argocd-gitops-bonus130-20260929/hashes.txt) gives SHA-256 hashes of
  the non-secret text captures.
- [`terminal-argocd-live.png`](argocd-gitops-bonus130-20260929/terminal-argocd-live.png) is an
  unedited Windows PowerShell screenshot of the live `kubectl` status: Application `Synced` /
  `Healthy`, available CivicPulse deployments, and ready Argo CD controllers.

The initial Argo installation was interrupted by a Docker Desktop restart. The raw evidence and
screenshot above were recaptured only after Kubernetes DNS, Argo CD, and all CivicPulse deployments
had recovered. This is local demo evidence, not a claim that a remote production cluster exists.

Run the repeatable procedure after `bash scripts/k8s-up.sh`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/argocd-gitops-demo.ps1
```

The declarative Application follows Argo CD's documented [declarative setup](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/) and
[automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/) model.

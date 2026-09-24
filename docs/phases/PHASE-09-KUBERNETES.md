# Phase 09 — Kubernetes

## Read
- assignment K8s section
- KUBERNETES
- DEVOPS
- SECURITY
- architecture
- load test requirements

## Implement
Kustomize:
- `k8s/base`
- `k8s/overlays/dev`
- `k8s/overlays/prod`

Resources:
- namespace `civicpulse`
- backend Deployment ≥2 replicas
- frontend Deployment ≥2
- PostgreSQL StatefulSet + PVC
- Redis Deployment + PVC
- four ClusterIP Services
- Ingress `/` and `/api`
- ConfigMap
- Secret placeholders
- HPA
- VPA
- PDB

Probes:
- startup
- liveness uses `/health`
- readiness uses `/ready`

Rolling:
- maxSurge 1
- maxUnavailable 0
- termination grace
- preStop

HPA:
- autoscaling/v2
- min 2
- max 10
- CPU target 60
- stabilization settings from assignment

VPA:
- Off/recommender only
- capture recommendations
- update requests
- explain HPA/VPA interaction

Install metrics-server and capture HPA load evidence.

## Gate
Kubernetes is deployed and demonstrated, not just syntactically valid.

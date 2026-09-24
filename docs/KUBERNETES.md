# Kubernetes Engineering Contract

Required namespace:
`civicpulse`

Required workload types:
- backend Deployment ≥2
- frontend Deployment ≥2
- PostgreSQL StatefulSet + PVC
- Redis Deployment + PVC

Required:
- four ClusterIP Services
- Ingress `/` → frontend and `/api` → backend
- ConfigMap + Secret separation
- startup/liveness/readiness probes
- resource requests/limits
- rolling update settings
- PDB
- HPA v2
- VPA in Off/recommender mode
- metrics-server
- load generation
- HPA evidence
- VPA recommendation evidence
- persistence and rollback evidence

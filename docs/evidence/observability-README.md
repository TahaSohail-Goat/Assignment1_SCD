# Optional observability evidence (ASG-BONUS-004, issue #123)

Captured 2026-09-28 from the local `observability` Compose profile. The dashboard
screenshot is [observability-grafana-dashboard.png](observability-grafana-dashboard.png),
captured from a real Grafana 12.2.0 browser session. It shows the backend scrape value
`1`, 25 HTTP requests and a nonzero request-rate graph. The triage p95 panel correctly
shows no data because no triage request was sent in the screenshot window; it does not
claim a latency measurement.

Verification on this machine:

```text
docker compose --profile observability up -d --build --wait
  backend, frontend, database, cache, prometheus and grafana healthy; migrate exited 0
GET /api/v1/targets on local Prometheus
  health: up
  lastError: (empty)
  scrapeUrl: http://backend:8000/metrics
GET /api/v1/query?query=up{job="civicpulse-backend"}
  instance: backend:8000
  value: 1
GET /api/v1/query?query=sum(http_requests_total)
  value: 7 before an additional eight GET /api/complaints requests
```

The dashboard also renders the real, later increased counter. The Compose profile is
optional; Grafana and Prometheus ports bind only to host loopback. The ignored `.env`
holds the locally generated Grafana admin password; no credential is in this evidence.

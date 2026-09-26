# Runbook

Every command in a section marked **checked in CI** is run, in this order, by the `integration`
job of `.github/workflows/ci.yml` on a clean runner (step "RUNBOOK commands"), so it works from a
fresh clone. Sections marked **pending** are written when the feature they describe is merged; none
of them is filled from memory.

Run everything from the repository root. Service names are `database`, `cache` and `backend`
(`compose.yaml`).

## 1. Local startup (checked in CI)

```
cp .env.example .env          # then edit POSTGRES_PASSWORD
docker compose up -d --build
curl -fsS http://localhost:8000/ready
```

`/ready` answers `{"status":"ready","checks":{"postgres":"ok","redis":"ok"}}` when both
dependencies answer, and `503` with the failing dependency named when one does not. The `migrate`
service runs `alembic upgrade head` and exits; the backend starts only after it succeeded.

Try it:

```
curl -fsS -X POST http://localhost:8000/api/complaints \
  -H 'Content-Type: application/json' \
  -d '{"text":"The water tap in our lane has had no supply for three days.","location":"Lane 3"}'
curl -fsS http://localhost:8000/api/complaints
```

## 2. Configuration (checked in CI)

All configuration is environment variables; `.env.example` lists every one, `.env` is git-ignored.

| Variable | Meaning |
|---|---|
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | database credentials; `compose.yaml` builds `DATABASE_URL` from them |
| `LOG_LEVEL` | `INFO` by default |
| `TRIAGE_PROVIDER` | `rules` (default), `simulated`; the hosted and Ollama providers are described in `docs/AI.md` |
| `BACKEND_PORT` | published port of the API, `8000` |

A missing `DATABASE_URL` or `REDIS_URL` stops the backend at start with a message naming it: the
settings have no defaults on purpose.

## 3. Logs (checked in CI)

```
docker compose logs --tail 20 backend
docker compose logs -f backend
```

One JSON object per line on stdout; every line carries `request_id`. Pass your own with
`curl -H 'X-Request-ID: my-id' ...` and search for it.

## 4. Health and readiness (checked in CI)

```
curl -fsS http://localhost:8000/health    # the process is alive; checks nothing outside itself
curl -fsS http://localhost:8000/ready     # PostgreSQL and Redis answer
curl -fsS http://localhost:8000/metrics   # Prometheus text
```

## 5. Database migration (checked in CI)

```
docker compose run --rm migrate alembic current
docker compose run --rm migrate alembic upgrade head
```

The application never creates or alters a table: only Alembic does. To go back one step:
`docker compose run --rm migrate alembic downgrade -1`.

## 6. Seed

Pending: `python -m app.seed` arrives with issue #41 and is wired into Compose afterwards.

## 7. Cache inspection (checked in CI)

```
curl -si http://localhost:8000/api/stats | grep -i '^x-cache'
docker compose exec cache redis-cli TTL stats:v1
docker compose exec cache redis-cli GET stats:v1
docker compose exec cache redis-cli CONFIG GET appendonly
```

`X-Cache` is `MISS` on the first call and after a new complaint, `HIT` until the 30 second TTL ends.
`TTL` shows the seconds left; `-2` means the key is absent. If Redis is down the API still answers
(stats come from PostgreSQL as a `MISS`).

## 8. Rate-limit diagnosis

Pending: the limiter arrives with issue #43.

## 9. LLM failure diagnosis

Pending: the hosted and Ollama providers arrive with issue #45 and the orchestration log fields are
in `docs/AI.md`. What holds now: a provider failure never fails a request; the complaint is stored
with `triaged_by="rules:fallback"` and one WARNING carries `complaint_id`, `provider`,
`error_class`.

## 10. Compose deployment (checked in CI)

```
docker compose up -d --build
docker compose ps
```

The stack has two networks: `edge` (published) and `internal` (`internal: true`, no route out).
Only `backend` is on both; `database` and `cache` publish no port. Data survives
`docker compose down` because it lives in the named volumes `pgdata` and `redisdata`.

## 11–12. Kubernetes deployment, HPA and VPA

Pending: written from the commands of issues #49, #50 and #52.

## 13. Rollback

First select the intended cluster explicitly. The following commands target the local rehearsal
cluster, not an arbitrary current context:

```powershell
kubectl --context kind-civicpulse -n civicpulse rollout history deployment/backend
kubectl --context kind-civicpulse -n civicpulse rollout undo deployment/backend
kubectl --context kind-civicpulse -n civicpulse rollout status deployment/backend --timeout=120s
```

Use this imperative reversal when the newest Deployment template is bad and the previous
revision is known good. It does not undo schema migrations, Secret or ConfigMap changes.
Confirm the application through the Ingress after the rollout.

For an auditable declarative recovery, restore the **previous source checkout and its full
image SHA**. Set `$previousSha` to the actual known-good deployment SHA (from its Actions summary).
Use a new, unused worktree directory; do not overwrite an existing checkout:

```powershell
git worktree add --detach ..\civicpulse-rollback $previousSha
$overlayPath = '..\civicpulse-rollback\k8s\overlays\prod\kustomization.yaml'
$overlayText = [IO.File]::ReadAllText((Resolve-Path $overlayPath))
[IO.File]::WriteAllText((Resolve-Path $overlayPath), $overlayText.Replace('REPLACE_WITH_COMMIT_SHA', $previousSha))
kubectl --context kind-civicpulse apply -k ..\civicpulse-rollback\k8s\overlays\prod
kubectl --context kind-civicpulse -n civicpulse rollout status deployment/backend --timeout=120s
kubectl --context kind-civicpulse -n civicpulse rollout status deployment/frontend --timeout=120s
```

The existing namespace Secret and persistent database remain. Ensure the cluster can pull
those SHA images (or load them into kind first, as CD does). Check migration compatibility
before applying an older application to a newer schema; this procedure never drops data.

Measured local rehearsal: [raw commands and output](evidence/cd-local-rollback.txt).
An intentionally nonexistent backend image left the old healthy replicas serving traffic.
Undo plus rollout verification and ingress smoke took **0.18 seconds**; restoring the prior
overlay took **0.94 seconds**. Both `/` and `/api/stats` returned 200 before and after each
recovery. These timings apply to a rejected image rollout with healthy previous pods, not
every possible outage. Images were built locally, tagged with the full `b442e8d` source SHA
and loaded into kind; GHCR publishing and the successful main-branch CD run are still pending.
The required video of both methods and explanations must still be recorded by the partners.

## 14. Incident response (Compose)

| Symptom | Look at | Likely cause |
|---|---|---|
| `/ready` is 503 | the `checks` in the body, then `docker compose ps` | the named dependency is down or unhealthy |
| backend restarts | `docker compose logs backend` | a missing variable, or `migrate` failed: `docker compose logs migrate` |
| `POST` answers 201 but `triaged_by` is `rules:fallback` | the WARNING with `error_class` | the configured provider failed; the fallback worked as designed |
| stats look stale | `X-Cache` and `TTL stats:v1` | within 30 seconds of a change made while Redis was down |

## 15. Clean teardown (checked in CI)

```
docker compose down        # keeps the data
docker compose down -v     # also removes pgdata and redisdata
```

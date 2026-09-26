# Engineering Notes

Issue #54; ASG-DOC-016..024, ASG-DATA-023. Source references below are file-and-line
references to integration commit `9134c7f`; later edits may move the lines.
Lecture slides are not a submission dependency: see `docs/SUBMISSION.md:99`, which records
that the instructor allowed Q2/Q4 to be answered from this project.

## 1. Three laptop/CI differences and how we freeze them

| Difference | Exact repository line | Effect and limit |
|---|---|---|
| Windows laptop with Python 3.14 versus Linux CI with Python 3.12 | `backend/Dockerfile:5` and `:19`: `FROM python:3.12.14-slim-bookworm` | Both image stages use the same Python patch and Debian userland. This does not make Windows-native tests identical to container tests. |
| Host Node 24 versus the frontend build's Node 22 | `frontend/Dockerfile:3`: `FROM node:22.23.3-alpine3.24`; `:7`: `RUN npm ci` | Pins build runtime and installs the lockfile dependency graph. Host npm state does not enter the runtime image. |
| Whatever database version is installed locally versus the cluster database | `k8s/base/postgres.yaml:48`: `image: postgres:16.10-alpine` | The cluster uses PostgreSQL 16.10. The PVC persists its data separately from container replacement. |

These are version tags, not a claim that upstream tags can never move. The new project shell
also provides Node 22/Python 3.12 locally, but the container definitions remain the shared baseline.

## 2. Our CI/CD maturity and the next step

Demonstrated today: continuous integration with automated lint/type checks, tests, image scans,
manifest validation and Compose integration (`.github/workflows/ci.yml:35` onward). Reviewed
feature changes reach dev through PRs. Continuous delivery/deployment automation is implemented:
`.github/workflows/cd.yml:13` calls the full CI suite, `:17` gates publishing on it, and `:76` gates the disposable
Kubernetes deployment on publishing. The [first main CD run](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36228513110)
passed the full test gate, published both images and generated both Syft SBOMs. Deployment
then failed while waiting for a completed ingress admission Job that upstream immediately
deletes (`ttlSecondsAfterFinished: 0`). After the reviewed fix reached main as `8074879`,
[CD run 36230267941](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941)
succeeded: full tests, GHCR publication, both Syft SBOMs, loading published digests under SHA
tags, Secret creation, Kubernetes rollout and real ingress smoke. The first failure remains
part of the record; the corrected run now demonstrates end-to-end delivery.

Our demonstrated level is CI plus automatic deployment of identifiable artifacts to the
ephemeral cluster, including rollout and ingress checks. The next operational step is a persistent
staging/production environment with observable promotion and recovery would provide ongoing
service operation. We do not claim unattended production operation from a cluster deleted at
job completion. The exact lecture taxonomy is not needed under the recorded instructor answer.

## 3. Build once, deploy the same bytes

`.github/workflows/cd.yml:116` pulls the backend **by the build job's digest**; `:117` gives those
bytes the source-SHA tag, and `:120` loads that existing image into kind. The deployment job has
no image build step. This binds the deployment to the published output instead of rebuilding
from a tag whose dependencies or base image could change. CI also builds verification images;
we do not claim the pipeline performs only one build in total.

For the frontend, `frontend/nginx.conf:27` proxies `/api/` to `http://backend:8000`. It keeps
browser requests relative to the current origin, so deploying the same frontend image to a
new host does not bake a different backend URL into its JavaScript. Without that choice the
image could work locally while sending a deployed browser to a laptop-specific address.

## 4. Correctness of probabilistic triage

Correctness means a validated category/priority/one-line summary within the domain contract,
a bounded failure path and durable complaint handling; it does not mean identical prose from
a live model on every call. `backend/app/services/triage.py:115` revalidates provider results;
`:108` bounds a call with a timeout; `:96` limits retry; `:79` uses validated rules fallback.
The service records who triaged the complaint and does not let arbitrary model fields bypass
its schema. Schema validity alone does not establish semantic quality: the hosted/offline
comparison below is still pending.

CI's backend job sets `TRIAGE_PROVIDER: simulated` (`.github/workflows/ci.yml:82`), while its
Compose integration selects rules (`:317`, locate the `TRIAGE_PROVIDER=rules` substitution).
Remote-provider tests use controlled HTTP replies (`backend/tests/test_remote_triage.py:56`),
and service tests exercise timeout/malformed/retry/fallback behavior without a live quota or
network response. Therefore changing hosted output does not make the correctness gate random.

## 5. Measured HPA lag

The configured load begins rising at 20 seconds; the baseline first samples desired replicas
of 3 at 52.53 seconds and a third Ready backend at 57.77 seconds, about **38 seconds** of
capacity lag. HPA's current-replica field reaches 3 at 68.26 seconds, about **48 seconds** after
the load step, with a five-second sampling interval and roughly one-second startup uncertainty.
Metrics collection, the HPA control loop, pod creation and readiness contribute to the lag;
this capture does not isolate their individual durations. Faster collection/control loops
could reduce part of the delay at a control-plane cost, while adequate minimum replicas avoid
relying on reactive scaling for immediate demand.

Sources: `docs/evidence/k8s-load-baseline50/samples.jsonl`, `hpa-watch.txt`, and the chart in
[evidence/k8s-load-README.md](evidence/k8s-load-README.md). Both complete runs made 9,559
requests with zero failed requests/dropped iterations. The adjusted run's desired count
stayed at 2 after applying the recorded VPA Target, 182m/250Mi; this is denominator behavior,
not evidence of a latency improvement.

## 6. Why VPA is Off

`k8s/base/vpa.yaml:13` sets `updateMode: "Off"`; `k8s/base/hpa.yaml:20` targets CPU utilization of
60 percent. CPU utilization is usage divided by requested CPU. If VPA automatically raises
that denominator, HPA may remove replicas; each remaining pod then takes more work, and VPA
may raise requests again. Off keeps recommendations observable while a reviewed request
change controls the denominator and HPA controls replica count. Our baseline and adjusted
captures demonstrate the denominator effect; they do not demonstrate an actual oscillation.
The baseline VPA's broad upper bound is a short-window recommendation, not production capacity.

## 7. Hosted-model caller placement

`compose.yaml:96` attaches the backend to **edge and internal**. The database (`:18`) and Redis
(`:38`) are internal-only, while the frontend (`:121`) is edge-only. `:186` marks internal as
`internal: true`. The backend therefore reaches database/cache by service DNS and can use
edge egress for a hosted LLM; the data services themselves do not need Internet access.
The real frontend isolation test failed to resolve `database`, as expected. Ollama's serving
container stays internal-only (`:143`), with a separate edge-only one-shot model downloader
(`:172`) sharing the model volume. No database port is published in production Compose.

## 8. The failure: waiting for a setup Job that no longer exists

**Symptoms.** The [first real main CD run, 36228513110](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36228513110)
passed every test job, published both GHCR images and emitted both Syft SBOMs. Its
`deploy-k8s` job then failed before application deployment, even though the ingress
controller had successfully rolled out. This is an actual project failure, not a simulated
incident or a claim that publication proved deployment.

**Faulty assumption encoded in our implementation.** In source `34e8402`,
`.github/workflows/cd.yml:112` waited for the completed `ingress-nginx-admission-patch` Job.
That command assumed the Job would remain queryable after it finished. This describes the
assumption in the AI-assisted implementation; it is not an invented personal recollection
by either student.

**Diagnostic evidence.** `gh run view 36228513110 --log-failed` showed, at
`2026-09-26T08:05:26.2875334Z`:

```text
Error from server (NotFound): jobs.batch "ingress-nginx-admission-patch" not found
```

Inspection of the pinned [ingress-nginx v1.15.1 kind manifest](https://github.com/kubernetes/ingress-nginx/blob/controller-v1.15.1/deploy/static/provider/kind/deploy.yaml#L632)
showed `ttlSecondsAfterFinished: 0`: the completed admission Job is eligible for immediate
deletion. Waiting on that temporary object races garbage collection. Controller availability
alone had not made this extra Job lookup safe.

**Correction and verification.** [PR #97](https://github.com/TahaSohail-Goat/Assignment1_SCD/pull/97)
changes the wait to the lasting result of the Job:

```text
kubectl wait --for=jsonpath='{.webhooks[0].clientConfig.caBundle}' validatingwebhookconfiguration/ingress-nginx-admission --timeout=120s
```

On the local kind cluster the setup Job was absent while this replacement wait succeeded.
`backend/tests/test_cd_workflows.py` adds a regression check against returning to the old
Job wait. Taha approved the fix, all ten CI checks passed, and it was merged into dev.
Promotion PR #98 is merged as main commit `8074879`. The corrected
[CD run 36230267941](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36230267941)
succeeded through deployment and the real ingress smoke test; rerunning the old SHA would
preserve the failure. The lesson is to test persistent readiness state, rather
than assuming a short-lived installer object survives long enough to inspect.

**Duration limit.** The diagnostic record supports this failure and its correction, but does
not establish more than one hour of active troubleshooting. We therefore do not claim the
assignment's >1-hour condition is met. ASG-DOC-024 remains partial unless a contributor can
provide a genuine qualifying duration/incident; elapsed waiting between sessions is not
silently counted as debugging time.

## Data, cache and persistence decisions collected from earlier packages

- Migration `backend/alembic/versions/0001_create_complaints.py:90` creates `(status, priority)`
  for the combined filter (or the leading status column). `:91` creates `created_at` for
  newest-first retrieval. These support the queries in `docs/DATA_MODEL.md:44`; the optimizer
  may still choose a sequential scan on a small table. No unmeasured speedup is claimed.
- `backend/app/services/stats.py:30` sets the 30-second TTL; `:62` provides invalidation after
  complaint commit. Invalidation makes ordinary writes visible promptly; TTL bounds stale
  entries after a missed invalidation or a reader/writer race. Deleting before commit could
  allow a reader to refill from the old database state.
- [PostgreSQL pod replacement](evidence/k8s-pg-persistence.txt): 30 rows before and after,
  identical full-row ordered fingerprint; new pod UID, same PVC UID. This tests pod
  replacement, not deletion of the PVC or a backup/restore disaster.
- [Rollback evidence index](evidence/k8s-rollback-index.md) and
  [zero-downtime evidence index](evidence/k8s-zero-downtime-index.md) identify the original
  captures without treating copied files as additional experiments. Required video is pending.

## Hosted provider evidence (issue #45, 2026-09-25)

The chosen Groq model is `openai/gpt-oss-20b` in `backend/app/providers/triage/llm.py`. Groq's [rate-limit table](https://console.groq.com/docs/rate-limits) listed 30 requests/minute, 1,000 requests/day, 8,000 tokens/minute and 200,000 tokens/day on its free plan when checked on 2026-09-25. Its [structured-output guide](https://console.groq.com/docs/structured-outputs) lists this model for strict JSON-schema output. These are published limits, not a measurement against an Artfever account; a live quota check and hosted call are still pending. `docs/AI.md` records the data-control and Ollama sources as well.

The offline model is `gemma3:1b` in `backend/app/providers/triage/ollama.py`. No hosted-versus-Ollama latency or quality comparison has been run. When both services are available, use the same synthetic complaint set, record each category/priority and elapsed time, and report the actual values here.
## Redis volume decision (issue #43)

`compose.yaml` enables Redis AOF and mounts `redisdata` at `/data`. The stats and triage cache values can be rebuilt, but rebuilding them immediately after a restart adds database and provider load. The rate-limit counters matter more: losing them grants each caller a fresh allowance and can produce a burst against the hosted model. AOF with `appendfsync everysec` preserves recent counters across ordinary restarts, with up to roughly one second of acknowledged writes still at risk on a crash. The counter implementation and exact admission behavior are documented in `docs/CACHE.md` Job 2.

# API Design

Answers the 18 design questions (`DQ-API-01…18`) of [`frs/api.md`](frs/api.md) and the open `triaged_by` decision, so that the backend, the typed client and the tests can be written without guessing. Source of truth for behaviour is [`docx/ASSIGNMENT.md`](../docx/ASSIGNMENT.md); this document adds **design decisions only where the assignment is silent**, and says so.

Every answer is marked **Fixed** (the assignment states it, with the clause) or **Decision** (this document decides it, and why). Where an answer is a number the assignment does not give, it is a configurable default, not a requirement.

## 1. One error model and one list envelope

**Error body (all error statuses)** — `DQ-API-01`, `DQ-API-02`. **Decision.**

```json
{
  "error": {
    "code": "validation_error",
    "message": "Human-readable summary",
    "details": [ { "field": "text", "message": "must be between 10 and 2000 characters" } ]
  }
}
```

| Status | `error.code` | `error.message` | `error.details` |
|---|---|---|---|
| 400 | `validation_error` | "Invalid request" | one `{field, message}` per invalid field or parameter (**field-level body**, §2.2 p5) |
| 404 | `not_found` | "Complaint not found" | absent |
| 409 | `invalid_transition` | names the attempted transition, for example "Cannot change status from resolved to open" (§2.2 p6) | `[{"from": "resolved", "to": "open"}]` |
| 429 | `rate_limited` | "Too many requests; retry after N seconds" | absent; the `Retry-After` header carries N (§2.4 p8) |
| 503 | `not_ready` | names the failed dependency, for example "postgres is unreachable" (§2.2 p6) | `[{"dependency": "postgres", "message": "…"}]` for **every** failed dependency |

The frontend shows `error.message` verbatim for a 409 (`ASG-FR-010`). Validation failures use **400, not FastAPI's default 422** (§2.2 p5, §4 C p19 say 400): the framework's validation error handler is replaced so that body errors **and** query-parameter errors produce the 400 above.

**Envelope of a list** — `DQ-API-03`. **Decision.** `{ "items": [Complaint…], "total": <int>, "page": <int>, "page_size": <int> }`.

## 2. Answers to the design questions

| ID | Answer | Basis | Why |
|---|---|---|---|
| **DQ-API-01** Error bodies | The model in §1 | Fixed: "400 with a field-level error body", "409 naming the attempted transition", "503 naming the failed dependency" (§2.2 p5–6). Decision: the JSON shape | One shape for every status keeps the typed client and the tests simple |
| **DQ-API-02** 400 vs 422 | **400** everywhere validation fails: body, query parameters | Fixed: 400 (§2.2 p5; §4 C p19) | The framework default (422) would contradict the contract; the handler is remapped once, for all routes |
| **DQ-API-03** Pagination | `page` starts at **1**, default **1**; `page_size` default **20**, maximum **100**. Sort: `created_at` **descending** (newest first), ties broken by `id`. `total` = number of complaints matching the filters (not the size of the page). `page_size` above 100, or `page`/`page_size` below 1 → **400** (rejected, not clamped). A page beyond the last → 200 with `items: []` and the real `total` | Fixed: `page`, `page_size ≤ 100`, "return total" (§2.2 p6). Decision: the rest | Deterministic order so pages never repeat or skip; the `created_at` index (§2.3 p8) serves "newest first"; reject instead of clamp so a wrong client is told |
| **DQ-API-04** Filters | Query parameters `category`, `priority`, `status`, each optional and single-valued, combined with **AND**. An invalid enum value → **400** naming the parameter | Fixed: filter by category, priority, status (§2.2 p6). Decision: names and semantics | The Dashboard applies all three at once (§2.1 p4); the `(status, priority)` index (§2.3 p8) serves the filter |
| **DQ-API-05** Field names and the new id | JSON names equal the column names of §2.3. **Create request:** `text`, `location`, `reporter_contact` (optional). **201 body:** the stored complaint, same representation as `GET` (§3), so the id, category, priority, `ai_summary` and `triaged_by` are all there; the response also carries `Location: /api/complaints/{id}`. **PATCH request:** `{"status": "<status>"}` | Fixed: the column names (§2.3 p7–8) and what the Submit view shows (§2.1 p4). Decision: the JSON | The client learns the id from the body (and header), which is what "POST a complaint, GET it back" needs (§3.4 p17) |
| **DQ-API-06** Malformed id | `GET /api/complaints/{id}` with an id that is not a UUID → **404** `not_found` | Fixed: "200 / 404" only (§2.2 p5). Decision: a malformed id is treated as an id that does not exist | The contract has no other status for this route; no 400 branch to test or explain |
| **DQ-API-07** Stats body and invalidation | `{"total": n, "by_category": {"water": n, …}, "by_priority": {"high": n, …}}`, **every** enum value present with 0 when empty. The cache is invalidated when a complaint is **created**; a status change does **not** invalidate it | Fixed: aggregates by category and priority, Redis-cached, TTL 30 s, `X-Cache: HIT\|MISS`, "invalidate on write" (§2.2 p6, §2.4 p8). Decision: the shape, and "write" = create | Counts by category and priority do not change when only a status changes. If a `by_status` count were ever added, the PATCH would have to invalidate too |
| **DQ-API-08** Recent triage outcomes | `GET /api/meta/providers` → `{"active_provider": "<TRIAGE_PROVIDER>", "recent": [ {"complaint_id", "provider", "latency_ms", "fallback": bool, "at"} … up to 20 ]}`, derived from the **`complaints` table** (newest 20: `triaged_by`, `triage_latency_ms`; `fallback` is `triaged_by == "rules:fallback"`) | Fixed: "which provider is active, and the last 20 triage outcomes (provider, latency ms, fallback y/n)" (§2.2 p6). Decision: the source and shape | With ≥ 2 replicas an in-memory list per pod would disagree; the table survives restarts and needs no extra store |
| **DQ-API-09** Rate limit | Fixed-window counter in Redis, key = client IP and window. Default **10 requests per 60 seconds** per IP, configurable (`RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW_SECONDS`). Only `POST /api/complaints` is limited. Client IP: the socket peer, or the **first** `X-Forwarded-For` entry when `TRUST_FORWARDED_FOR=true` (set behind the Ingress). `Retry-After` = seconds to the end of the window | Fixed: Redis-backed, keyed by client IP, 429 with `Retry-After`, protects `POST /api/complaints` (§2.4 p8). Decision: the numbers, the window type, the IP source | The assignment gives no threshold, only "tens of requests per minute" for the free LLM tier (§2.4 p8); 10 per minute stays well under it. A fixed window is the simplest of the two allowed designs and is testable with a clock |
| **DQ-API-10** Order of checks | 1) rate limit, 2) validation, 3) triage-cache lookup and triage, 4) persist, 5) invalidate stats | Fixed: "Validate → triage → persist", protected by the limiter (§2.2 p5, §2.4 p8). Decision: limiter first | The limiter is the cheapest check and protects the LLM quota; a client sending garbage still counts, which is what a limiter is for |
| **DQ-API-11** Health and readiness | `GET /health` → **200** `{"status": "ok"}`; it checks **nothing external** (neither PostgreSQL nor Redis). `GET /ready` → **200** `{"status": "ready", "checks": {"postgres": "ok", "redis": "ok"}}`, else **503** with the §1 error naming every failed dependency. Each dependency check has a **1 second** timeout and the two run concurrently | Fixed: `/health` "must not touch the database"; `/ready` "200 only if Postgres and Redis are both reachable; 503 naming the failed dependency" (§2.2 p6) | Liveness that depends on a dependency turns a slow database into a restart loop (§2.2 p6). Concurrent 1-second checks answer within a probe timeout; the manifests set `timeoutSeconds` to match (Phase 09) |
| **DQ-API-12** Metrics | Prometheus text. Counter `http_requests_total{method,route,status}`; histogram `http_request_duration_seconds{method,route}` (buckets 0.005 … 10); histogram `triage_duration_seconds{provider}` (buckets 0.05 … 30); counter `triage_fallback_total{provider,error_class}`; counter `triage_cache_total{result="hit\|miss"}`; counter `stats_cache_total{result="hit\|miss"}`; counter `rate_limited_total`. `route` is the **route template** (`/api/complaints/{id}`), never the raw path | Fixed: request count, request latency histogram, triage latency, fallback counter (§2.2 p6). Decision: names, labels, buckets, and the two cache counters | The template keeps label cardinality bounded; the cache counters give the measured hit rate the assignment asks for (`ASG-AI-017`); the triage buckets reach past the 10 s timeout plus one retry |
| **DQ-API-13** `X-Request-ID` | An incoming value is accepted if it matches `[A-Za-z0-9._-]{1,64}`; otherwise a UUID4 is generated. The value is **always echoed** in the response header `X-Request-ID` and carried by every log line | Fixed: "propagated from an X-Request-ID header (generate one if absent)", every log line carries it (§2.2 p7). Decision: validation, format, echo | A client can correlate its request with the logs; an arbitrary long or hostile value never reaches the logs |
| **DQ-API-14** Latency and confidence | `triage_latency_ms` is the **measured wall-clock time of the whole triage step** (cache lookup, provider calls, the retry, and the rule-based fallback if used). On a cache hit it is the time of the lookup. `confidence` is **not stored and not returned** | Fixed: `triage_latency_ms integer` (§2.3 p8); `TriageResult.confidence` (§2.5 p9); no `confidence` column in the minimum schema. Decision: the semantics | The latency then shows what the citizen waited, including failures; the schema stays the minimum one |
| **DQ-API-15** Redis down at request time | The limiter **fails open** (the request is admitted), the triage cache is skipped (a miss), `/api/stats` is computed from PostgreSQL and answered with `X-Cache: MISS`; each case logs one WARNING with the request id. `/ready` reports 503 naming `redis` | Fixed: `/ready` must fail when Redis is unreachable (§2.2 p6). Decision: fail open for the rest | The cache and the limiter are optimizations and protections, not the source of truth; a Redis outage must not stop citizens from reporting. In Kubernetes the failing readiness probe removes the pod anyway |
| **DQ-API-16** PATCH to the same status, unknown status | The same status (for example `open` → `open`) → **409** `invalid_transition` (it is not one of the four allowed transitions). A value that is not one of `open`, `in_progress`, `resolved`, `rejected` → **400** `validation_error` | Fixed: "Everything else is 409" (§2.2 p6) for transitions. Decision: an unknown value is invalid input, not a transition | A 409 names an attempted transition; an unknown status has none |
| **DQ-API-17** PATCH success | **200** with the updated complaint (the same representation as `GET`) | Decision (the assignment only specifies the 409 case) | The Dashboard and the typed client get the new state without a second request |
| **DQ-API-18** PATCH on an unknown id | **404** `not_found` (a malformed id too, as in DQ-API-06) | Decision, consistent with `GET` (§2.2 p5) | One rule for ids on both routes |

## 3. Shapes for the typed client (`ASG-FR-013`)

| Schema | Fields |
|---|---|
| `ComplaintCreate` | `text` (string, 10–2000), `location` (string, 3–200), `reporter_contact` (string or null, optional) |
| `Complaint` | `id` (UUID), `text`, `location`, `reporter_contact` (string or null), `category` (`water`, `electricity`, `sanitation`, `roads`, `streetlights`, `other`), `priority` (`high`, `normal`, `low`), `status` (`open`, `in_progress`, `resolved`, `rejected`), `ai_summary` (string or null, ≤ 140), `triaged_by` (§4), `triage_latency_ms` (integer), `created_at`, `updated_at` (ISO 8601, UTC) |
| `StatusUpdate` | `status` (the four statuses) |
| `ComplaintPage` | `items` (`Complaint[]`), `total`, `page`, `page_size` |
| `Stats` | `total`, `by_category` (object with the six categories), `by_priority` (object with the three priorities) |
| `ProvidersMeta` | `active_provider` (string), `recent` (up to 20 × `{complaint_id, provider, latency_ms, fallback, at}`) |
| `Health` / `Ready` | `{"status": "ok"}` / `{"status": "ready", "checks": {"postgres", "redis"}}` |
| `Error` | the model of §1 |

Field lengths and enums are those of §2.3 (p7–8). The list endpoint takes `category`, `priority`, `status`, `page`, `page_size`.

## 4. `triaged_by` values and the seed command

**`triaged_by`** (`ASG-DATA-013`; previously an open question). **Fixed:** the four values `llm:groq`, `llm:ollama`, `rules`, `rules:fallback` (§2.3 p7) must all be accepted. **Decision:** the column is text with a `CHECK` that also allows `simulated` (the `SimulatedTriage` used in CI) and `llm:<provider>` for any other hosted provider the team documents (for example `llm:gemini`). The frontend shows the value as returned.

**Seed command** (`ASG-DATA-019`). **Decision:** `python -m app.seed` (module `backend/app/seed.py`), run after the migrations. It is idempotent: each seed complaint has a **deterministic UUID** derived from its text, and rows are inserted with `ON CONFLICT (id) DO NOTHING`, so running it twice adds nothing (§2.3 p8). The seed content (at least 30 realistic complaints across the categories) is the work of issue #41; how Compose and Kubernetes run it (a one-shot service and a Job) is decided in Phases 08 and 09.

## 5. What the frontend owner should confirm

The shapes work for the Submit view (needs `category`, `priority`, `ai_summary`, `triaged_by` from the 201 body, and the 400 `details`) and the Dashboard (needs `items`, `total`, `page`, `page_size`, the filters, and `error.message` of a 409). These answers also settle the frontend design questions `DQ-FE-03` (defaults and page size), `DQ-FE-04` (where the 409 message and the field errors sit) and, with `X-Cache` sent by the same origin behind the nginx proxy, part of `DQ-FE-10`.

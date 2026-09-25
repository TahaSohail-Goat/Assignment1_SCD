# Functional Requirements — API and Domain Rules (`ASG-FR-020…037`)

Catalog for the nine backend operations and the domain rules behind them. Index, rules and entry template: [`../FRs.md`](../FRs.md). Source: [`docx/ASSIGNMENT.md`](../../docx/ASSIGNMENT.md) §2.2 (p5–7), §2.3–2.5 where they constrain the API, rubric part C. Product context: [`../PRD.md`](../PRD.md).

**Contract (owner decision, confirmed by the instructor: no tenth endpoint): nine operations.**

| # | Operation | Entry |
|---|---|---|
| 1 | `POST /api/complaints` | FR-020 · FR-021 · FR-022 |
| 2 | `GET /api/complaints/{id}` | FR-023 |
| 3 | `GET /api/complaints` | FR-024 · FR-025 · FR-026 |
| 4 | `PATCH /api/complaints/{id}/status` | FR-027 · FR-028 · FR-034 · FR-035 |
| 5 | `GET /api/stats` | FR-029 |
| 6 | `GET /api/meta/providers` | FR-030 |
| 7 | `GET /health` | FR-031 |
| 8 | `GET /ready` | FR-032 |
| 9 | `GET /metrics` | FR-033 |

Cross-cutting: FR-036 (all nine to contract) and FR-037 (end-to-end flow). Where the assignment does not fix a detail, the entry says so and points to a **DQ-API-nn** row in [*Design questions*](#design-questions-for-phase-02) at the end. Behaviour owned by other requirement families (rate limiting, caching, triage, schema, logging) is referenced by ID, not repeated.

---

### ASG-FR-020 — Create a complaint

- **Source:** §2.2 p5 (API contract, row 1); §2.5 p11–12 (triage contract); §1.2 p2.
- **Actor:** Citizen, through the Submit view.
- **Precondition:** The backend is running; `TRIAGE_PROVIDER` selects a provider; `RuleBasedTriage` is always available as fallback; PostgreSQL is reachable.
- **Trigger:** `POST /api/complaints` with the complaint text, the location and, optionally, a contact (field names: DQ-API-05).
- **Main flow:**
  1. The rate limiter admits the request (FR-022).
  2. The input is validated (FR-021).
  3. Triage runs **synchronously**: content-hash cache lookup, else the selected provider with a 10 s timeout and one jittered retry on timeout/429/5xx, then validation of the provider output against `TriageResult` (`ASG-AI-010…016`).
  4. The complaint is persisted with a server-generated UUID, status `open`, `triaged_by`, `ai_summary`, `triage_latency_ms` and UTC timestamps (`ASG-DATA-005…015`).
  5. The stats cache is invalidated (`ASG-CACHE-005`).
  6. The API answers **201**. The body carries what the Submit view must show: the category, priority, AI summary and the producing provider (`ASG-FR-006`, §2.1 p4). The rest of the body, and how the client learns the new complaint's id, are not specified (DQ-API-05).
- **Alternate / failure flows:**
  - Invalid input → FR-021 (400).
  - Limit exceeded → FR-022 (429).
  - Provider raises, times out, is rate-limited (429), returns 5xx or returns malformed output → `RuleBasedTriage` decides, `triaged_by = "rules:fallback"`, one WARNING is logged (`ASG-NFR-011`), and the answer is **still 201** — the user never sees a 500 because a third party failed (`ASG-AI-015`).
  - The same text was triaged before → the cached result is used and the provider is not called (`ASG-AI-016`); the complaint is still stored as its own row.
- **Postcondition:** Exactly one new row exists with `status = open`; the next `GET /api/stats` includes it; every field the response does carry equals the stored value.
- **Acceptance criteria:**
  - AC-1: A valid body → 201, and the body carries the category, priority, AI summary and the producing provider (what §2.1 p4 says the Submit view shows). The other fields of the body, including how the client learns the new complaint's id, are DQ-API-05.
  - AC-2: The stored row has `status = open` and `created_at`/`updated_at` in UTC.
  - AC-3: With a provider that **always raises**, the request → 201 and `triaged_by == "rules:fallback"` (the test the assignment says to write "if you write no other", `ASG-AI-022`).
  - AC-4: After a successful POST, the next stats read is a cache MISS and counts the new complaint (`ASG-CACHE-005`).
  - AC-5: Posting the same text twice creates two rows and calls the provider once (`ASG-AI-016`).
  - AC-6: A client that has just created a complaint can retrieve **that** complaint afterwards — the CI integration job is "POST a complaint, GET it back, assert the category" (§3.4 p17, `ASG-CICD-010`). The mechanism by which the client learns the id (a body field, a header, or the list) is DQ-API-05.
- **Test mapping:** `IT` create valid; `IT` always-raising provider → 201 + `rules:fallback`; `IT` duplicate text → one provider call, two rows; `IT` POST then stats → MISS with new count.
- **Evidence mapping:** pytest report (CI artifact); curl/`http` capture of one 201 in `docs/evidence/`; matrix row `ASG-FR-020`.

### ASG-FR-021 — Reject invalid input with 400 and field-level errors

- **Source:** §2.2 p5 (row 1); §2.3 p7 (length limits); §4 C p19 ("field-level validation errors").
- **Actor:** Citizen (through the Submit view or any HTTP client).
- **Precondition:** As FR-020.
- **Trigger:** `POST /api/complaints` whose body violates the rules the assignment states: `text` 10–2000 characters, `location` 3–200 characters, the contact optional (`ASG-DATA-006…008`).
- **Main flow:**
  1. The body is validated before triage or persistence.
  2. Invalid → **400** with an error body that identifies each offending field.
  3. Nothing is triaged, stored or cached.
- **Alternate / failure flows:**
  - Several fields invalid at once → all offending fields are identified in the same response.
  - A required field missing → treated as invalid for that field.
- **Postcondition:** No row is created; the provider is not called.
- **Acceptance criteria:**
  - AC-1: `text` of 9 characters → 400 naming `text`; 10 characters → accepted.
  - AC-2: `text` of 2001 characters → 400 naming `text`; 2000 characters → accepted.
  - AC-3: `location` of 2 characters → 400 naming `location`; 3 and 200 characters → accepted; 201 → 400.
  - AC-4: A body with an invalid `text` **and** an invalid `location` → one 400 that names both.
  - AC-5: The status code is **400**, not the framework default (see DQ-API-02).
  - AC-6: The database also enforces the `text` length (`ASG-DATA-006`): inserting a 9-character text directly fails.
- **Test mapping:** `UT` validation boundaries (9/10, 2000/2001, 2/3, 200/201); `IT` 400 status and field names; `IT` DB constraint rejects a direct insert.
- **Evidence mapping:** pytest report; matrix row `ASG-FR-021`.

### ASG-FR-022 — Answer 429 with Retry-After when the rate limit is exceeded

- **Source:** §2.2 p5 (row 1); §2.4 p8 (Job 2).
- **Actor:** Citizen or any client calling `POST /api/complaints` repeatedly.
- **Precondition:** Redis is reachable; the limiter counter is keyed by client IP and lives in Redis, shared by all backend replicas (`ASG-CACHE-007…010`).
- **Trigger:** More `POST /api/complaints` requests from one client IP than the configured limit within the window (limit and window: DQ-API-09).
- **Main flow:**
  1. Each POST increments the client's counter.
  2. Over the limit → **429** with a `Retry-After` header; the request is not triaged or stored.
- **Alternate / failure flows:**
  - Window elapses → requests are admitted again.
  - Two backend replicas → they share one counter (no "four pods, four times the traffic").
- **Postcondition:** The rejected request left no row and did not call the provider.
- **Acceptance criteria:**
  - AC-1: The request after the limit → 429 with a `Retry-After` header holding a positive number of seconds.
  - AC-2: After the window, the same client is admitted again.
  - AC-3: With two backend instances behind one Redis, requests split across both still hit the same limit.
  - AC-4: The limiter protects `POST /api/complaints` (§2.4 p8). Whether any other endpoint is limited is not specified (DQ-API-09).
- **Test mapping:** `IT` limit → 429 + header; `IT` window reset; `IT` two app instances, one Redis; `DEMO` the 429 capture.
- **Evidence mapping:** curl capture of the 429 and header in `docs/evidence/`; matrix rows `ASG-FR-022`, `ASG-CACHE-009`.

### ASG-FR-023 — Retrieve one complaint

- **Source:** §2.2 p5 (row 2).
- **Actor:** Operator or client.
- **Precondition:** The complaint may or may not exist.
- **Trigger:** `GET /api/complaints/{id}`.
- **Main flow:** Existing id → **200** with the complaint. Unknown id → **404**.
- **Alternate / failure flows:** An id that is not a valid UUID → not specified (DQ-API-06).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: The id of an existing complaint (for example one just created through FR-020 and identified as decided in DQ-API-05, or found in the list of FR-024) → 200 and the stored values.
  - AC-2: A well-formed id that does not exist → 404.
- **Test mapping:** `IT` create then get (id obtained as decided in DQ-API-05); `IT` unknown id → 404.
- **Evidence mapping:** pytest report; matrix row `ASG-FR-023`.

### ASG-FR-024 — Filter the complaint list

- **Source:** §2.2 p6 (row 3); §2.1 p4 (Dashboard filters).
- **Actor:** Operator, through the Dashboard.
- **Precondition:** Complaints exist.
- **Trigger:** `GET /api/complaints` with any of `category`, `priority`, `status` (parameter names and value handling: DQ-API-04).
- **Main flow:** Only complaints matching the given filters are returned.
- **Alternate / failure flows:** No filter → all complaints. The Dashboard offers all three filters at once (§2.1 p4), so filters must be usable **together**; an invalid enum value → not specified (DQ-API-04).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: `category=water` returns only water complaints.
  - AC-2: `priority=high`, `status=open` each filter correctly.
  - AC-3: Two or three filters together return only complaints matching all of them.
  - AC-4: A filter that matches nothing → an empty page with total 0, not an error.
- **Test mapping:** `IT` each filter alone; `IT` combined filters; `IT` no match. The seeded data set (`ASG-DATA-019…021`) gives a realistic fixture.
- **Evidence mapping:** pytest report; matrix row `ASG-FR-024`.

### ASG-FR-025 — Paginate the complaint list

- **Source:** §2.2 p6 (row 3): "paginate (page, page_size ≤ 100)".
- **Actor:** Operator, through the Dashboard.
- **Precondition:** More complaints exist than fit on one page.
- **Trigger:** `GET /api/complaints` with `page` and `page_size`.
- **Main flow:** The response contains only the requested page; `page_size` never exceeds **100**.
- **Alternate / failure flows:** `page_size` above 100 → not specified whether it is rejected or clamped (DQ-API-03); defaults and the first page number are not specified (DQ-API-03).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: With 30 seeded complaints and `page_size=10`, three pages of 10 are returned without overlap.
  - AC-2: A page beyond the last returns an empty page, not an error.
  - AC-3: `page_size=100` is accepted; a request for more than 100 items never returns more than 100.
  - AC-4: The order of items is deterministic between requests so pages do not repeat or skip items (which order: DQ-API-03).
- **Test mapping:** `IT` page walk over the seed data; `IT` page_size boundary (100 / 101).
- **Evidence mapping:** pytest report; matrix row `ASG-FR-025`.

### ASG-FR-026 — Return the total

- **Source:** §2.2 p6 (row 3): "return total".
- **Actor:** Operator, through the Dashboard (page controls need it).
- **Precondition:** As FR-025.
- **Trigger:** Every `GET /api/complaints`.
- **Main flow:** The response includes `total`. The assignment does not say whether it counts all complaints or only those matching the filters; the Dashboard's pagination needs the count of the **matching** set (DQ-API-03).
- **Alternate / failure flows:** No matches → total 0.
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: With 30 complaints and no filter, `total` is 30 regardless of `page` and `page_size`.
  - AC-2: With a filter matching 7 complaints, the returned `total` is consistent with the filtered set (7) once DQ-API-03 is settled.
- **Test mapping:** `IT` total with and without filters.
- **Evidence mapping:** pytest report; matrix row `ASG-FR-026`.

### ASG-FR-027 — Change a complaint's status under the state machine

- **Source:** §2.2 p6 (row 4, Domain rules).
- **Actor:** Operator, through the Dashboard.
- **Precondition:** The complaint exists and has a current status.
- **Trigger:** `PATCH /api/complaints/{id}/status` with the requested new status (body shape: DQ-API-05).
- **Main flow:**
  1. The current and requested status are looked up in the transition table (FR-034/035).
  2. Allowed → the status is updated and `updated_at` is set (the `created_at / updated_at` columns, §2.3 p8); the request succeeds. The assignment states **no success status code and no response body** for this operation (DQ-API-17).
  3. Not allowed → FR-028.
- **Alternate / failure flows:** Unknown id → **not specified for this operation**: §2.2 p5 states 404 only for `GET /api/complaints/{id}` (DQ-API-18). A requested status that is not one of the four → not specified (DQ-API-16).
- **Postcondition:** On success the stored status equals the requested one.
- **Acceptance criteria:**
  - AC-1: `open → in_progress` succeeds, and a following `GET /api/complaints/{id}` shows `in_progress` (the exact success code and body: DQ-API-17).
  - AC-2: `in_progress → resolved` succeeds and a following GET shows `resolved`.
  - AC-3: `open → rejected` and `in_progress → rejected` succeed and a following GET shows `rejected`.
  - AC-4: Every other pair → 409 (FR-028) and the stored status is unchanged.
  - AC-5: `updated_at` changes on success and does not on a rejected transition.
- **Test mapping:** `IT` each allowed transition; `UT` parametrised over all 16 pairs (FR-034).
- **Evidence mapping:** pytest report; matrix row `ASG-FR-027`.

### ASG-FR-028 — Answer 409 naming the attempted transition

- **Source:** §2.2 p6 (row 4); §2.1 p4 (the UI must show "the server's 409 message, not a generic 'error'").
- **Actor:** Operator.
- **Precondition:** A transition not allowed by FR-034 is requested.
- **Trigger:** `PATCH /api/complaints/{id}/status` with a forbidden transition.
- **Main flow:** The API answers **409**; the message **names the attempted transition** (from-status and to-status). The status is not changed.
- **Alternate / failure flows:** Terminal source (`resolved`/`rejected`) → always 409. Same-status request (for example `open → open`) → "everything else is 409" (DQ-API-16).
- **Postcondition:** The complaint is unchanged.
- **Acceptance criteria:**
  - AC-1: `resolved → open` → 409 and the message contains both `resolved` and `open`.
  - AC-2: `open → resolved` → 409 and the message contains both.
  - AC-3: The message is a single human-readable string the frontend can display verbatim (`ASG-FR-010`); its exact format is DQ-API-01.
  - AC-4: After any 409 the stored status and `updated_at` are unchanged.
- **Test mapping:** `UT` message content for representative pairs; `IT` 409 status and unchanged row.
- **Evidence mapping:** pytest report; screenshot of the Dashboard showing the verbatim message (frontend evidence); matrix row `ASG-FR-028`.

### ASG-FR-029 — Aggregate statistics, cached

- **Source:** §2.2 p6 (row 5); §2.4 p8 (Job 1); §2.1 p4 (Stats view).
- **Actor:** Operator, through the Stats view.
- **Precondition:** Redis and PostgreSQL are reachable.
- **Trigger:** `GET /api/stats`.
- **Main flow:** The response holds aggregate counts by category and priority. It is a **read-through cache** in Redis with a 30 s TTL and reports `X-Cache: HIT` or `MISS`; a new complaint invalidates it (`ASG-CACHE-002…005`).
- **Alternate / failure flows:** Cache empty or expired → MISS, the aggregate is computed and stored. The shape of the body and whether status changes must also invalidate it → DQ-API-07.
- **Postcondition:** The cache holds a fresh aggregate for up to 30 s unless invalidated.
- **Acceptance criteria:**
  - AC-1: First call → `X-Cache: MISS`; an immediate second call → `X-Cache: HIT` with identical body.
  - AC-2: After `POST /api/complaints`, the next call → MISS and the counts include the new complaint.
  - AC-3: After the TTL (30 s) has elapsed without writes → MISS again.
  - AC-4: The counts equal the counts computed directly from the table.
- **Test mapping:** `IT` MISS→HIT; `IT` invalidation on write; `IT` TTL expiry (using an injected clock or a shortened TTL — never `time.sleep()`, `ASG-NFR-015`); `CI` the compose integration job asserts MISS→HIT (`ASG-CICD-010`).
- **Evidence mapping:** curl capture of MISS then HIT in `docs/evidence/`; matrix rows `ASG-FR-029`, `ASG-CACHE-002…005`.

### ASG-FR-030 — Provider metadata and recent triage outcomes

- **Source:** §2.2 p6 (row 6): "Which triage provider is active, and the last 20 triage outcomes (provider, latency ms, fallback y/n). This is your observability surface."; §4 F p20.
- **Actor:** Operator or reviewer.
- **Precondition:** A provider is configured; some triage may have happened.
- **Trigger:** `GET /api/meta/providers`.
- **Main flow:** The response names the **active provider** and lists the **last 20 triage outcomes**, each with provider, latency in ms and whether it was a fallback.
- **Alternate / failure flows:** Fewer than 20 outcomes → all of them. None yet → an empty list. Where the outcomes are stored (they must be consistent across replicas) → DQ-API-08.
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: After 25 triaged complaints the list has exactly 20 entries, the most recent ones.
  - AC-2: A fallback triage appears with fallback = yes and provider identifying the rules fallback.
  - AC-3: Each entry's latency equals the `triage_latency_ms` recorded for that complaint (`ASG-AI-023`).
  - AC-4: The active provider matches `TRIAGE_PROVIDER`.
- **Test mapping:** `IT` 25 posts → 20 entries; `IT` fallback entry; `UT` mapping of stored values to the response.
- **Evidence mapping:** capture of the response with a fallback entry; matrix rows `ASG-FR-030`, `ASG-AI-023`.

### ASG-FR-031 — Liveness (`/health`)

- **Source:** §2.2 p6 (row 7) and p6 text on probes; §3.3 p15.
- **Actor:** Platform probe (Kubernetes startup and liveness probes, Compose healthcheck).
- **Precondition:** The process is running.
- **Trigger:** `GET /health`.
- **Main flow:** Answers successfully while the process is alive (§2.2 p6: "Liveness. Process is alive."; the exact success code is not stated for this endpoint, DQ-API-11 — a Kubernetes `httpGet` probe treats 200–399 as success). It **must not touch the database**.
- **Alternate / failure flows:** PostgreSQL down → `/health` still answers successfully. Process hung → the probe times out and Kubernetes restarts the pod. Whether `/health` may check Redis is not specified (DQ-API-11).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: With PostgreSQL stopped, `GET /health` still answers with a success status.
  - AC-2: A test proves `/health` opens no database session (for example, the handler runs with a session factory that raises if called).
  - AC-3: The liveness and startup probes call `/health` (`ASG-K8S-016/017`).
- **Test mapping:** `UT` handler without a DB dependency; `IT` DB down → success status; `CI` manifest check for the probe paths.
- **Evidence mapping:** pytest report; matrix rows `ASG-FR-031`, `ASG-K8S-017`.

### ASG-FR-032 — Readiness (`/ready`)

- **Source:** §2.2 p6 (row 8) and probe text; §3.3 p15.
- **Actor:** Platform probe (Kubernetes readiness probe, Compose healthcheck, CI wait step).
- **Precondition:** The process is running.
- **Trigger:** `GET /ready`.
- **Main flow:** **200 only if PostgreSQL and Redis are both reachable.** Otherwise **503** naming the failed dependency.
- **Alternate / failure flows:** Only PostgreSQL down → 503 naming PostgreSQL. Only Redis down → 503 naming Redis. Both down → not specified which are named (DQ-API-11).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: Both dependencies up → 200.
  - AC-2: PostgreSQL down → 503 and the body names PostgreSQL.
  - AC-3: Redis down → 503 and the body names Redis.
  - AC-4: The readiness probe calls `/ready` and the liveness probe does **not** (`ASG-K8S-018`).
- **Test mapping:** `IT` each dependency stopped in turn (or replaced with a failing stub); `CI` compose integration waits on `/ready` (`ASG-CICD-010`).
- **Evidence mapping:** capture of the 503 body; matrix rows `ASG-FR-032`, `ASG-K8S-018`.

### ASG-FR-033 — Prometheus metrics (`/metrics`)

- **Source:** §2.2 p6 (row 9).
- **Actor:** Metrics scraper (Prometheus, if used — bonus `ASG-BONUS-004`), or an operator with `curl`.
- **Precondition:** The process is running.
- **Trigger:** `GET /metrics`.
- **Main flow:** Returns metrics in the **Prometheus text format** covering: **request count**, **request latency histogram**, **triage latency**, **fallback counter**.
- **Alternate / failure flows:** None specified. Metric names, labels and buckets → DQ-API-12.
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: The response parses as Prometheus text exposition format.
  - AC-2: After some requests, a request-count series has increased.
  - AC-3: The latency histogram series exist (buckets, sum, count).
  - AC-4: After a triage, a triage-latency series exists; after a fallback, the fallback counter has increased by one.
- **Test mapping:** `IT` scrape before and after traffic and compare; `IT` fallback increments the counter.
- **Evidence mapping:** capture of `/metrics`; matrix row `ASG-FR-033`.

### ASG-FR-034 — The status state machine

- **Source:** §2.2 p6 (Domain rules).
- **Actor:** The service layer applying `PATCH` requests (FR-027).
- **Precondition:** A current status and a requested status.
- **Trigger:** Any status change request.
- **Main flow:** Only these transitions are allowed: `open → in_progress`, `in_progress → resolved`, `open → rejected`, `in_progress → rejected`. `resolved` and `rejected` are **terminal**. "Everything else is 409."
- **Alternate / failure flows:** See the matrix below.
- **Postcondition:** The stored status is either the requested one (allowed) or unchanged (forbidden).
- **Acceptance criteria:**
  - AC-1: The matrix below is exhaustive: 4 allowed pairs and 12 forbidden pairs, 16 in total.
  - AC-2: A parametrised test asserts the outcome of **all 16** pairs.
  - AC-3: `open → resolved` is **forbidden** (a complaint must pass through `in_progress`).
- **Test mapping:** `UT` all 16 pairs (parametrised); `IT` through the API for the allowed ones and a sample of forbidden ones.
- **Evidence mapping:** pytest report; matrix row `ASG-FR-034`.

**Transition matrix** (row = current status, column = requested status; ✅ allowed, ❌ 409):

| from \ to | open | in_progress | resolved | rejected |
|---|---|---|---|---|
| **open** | ❌ | ✅ | ❌ | ✅ |
| **in_progress** | ❌ | ❌ | ✅ | ✅ |
| **resolved** (terminal) | ❌ | ❌ | ❌ | ❌ |
| **rejected** (terminal) | ❌ | ❌ | ❌ | ❌ |

The diagonal (same status) is ❌ because the assignment allows nothing that is not listed ("Everything else is 409"); DQ-API-16 asks for confirmation.

### ASG-FR-035 — The transition table is explicit data

- **Source:** §2.2 p6: "Implement it as an explicit transition table, not a chain of ifs."; §4 C p20.
- **Actor:** The developers and reviewers (a design constraint the reviewers check).
- **Precondition:** None.
- **Trigger:** Implementation and review of the state machine.
- **Main flow:** The allowed transitions are declared as a table (for example a mapping from a status to the set of statuses it may move to) that the service consults; adding or removing a transition is a data change, not a control-flow change.
- **Alternate / failure flows:** None.
- **Postcondition:** The rules of FR-034 exist in exactly one place.
- **Acceptance criteria:**
  - AC-1: The transition rules appear once, as a table; no `if`/`elif` chain compares statuses to decide legality.
  - AC-2: The frontend contains no copy of the table (`ASG-FR-003`).
  - AC-3: A unit test iterates the table itself, so a row added to the table without a matching decision fails the test.
- **Test mapping:** `UT` parametrised over the table; code inspection during review (rubric C3).
- **Evidence mapping:** file and line reference for the table in `docs/ENGINEERING-NOTES.md`; matrix row `ASG-FR-035`.

### ASG-FR-036 — All nine endpoints conform to the contract

- **Source:** §2.2 p5–6; §4 C p19 ("All ten endpoints to contract, correct status codes, field-level validation errors" — the source lists nine; owner decision, confirmed by the instructor: nine).
- **Actor:** Reviewer / evaluator.
- **Precondition:** The backend is deployed.
- **Trigger:** A contract check against the table in §2.2.
- **Main flow:** Each of the nine operations exists at the stated method and path and returns the status codes stated in FR-020…033.
- **Alternate / failure flows:** If the instructor names a tenth endpoint later, `ASG-FR-038` is added; no tenth endpoint is invented now.
- **Postcondition:** The OpenAPI schema lists exactly these operations; the typed frontend client (`ASG-FR-013`) is generated from or checked against it.
- **Acceptance criteria:**
  - AC-1: A test enumerates the nine `(method, path)` pairs and asserts each is registered.
  - AC-2: For each operation, the status codes **the assignment states** are asserted at least once: `POST` 201 / 400 / 429; `GET` by id 200 / 404; `PATCH` 409; `/ready` 200 / 503. Codes the assignment does not state (`PATCH` success and unknown id, `/health` success) are asserted once DQ-API-17, DQ-API-18 and DQ-API-11 are settled.
  - AC-3: The generated OpenAPI document contains the nine operations.
- **Test mapping:** `IT` contract test over the table; `CI` the OpenAPI/client check.
- **Evidence mapping:** contract-test report; the OpenAPI JSON; matrix row `ASG-FR-036`.

### ASG-FR-037 — End-to-end intake flow

- **Source:** §1.2 p2 ("validates it, triages it … persists it durably, and surfaces it on a live operations dashboard with aggregate statistics"); §3.4 p17 (integration job).
- **Actor:** Citizen and Operator.
- **Precondition:** The whole system is running (Compose or Kubernetes) with seeded data.
- **Trigger:** A citizen submits a complaint.
- **Main flow:**
  1. The citizen submits it (FR-020) and sees category, priority, summary and provider.
  2. The complaint appears in the Dashboard list (FR-024/025) and can be advanced (FR-027).
  3. The Stats view counts it, with the correct `X-Cache` state (FR-029).
- **Alternate / failure flows:** Provider failure → the same flow with `rules:fallback`. Rate limit → the citizen is told to retry later.
- **Postcondition:** The complaint is durable: it survives `docker compose down` then `up`, and deletion of the PostgreSQL pod (`ASG-DATA-022/023`).
- **Acceptance criteria:**
  - AC-1: POST a complaint, GET it back, and assert the category (as the CI integration job does, `ASG-CICD-010`).
  - AC-2: Stats `X-Cache` goes MISS → HIT across two reads.
  - AC-3: The complaint is visible in the Dashboard list and in the Stats counts.
  - AC-4: After a restart of the stack, the complaint is still returned.
- **Test mapping:** `CI` compose integration job; `DEMO` the video (clean clone → running system → triage → fallback).
- **Evidence mapping:** CI run link; demo video; matrix row `ASG-FR-037`.

---

## Design questions for Phase 02

The assignment leaves these details open. They are **not decided here**; Phase 02 (API design and ADRs) answers each one, and the answer is recorded in the design document or ADR before the endpoint is implemented.

| ID | Question | What the assignment says | Why it matters | Answered in |
|---|---|---|---|---|
| DQ-API-01 | Error-body format for 400, 404, 409, 429, 503 (field-level structure, message text) | "400 with a field-level error body"; "409 naming the attempted transition"; "503 naming the failed dependency" | The Dashboard must show the 409 message verbatim (`ASG-FR-010`) | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-02 | Status code for validation errors | Says **400** | FastAPI/Pydantic answer **422** by default, so this must be remapped deliberately — for the body **and** for query parameters and path ids? | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-03 | Pagination: defaults, first page number, response envelope, sort order (the `created_at` index suggests newest first, but the assignment does not say), what `total` counts, behaviour for `page_size` > 100 (reject or clamp) | `page`, `page_size` ≤ 100, "return total" | The frontend pagination controls and the tests depend on it | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-04 | Filter parameter names, combination semantics, handling of an invalid enum value | Filter by category, priority, status | The Dashboard applies all three together | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-05 | Request and response field names (the contact field, fields in the 201 body, the PATCH body) and **how the client learns the new complaint's id** (a body field, a `Location` header, or via the list) | Column names in §2.3; the Submit view shows category, priority, AI summary, provider; the CI job does "POST a complaint, GET it back" (§3.4 p17), so the id must be obtainable | The typed client, the Submit view's follow-up and every test depend on exact names and on the id | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-06 | Non-UUID id in `/api/complaints/{id}` | 200 / 404 only | 404 vs 400 | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-07 | Shape of the stats body; whether a status change must invalidate the stats cache | "Aggregate counts by category and priority"; "Invalidate on write" | Counts by category/priority do not change when only a status changes | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-08 | Source of "the last 20 triage outcomes" and its shape | "which provider is active, and the last 20 triage outcomes (provider, latency ms, fallback y/n)" | With ≥ 2 replicas an in-memory list per pod would be inconsistent; the data may instead be derived from stored complaints | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-09 | Rate-limit threshold and window; whether any endpoint besides `POST /api/complaints` is limited; how the client IP is determined behind the Ingress; fixed window vs token bucket; behaviour if Redis is down | "keyed by client IP", 429 with `Retry-After` | Behind an Ingress every request may appear to come from one address unless forwarded headers are honoured | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-10 | Order of the rate-limit check, validation and the triage-cache lookup | POST is "Validate → triage → persist" and is protected by the limiter | Determines which requests consume quota | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-11 | Success status and body of `/health`, and the body of `/ready`; whether `/health` may check Redis (only the database is excluded); which dependencies are named when both fail; timeouts of the dependency checks | `/health` "must not touch the database"; 503 "naming the failed dependency" | Probe timing and the readable failure message | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-12 | Metric names, labels and histogram buckets for `/metrics` | request count, latency histogram, triage latency, fallback counter | Needed for the optional Prometheus/Grafana bonus and for tests | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-13 | `X-Request-ID`: echoed in the response? format of a generated id? validation of an incoming value? | "propagated from an X-Request-ID header (generate one if absent)" | Log correlation and tests | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-14 | Value of `triage_latency_ms` on a cache hit and on a fallback; whether `confidence` is stored or returned | column `triage_latency_ms integer`; `TriageResult.confidence`; no `confidence` column in the minimum schema | The observability surface and the measured hit rate | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-15 | Behaviour of the API when Redis is unavailable at request time (limiter and caches are Redis-backed) | `/ready` must fail when Redis is unreachable | Fail open or closed for POST and stats | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-16 | A `PATCH` to the same status, and an unknown status value | "Everything else is 409" | 409 vs 400 for these two cases | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-17 | Success status code and response body of `PATCH /api/complaints/{id}/status` | Only "Enforce the state machine. Invalid transition → 409 naming the attempted transition." (§2.2 p6) | The typed client, the Dashboard's refresh after an update and the contract test (FR-036); 200 with the updated complaint, or 200/204 without a body, are all consistent with the text | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |
| DQ-API-18 | Unknown id on `PATCH /api/complaints/{id}/status` | 404 is stated only for `GET /api/complaints/{id}` ("200 / 404", §2.2 p5) | 404 is the natural reading but the PATCH row does not say it; related to DQ-API-06 (non-UUID id) | [API_DESIGN §2](../API_DESIGN.md#2-answers-to-the-design-questions) |

# Functional Requirements — Frontend (`ASG-FR-001…017`)

Catalog for the React frontend: the three views, the API client and the runtime configuration. Index, rules and entry template: [`../FRs.md`](../FRs.md). Source: [`docx/ASSIGNMENT.md`](../../docx/ASSIGNMENT.md) §2.1 (p4–5), rubric part B (§4 p19). Behaviour of the API these views call is in [`api.md`](api.md) and is referenced by ID, not copied.

The frontend **owns presentation and interaction, and no business rules** (§2.1 p4). Category, priority and the validity of a status transition are decided by the backend; this catalog contains no transition table and no triage logic. Where the assignment does not fix a detail, the entry says so and points to a **DQ-FE-nn** row in [*Design questions*](#design-questions) at the end.

| View or area | Entries | Rubric line (§4 B) |
|---|---|---|
| Whole frontend | FR-001 · FR-002 · FR-003 | — |
| Submit | FR-004 · FR-005 · FR-006 · FR-007 | B1 (5) |
| Dashboard | FR-008 · FR-009 · FR-010 | B2 (5) |
| Stats | FR-011 · FR-012 | B3 (3) |
| API client and safety | FR-013 · FR-014 · FR-015 | — |
| Runtime configuration | FR-016 · FR-017 | B4 (3) |
| Component tests | see [*Component tests*](#component-tests) (`ASG-NFR-014`) | B5 (2) |

---

### ASG-FR-001 — Frontend stack

- **Source:** §2.1 p4 ("React 18 + Vite + TypeScript").
- **Actor:** Developer and the CI `lint-and-type` job.
- **Precondition:** The frontend sources exist.
- **Trigger:** Install, build and type-check the frontend.
- **Main flow:**
  1. The frontend is built with Vite and written in TypeScript on React 18.
  2. `tsc --noEmit` and eslint pass (§3.4 p17, job `lint-and-type`).
- **Alternate / failure flows:** A type error → the CI job fails.
- **Postcondition:** A production build exists.
- **Acceptance criteria:**
  - AC-1: The frontend's dependency manifest names React 18, Vite and TypeScript.
  - AC-2: `tsc --noEmit` exits 0 on the sources.
- **Test mapping:** `CI` type check and lint.
- **Evidence mapping:** CI run log; matrix row `ASG-FR-001`.

### ASG-FR-002 — Only the submission form, the dashboard and the stats view

- **Source:** §2.1 p4 ("Present a submission form and an operations dashboard. Nothing else."; the three required views).
- **Actor:** Citizen and Operator.
- **Precondition:** The frontend is served.
- **Trigger:** A user opens the application.
- **Main flow:** The application offers exactly three views: Submit, Dashboard and Stats.
- **Alternate / failure flows:** A route that does not exist is not one of the three views (what it shows: DQ-FE-08).
- **Postcondition:** No state changes.
- **Acceptance criteria:**
  - AC-1: Each of the three views can be reached and renders.
  - AC-2: The application has no login, role or settings screen (the assignment defines none).
- **Test mapping:** `UT` (component) each view renders; `INS` the route list.
- **Evidence mapping:** screenshots of the three views in the demo; matrix row `ASG-FR-002`.

### ASG-FR-003 — The frontend duplicates no backend rule

- **Source:** §2.1 p4 ("Triage category, priority and valid status transitions are decided by the backend and rendered by the frontend, never duplicated in it").
- **Actor:** Developer (reviewer) and the component tests.
- **Precondition:** The frontend sources exist.
- **Trigger:** Review and test of the frontend.
- **Main flow:** Category, priority and the outcome of a status change come from API responses and are rendered as received.
- **Alternate / failure flows:** The frontend does not decide which status changes are allowed; it sends the requested change and renders the answer, including the 409 (FR-010).
- **Postcondition:** One source of truth for the rules: the backend.
- **Acceptance criteria:**
  - AC-1: The frontend sources contain no table or list of valid status transitions.
  - AC-2: The frontend sources contain no code that derives a category or a priority from the complaint text.
  - AC-3: With a mocked API that allows a transition the usual state machine would forbid, the view shows what the API answered.
- **Test mapping:** `INS` search of the frontend sources for a transition table; `UT` (component) AC-3.
- **Evidence mapping:** review note in the PR; matrix row `ASG-FR-003`.

### ASG-FR-004 — Submit view fields

- **Source:** §2.1 p4 (Submit: "Free-text complaint, location, optional contact").
- **Actor:** Citizen.
- **Precondition:** The Submit view is open.
- **Trigger:** The citizen fills the form.
- **Main flow:** The form has a free-text complaint field, a location field and an optional contact field.
- **Alternate / failure flows:** The contact field is left empty → the form can still be submitted. The format of a contact is not specified (DQ-FE-01).
- **Postcondition:** No state changes until the form is submitted.
- **Acceptance criteria:**
  - AC-1: The form shows the three fields; the contact is marked optional.
  - AC-2: A form with a valid text and location and an empty contact is accepted by the client-side validation.
- **Test mapping:** `UT` (component) form fields and optional contact.
- **Evidence mapping:** screenshot of the Submit view; matrix row `ASG-FR-004`.

### ASG-FR-005 — Client-side validation that mirrors the server

- **Source:** §2.1 p4 ("Client-side validation that *mirrors* server rules without replacing them"); the server rules are `ASG-DATA-006` (text 10–2000 characters) and `ASG-DATA-007` (location 3–200 characters); `ASG-FR-021` for the 400 answer.
- **Actor:** Citizen.
- **Precondition:** The Submit view is open.
- **Trigger:** The citizen submits or edits the form.
- **Main flow:** The view checks the same limits as the server before sending and shows what is wrong next to the field.
- **Alternate / failure flows:** The server is still authoritative: if it answers 400 with field-level errors (FR-021), the view shows them next to the fields (the error-body format: DQ-FE-04).
- **Postcondition:** No request is sent for input that fails the mirrored rules.
- **Acceptance criteria:**
  - AC-1: A text of 9 characters is refused before any request; a text of 10 characters is accepted.
  - AC-2: A location of 2 characters is refused; a location of 3 characters is accepted.
  - AC-3: A text of 2001 characters or a location of 201 characters is refused.
  - AC-4: When the (mocked) server answers 400 with a field-level error for input the client accepted, the view shows that error at the field.
- **Test mapping:** `UT` (component) AC-1…AC-3 boundaries; `UT` (component) AC-4 with a mocked 400.
- **Evidence mapping:** Vitest report; matrix row `ASG-FR-005`.

### ASG-FR-006 — Show the triage result

- **Source:** §2.1 p4 ("Show the returned category, priority, AI summary, and which provider produced it"); rubric B1.
- **Actor:** Citizen.
- **Precondition:** The form was submitted and the API answered 201 (FR-020).
- **Trigger:** The 201 response arrives.
- **Main flow:** The view shows the returned category, priority, AI summary and the provider that produced them.
- **Alternate / failure flows:** When the API used the rule-based fallback, the view shows the producing provider exactly as the API returned it (`ASG-AI-015`); the frontend adds no special case. Which response fields carry these values: DQ-API-05.
- **Postcondition:** The citizen sees the outcome of the triage.
- **Acceptance criteria:**
  - AC-1: With a mocked 201 body, the four values are visible.
  - AC-2: With a mocked fallback response, the provider shown is the one in the response.
- **Test mapping:** `UT` (component) result rendering; `UT` (component) fallback provider shown as returned.
- **Evidence mapping:** screenshot of a result and of a fallback result (demo, rubric F); matrix row `ASG-FR-006`.

### ASG-FR-007 — Honest loading state

- **Source:** §2.1 p4 ("Render the loading state honestly — AI calls take seconds"); rubric B1.
- **Actor:** Citizen.
- **Precondition:** The form was submitted.
- **Trigger:** The request to `POST /api/complaints` is in flight.
- **Main flow:** While the request is pending the view shows a loading state, and only the real outcome replaces it.
- **Alternate / failure flows:** The request fails (400, 429, network) → the loading state ends and the failure is shown (429: `Retry-After`, FR-022). Whether the submit control is disabled while pending is not specified (DQ-FE-02).
- **Postcondition:** The view shows either a result (FR-006) or an error.
- **Acceptance criteria:**
  - AC-1: With a mocked request that resolves after several seconds, the loading state is visible for the whole wait and no result is shown before the response.
  - AC-2: When the request fails, the loading state disappears and an error is shown.
- **Test mapping:** `UT` (component) delayed mock, fake timers.
- **Evidence mapping:** Vitest report; short capture in the demo; matrix row `ASG-FR-007`.

### ASG-FR-008 — Dashboard: paginated, filterable list

- **Source:** §2.1 p4; §2.2 p6 (`page_size ≤ 100`); rubric B2; API side `ASG-FR-024…026`.
- **Actor:** Operator.
- **Precondition:** The Dashboard is open; complaints exist.
- **Trigger:** The dashboard loads, or the operator changes a filter or a page.
- **Main flow:** The view requests `GET /api/complaints` with the chosen category, priority and status filters and page, and lists the returned page; it can apply the three filters together.
- **Alternate / failure flows:** No filter → all complaints. Defaults, page numbering and the response shape are not specified (DQ-API-03, DQ-FE-03).
- **Postcondition:** The list shows the requested page.
- **Acceptance criteria:**
  - AC-1: Choosing a category, a priority or a status sends that filter to the API and shows the returned list.
  - AC-2: The three filters can be combined in one request.
  - AC-3: The operator can move to the next and previous page.
  - AC-4: The view never requests a `page_size` above 100.
- **Test mapping:** `UT` (component) filter change → request parameters; `UT` (component) page navigation; `INS` maximum page size.
- **Evidence mapping:** Vitest report; screenshot of the dashboard; matrix row `ASG-FR-008`.

### ASG-FR-009 — Dashboard: advance a complaint's status

- **Source:** §2.1 p4 ("Operator can advance status"); rubric B2; API side `ASG-FR-027`.
- **Actor:** Operator.
- **Precondition:** The Dashboard shows a complaint.
- **Trigger:** The operator chooses a new status for a complaint.
- **Main flow:** The view sends `PATCH /api/complaints/{id}/status` with the chosen status and shows the result from the API.
- **Alternate / failure flows:** The API refuses the change with 409 → FR-010. The frontend does not pre-filter the choices by a transition table (FR-003), so which choices the control offers is a design question (DQ-FE-05). The success response of the PATCH is not specified (DQ-API-17), so the view must not depend on its body: it can refresh the row from the list.
- **Postcondition:** The list shows the status the server holds.
- **Acceptance criteria:**
  - AC-1: Choosing a status sends one PATCH for that complaint with that status.
  - AC-2: After a successful answer the row shows the new status.
- **Test mapping:** `UT` (component) PATCH sent; `UT` (component) row updated after success.
- **Evidence mapping:** Vitest report; demo capture of a status change; matrix row `ASG-FR-009`.

### ASG-FR-010 — Surface the server's 409 message verbatim

- **Source:** §2.1 p4 ("an invalid transition must surface the server's 409 message, not a generic 'error'"); rubric B2 ("server's 409 message surfaced verbatim"); API side `ASG-FR-028`.
- **Actor:** Operator.
- **Precondition:** The operator requests a change the backend refuses.
- **Trigger:** The API answers 409.
- **Main flow:** The view shows the message from the 409 response exactly as received.
- **Alternate / failure flows:** Where the message sits in the error body is not specified (DQ-API-01, DQ-FE-04). Other errors (404, 5xx, network) are shown as errors of their own kind, not as a 409 message.
- **Postcondition:** The complaint keeps its previous status in the view.
- **Acceptance criteria:**
  - AC-1: With a mocked 409 carrying a known message, that exact text is visible and no generic "error" text replaces it.
  - AC-2: After the 409 the row still shows the previous status.
- **Test mapping:** `UT` (component) mocked 409.
- **Evidence mapping:** Vitest report; screenshot of a 409 message; matrix row `ASG-FR-010`.

### ASG-FR-011 — Stats view: aggregate counts

- **Source:** §2.1 p4 ("Aggregate counts by category and priority"); rubric B3; API side `ASG-FR-029`.
- **Actor:** Operator.
- **Precondition:** The Stats view is open.
- **Trigger:** The view loads.
- **Main flow:** The view requests `GET /api/stats` and shows the counts by category and by priority.
- **Alternate / failure flows:** The shape of the stats body is not specified (DQ-API-07); an error response is shown as an error.
- **Postcondition:** The view shows the counts of the response.
- **Acceptance criteria:**
  - AC-1: With a mocked stats body, the counts by category and by priority are visible and equal to the mocked values.
- **Test mapping:** `UT` (component) stats rendering.
- **Evidence mapping:** Vitest report; screenshot of the Stats view; matrix row `ASG-FR-011`.

### ASG-FR-012 — Stats view: show the cache state from `X-Cache`

- **Source:** §2.1 p4 ("Display whether the response was a cache hit, from the X-Cache header"); §2.4 p8; rubric B3; API side `ASG-CACHE-004`.
- **Actor:** Operator.
- **Precondition:** The stats response carries an `X-Cache` header.
- **Trigger:** The stats response arrives.
- **Main flow:** The view reads the `X-Cache` header of the response and shows whether it was a HIT or a MISS.
- **Alternate / failure flows:** A response without the header is not shown as a hit (what is shown instead: DQ-FE-06). Whether JavaScript can read the header at all depends on the runtime-configuration mechanism (DQ-FE-10).
- **Postcondition:** The cache state on screen is the one the server reported.
- **Acceptance criteria:**
  - AC-1: A response with `X-Cache: HIT` is shown as a hit.
  - AC-2: A response with `X-Cache: MISS` is shown as a miss.
  - AC-3: A response without the header is not shown as a hit.
- **Test mapping:** `UT` (component) HIT, MISS and missing header.
- **Evidence mapping:** Vitest report; demo capture of MISS then HIT; matrix row `ASG-FR-012`.

### ASG-FR-013 — Typed API client checked against the OpenAPI schema

- **Source:** §2.1 p5 ("A typed API client generated from or checked against the backend's OpenAPI schema").
- **Actor:** Developer and the CI.
- **Precondition:** The backend publishes an OpenAPI schema (§2.2 p5).
- **Trigger:** The API client is written or the schema changes.
- **Main flow:** The client's types are generated from the schema, or checked against it, so a schema change that breaks the client is caught before merge.
- **Alternate / failure flows:** Generated or checked is the team's choice (DQ-FE-07); either satisfies the assignment.
- **Postcondition:** The client's types match the schema.
- **Acceptance criteria:**
  - AC-1: A documented command regenerates or checks the client types against the schema.
  - AC-2: Changing a field of the schema so it no longer matches the client makes that command or the type check fail.
  - AC-3: No API response is typed as `any`.
- **Test mapping:** `CI` type check and schema check; `INS` no `any` on API responses.
- **Evidence mapping:** CI log of the check; matrix row `ASG-FR-013`.

### ASG-FR-014 — Error boundary

- **Source:** §2.1 p5 ("An error boundary").
- **Actor:** Citizen and Operator.
- **Precondition:** A component throws while rendering.
- **Trigger:** The render error.
- **Main flow:** An error boundary catches it and shows a fallback instead of a blank page.
- **Alternate / failure flows:** What the fallback shows is not specified (DQ-FE-08).
- **Postcondition:** The application does not white-screen.
- **Acceptance criteria:**
  - AC-1: A child component that throws during render is replaced by the fallback, and the rest of the page keeps working.
- **Test mapping:** `UT` (component) throwing child.
- **Evidence mapping:** Vitest report; matrix row `ASG-FR-014`.

### ASG-FR-015 — No secrets in the frontend

- **Source:** §2.1 p5 ("No secrets in frontend code — anything in a browser bundle is public, and 'it's minified' is not a defence"); the same rule as `ASG-NFR-017`.
- **Actor:** Developer and the CI.
- **Precondition:** A production build exists.
- **Trigger:** Review and scan of the sources and of the build output.
- **Main flow:** Neither the sources nor the build output contain a credential, key or token.
- **Alternate / failure flows:** A hit in the scan fails the check.
- **Postcondition:** The bundle contains only public information.
- **Acceptance criteria:**
  - AC-1: A secret scan of the sources finds nothing.
  - AC-2: A scan of the build output for keys, tokens and passwords finds nothing.
- **Test mapping:** `CI` secret scan; `INS` bundle scan.
- **Evidence mapping:** scan output; matrix row `ASG-FR-015`.

### ASG-FR-016 — Runtime configuration: build once, deploy many

- **Source:** §2.1 p4 ("no baked-in API URL"; "build-once-deploy-many"); rubric B4 ("no baked-in API URL; one image runs in any environment").
- **Actor:** Platform automation and the developer.
- **Precondition:** One frontend image exists.
- **Trigger:** The image starts in an environment (Compose, Kubernetes, CI).
- **Main flow:** The frontend learns where the API is at container start, not at build time.
- **Alternate / failure flows:** The value is missing at start → not specified what the frontend does (DQ-FE-09).
- **Postcondition:** The same image works in every environment.
- **Acceptance criteria:**
  - AC-1: The built bundle contains no environment-specific absolute backend URL.
  - AC-2: The same image, started with two different configurations, talks to two different backends without a rebuild.
- **Test mapping:** `INS` search of the build output for absolute URLs; `DEMO` one image in two environments (Compose and Kubernetes).
- **Evidence mapping:** build-output search result; demo capture; matrix row `ASG-FR-016`.

### ASG-FR-017 — Runtime configuration mechanism stated in an ADR

- **Source:** §2.1 p4 ("serve /config.js generated at container start from environment variables, or proxy /api through nginx so the frontend never needs an absolute backend URL at all. State your choice in an ADR").
- **Actor:** Developer.
- **Precondition:** FR-016 applies.
- **Trigger:** The mechanism is chosen and implemented (Phase 03).
- **Main flow:** The team picks one of the two mechanisms the assignment names and records the decision and its reasons in [`docs/adr/0002-frontend-runtime-config.md`](../adr/0002-frontend-runtime-config.md).
- **Alternate / failure flows:** A different mechanism is not excluded by the assignment, but it must still meet FR-016 and be justified in the ADR.
- **Postcondition:** The ADR states the choice, and the implementation matches it.
- **Acceptance criteria:**
  - AC-1: The ADR names the chosen mechanism and why the other was not chosen.
  - AC-2: The implementation is the one the ADR names.
- **Test mapping:** `INS` ADR and implementation agree; `DEMO` as FR-016.
- **Evidence mapping:** `docs/adr/0002-frontend-runtime-config.md`; matrix row `ASG-FR-017`.

---

## Component tests

The assignment requires **at least 5 meaningful component tests passing in CI** (§3.4 p17, §4 B5; `ASG-NFR-014`). Test files and names are decided in Phase 03; the scenarios below are what the tests must cover, so the count is reached with tests that mean something.

| Test | Scenario | Entries |
|---|---|---|
| T-FE-01 | Submit view refuses input below and above the limits and accepts input at the limits | FR-005 |
| T-FE-02 | Submit view shows a loading state for a slow request and then the result | FR-007, FR-006 |
| T-FE-03 | Submit view shows the category, priority, AI summary and provider of a fallback response | FR-006 |
| T-FE-04 | Dashboard sends the chosen filters and page, and never asks for more than 100 per page | FR-008 |
| T-FE-05 | Dashboard shows the server's 409 message verbatim and keeps the old status | FR-010, FR-009 |
| T-FE-06 | Stats view shows the counts and the HIT or MISS state from `X-Cache` | FR-011, FR-012 |
| T-FE-07 | The error boundary replaces a throwing child with the fallback | FR-014 |
| T-FE-08 | The frontend contains no transition table (search test) | FR-003 |

Eight scenarios for a minimum of five; none of them tests a framework.

## Design questions

The assignment leaves these details open. They are **not decided here**; Phase 03 (frontend) answers each one before the view is built, and the answer goes into the code or the ADR.

| ID | Question | What the assignment says |
|---|---|---|
| DQ-FE-01 | Format and length of the optional contact | "optional contact" only |
| DQ-FE-02 | Whether the submit control is disabled while a request is pending | "Render the loading state honestly" only |
| DQ-FE-03 | Default page size, page controls and what the list shows on an empty page | `page_size ≤ 100`; depends on DQ-API-03 |
| DQ-FE-04 | Where the field-level errors and the 409 message sit in the error body | "field-level error body", "409 naming the attempted transition"; depends on DQ-API-01 |
| DQ-FE-05 | How the operator picks the target status without the frontend embedding transition rules (for example every status offered, the server refuses the rest) | "Operator can advance status"; valid transitions "decided by the backend" |
| DQ-FE-06 | What the Stats view shows when `X-Cache` is absent | "Display whether the response was a cache hit" |
| DQ-FE-07 | Generated or checked API client, and the tool | "generated from or checked against" |
| DQ-FE-08 | What an unknown route and the error-boundary fallback show | "An error boundary" only |
| DQ-FE-09 | What the frontend does when its runtime configuration is missing at start | "no baked-in API URL" |
| DQ-FE-10 | Browsers let JavaScript read a response header such as `X-Cache` on a cross-origin call only if the server exposes it; same-origin (an nginx `/api` proxy) needs nothing. Which applies follows from the mechanism chosen for FR-017 | "Display whether the response was a cache hit, from the X-Cache header" |

## Coverage

| Group | IDs | Count | Status |
|---|---|---|---|
| Frontend | `ASG-FR-001…017` | 17 | Catalog in this file (#14) |

# Functional Requirements — Index and Entry Template

Functional requirements are extracted from [`docx/ASSIGNMENT.md`](../docx/ASSIGNMENT.md) and identified in [`ASSIGNMENT_TRACEABILITY.md`](ASSIGNMENT_TRACEABILITY.md). This file is the **index** and the **shared entry template**; the entries live in the catalogs below.

## Catalogs

| Catalog | IDs | File | Issue | Author |
|---|---|---|---|---|
| Frontend (views, client, runtime config) | `ASG-FR-001…017` | [`frs/frontend.md`](frs/frontend.md) | #14 | `TahaSohail-Goat` |
| API and domain rules (nine endpoints, state machine) | `ASG-FR-020…037` | [`frs/api.md`](frs/api.md) | #15 | `TahaSohail-Goat` |

`ASG-FR-018` and `ASG-FR-019` are intentionally unused (a gap left between the two groups). IDs are never reused or renumbered.

Owner decision B-004: the API contract is the **nine** operations listed in the assignment's table (§2.2 p5–6).

## Rules for every catalog

1. **Source first.** Each entry cites the assignment section and page. If the assignment does not say something, the entry does not say it either: the gap goes to that catalog's *Design questions* table, to be settled in Phase 02 (API design / ADRs) — never invented.
2. **Behaviour, not implementation.** Entries state observable behaviour and how it is verified. Class names, frameworks and layer placement belong to Phase 02 and later, except where the assignment itself fixes them.
3. **Testable acceptance criteria.** Each criterion is a yes/no statement with the input and the expected result. Number them `AC-<n>` inside the entry.
4. **Cross-reference, do not copy.** Behaviour owned by another ID (rate limiting, caching, triage, schema) is referenced by that ID, not restated.
5. **Traceability.** Every entry names its `ASG-*` ID; the row in the matrix is updated in the phase that implements it.

## Entry template

Copy this block for each requirement. Keep every field; write `None` or `Not specified by the assignment (see DQ-…)` rather than deleting one.

```markdown
### ASG-FR-0xx — <short title>

- **Source:** §x.y pN (and any other clause that constrains it)
- **Actor:** who or what initiates it (Citizen, Operator, Platform probe, …)
- **Precondition:** state that must hold before
- **Trigger:** the event or request that starts it
- **Main flow:**
  1. …
- **Alternate / failure flows:**
  - <condition> → <observable result>
- **Postcondition:** state that holds afterwards
- **Acceptance criteria:**
  - AC-1: <input> → <expected result>
- **Test mapping:** `UT` | `IT` | `CI` | `DEMO` — <scenario>
- **Evidence mapping:** <artifact or capture that proves it>; matrix row `ASG-FR-0xx`
```

Legend for **Test mapping**: `UT` unit test · `IT` integration test against the running app with real PostgreSQL and Redis · `CI` a check inside a GitHub Actions job · `DEMO` shown live or in the demo video. Test names are chosen when the tests are written (Phase 03/04); entries describe the *scenario*.

## Coverage

| Group | IDs | Count | Status |
|---|---|---|---|
| Frontend | `ASG-FR-001…017` | 17 | Catalog in [`frs/frontend.md`](frs/frontend.md) (#14) |
| API and domain | `ASG-FR-020…037` | 18 | Catalog in [`frs/api.md`](frs/api.md) (#15) |
| **Total** | | **35** | |

The gate for Phase 01 (`docs/phases/PHASE-01-REQUIREMENTS.md`): every mandatory assignment obligation is represented by a requirement ID or documented as non-requirement / bonus / future. Non-functional obligations are catalogued in [`NFRs.md`](NFRs.md); product scope in [`PRD.md`](PRD.md).

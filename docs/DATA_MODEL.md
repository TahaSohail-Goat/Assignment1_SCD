# Data Model

The schema of the `complaints` table, the constraints that protect it, the two indexes and the query each one serves. It follows the minimum schema of [`docx/ASSIGNMENT.md`](../docx/ASSIGNMENT.md) §2.3 (p7–8) exactly; choices the assignment leaves open are marked **Decision** and come from [`API_DESIGN.md`](API_DESIGN.md). The source of the DDL is the migration [`backend/alembic/versions/0001_create_complaints.py`](../backend/alembic/versions/0001_create_complaints.py); a test compares the ORM models with the migrated database so the two cannot drift.

**Database:** PostgreSQL 16 (`ASG-DATA-001`). **Schema changes:** only through Alembic migrations, which are versioned, reviewable and reversible (`ASG-DATA-002…004`). There is no `CREATE TABLE` in application code (`ASG-DATA-003`); a test scans `backend/app/` for schema DDL.

## Enumerated types

| PostgreSQL type | Values | Requirement |
|---|---|---|
| `complaint_category` | `water`, `electricity`, `sanitation`, `roads`, `streetlights`, `other` | `ASG-DATA-009` |
| `complaint_priority` | `high`, `normal`, `low` | `ASG-DATA-010` |
| `complaint_status` | `open`, `in_progress`, `resolved`, `rejected` | `ASG-DATA-011` |

The same vocabulary is defined once in code (`backend/app/domain.py`) and used by the API and the services.

## Table `complaints`

| Column | Type | Null | Default | Rule | Requirement |
|---|---|---|---|---|---|
| `id` | `uuid` | no | `gen_random_uuid()` | primary key, server-generated | `ASG-DATA-005` |
| `text` | `text` | no | | 10–2000 characters, `CHECK` in the database **and** validated by the application | `ASG-DATA-006` |
| `location` | `text` | no | | 3–200 characters, `CHECK` | `ASG-DATA-007` |
| `reporter_contact` | `text` | yes | | optional | `ASG-DATA-008` |
| `category` | `complaint_category` | no | | | `ASG-DATA-009` |
| `priority` | `complaint_priority` | no | | | `ASG-DATA-010` |
| `status` | `complaint_status` | no | `'open'` | | `ASG-DATA-011` |
| `ai_summary` | `text` | yes | | one line, ≤ 140 characters (`CHECK`: length and no CR or LF) | `ASG-DATA-012` |
| `triaged_by` | `text` | no | | see below | `ASG-DATA-013` |
| `triage_latency_ms` | `integer` | no | | `CHECK (triage_latency_ms >= 0)`; measured wall-clock time of the triage step (`API_DESIGN.md` DQ-API-14) | `ASG-DATA-014` |
| `created_at` | `timestamptz` | no | `now()` | UTC | `ASG-DATA-015` |
| `updated_at` | `timestamptz` | no | `now()` | UTC; set to `now()` by every status change | `ASG-DATA-015` |

**`triaged_by`** (`ASG-DATA-013`). The four values of the assignment, `llm:groq`, `llm:ollama`, `rules` and `rules:fallback`, are all accepted. **Decision:** a `CHECK` also accepts `simulated` (the CI provider) and `llm:<provider>` for any other documented hosted provider (for example `llm:gemini`). Anything else is rejected by the database.

**No foreign keys:** the minimum schema has one table, so there are no relationships to declare.

**Constraints, by name** (each has a test that the database itself refuses a violating row): `ck_complaints_text_length`, `ck_complaints_location_length`, `ck_complaints_ai_summary_one_line`, `ck_complaints_triaged_by`, `ck_complaints_triage_latency_ms`. The assignment's own example, a 9-character text, is one of the tested cases.

## Indexes and the query each one serves (`ASG-DATA-016…018`)

| Index | Columns | Query it serves |
|---|---|---|
| `ix_complaints_status_priority` | `(status, priority)` | The dashboard filter: `SELECT … FROM complaints WHERE status = :s AND priority = :p …` (and `WHERE status = :s` alone, since `status` is the leading column). Without it, every filtered list is a full scan. |
| `ix_complaints_created_at` | `(created_at)` | The newest-first listing with pagination: `SELECT … FROM complaints ORDER BY created_at DESC, id LIMIT :page_size OFFSET :offset` (`ASG-FR-025`), and the "last 20 triage outcomes" of `/api/meta/providers`: the same `ORDER BY created_at DESC LIMIT 20`. |

Two queries have **no** dedicated index on purpose: the statistics (`GROUP BY category` and `GROUP BY priority`) read every row and are cached for 30 seconds (`ASG-CACHE-002…003`), so an index would not help; a filter on `category` alone is a scan of a small table. If the table grew to where that matters, a `category` index would be the next migration, and this section would say which query justifies it.

## Migrations

- Location `backend/alembic/versions/`; the environment (`backend/alembic/env.py`) reads `DATABASE_URL`; no URL is stored in the repository.
- `upgrade` creates the three enum types, the table, its constraints and the two indexes; `downgrade` drops them in reverse order. Both are tested on an empty database, and upgrade after downgrade works again.
- One migration head. Only the owner of the data layer adds migrations, so the head cannot fork.

## Seed data

The seed command will live in `backend/app/seed.py` and run as `python -m app.seed` after the migrations (`docs/API_DESIGN.md` §4). It is idempotent by design: every seed complaint has a fixed UUID derived from its text and is inserted with `ON CONFLICT (id) DO NOTHING` (`SqlComplaintRepository.add_many_if_absent`), so a second run adds nothing (`ASG-DATA-021`). The content (at least 30 complaints in Urdu-influenced English across the categories, `ASG-DATA-019…020`) is issue #41.

## Persistence, backup and restore

- **Persistence contract (`ASG-DATA-022…023`):** `docker compose down` then `up` must keep every row (a named volume, Phase 08), and deleting the PostgreSQL pod must keep every row (a PersistentVolumeClaim, Phase 09). Both are demonstrated with real captures in those phases; nothing is claimed here.
- **Backup and restore:** the data lives in one database, so `pg_dump` of `complaints` is a complete logical backup and `psql < dump.sql` restores it into a database that has been migrated to the same revision. The enum types and constraints travel with the dump. Redis holds only rebuildable data (caches and rate-limit counters); whether and why its AOF persistence is enabled is documented with the cache design (Phase 06).

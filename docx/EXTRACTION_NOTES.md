# Extraction Notes — `ASSIGNMENT_SOURCE.pdf` → `ASSIGNMENT.md`

Records how the Markdown transcription was produced and every place where the **source itself** is ambiguous, inconsistent, truncated or references material not supplied. Nothing here changes the assignment; ambiguities that affect decisions are resolved in the PR or issue, and the instructor's answers are in the decisions table of [`docs/SUBMISSION.md`](../docs/SUBMISSION.md).

## 1. Source provenance

| Property | Value |
|---|---|
| File | `docx/ASSIGNMENT_SOURCE.pdf` (preserved unchanged) |
| Size | 400,818 bytes |
| SHA-256 | `28429068756abdac6ce7ef814d19c5fc3ddd20115787618241b49b81245e420c` |
| Pages | 26 |
| PDF title metadata | "Software Construction and Design - Assignment 1" |
| Producer | Skia/PDF m155 Google Docs Renderer |
| Embedded images | 1 (architecture diagram, page 3) |
| Hyperlinks | none |
| Extraction date | 2026-09-25 |

> Note: verify the hash with `Get-FileHash docx\ASSIGNMENT_SOURCE.pdf -Algorithm SHA256` (PowerShell) or `sha256sum docx/ASSIGNMENT_SOURCE.pdf`. The value is compared case-insensitively; it was identical before and after the prompt-pack folder was flattened into the repository root.

If a DOCX version of the assignment is supplied later, store it unchanged as `docx/ASSIGNMENT_SOURCE.docx` (per `START_HERE.md`) and re-run the comparison in §2.

## 2. Method and verification

1. `pdftotext -enc UTF-8` (poppler, bundled with Git for Windows) produced the text layer. **UTF-8 must be requested explicitly**; the default Latin-1 output replaces `—`, `≥`, `→`, `≤`, `×`, `÷`, `↔`, `−` with `?`/`�` (EN-01).
2. PyMuPDF rendered all 26 pages to PNG; pages containing tables, code blocks, the diagram and the numbered lists were inspected visually to recover table structure, indentation, emphasis and the diagram.
3. `docx/ASSIGNMENT.md` was written by hand from (1) and (2), section by section, with `PDF page N` HTML-comment markers.
4. **Mechanical check:** the PDF text layer and the Markdown were normalised (Markdown syntax, transcriber notes, comments, Mermaid and image lines removed; case, punctuation and whitespace folded) and compared token-by-token with `difflib.SequenceMatcher`.
   - PDF tokens: 5,557 · Markdown tokens: 5,567 · similarity **0.9973**.
   - 10 differing blocks, all benign and explained: 3 PDF word-wrap artefacts in table cells (`metho d`, `build-pus h`, `deploy-k 8s`), 2 repeated table headers added by the transcriber, 4 spacing differences around the `</cite>` code spans, 1 title heading added.
   - **No source text is omitted.**
5. Re-run the check whenever `ASSIGNMENT.md` is edited. (The comparison script is intentionally not committed; it is a one-off Phase 00 validation.)

## 3. Extraction notes

| ID | Where | Observation | Handling |
|---|---|---|---|
| EN-01 | whole PDF | Default `pdftotext` (Latin-1) corrupts non-ASCII typography. | Re-extracted as UTF-8; symbols checked against rendered pages. |
| EN-02 | bullets/lists | The text layer has a zero-width space (U+200B) after every bullet and list marker. | Dropped; not part of the content. |
| EN-03 | §2.5 p10 | The Groq and Gemini paragraphs contain literal `<cite index="…">…</cite>` tags (markup residue from the authoring tool). The rendered PDF shows them as visible text. | Preserved verbatim inside code spans so they stay visible in Markdown. They carry no requirement. The Markdown display layer of some editors shows `<` as `(`; the file bytes are `<` (U+003C). |
| EN-04 | §2.2 p6 | API-contract row `GET /api/stats`: the behaviour cell ends at `` `X-Cache: HIT`` (unclosed backtick). The rest of the cell is missing — probably a `\|` inside a Markdown table cell was read as a column delimiter when the source document was produced. | Transcribed exactly as it appears (backtick escaped). §2.4 supplies the intended semantics: `X-Cache: HIT\|MISS`. Informational. |
| EN-05 | §2 p3 | The architecture diagram is a raster image; its text is not in the text layer. | Extracted unchanged to `docx/assets/architecture-diagram.png` (1160×1086 px); also transcribed as Mermaid. Diagram content: Citizen/Operator → HTTP → frontend (React+Vite→nginx, multi-stage) and backend (FastAPI+Pydantic) inside `docker network: edge`, `/api proxied`; `postgres:16 · volume pgdata` and `redis:7 · cache + rate limiter` inside `docker network: internal (internal: true)`; backend → `TriageProvider (interface)` → default: `Groq or Gemini · free tier · JSON mode`; CI: `SimulatedTriage · deterministic fake`; on `timeout · 429 · bad JSON` → `RuleBasedTriage · fallback`. |
| EN-06 | §4 p19–22 | **Arithmetic inconsistency.** Header: "Total Marks 150" and §4: "150 marks". The rubric section totals are A 15 + B 18 + C 25 + D 12 + E 10 + F 25 + G 15 + H 20 + I 20 + J 15 = **175**. Each section's item marks do sum to its stated section total (verified in `docs/RUBRIC.md`). Additionally §5.1 says parts A–G are "110 marks" but A–G sum to **120**, H–J to 55. | Transcribed as written. The instructor left the rubric to the teaching assistant. |
| EN-07 | §5 p25 | Section numbering jumps from 5.5 to 5.7; there is no 5.6. | Numbering preserved. Possibly a removed section; not assumed to contain any requirement. Logged with the other unsupplied material (EN-13). |
| EN-08 | §2.2 p5–6, §2.3 p7–8, §3.2 p12–13, §5.7 p25–26 | Tables/code blocks/trees that continue across a page break. | Reassembled into one table/block; where Markdown required a header row on the continuation, the header was repeated and flagged with a transcriber note. |
| EN-09 | header p1 vs §5.1 p23 | Header says "Duration 2 Weeks"; §5.1 says "roughly 35–45 hours per student over four weeks" and "As written, 4 weeks, teams of 2". No calendar deadline appears anywhere in the source. | The instructor said the deadline is the Google Classroom one ("next Tuesday"). |
| EN-10 | §2.2 p5–6 vs §4 C p19 | The API-contract table lists **9** operations (POST/GET/GET/PATCH `/api/complaints…`, `/api/stats`, `/api/meta/providers`, `/health`, `/ready`, `/metrics`); rubric C says "All **ten** endpoints to contract". | All 9 listed are mandatory; the instructor confirmed there is no tenth. |
| EN-11 | §2.3 p7 | `triaged_by` is enumerated as `llm:groq · llm:ollama · rules · rules:fallback`. No value is given for `SimulatedTriage`, for Gemini or for any other permitted hosted provider. | Open design question, decided in Phase 05/07 (ADR). |
| EN-12 | §1.4 p3 vs §4 bonus | §1.4 says a push to main "builds **signed** and scanned images"; image signing (Cosign) appears only as bonus (+3). | The instructor said signing is not required. |
| EN-13 | throughout | Material referenced but **not supplied**: Lecture 01 (Era 3, Era 5, slide 34), Lecture 03 (question, slide 32 "CI/CD maturity ladder"), Lecture 04 (`depends_on` lesson), CLO 4, CLO 8, course policy on plagiarism/late work, and the contents of `scripts/check_submission.py`, `docs/TRIAGE.md` and `LICENSE` (listed in §5.7 without a specification). | Not invented. The instructor said the lecture material is not necessary and that `check_submission.py` is ours to write if we want to; `LICENSE` and the purpose of `docs/TRIAGE.md` stay undecided. |
| EN-14 | §3.3 p15 vs §4 bonus | §3.3 says "Demonstrate a zero-downtime rollout…"; the rubric scores it only as bonus (+4). | We do the demo anyway. |
| EN-15 | §2.1 p4 vs §3.1 p12 | Frontend served by `nginx:alpine` (§2.1) vs `nginx:1.27-alpine` (§3.1). §5.3 penalises unpinned base images. | The pinned tag in §3.1 governs. Informational. |
| EN-16 | §1.2 p2 | "five cooperating containers". Services named in the source: frontend, backend, postgres, redis and (offline AI path) ollama = five, but ollama is described as an alternative provider, not a mandatory container. | Informational; the count is only met if ollama runs in the default Compose stack. |
| EN-17 | §3.4 p17 vs §2.2 layout | §3.4 defines the branch model as "dev for work, main for deployable software" and triggers `ci.yml` "on push to dev"; the rubric says "dev plus feature branches". The pack (`docs/GITHUB_WORKFLOW.md`) uses `dev/<issue-number>-<slug>`. Git cannot hold a branch `dev` and branches `dev/*` at once (ref-namespace collision). | Owner decision: `dev` plus `feature/<n>-<slug>` (`docs/GITHUB_WORKFLOW.md`). |
| EN-18 | emphasis | Bold/italic were reproduced on a best-effort basis from the rendered pages. | Formatting only; no requirement depends on it. |
| EN-19 | date | "verified September 2026" (§2.5 p10) — provider limits were verified by the author only. | The assignment itself tells students to re-check live limits and cite what they saw. |
| EN-20 | title table p1 | The first two rows of the title table span both columns. | Reproduced with an empty second cell. |

## 4. What was deliberately NOT done

- No requirement was corrected, reordered, merged or "improved".
- No missing information was invented (see EN-04, EN-11, EN-13).
- Inconsistencies were recorded, not resolved.

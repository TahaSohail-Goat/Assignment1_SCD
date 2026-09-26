# Demo video script (ASG-DOC-014, ASG-DOC-015)

The assignment asks for a video of **at most 5 minutes with both partners speaking** that covers: clean
clone to running system, AI triage, fallback, network isolation failing, HPA scaling and rollback
(`docx/ASSIGNMENT.md` §4 J, p22; §3.2 p13 and §3.4 p18–19 for the failing ping and both rollbacks).
The video is recorded by the two contributors: nothing in this file has been recorded yet, and no
capture here is presented as the video.

Split: **A** = Taha, **B** = Artfever. Record the screen at 1080p, terminal font large. Upload as an
unlisted video and paste the link into `docs/SUBMISSION.md` (row 4) and the traceability row `ASG-SUB-004`.

## Before recording (10 minutes, not on camera)

- Windows or Linux with Docker, `kind`, `kubectl`, `k6` (or use the captured run) and a browser.
- A fresh clone in an empty folder: `git clone https://github.com/TahaSohail-Goat/Assignment1_SCD demo && cd demo`.
- For the hosted-model shot: a Groq key in the shell only (`export GROQ_API_KEY=...`), never in a file.
- Have the successful CD run and the GHCR package pages open in browser tabs.
- Rehearse once with a stopwatch; cut what does not fit in 5:00.

## Shot list

| Time | Who | On screen | Say | Command / action |
|---|---|---|---|---|
| 0:00–0:20 | A | README top | What CivicPulse is: citizens report civic problems, the system triages each one (category, priority, one-line summary) and the office sees a dashboard. Two contributors, two AI assistants, all disclosed. | Show `README.md` and `docs/AI-USAGE.md` |
| 0:20–1:05 | B | Terminal, then the browser | Clean clone to a running system with one command; migrations and 30 seeded complaints load automatically. | `cp .env.example .env && docker compose up --build`; wait for healthy; open <http://localhost:8080>; show the Dashboard with the seeded rows |
| 1:05–1:50 | A | Browser, then curl | Submit a complaint: the category, priority and summary come back from the triage provider. Show the stats cache: first call `MISS`, second `HIT`; a new complaint makes the next call `MISS`. | Submit view with "Water has not reached our street for three days"; `curl -si localhost:8000/api/stats \| grep -i x-cache` twice |
| 1:50–2:30 | B | Terminal | The fallback: point the backend at the hosted provider with a key that cannot work; the request still returns `201`, `triaged_by` is `rules:fallback`, one warning is logged, `/api/meta/providers` lists it. Then, if a real key is available, show the same complaint triaged by `llm:groq`. | `TRIAGE_PROVIDER=llm GROQ_API_KEY=not-a-real-key docker compose up -d backend`, POST, `docker compose logs --tail 20 backend \| grep fallback`, `curl localhost:8000/api/meta/providers` |
| 2:30–2:50 | A | Terminal | Rate limit: the twelfth request in a minute answers `429` with `Retry-After`. | the loop from RUNBOOK section 8 |
| 2:50–3:20 | B | Terminal | **Network isolation fails on purpose:** the frontend is on `edge` only and cannot reach the database. Then show the network layout. | `docker compose exec frontend ping -c 1 database` (must fail: "bad address"), `docker network inspect civicpulse_internal --format '{{.Internal}}'` |
| 3:20–3:35 | A | Terminal | Persistence: down then up keeps every row. | `docker compose down`, `docker compose up -d`, `curl localhost:8000/api/stats` |
| 3:35–4:10 | B | Terminal, Actions tab | Kubernetes: one command creates the cluster and deploys; show the HPA and the scale-out capture and the measured lag. Explain the VPA is `Off` and why. | `bash scripts/k8s-up.sh` (start it before recording and cut to the finished result), `kubectl -n civicpulse get hpa`, show `docs/evidence/k8s-load-comparison.png` |
| 4:10–4:50 | A | Terminal | **Rollback, both mechanisms**, and when to use each: `rollout undo` is the fast imperative answer when the previous ReplicaSet is fine; re-applying the previous overlay with the previous SHA is the auditable one that also restores configuration. | `kubectl -n civicpulse rollout undo deployment/backend`, then the `docs/RUNBOOK.md` section 13 commands |
| 4:50–5:00 | both | Browser: the Actions run and GHCR | The pipeline: a push to `main` tested, published by SHA, and deployed. | show cd run 36230267941 and the GHCR pages |

## What each partner must be able to say (viva preparation)

Both partners speak; each answers for the other's code at the viva, so rehearse the parts that are not
yours: `docs/ENGINEERING-NOTES.md` (the eight answers), `docs/TRIAGE.md`, `docs/CACHE.md`, `docs/adr/`.

## After recording

- Add the link: `docs/SUBMISSION.md` (item 4) and `docs/ASSIGNMENT_TRACEABILITY.md` (`ASG-SUB-004`,
  `ASG-DOC-014`, `ASG-DOC-015`, `ASG-DEVOPS-017`, `ASG-K8S-021`, `ASG-CICD-028…031` mention the video).
- Re-run `python scripts/check_submission.py` and paste its output into the submission.

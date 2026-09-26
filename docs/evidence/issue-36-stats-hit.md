# Issue #36: Stats view reads X-Cache

[`issue-36-stats-hit.png`](issue-36-stats-hit.png) was captured on 2026-09-26 from the actual Vite/React frontend in headless Chrome. A Playwright route supplied `GET /api/stats` with `X-Cache: HIT` and a controlled JSON body containing three complaints: water 2, roads 1; high 1, normal 2. The view displayed those counts and `Cache: HIT`.

Command: `python capture_stats.py` (temporary capture script, removed after the run). Output: `Captured docs\evidence\issue-36-stats-hit.png; X-Cache: HIT; total: 3`. The response was mocked at the browser network boundary; this capture does not claim a live Redis cache hit. The component suite separately covers HIT, MISS, and a missing header.

Requirements: ASG-FR-011, ASG-FR-012; issue #36.

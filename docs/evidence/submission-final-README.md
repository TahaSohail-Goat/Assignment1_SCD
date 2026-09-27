# Final submission verification (2026-09-27)

Requirements: ASG-SUB-001..007, ASG-DOC-014/015, ASG-CICD-030, ASG-DEVOPS-017.

## Demo links

- **Primary:** [YouTube - Unlisted](https://youtu.be/bExMGzoHYow).
- **Backup:** [Google Drive - demo video.mp4](https://drive.google.com/file/d/1uNGCvKnzy_vpxxolNp6qQp8R4ht3Ip58/view?usp=drive_link).

Both links were supplied by Artfever. Requests used no account cookies or credentials.
YouTube's player response reports `playabilityStatus=OK`, `isUnlisted=true`, and
278 seconds (4:38). Drive served the actual MP4 with HTTP 200: 25,609,625 bytes,
277.449 seconds, H.264 848x478 video and AAC audio. The different rounded durations
do not establish byte identity between platform encodes. The downloaded backup's
SHA-256 and allowlisted public metadata are in [submission-final-video.json](submission-final-video.json).
The video binary and full web responses remain outside Git.

Visual sampling of the uploaded backup confirms startup, seeded Dashboard/Stats,
hosted submission, fallback, failed frontend-to-database ping, HPA scaling and rollback.
The source recording retained genuine command output; long waits are visibly accelerated.
The HPA run used 80 requests/s, scaled two to three replicas and completed 14,989 requests
without failures or dropped iterations. Rollback used the local b442e8d rehearsal baseline;
its images were previously built/loaded locally. This is not a GHCR pull claim.

**Speaker verification:** an audio track is present; confirmation that both contributors'
real voice-overs are included has been requested from Artfever and is part of final review.
Audio-stream metadata alone is not proof of the number or identity of speakers.

The final footage does not add a persistence down/up demonstration or prove a rolling
update under simultaneous load. Existing CI and zero-downtime captures remain their own
evidence; optional bonus claims are not inferred from this video.

## Repository and deployment audit

- Main source: `df7649c6b23792bb6f1695573944a2df14693b41` (#117).
- [CD 36310273819](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36310273819)
  passed tests, image/SBOM publishing, production overlay deployment, Ingress smoke and cleanup.
- [Release candidate v1.0.0-rc.1](https://github.com/TahaSohail-Goat/Assignment1_SCD/releases/tag/v1.0.0-rc.1)
  is the previously verified tag at cee7292; documentation merges do not move it.
- Main shortlog: 120 Artfever (51.7%), 112 Taha Sohail (48.3%), total 232.
- Full tracked-tree scan: 321 files, 74 Markdown files, zero missing relative Markdown targets.
  External URLs/anchors were not blanket-validated; both video links were checked separately.
- Submission checker: **28 passed, 1 historical warning, 0 failed**. It includes tracked-history
  credential-pattern scanning. Pattern matching cannot prove absence of arbitrary secrets.
- [Raw audit output](submission-final-audit.json) identifies the exact revision and commands.

## Honest sign-off and closure

Historical conventional-prefix failures remain FAIL. Original screenshot clauses remain
BLOCKED because the owner removed those capture tasks; no instructor waiver is invented.
Optional bonuses remain separate. The final documentation/video PR requires partner review,
then a protected dev-to-main merge and fresh CD. Close #55/#56/#31 only after the video
review and final promotion meet their criteria. Classroom submission is a human action;
this audit does not claim it has happened or guarantee a grade.

# Release verification (issue #115)

> Follow-up, 2026-09-27: the video is now uploaded; [primary/backup links and verification](submission-final-README.md). Pending-video wording below describes the original capture date. #113/#114 and #116/#117 are merged; original raw evidence is preserved.

Verified by Artfever on 2026-09-27 (Asia/Karachi; GitHub timestamps are UTC).
Requirements: ASG-CICD-021/022, ASG-SUB-002/003/005/007, ASG-DOC-010.

## Reviewed source and real runs

- Source: `cee72923a380fdffdf5ed8de2ef0ce5cb58abadb`, reviewed promotion #114.
- [Main CD 36260737154](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36260737154): successful tests, image/SBOM publishing, production overlay, Ingress smoke and ephemeral cluster cleanup.
- Annotated tag `v1.0.0-rc.1` points to that exact source; no source commit was made to trigger release.
- [Release run 36268651309](https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36268651309): all ten test jobs, build-push and release-notes passed. Trigger was tag push.
- [Published prerelease](https://github.com/TahaSohail-Goat/Assignment1_SCD/releases/tag/v1.0.0-rc.1): generated notes, not a draft. Candidate status reflects the held demo video.
- [Raw GitHub response](release-verification-github.json) records the source, jobs, release flag and notes.

## Registry verification

`docker buildx imagetools inspect` independently resolved both published semver tags;
[raw command outputs](release-verification-registry.json) retain platform manifests and digests.

| Image tag | OCI index digest |
|---|---|
| `ghcr.io/tahasohail-goat/civicpulse-backend:1.0.0-rc.1` | `sha256:b1840154220370e605786e310c3fdd404d651563b33588d553684aed1737448b` |
| `ghcr.io/tahasohail-goat/civicpulse-frontend:1.0.0-rc.1` | `sha256:bfe5ba78988fae471d0c8177400e04cc3c0f08ba5a816653b72fbf720876c887` |

This verifies publication, not deployment of the semver tags. Main CD deploys its SHA-tagged
images and checks their registry digests. The release workflow builds separately and does
not deploy; no equality between its image digests and the CD image digests is claimed.

## Submission snapshot and limitations

[Audit output](release-verification-audit.json): 28 pass, 1 historical warning, 0 fail.
At main `cee7292`, Artfever has 118/229 (51.5%) and Taha 111/229 (48.5%).
These are measured counts for that revision, not predictions of later documentation merges.

The mechanical checker is not a grade. Historical conventional-prefix failures and the
owner-removed screenshot tasks' rubric caveats remain in the checklist. Optional bonuses
are not newly required. Video recording and its link remain on hold; #55/#56/#31 stay open.
The documentation evidence PR still needs partner review and a protected promotion; use
that promotion's CD link and revision when preparing the eventual final submission.

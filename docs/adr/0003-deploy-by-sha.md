# ADR 0003 — Immutable Deployment Reference

## Status
Proposed for partner review in #52; implementation and local rehearsal complete,
successful main-branch CD run pending.

## Decision
Publish both images with the full merged commit SHA and `latest`; deploy only the SHA tag.
The build job exposes both registry digests. The ephemeral kind job pulls by those digests,
tags the verified images with the source SHA and loads them into kind before applying the
production overlay. A mutable registry tag cannot change the bytes selected by that job.

The workflow replaces the overlay placeholder only in the runner checkout. It does not push
an automated commit to protected main. The source SHA is stored in the deployment annotation
`civicpulse/source-sha` and the job summary alongside the digests; `git show <SHA>` identifies
the exact source. The ephemeral cluster is deleted at the end, so the Actions summary is its
durable deployment record. This is an assignment deployment demonstration, not a persistent
production hosting service.

`test` calls the existing CI workflow through `workflow_call`, so lint, types, tests, coverage,
builds, vulnerability scans, manifests and Compose integration all gate publishing. Both
publishing and deployment have explicit `needs:` edges. The release workflow repeats that gate
for `v*` tags before publishing exact semver image tags and generated release notes.

Registry access uses the scoped `GITHUB_TOKEN`; only publishing jobs receive `packages: write`.
Deployment receives `packages: read` and takes the database password from the repository's
`CIVICPULSE_DB_PASSWORD` Actions Secret. The optional `GROQ_API_KEY` also comes from Secrets;
the demonstrated rules provider does not need a live hosted-model key. The real Kubernetes
Secret is created before workloads and never included in diagnostics or committed artifacts.

## Rationale
The assignment requires "What is production running?" to be answerable from the Git history.

## Rollback and limitations

Use `kubectl rollout undo` for an urgent Deployment-template reversal; it does not restore
ConfigMaps, Secrets or database schemas. Afterwards re-apply the previous source overlay with
its SHA to restore the declared configuration. Commands and measured local results are in
`docs/RUNBOOK.md` section 13 and `docs/evidence/cd-local-rollback.txt`.

The local rehearsal loaded locally built images under full SHA names; it does not prove GHCR
publication or successful Actions deployment. Those need a green `cd.yml` run after this PR
is reviewed, merged into dev and promoted to main. Both-partner video evidence remains pending.

## References

- Assignment section 3.4: ASG-CICD-012..023, 028..031; rubric ADR ASG-DOC-010.
- [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Anchore Syft SBOM action](https://github.com/anchore/sbom-action)

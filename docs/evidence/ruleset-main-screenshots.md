# Main branch ruleset screenshots (ASG-GH-001, ASG-DOC-027)

Artfever captured these unedited GitHub browser screenshots on 2026-09-29 from the
read-only [main ruleset view](https://github.com/TahaSohail-Goat/Assignment1_SCD/rules/23990471?ref=refs%2Fheads%2Fmain):

- [Overview](ruleset-main-overview.png): `main` is Active and targets the default/main branch.
- [Branch rules](ruleset-main-rules.png): pull requests, status checks and force-push blocking are enabled.
- [Approval detail](ruleset-main-approval.png): one approving review is required.
- [Status-check detail](ruleset-main-status-checks.png): the ten required CI checks are listed.

The four images are separate scroll positions of the same ruleset page; the detail
captures do not repeat the page title. The live GitHub ruleset API, queried as Artfever,
also reported ruleset `23990471` active, one required approval, merge commits only,
the same ten status checks, and force pushes blocked. The existing
[ruleset export](ruleset-main.json) and [CI gate evidence](ci-gate.md) provide
machine-readable and behavioral corroboration. These captures show the read-only
ruleset view; they do not imply Artfever has repository admin access.
Earlier audit reports describe the screenshot as missing at the time they were
captured; this dated evidence supersedes that historical status.

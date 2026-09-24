# Quality Gates

A phase cannot be marked complete if its gate is red.

## Global
- tests pass
- lint/type checks pass
- no secrets
- no unpinned forbidden images
- no localhost service communication
- no accidental direct main commits
- docs updated

## Assignment Gates
Also verify the relevant rubric item(s) and automatic deductions.

## Final Gate
Run:
`python scripts/check_submission.py`

Then perform a manual rubric audit because the script is only a lint, not a grader.

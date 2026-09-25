"""Deliberately failing test: evidence that the CI gate blocks a red pull request (ASG-CICD-027).

This file exists only in the evidence pull request. The fix commit in the same pull request
removes it, and the checks turn green.
"""


def test_this_test_fails_on_purpose_to_show_that_ci_blocks_the_merge() -> None:
    assert 1 + 1 == 3

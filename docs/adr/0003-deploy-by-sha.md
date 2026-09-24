# ADR 0003 — Immutable Deployment Reference

## Status
Proposed

## Decision
Publish images with commit SHA tags and deploy by immutable SHA/digest, never `latest`.

## Rationale
The assignment requires "What is production running?" to be answerable from the Git history.

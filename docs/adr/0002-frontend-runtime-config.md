# ADR 0002 — Frontend Runtime API Configuration

## Status
Proposed

## Decision
Use a strategy that preserves build-once-deploy-many. The implementation must not bake an environment-specific backend URL into the compiled browser bundle.

Document the selected method after comparing:
- `/config.js` at container start
- nginx `/api` proxy

## Verification
Point to the exact implementation lines.

# ADR 0001 — Replaceable Triage Provider

## Status
Accepted for the provider boundary; implementation evidence is tracked by #44–#46.

## Context
Assignment §2.5 requires a replaceable `TriageProvider` with a `name` and `triage(text, location) -> TriageResult`. The four implementations are a hosted LLM, Ollama, rules, and a deterministic simulated provider. `TriageResult` validates the category, priority and summary. The application must contain timeout, retry and fallback behavior around remote providers without letting model output bypass schema validation (ASG-AI-001…015).

## Decision
Define the assignment's small synchronous provider protocol in `backend/app/providers/triage/base.py`. Every provider returns a validated `TriageResult`; it never returns raw JSON or a provider-specific response to the service. `TRIAGE_PROVIDER` selects the primary provider in the factory. The service owns orchestration: cache lookup, latency measurement, one fallback to rules, and persistence of `triaged_by`. A malformed LLM response is a provider failure, not a valid result. The rule provider is the always-available fallback; simulated triage is pinned in CI.

The cache key includes the active provider, exact `text` and `location` encoded unambiguously and hashed with SHA-256. It contains no readable complaint data. Cached values are validated against `TriageResult` on read, have a 24-hour Redis TTL, and keep the provider label that produced them. Switching the configured provider therefore cannot reuse another provider's result. Metrics count cache hits and misses. The cache does not become the source of truth for complaint records; PostgreSQL remains that source.

## Alternatives and consequences
Embedding HTTP calls and fallback in routes would make the frontend and HTTP layer depend on a particular provider. Putting provider selection into the frontend would expose configuration and duplicate backend authority. Keeping one protocol lets #45 add hosted and Ollama clients without changing routes or persistence. A Redis outage must not prevent a complaint from being submitted; the service treats it as a cache miss and proceeds through normal triage. Any cache hit skips provider inference but still creates a distinct complaint row with its own measured `triage_latency_ms`.

## Verification
Provider contract and fallback tests belong to #44; hosted and Ollama failure tests to #45; duplicate-input, cache TTL, corrupted-value and hit-rate tests to #46. The current issue also tests an injection attempt; the structured output is validated before a provider result reaches the service. The completed implementation must be checked against the decisions above before this ADR is considered evidence of behavior.

# ADR 0001 — Replaceable Triage Provider

## Status
Proposed

## Context
The assignment explicitly requires the triage implementation to be replaceable and resilient to rate limits, slowness, and incorrect responses.

## Decision
Use a `TriageProvider` interface with implementations for hosted LLM, Ollama, rules fallback, and simulated CI behavior.

## Consequences
- provider choice becomes configuration
- reliability belongs around the provider
- CI is deterministic

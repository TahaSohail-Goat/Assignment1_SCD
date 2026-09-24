# Phase 07 — AI Layer

## Read
- complete assignment AI section
- AI
- BACKEND
- CACHE
- SECURITY
- relevant provider documentation as needed

## Implement
Create a replaceable `TriageProvider` abstraction with:
- hosted LLM implementation
- Ollama implementation
- deterministic rules implementation
- deterministic simulated implementation for CI

Use the required `TriageResult` Pydantic schema.

Reliability contract:
- structured response request
- schema validation
- 10s timeout
- exactly one jittered retry for timeout/429/5xx
- no retry on 400
- safe rules fallback
- `triaged_by`
- 24h content-hash cache
- `triage_latency_ms`
- provider metadata
- prompt-injection guardrail and test
- deterministic CI
- PII/data-governance ADR

Before choosing a hosted provider, verify current official limits/privacy terms rather than copying stale notes.

## Gate
LLM unreliability is contained by surrounding engineering.

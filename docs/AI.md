# AI Engineering Contract

The AI provider is replaceable.

Required interface:
- `TriageResult`
- `TriageProvider`

Required provider paths:
- hosted LLM
- Ollama
- rule-based fallback
- simulated CI provider

Required reliability:
- structured output request
- Pydantic validation
- 10-second hard timeout
- one jittered retry for timeout/429/5xx
- no retry for 400
- rule fallback
- `triaged_by`
- 24-hour content-hash cache
- latency measurement
- prompt-injection protection
- deterministic CI
- PII/data-governance ADR

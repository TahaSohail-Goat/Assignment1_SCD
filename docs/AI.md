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

## Provider choices checked on 2026-09-25

The hosted implementation uses Groq's OpenAI-compatible chat endpoint with `openai/gpt-oss-20b`. Groq's [structured-output documentation](https://console.groq.com/docs/structured-outputs) lists this model for strict JSON-schema output, and its [free-plan limits page](https://console.groq.com/docs/rate-limits) currently lists **30 requests/minute, 1,000 requests/day, 8,000 tokens/minute, and 200,000 tokens/day** for it. Limits are account- and model-dependent and must be checked again before a live demo. Older `llama-3.1-8b-instant` examples in Groq documentation are stale for the free/developer tier: the [deprecation page](https://console.groq.com/docs/deprecations) says it was retired there on 2026-08-16. The provider requests strict JSON-schema output, then validates the returned object with `TriageResult` regardless.

Groq's [data controls](https://console.groq.com/docs/your-data) say inference data is not retained by default, but may be temporarily logged for reliability or abuse investigations for up to 30 days unless Zero Data Retention is enabled; usage metadata remains. ADR 0004 records the project's choice to use hosted mode only for synthetic demonstrations. No API key is logged or committed; `GROQ_API_KEY` is read from the environment.

The offline implementation calls Ollama's [`POST /api/chat`](https://docs.ollama.com/api/chat) with `stream: false` and a JSON schema in `format`, as documented in Ollama's [structured-output guide](https://docs.ollama.com/capabilities/structured-outputs). The default `gemma3:1b` is a [published 1B-parameter model](https://ollama.com/library/gemma3%3A1b); the default service URL is `http://ollama:11434` inside the deployment network. Provider methods make one call. `TriageService` owns the 10-second cutoff, the single jittered retry for typed timeout/429/5xx errors, and rules fallback.

The hosted-versus-offline latency and quality comparison has not been measured; record real runs in `docs/ENGINEERING-NOTES.md` when both services are available.

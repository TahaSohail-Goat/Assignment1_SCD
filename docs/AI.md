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

## Live comparison (2026-09-26, issue #112)

Artfever confirmed ZDR before hosted requests. Two uncached rounds of the same 12
synthetic cases used the production providers and unchanged timeout/retry/fallback
policy. Groq returned 24/24 valid model responses, with 24/24 category and 20/24
priority agreements against the predefined experiment labels; median service
latency was 663 ms. CPU-only `gemma3:1b` returned 22/24 valid responses and two
fallbacks; among valid responses, category agreement was 11/22 and priority 15/22,
with an 18,299.5 ms service median including retries. Labels are experiment
judgments, not assignment-prescribed urgency rules or a general accuracy benchmark.

The first live run exposed and fixed the Compose downloader's shell argument
splitting and Groq's rejection of the default urllib user-agent on this connection.
The hosted client now identifies itself as `CivicPulse/1.0`. Successful response
headers reported 1,000 requests/day and 8,000 tokens/minute; RPM/TPD remain the
published values above. All original failures, actual outputs, model identity,
memory/network evidence and live API checks are retained in the
[comparison report](evidence/provider-comparison-README.md). Both provider paths
were exercised through complaint creation, retrieval and provider metadata.
The app was restored to rules mode after measurement; Published demo and backup links are recorded in [final video evidence](evidence/submission-final-README.md).

# Engineering Notes

Answer the assignment's eight questions with references to your own repository files and line numbers.

1. Three laptop/CI differences and exact freezing lines.
2. CI/CD maturity ladder position and justification.
3. Exact build-once-deploy-many line and failure without it.
4. Meaning of "correct" for probabilistic triage and how CI stays deterministic.
5. Measured HPA lag and where the time went.
6. Why VPA is Off and how HPA/VPA can conflict.
7. Where the hosted-LLM calling service can live despite `internal: true`, and how the architecture resolves it.
8. One significant failure, initial mistaken belief, and exact diagnostic evidence.

Generic answers receive no credit; reference real files and lines.

## Hosted provider evidence (issue #45, 2026-09-25)

The chosen Groq model is `openai/gpt-oss-20b` in `backend/app/providers/triage/llm.py`. Groq's [rate-limit table](https://console.groq.com/docs/rate-limits) listed 30 requests/minute, 1,000 requests/day, 8,000 tokens/minute and 200,000 tokens/day on its free plan when checked on 2026-09-25. Its [structured-output guide](https://console.groq.com/docs/structured-outputs) lists this model for strict JSON-schema output. These are published limits, not a measurement against an Artfever account; a live quota check and hosted call are still pending. `docs/AI.md` records the data-control and Ollama sources as well.

The offline model is `gemma3:1b` in `backend/app/providers/triage/ollama.py`. No hosted-versus-Ollama latency or quality comparison has been run. When both services are available, use the same synthetic complaint set, record each category/priority and elapsed time, and report the actual values here.
## Redis volume decision (issue #43)

`compose.yaml` enables Redis AOF and mounts `redisdata` at `/data`. The stats and triage cache values can be rebuilt, but rebuilding them immediately after a restart adds database and provider load. The rate-limit counters matter more: losing them grants each caller a fresh allowance and can produce a burst against the hosted model. AOF with `appendfsync everysec` preserves recent counters across ordinary restarts, with up to roughly one second of acknowledged writes still at risk on a crash. The counter implementation and exact admission behavior are documented in `docs/CACHE.md` Job 2.

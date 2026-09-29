# OpenTelemetry trace evidence (ASG-BONUS-005, issue #131)

Captured locally on 2026-09-29 from the opt-in `tracing` Compose profile. A synthetic complaint
was submitted through the CivicPulse browser UI while `TRIAGE_PROVIDER=llm` used the configured
Groq provider. Jaeger recorded one trace, `2e956807f23334582490acecafd25206`, with these spans:

1. `civicpulse-browser` — `POST` client span;
2. `civicpulse-backend` — `POST /api/complaints` server span, linked through `traceparent`;
3. `civicpulse-backend` — `triage.provider`, tagged `llm:groq`.

[otel-trace.png](otel-trace.png) is the Jaeger UI view: it shows two services, depth three and
three spans. [otel-trace.json](otel-trace.json) is the raw Jaeger response for that trace. It has
no complaint text, location, contact details, provider request/response body, authorization
header or API key. Jaeger’s UI and OTLP receiver were published only on `127.0.0.1`.

The screenshot records a 387 ms trace and a 353.42 ms provider span from this one run. These are
observations, not a performance claim or benchmark.

# Triage operations and evidence

This file exists because assignment §5.7 names `docs/TRIAGE.md` without defining its contents. The team uses it as the operational and measurement companion to the AI requirements in `docs/AI.md` and the decisions in ADRs 0001 and 0004. It does not add a new assignment requirement.

## Provider modes

`TRIAGE_PROVIDER` selects the primary provider. The supported implementations are hosted LLM, Ollama, rules and simulated. CI uses simulated triage for deterministic results. Rules are the always-available fallback for a failed primary provider. The deployment default for real complaint data is offline Ollama or rules; hosted mode is for synthetic demonstrations under the conditions in [ADR 0004](adr/0004-pii-and-data-governance.md).

## What to measure

- Record the number of triage-cache hits and misses over a named test interval. Hit rate = hits / (hits + misses), with the denominator shown; never call an estimate a measurement.
- For a known duplicate complaint, compare the provider-call count before and after cache lookup and record the 24-hour TTL actually observed in Redis.
- Record `triage_latency_ms` from the API and the latest 20 outcomes from `/api/meta/providers`, including provider label and whether fallback occurred.
- Run the prompt-injection test with an untrusted instruction embedded in complaint text and record the validated category returned, not merely the prompt sent.
- For hosted versus Ollama comparisons, use the same synthetic inputs and record latency and classification outcome. The assignment asks for a measured trade-off, not a claim that one provider is always faster or better.

## Cache measurement, 2026-09-25

`backend/.venv/Scripts/pytest.exe -m "not integration" -q` passed 289 tests with 32 database tests deselected. In `test_duplicate_uses_one_inference_and_24_hour_ttl`, two sequential calls with the same synthetic text and location produced one cache miss, one hit, one provider call and a stored TTL of 86,400 seconds. The observed hit rate for that two-request in-memory run was **1 / (1 + 1) = 50%**. This measures the test interval only; a real Redis 7 workload hit rate remains to be measured in Compose.

The hosted-versus-offline comparison and a deployment privacy check are pending live services. Record exact commands, dates, input sets and outputs here when available.


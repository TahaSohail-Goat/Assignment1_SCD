# Live hosted versus offline triage — issue #112

> Follow-up, 2026-09-27: the video is now uploaded; [primary/backup links and verification](submission-final-README.md). Pending-video wording below describes the original capture date. #113/#114 and #116/#117 are merged; original raw evidence is preserved.

Requirements: ASG-AI-003/005/006/009/025, ASG-GEN-005. ASG-AI-025 is a recommended
measurement in the assignment; working provider paths are mandatory.

## Method fixed before measurement

`scripts/compare_triage.py` at `acadbe5` defines 12 synthetic cases, spanning all
six categories and three priorities, including one instruction-injection attempt.
The expected labels were written before either model ran. They are experiment
judgments, not a priority policy prescribed by the assignment or a human-reviewed
benchmark. Two rounds give 24 scored requests per provider. The first, separate
call is an unscored initial-load observation; it is not silently discarded.
The final capture runner is `1f84cf0` (adds safe HTTP status recording); the fixture
set is unchanged. Ollama ran at that revision. Groq's corrected run uses `6d5558b`,
whose only provider change is the hosted client identification header described below.

Both providers receive identical text/location and the same production system
prompt and schema. The runner calls the existing `TriageService` with no Redis
cache and no database writes. The normal 10-second **per-attempt** deadline, one
jittered retry and rules fallback remain enabled. Consequently a failed service
request can take approximately 20 seconds. All attempts, validated results,
fallback flags and service latency are retained. Quality scores use only actual
model successes; a rules fallback is never credited as a model answer. Groq calls
are sequential and spaced by ten seconds to limit quota consumption.

Model defaults: Groq `openai/gpt-oss-20b`, Ollama `gemma3:1b`. Default sampling
settings are unchanged. This compares the deployed provider configurations, not
equal-sized models or controlled inference hardware. Short synthetic cases and
two repetitions cannot establish population accuracy or stable tail latency.
Summary fidelity must be inspected in the recorded outputs; valid JSON alone
does not imply a correct summary. An initial call can include model loading and
network setup; scored calls reflect a warmed service unless otherwise recorded.

## Reproduction

Start Docker and the application with `TRIAGE_PROVIDER=rules`; enable Compose's
`offline` profile to download the pinned Ollama image and model. Only the one-shot
downloader uses the edge network. The serving Ollama container is internal-only.
The first download needs Internet; inference uses the persisted local model.

Copy the runner into the backend container and invoke it with Python's module
search path set to `/app`:

```text
docker compose cp scripts/compare_triage.py backend:/tmp/compare_triage.py
docker compose exec -T -e PYTHONPATH=/app backend python /tmp/compare_triage.py --provider ollama --source-sha <tested-source-sha>
docker compose exec -T -e PYTHONPATH=/app backend python /tmp/compare_triage.py --provider groq --source-sha <tested-source-sha> --zdr-confirmed
```

The Groq command requires a key already supplied securely through the backend
environment and operator confirmation of ZDR under ADR 0004. Never put the key
in the command. stdout contains JSON evidence; stderr contains progress. The
runner records only an allowlist of rate-limit response headers, never request
authorization headers. Only the synthetic fixtures are transmitted to Groq.

## Defects found by executing the live path

1. Both Compose files supplied a scalar command to `/bin/sh -c`. The installed
   Compose parser reduced it to `["ollama", "serve"]`, so the downloader exited
   successfully without fetching a model. `ollama list` was empty after that first
   startup. The fix passes the whole script as one argv element. The new two-file
   regression failed before the fix; all 33 container-file tests passed afterward.
   [Before/after command evidence](provider-comparison-downloader.json) retains
   the actual normalized arguments. The corrected one-shot download exited zero
   and installed the expected 815,319,791-byte model.
2. On this connection Groq rejected the default Python urllib client with HTTP 403.
   A read-only `/models` probe with the same key and `User-Agent: CivicPulse/1.0`
   returned 200 and confirmed `openai/gpt-oss-20b` was available. The hosted provider
   now identifies itself with that header; its request regression failed before
   the change and all 13 remote-provider tests passed afterward. The original run
   remains separate transport-failure evidence, not a model-quality result. The
   corrected Groq run repeats every fixed case. Existing processes retained their
   originally imported provider code; the failed and corrected Groq runs briefly
   overlapped, each sequential with ten-second spacing. The Ollama and Groq runs
   also partly overlapped; no simultaneous calls were made to the Ollama model.

## Offline environment

[Environment capture](provider-comparison-environment.json): Intel i7-11800H,
8 physical / 16 logical cores, 23.8 GiB host RAM; Docker VM about 11.6 GiB.
Ollama 0.34.0, `gemma3:1b` / Q4_K_M / 999.89M parameters, digest
`8648f39daa8fbf5b18c7b4e6a8fb4990c692751d49917417b8842ca5758e7ffc`.
CPU inference (`size_vram=0`), context 4096, container cap two CPUs / 3 GiB.
The two existing kind demo clusters were stopped, preserving their containers/data.
The normal four-service application stayed running. Ollama's only attached network
was the Docker network inspected as `internal=true`, with no external gateway.
This verifies the serving topology; the one-shot downloader necessarily used Internet.

Ollama's lifetime cgroup memory peak after the run was 1,062,825,984 bytes
(about 1.0 GiB, including charged page cache); a Docker working-set snapshot was
about 980 MiB. This is a short CPU-run measurement, not a memory guarantee for
larger contexts/models or concurrent requests.

## Published limits checked 2026-09-26

[Groq's limits page](https://console.groq.com/docs/rate-limits) lists the free-plan
`openai/gpt-oss-20b` limits as 30 RPM, 1,000 RPD, 8,000 TPM and 200,000 TPD.
Actual organization limits can differ. Response-header request limits refer to
requests per day; token limits refer to tokens per minute. Headers do not prove
the account's billing plan or every console setting.

[Groq's data documentation](https://console.groq.com/docs/your-data) and
[ADR 0004](../adr/0004-pii-and-data-governance.md) govern hosted use.

## Results

Captured 2026-09-26. The raw files include timestamps, every input, expected label,
validated output, retry/error class, latency and safe HTTP status/limit headers:
[Ollama](provider-comparison-ollama.json), [corrected Groq](provider-comparison-groq.json),
and [Groq before the client fix](provider-comparison-groq-before-fix.json).

| Measure | Groq `openai/gpt-oss-20b` | Ollama `gemma3:1b`, two CPU cores |
|---|---:|---:|
| Scored service requests | 24 | 24 |
| Valid model responses | 24/24 | 22/24 |
| Rules fallbacks | 0 | 2 |
| Category agreement, valid responses only | 24/24 (100%) | 11/22 (50%) |
| Priority agreement, valid responses only | 20/24 (83.3%) | 15/22 (68.2%) |
| Both labels agree, valid responses only | 20/24 (83.3%) | 9/22 (40.9%) |
| Model supplies both expected labels, all requests | 20/24 | 9/24 |
| Service median, including retry/fallback time | 663 ms | 18,299.5 ms |
| Service minimum / maximum | 302 / 1,079 ms | 9,302 / 20,425 ms |
| Separate initial call | 724 ms, model response | 17,709 ms, model response after retry |

In this setup, the median service response was about 27.6 times faster with Groq.
This includes network transit, validation and orchestration; it is not a pure
tokens-per-second model benchmark. Ollama's successful retry does not erase the
first timed-out attempt. Its two fallbacks were a timeout followed by malformed
output (water-high, round 1), and two timeouts (injection-high, round 1).

### Quality inspection and limitations

- Groq's four priority disagreements: library noticeboard `low` rather than the
  experiment's `normal` in both rounds; blank meter display `low` in round 2;
  broken streetlight `high` in round 2. Some are defensible judgments: the
  assignment does not define an exact urgency policy. They remain disagreements
  rather than silently changing the expected labels after seeing results.
- Ollama sometimes returned `water` for electrical problems, `roads` for a library
  noticeboard, and different categories across rounds. Its summaries could add
  unsupported details: "City officials report" and "underground testing zone"
  were absent from the corresponding complaints. One meter summary incorrectly
  asserted no apparent malfunction. These show why schema validity is insufficient.
- Both Groq injection responses and Ollama's one valid injection response returned
  `electricity/high`; the other Ollama injection request used rules fallback.
  This small example does not establish general prompt-injection immunity.
- These are assistant-authored synthetic labels, awaiting partner review, with
  no blinded human assessment and no statistical confidence claim. No new
  mandatory accuracy threshold or priority business rule is introduced.

The practical trade-off here is fast, stronger hosted classification with external
processing and quotas versus an internal-only, key-free local route that uses about
1 GiB RAM but is slower and less reliable on this two-core limit. We retain schema
validation, bounded retries, explicit fallback attribution and operator review of
results. This is evidence for this configuration, not a claim about every Ollama model.

### Account limits and application integration

The successful Groq headers actually reported `x-ratelimit-limit-requests=1000`
(RPD) and `x-ratelimit-limit-tokens=8000` (TPM), matching those two published values.
RPM/TPD remain published limits, not independently exhausted/verified. No billing
plan or ZDR setting is inferred from headers: ZDR was explicitly confirmed by
Artfever before hosted calls, and the key was supplied through the existing environment.

[API evidence](provider-comparison-api.json) records three separate synthetic POSTs,
all HTTP 201, subsequent GET agreement and matching `/api/meta/providers` entries:
the first Ollama POST fell back at 19,152 ms, its identical-input repeat returned
`llm:ollama` at 7,531 ms, and Groq returned `llm:groq` at 697 ms. Both Ollama results
are retained; none of these extra smoke requests contributes to the benchmark.
All five long-running Compose services were healthy. The smoke created three
clearly marked synthetic complaints; existing records were untouched.

After measurement the backend was restored to `rules`, the Ollama model was
unloaded from memory (image/model volume retained), and both pre-existing kind
clusters were restarted. The demo video remains on hold.

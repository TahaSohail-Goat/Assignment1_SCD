"""Prometheus metrics (docs/API_DESIGN.md, DQ-API-12).

One private registry, so tests and repeated app creation never register a metric twice.
``route`` is always the route template, never the raw path, to keep label cardinality bounded.
"""

from prometheus_client import CollectorRegistry, Counter, Histogram

REGISTRY = CollectorRegistry()

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "HTTP requests by method, route template and status",
    ["method", "route", "status"],
    registry=REGISTRY,
)
HTTP_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency by method and route template",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
    registry=REGISTRY,
)
TRIAGE_DURATION = Histogram(
    "triage_duration_seconds",
    "Triage latency by provider",
    ["provider"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 20, 30),
    registry=REGISTRY,
)
TRIAGE_FALLBACK = Counter(
    "triage_fallback_total",
    "Triage requests answered by the rule-based fallback",
    ["provider", "error_class"],
    registry=REGISTRY,
)
TRIAGE_CACHE = Counter(
    "triage_cache_total", "Triage content-hash cache lookups", ["result"], registry=REGISTRY
)
STATS_CACHE = Counter(
    "stats_cache_total", "Statistics cache lookups", ["result"], registry=REGISTRY
)
RATE_LIMITED = Counter(
    "rate_limited_total", "Requests refused with 429 by the rate limiter", registry=REGISTRY
)

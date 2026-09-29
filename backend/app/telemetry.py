"""Opt-in OpenTelemetry tracing without recording complaint content or secrets."""

from dataclasses import dataclass

from opentelemetry import propagate
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind, Tracer
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send


@dataclass(frozen=True)
class Telemetry:
    tracer: Tracer
    provider: TracerProvider


def configure(endpoint: str | None) -> Telemetry | None:
    if not endpoint:
        return None
    provider = TracerProvider(resource=Resource.create({"service.name": "civicpulse-backend"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    return Telemetry(provider.get_tracer("civicpulse.backend"), provider)


class TraceRequestMiddleware:
    def __init__(self, app: ASGIApp, tracer: Tracer) -> None:
        self.app = app
        self.tracer = tracer

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        context = propagate.extract(dict(Headers(scope=scope)))
        with self.tracer.start_as_current_span(
            f"{scope['method']} {scope['path']}", context=context, kind=SpanKind.SERVER
        ) as span:
            span.set_attribute("http.request.method", scope["method"])
            span.set_attribute("url.path", scope["path"])
            await self.app(scope, receive, send)

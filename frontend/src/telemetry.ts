import { ZoneContextManager } from '@opentelemetry/context-zone'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { resourceFromAttributes } from '@opentelemetry/resources'
import { BatchSpanProcessor, WebTracerProvider } from '@opentelemetry/sdk-trace-web'

const endpoint = import.meta.env.VITE_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT

if (endpoint) {
  const provider = new WebTracerProvider({
    resource: resourceFromAttributes({ 'service.name': 'civicpulse-browser' }),
    spanProcessors: [new BatchSpanProcessor(new OTLPTraceExporter({ url: endpoint }))],
  })
  provider.register({ contextManager: new ZoneContextManager() })
  registerInstrumentations({
    tracerProvider: provider,
    instrumentations: [new FetchInstrumentation({ propagateTraceHeaderCorsUrls: [/\/api\//] })],
  })
}

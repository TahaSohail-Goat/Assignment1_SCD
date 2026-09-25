# ADR 0002 — Frontend Runtime API Configuration

## Status
Accepted for frontend issue #34. The production nginx configuration is owned by #48.

## Context
The assignment requires build-once-deploy-many: a Vite build must not contain an environment-specific API URL (ASG-FR-016). It permits either a `/config.js` generated when the container starts or an nginx proxy for `/api` (ASG-FR-017). Browser bundles are public, so neither choice can carry secrets (ASG-FR-015, ASG-NFR-017).

## Decision
Use same-origin `/api` requests and an nginx `/api` reverse proxy. The client calls only relative paths in `frontend/src/api/client.ts`. Local Vite development uses the proxy in `frontend/vite.config.ts`. The production nginx route and service name will be added in #48, which owns `frontend/nginx.conf` and the container image.

This means one compiled frontend can be promoted between environments. Each environment changes only the nginx upstream at deployment; the browser fetches `/api/...` on the same origin from which it loaded the app. No API host, port, credential, or environment-specific URL is injected into static assets.

## Alternative considered
Generating `/config.js` at container start would also meet the assignment. It requires a startup script, safe JavaScript escaping for every value, and a public runtime configuration object. The proxy is simpler here and keeps the client independent of deployment hostnames. The proxy must preserve the API path, forward headers, and reach the backend by the container or Kubernetes service name, never `localhost`.

## Consequences and verification
Without a runtime mechanism, a Vite `import.meta.env` API URL is fixed when the bundle is built; promoting that same image to another environment points the browser at the wrong backend. The relative `/api` paths avoid that failure. `npm run build` followed by a search of `dist/` for absolute backend URLs and secret patterns checks the browser output. The full two-environment demonstration waits for the production nginx configuration in #48. The frontend type declarations are generated from the design OpenAPI snapshot until a backend `/openapi.json` exists. Set `OPENAPI_SCHEMA` to the backend schema path and run `npm run check:api-contract`; the check then compares the committed types to that schema and fails on drift.

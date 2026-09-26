#!/usr/bin/env bash
# The second command of the quickstart: put CivicPulse on a local Kubernetes cluster (kind).
#
#   bash scripts/k8s-up.sh
#
# Needs: docker, kind and kubectl on the PATH. It creates the cluster `civicpulse` if it does not
# exist, installs ingress-nginx, metrics-server and the VPA recommender, builds both images from
# this checkout, loads them into the cluster, creates the Secret out of band (a random password;
# nothing is written to the repository) and applies k8s/overlays/dev. It then seeds the database
# and answers through the Ingress. Remove everything with: kind delete cluster --name civicpulse
#
# INGRESS_PORT (default 8090) is the local port used to reach the Ingress. It is deliberately not
# 8080: the first quickstart command (docker compose up) publishes the frontend on 8080, and a
# smoke test that reached that stack instead of the cluster would prove nothing. The script fails
# at the start if the port is taken, and proves the smoke request went through the Ingress
# controller of this cluster by finding it in the controller's own access log.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

CLUSTER="${CLUSTER:-civicpulse}"
INGRESS_PORT="${INGRESS_PORT:-8090}"
NODE_IMAGE="${KIND_NODE_IMAGE:-kindest/node:v1.37.0}"
INGRESS_MANIFEST="https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.15.1/deploy/static/provider/kind/deploy.yaml"
METRICS_MANIFEST="https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.9.0/components.yaml"
VPA_BASE="https://raw.githubusercontent.com/kubernetes/autoscaler/vertical-pod-autoscaler-1.8.0/vertical-pod-autoscaler/deploy"

for tool in docker kind kubectl; do
  command -v "$tool" > /dev/null || { echo "missing tool: $tool" >&2; exit 1; }
done

port_in_use() { (exec 3<> "/dev/tcp/127.0.0.1/$1") 2> /dev/null; }
if port_in_use "$INGRESS_PORT"; then
  echo "local port $INGRESS_PORT is already in use (another service owns it); set INGRESS_PORT to a free port" >&2
  exit 1
fi

if ! kind get clusters | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER" --image "$NODE_IMAGE" --wait 120s
fi
kubectl config use-context "kind-$CLUSTER" > /dev/null
kubectl label node "$CLUSTER-control-plane" ingress-ready=true --overwrite

echo "== ingress-nginx, metrics-server, VPA recommender"
kubectl apply -f "$INGRESS_MANIFEST"
kubectl apply -f "$METRICS_MANIFEST"
# kind's kubelet certificate is not trusted by metrics-server: a local-cluster exception only.
kubectl -n kube-system patch deployment metrics-server --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]' || true
kubectl apply -f "$VPA_BASE/vpa-v1-crd-gen.yaml"
kubectl apply -f "$VPA_BASE/vpa-rbac.yaml"
kubectl apply -f "$VPA_BASE/recommender-deployment.yaml"
kubectl wait --for=condition=Established crd/verticalpodautoscalers.autoscaling.k8s.io --timeout=60s
kubectl -n ingress-nginx rollout status deployment/ingress-nginx-controller --timeout=180s
# The admission Job is deleted by upstream as soon as it finishes: wait for its lasting result.
kubectl wait --for=jsonpath='{.webhooks[0].clientConfig.caBundle}' \
  validatingwebhookconfiguration/ingress-nginx-admission --timeout=120s
kubectl -n kube-system rollout status deployment/metrics-server --timeout=120s

echo "== images"
docker build -t civicpulse-backend:dev backend
docker build -t civicpulse-frontend:dev frontend
kind load docker-image --name "$CLUSTER" civicpulse-backend:dev civicpulse-frontend:dev

echo "== namespace and Secret (out of band; the overlays never render the placeholder Secret)"
kubectl apply -f k8s/base/namespace.yaml
if ! kubectl -n civicpulse get secret civicpulse-secrets > /dev/null 2>&1; then
  kubectl -n civicpulse create secret generic civicpulse-secrets \
    --from-literal=POSTGRES_PASSWORD="$(openssl rand -hex 16)" \
    --from-literal=GROQ_API_KEY="unused"
fi

echo "== apply k8s/overlays/dev"
kubectl apply -k k8s/overlays/dev
kubectl -n civicpulse rollout status statefulset/database --timeout=180s
kubectl -n civicpulse rollout status deployment/cache --timeout=120s
kubectl -n civicpulse rollout status deployment/backend --timeout=240s
kubectl -n civicpulse rollout status deployment/frontend --timeout=120s

echo "== seed (30 synthetic complaints, idempotent)"
kubectl -n civicpulse exec deploy/backend -- python -m app.seed

echo "== smoke test through the Ingress on local port $INGRESS_PORT"
forward_log="$(mktemp)"
kubectl -n ingress-nginx port-forward service/ingress-nginx-controller "$INGRESS_PORT:80" > "$forward_log" 2>&1 &
forward_pid=$!
trap 'kill "$forward_pid" 2> /dev/null || true; rm -f "$forward_log"' EXIT
for _ in $(seq 30); do
  port_in_use "$INGRESS_PORT" && break
  kill -0 "$forward_pid" 2> /dev/null || { echo "the port-forward exited:" >&2; cat "$forward_log" >&2; exit 1; }
  sleep 1
done
port_in_use "$INGRESS_PORT" || { echo "the port-forward never started listening" >&2; exit 1; }
marker="k8s-up-smoke-$RANDOM$RANDOM"
curl -fsS --retry 20 --retry-delay 2 --retry-all-errors -H 'Host: civicpulse.local' \
  "http://127.0.0.1:$INGRESS_PORT/" | grep -qi '<html'
curl -fsS -H 'Host: civicpulse.local' "http://127.0.0.1:$INGRESS_PORT/api/stats?smoke=$marker"
echo
kill -0 "$forward_pid" 2> /dev/null || { echo "the port-forward died during the smoke test" >&2; exit 1; }
# The request must be in this cluster's Ingress controller log: a different service that happened
# to answer on the port would not be there.
kubectl -n ingress-nginx logs deploy/ingress-nginx-controller --tail=200 | grep -q "$marker" \
  || { echo "the smoke request did not pass through the Ingress controller of this cluster" >&2; exit 1; }
echo "confirmed in the Ingress controller log: $marker"
kubectl -n civicpulse get pods,hpa
echo "Ready. To browse: kubectl -n ingress-nginx port-forward service/ingress-nginx-controller $INGRESS_PORT:80"
echo "then open http://civicpulse.local:$INGRESS_PORT (add '127.0.0.1 civicpulse.local' to your hosts file)." # NOSONAR loopback

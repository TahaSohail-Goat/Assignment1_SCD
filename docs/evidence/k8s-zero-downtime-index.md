# Kubernetes rolling replacement evidence (#54)

Original captures (two runs, not new measurements):

- [Baseline summary](k8s-load-baseline50/summary.json), [rollout command](k8s-load-baseline50/set-image.txt), [rollout completion](k8s-load-baseline50/rollout-status.txt).
- [Adjusted summary](k8s-load-adjusted50/summary.json), [rollout command](k8s-load-adjusted50/set-image.txt), [rollout completion](k8s-load-adjusted50/rollout-status.txt).

Each complete run served 9,559 requests with zero HTTP failures and zero dropped iterations.
The timestamped metadata and samples place replacement during traffic. The new image tag
points to the same digest: this demonstrates pod replacement/connection draining, not changed
business behavior. Traffic traversed the frontend Service/nginx, not the ingress controller.
The [measurement method and failed attempts](k8s-load-README.md) state the limitations.
No video is claimed; both partners still need to record the required demo.

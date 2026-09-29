# Zero-downtime rolling update under live load (ASG-BONUS-001)

The assignment awards this optional bonus for a rolling update demonstrated under live load with
zero failed requests. The recorded experiments satisfy that condition without relying on an
edited screenshot:

| Capture | Live traffic | Rolling-update evidence | Result |
|---|---:|---|---|
| [baseline50](k8s-load-baseline50/) | 9,559 requests | [`set-image.txt`](k8s-load-baseline50/set-image.txt), [`rollout-status.txt`](k8s-load-baseline50/rollout-status.txt) | [`summary.json`](k8s-load-baseline50/summary.json): `http_req_failed = 0`, zero dropped iterations, checks = 1 |
| [adjusted50](k8s-load-adjusted50/) | 9,559 requests | [`set-image.txt`](k8s-load-adjusted50/set-image.txt), [`rollout-status.txt`](k8s-load-adjusted50/rollout-status.txt) | [`summary.json`](k8s-load-adjusted50/summary.json): `http_req_failed = 0`, zero dropped iterations, checks = 1 |
| [bonus128-20260929](k8s-load-bonus128-20260929/) | 9,559 requests | [`set-image.txt`](k8s-load-bonus128-20260929/set-image.txt), [`rollout-status.txt`](k8s-load-bonus128-20260929/rollout-status.txt) | [`summary.json`](k8s-load-bonus128-20260929/summary.json): `http_req_failed = 0`, zero dropped iterations, checks = 1; [terminal capture](k8s-load-bonus128-20260929/terminal-k6-rollout-summary.png) |

The in-cluster k6 pod started first. The capture helper issued `kubectl set image` at about
70 seconds while traffic continued. The replacement used a second tag of the same image digest,
deliberately isolating pod replacement and connection draining from application behavior.

The uploaded demo video shows scaling and rollback separately. It is not presented as proof of a
simultaneous rollout-under-load recording; the unedited command output and k6 summaries above are
the evidence for this optional bonus.

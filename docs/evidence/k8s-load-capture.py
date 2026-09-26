"""Capture actual k6/HPA measurements; never overwrite an earlier run.

Run from the repository root. Raw per-request k6 JSON stays outside Git in --raw-dir;
the committed CSV is a 10-second aggregation of http_reqs points from that file.
"""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--raw-dir", required=True)
parser.add_argument("--rate", default="50")
parser.add_argument("--hold", default="180s")
parser.add_argument("--rollout-image")
args = parser.parse_args()
out = Path("docs/evidence") / ("k8s-load-" + args.name)
out.mkdir()  # refuses to replace captured evidence
raw = Path(args.raw_dir) / (args.name + ".json")
kube = ["kubectl", "--context", "kind-civicpulse", "-n", "civicpulse"]


def capture(arguments, filename):
    result = subprocess.run(
        kube + arguments, capture_output=True, text=True, timeout=30
    )
    (out / filename).write_text(result.stdout + result.stderr, encoding="utf-8")
    return result


pod_name = "load-" + args.name
config_name = "workload-" + args.name
subprocess.run(
    kube + ["create", "configmap", config_name, "--from-file=load/k6-script.js"],
    check=True,
)
pod = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": pod_name, "namespace": "civicpulse"},
    "spec": {
        "restartPolicy": "Never",
        "containers": [
            {
                "name": "k6",
                "image": "grafana/k6:2.2.0",
                "command": [
                    "sh",
                    "-c",
                    "while [ ! -f /tmp/start ]; do sleep 1; done; k6 run --quiet --out json=/tmp/raw.json --summary-export /tmp/summary.json /scripts/k6-script.js; echo $? > /tmp/exit; sleep 3600",
                ],
                "env": [
                    {"name": "BASE_URL", "value": "http://frontend"},
                    {"name": "RATE", "value": args.rate},
                    {"name": "HOLD", "value": args.hold},
                ],
                "resources": {
                    "requests": {"cpu": "500m", "memory": "256Mi"},
                    "limits": {"cpu": "2", "memory": "1Gi"},
                },
                "volumeMounts": [
                    {"name": "workload", "mountPath": "/scripts", "readOnly": True}
                ],
            }
        ],
        "volumes": [{"name": "workload", "configMap": {"name": config_name}}],
    },
}
subprocess.run(
    kube + ["create", "-f", "-"], input=json.dumps(pod), text=True, check=True
)
subprocess.run(
    kube + ["wait", "--for=condition=Ready", "pod/" + pod_name, "--timeout=180s"],
    check=True,
)
capture(
    [
        "get",
        "deployment",
        "backend",
        "-o",
        "jsonpath={.spec.template.spec.containers[0].resources}",
    ],
    "requests-before.json",
)
started = datetime.now(timezone.utc)
metadata = {
    "started_utc": started.isoformat(),
    "rate": args.rate,
    "hold": args.hold,
    "context": "kind-civicpulse",
    "base_url": "http://frontend",
    "k6_image": "grafana/k6:2.2.0",
    "source_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip(),
    "workload_sha256": hashlib.sha256(
        Path("load/k6-script.js").read_bytes()
    ).hexdigest(),
    "rollout_image": args.rollout_image,
}
(out / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
with (
    (out / "hpa-watch.txt").open("w", encoding="utf-8") as watch_output,
    (out / "samples.jsonl").open("w", encoding="utf-8") as samples,
):
    watch = subprocess.Popen(
        kube + ["get", "hpa", "backend-hpa", "-w"],
        stdout=watch_output,
        stderr=subprocess.STDOUT,
    )
    subprocess.run(kube + ["exec", pod_name, "--", "touch", "/tmp/start"], check=True)
    clock_start = time.monotonic()
    rolled = False
    try:
        while True:
            finished = subprocess.run(
                kube + ["exec", pod_name, "--", "cat", "/tmp/exit"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            if finished.returncode == 0:
                metadata["k6_exit_code"] = int(finished.stdout.strip())
                break
            elapsed = time.monotonic() - clock_start
            observation = {
                "utc": datetime.now(timezone.utc).isoformat(),
                "elapsed_seconds": round(elapsed, 2),
            }
            for resource, name in [("hpa", "backend-hpa"), ("deployment", "backend")]:
                result = subprocess.run(
                    kube + ["get", resource, name, "-o", "json"],
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
                observation[resource] = (
                    json.loads(result.stdout).get("status", {})
                    if result.returncode == 0
                    else {"error": result.stderr}
                )
            samples.write(json.dumps(observation) + "\n")
            samples.flush()
            if args.rollout_image and elapsed >= 70 and not rolled:
                capture(
                    [
                        "set",
                        "image",
                        "deployment/backend",
                        "backend=" + args.rollout_image,
                    ],
                    "set-image.txt",
                )
                (out / "rollout-start-utc.txt").write_text(
                    datetime.now(timezone.utc).isoformat(), encoding="utf-8"
                )
                rolled = True
            time.sleep(5)
    finally:
        watch.terminate()
        watch.wait(timeout=10)
    metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()

capture(["logs", pod_name], "k6.txt")
subprocess.run(
    kube + ["cp", pod_name + ":/tmp/summary.json", str(out / "summary.json")],
    check=True,
)
subprocess.run(
    kube + ["cp", pod_name + ":/tmp/raw.json", os.path.relpath(raw)], check=True
)

capture(["describe", "vpa", "backend-vpa"], "vpa.txt")
capture(["top", "pods"], "top-pods.txt")
capture(["get", "pods", "-o", "wide"], "pods.txt")
capture(
    ["rollout", "status", "deployment/backend", "--timeout=20s"], "rollout-status.txt"
)
buckets = {}
with raw.open(encoding="utf-8") as raw_data:
    for line in raw_data:
        point = json.loads(line)
        if point.get("type") == "Point" and point.get("metric") == "http_reqs":
            timestamp = datetime.fromisoformat(
                point["data"]["time"].replace("Z", "+00:00")
            )
            bucket = int((timestamp - started).total_seconds() // 10) * 10
            buckets[bucket] = buckets.get(bucket, 0) + point["data"]["value"]
with (out / "requests-per-10s.csv").open("w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        ["seconds_since_start", "completed_requests", "requests_per_second"]
    )
    for second, count in sorted(buckets.items()):
        writer.writerow([second, count, count / 10])
metadata["raw_k6_sha256"] = hashlib.file_digest(raw.open("rb"), "sha256").hexdigest()
(out / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
print(json.dumps(metadata, indent=2))

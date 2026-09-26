"""Render the two completed captures. Requires matplotlib; no values are invented."""

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True, constrained_layout=True)
for axis, name in zip(axes, ["baseline50", "adjusted50"], strict=True):
    directory = root / ("k8s-load-" + name)
    samples = [
        json.loads(line)
        for line in (directory / "samples.jsonl").read_text().splitlines()
    ]
    metadata = json.loads((directory / "metadata.json").read_text())
    resources = json.loads((directory / "requests-before.json").read_text())
    seconds = [sample["elapsed_seconds"] for sample in samples]
    counts = [sample["hpa"].get("currentReplicas", 0) for sample in samples]
    axis.step(
        seconds,
        counts,
        where="post",
        color="#175ba6",
        label="Observed HPA replicas",
        linewidth=2,
    )
    axis.step(
        seconds,
        [s["hpa"].get("desiredReplicas", 0) for s in samples],
        where="post",
        color="#159895",
        linestyle=":",
        label="HPA desired replicas",
        linewidth=2,
    )
    axis.set_ylim(0, max(counts) + 1)
    axis.set_ylabel("Replicas")
    axis.set_title(
        f"{name}: CPU request {resources['requests']['cpu']}, memory {resources['requests']['memory']}"
    )
    axis.grid(alpha=0.2)
    rates = axis.twinx()
    rows = list(csv.DictReader((directory / "requests-per-10s.csv").open()))
    rates.plot(
        [float(r["seconds_since_start"]) + 5 for r in rows],
        [float(r["requests_per_second"]) for r in rows],
        color="#e08214",
        label="Completed requests/s (10s bins)",
    )
    hold = int(metadata["hold"].rstrip("s"))
    rates.plot(
        [0, 20, 21, 21 + hold, 22 + hold, 52 + hold],
        [10, 10, float(metadata["rate"]), float(metadata["rate"]), 10, 10],
        color="#6b6b6b",
        linestyle="--",
        label="Configured arrival rate",
    )
    rates.set_ylabel("Requests/s")
    rates.set_ylim(0, float(metadata["rate"]) * 1.3)
    handles1, labels1 = axis.get_legend_handles_labels()
    handles2, labels2 = rates.get_legend_handles_labels()
    axis.legend(handles1 + handles2, labels1 + labels2, loc="upper right", fontsize=8)
axes[-1].set_xlabel("Seconds since capture start (UTC timestamp in each metadata.json)")
fig.suptitle(
    "Measured backend scaling before and after applying the VPA recommendation"
)
fig.savefig(root / "k8s-load-comparison.png", dpi=180)

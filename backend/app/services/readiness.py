"""Readiness: PostgreSQL and Redis must both answer (ASG-FR-032, docs/API_DESIGN.md DQ-API-11).

The checks run concurrently and each has its own timeout, so ``/ready`` answers within one
probe timeout even when both dependencies are down. Nothing from an exception message is
returned to the caller (it could carry connection details); the exception is logged instead.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger("app.readiness")


class DependencyProbe(Protocol):
    name: str

    def check(self) -> None: ...


@dataclass(frozen=True)
class ReadinessReport:
    checks: dict[str, str]  # dependency name -> "ok" or the failure reason

    @property
    def ready(self) -> bool:
        return all(state == "ok" for state in self.checks.values())

    @property
    def failed(self) -> dict[str, str]:
        return {name: state for name, state in self.checks.items() if state != "ok"}


class ReadinessService:
    def __init__(self, probes: list[DependencyProbe], timeout_seconds: float = 1.0) -> None:
        self._probes = probes
        self._timeout = timeout_seconds
        self._executor = ThreadPoolExecutor(
            max_workers=max(1, len(probes)), thread_name_prefix="ready"
        )

    def run(self) -> ReadinessReport:
        futures = {self._executor.submit(probe.check): probe for probe in self._probes}
        done, _pending = wait(futures, timeout=self._timeout)
        checks: dict[str, str] = {}
        for future, probe in futures.items():
            if future not in done:
                checks[probe.name] = "timed out"
                logger.warning("dependency check timed out", extra={"dependency": probe.name})
                continue
            error = future.exception()
            if error is None:
                checks[probe.name] = "ok"
            else:
                checks[probe.name] = "unreachable"
                logger.warning(
                    "dependency check failed",
                    extra={"dependency": probe.name, "error_class": type(error).__name__},
                )
        return ReadinessReport(checks=checks)

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)

"""Choosing the provider from TRIAGE_PROVIDER (ASG-AI-004).

``PROVIDERS`` is the one registry: each entry builds a provider from the settings. The hosted
and Ollama providers add their entries when they are implemented (issue #45); until then their
names are refused at start with a message that lists what is available, instead of failing on
the first complaint.
"""

from collections.abc import Callable

from app.config import Settings
from app.providers.triage.base import TriageProvider
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


class UnknownProviderError(ValueError):
    pass


PROVIDERS: dict[str, Callable[[Settings], TriageProvider]] = {
    "rules": lambda settings: RuleBasedTriage(),
    "simulated": lambda settings: SimulatedTriage(),
}


def build_provider(name: str, settings: Settings) -> TriageProvider:
    try:
        builder = PROVIDERS[name.strip().lower()]
    except KeyError:
        available = ", ".join(sorted(PROVIDERS))
        raise UnknownProviderError(
            f"TRIAGE_PROVIDER={name!r} is not available; choose one of: {available}"
        ) from None
    return builder(settings)

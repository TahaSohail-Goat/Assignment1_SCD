"""RuleBasedTriage: the deterministic keyword fallback (ASG-AI-007).

Always available, never fails, no network, no randomness: the same text gives the same answer.
The keyword lists are this project's own design (the assignment fixes only that the provider
exists, is deterministic and never fails); they are plain data so they can be reviewed.
"""

import re

from app.domain import AI_SUMMARY_MAX, Category, Priority
from app.providers.triage.base import TriageResult

CATEGORY_KEYWORDS: dict[Category, tuple[str, ...]] = {
    Category.WATER: ("water", "pipe", "tap", "leak", "supply", "tanker", "hydrant"),
    Category.ELECTRICITY: (
        "electric",
        "power",
        "voltage",
        "transformer",
        "wire",
        "load shedding",
        "blackout",
        "meter",
    ),
    Category.SANITATION: (
        "garbage",
        "waste",
        "sewer",
        "sewage",
        "drain",
        "gutter",
        "trash",
        "dump",
        "sanitation",
        "stink",
        "smell",
    ),
    Category.ROADS: (
        "road",
        "pothole",
        "footpath",
        "pavement",
        "bridge",
        "traffic",
        "crossing",
        "asphalt",
    ),
    Category.STREETLIGHTS: ("streetlight", "street light", "lamp", "light pole", "dark street"),
}

HIGH_PRIORITY = (
    "danger",
    "urgent",
    "emergency",
    "fire",
    "electrocut",
    "live wire",
    "flood",
    "injur",
    "accident",
    "collapse",
    "sparking",
    "hospital",
    "school",
    "children",
    "child",
)
LOW_PRIORITY = ("minor", "small", "cosmetic", "suggestion", "whenever", "no hurry")


def _matches(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _summary(text: str) -> str:
    """The first sentence, on one line, cut to the limit of the assignment."""
    one_line = re.sub(r"\s+", " ", text).strip()
    first = re.split(r"(?<=[.!?])\s", one_line, maxsplit=1)[0]
    if len(first) > AI_SUMMARY_MAX:
        first = first[: AI_SUMMARY_MAX - 1].rstrip() + "…"
    return first or "Complaint"


class RuleBasedTriage:
    name = "rules"

    def triage(self, text: str, location: str) -> TriageResult:
        lowered = f"{text} {location}".lower()
        scores = {
            category: _matches(lowered, words) for category, words in CATEGORY_KEYWORDS.items()
        }
        best = max(scores.values())
        # Ties go to the category listed first, so the answer never depends on dict order.
        category = next((c for c in CATEGORY_KEYWORDS if scores[c] == best), Category.OTHER)
        if best == 0:
            category = Category.OTHER

        if _matches(lowered, HIGH_PRIORITY):
            priority = Priority.HIGH
        elif _matches(lowered, LOW_PRIORITY):
            priority = Priority.LOW
        else:
            priority = Priority.NORMAL

        confidence = 0.3 if best == 0 else 0.6 if best == 1 else 0.9
        return TriageResult(
            category=category, priority=priority, summary=_summary(text), confidence=confidence
        )

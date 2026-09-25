"""Domain values shared by every layer: the enums of assignment section 2.3.

The database columns, the API schemas and the services all use these, so the vocabulary
has one definition. Rules about *changing* a status live in the services layer.
"""

import re
from enum import StrEnum


class Category(StrEnum):
    WATER = "water"
    ELECTRICITY = "electricity"
    SANITATION = "sanitation"
    ROADS = "roads"
    STREETLIGHTS = "streetlights"
    OTHER = "other"


class Priority(StrEnum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class Status(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


# Lengths fixed by the assignment (section 2.3).
TEXT_MIN, TEXT_MAX = 10, 2000
LOCATION_MIN, LOCATION_MAX = 3, 200
AI_SUMMARY_MAX = 140

# triaged_by: the four values of section 2.3 plus `simulated` and `llm:<provider>`
# (docs/API_DESIGN.md, section 4). The same rule is a CHECK constraint in the database.
TRIAGED_BY_FIXED = ("rules", "rules:fallback", "simulated")
TRIAGED_BY_LLM = re.compile(r"llm:[a-z0-9][a-z0-9_.-]*")


def is_valid_triaged_by(value: str) -> bool:
    return value in TRIAGED_BY_FIXED or TRIAGED_BY_LLM.fullmatch(value) is not None

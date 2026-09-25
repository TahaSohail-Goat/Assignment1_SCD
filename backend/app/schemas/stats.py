"""The statistics body (docs/API_DESIGN.md, DQ-API-07).

Every category and priority is present, with 0 when there is none.
"""

from pydantic import BaseModel

from app.domain import Category, Priority


class Stats(BaseModel):
    total: int
    by_category: dict[Category, int]
    by_priority: dict[Priority, int]

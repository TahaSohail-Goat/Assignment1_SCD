"""GET /api/stats (ASG-FR-029): aggregates, cached, with the X-Cache header (ASG-CACHE-004)."""

from fastapi import APIRouter, Request, Response

from app.schemas.stats import Stats
from app.services.stats import StatsService

router = APIRouter(prefix="/api", tags=["stats"])


@router.get(
    "/stats",
    response_model=Stats,
    responses={
        200: {
            "headers": {
                "X-Cache": {
                    "description": "HIT if served from Redis, MISS if computed",
                    "schema": {"type": "string", "enum": ["HIT", "MISS"]},
                }
            }
        }
    },
)
def get_stats(request: Request, response: Response) -> Stats:
    service: StatsService = request.app.state.stats
    result = service.get()
    response.headers["X-Cache"] = result.cache
    return result.stats

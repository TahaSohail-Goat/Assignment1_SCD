"""The statistics service and its cache: hit, miss, TTL, invalidation, Redis down.

ASG-FR-029, ASG-CACHE-002 to ASG-CACHE-005. The TTL is tested with a clock the test moves by
hand, so nothing sleeps.
"""

import json

import pytest

from app.domain import Category, Priority
from app.services.complaints import ComplaintService, NewComplaintInput
from app.services.stats import CACHE_KEY, TTL_SECONDS, StatsService
from tests.fakes import FakeCache, FakeUnitOfWork, StubTriager

DATA = NewComplaintInput(
    text="Water has not reached our street for three days.",
    location="Street 5, Model Town",
    reporter_contact=None,
)


@pytest.fixture
def unit_of_work() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture
def cache() -> FakeCache:
    return FakeCache()


@pytest.fixture
def stats(unit_of_work: FakeUnitOfWork, cache: FakeCache) -> StatsService:
    return StatsService(unit_of_work, cache)


@pytest.fixture
def complaints(unit_of_work: FakeUnitOfWork, stats: StatsService) -> ComplaintService:
    return ComplaintService(unit_of_work, StubTriager(), after_create=stats.invalidate)


def test_the_ttl_is_thirty_seconds_and_the_key_is_versioned() -> None:
    assert TTL_SECONDS == 30
    assert CACHE_KEY == "stats:v1"


def test_the_first_call_is_a_miss_and_the_second_a_hit_with_an_identical_body(
    stats: StatsService, complaints: ComplaintService
) -> None:
    complaints.create(DATA)

    first = stats.get()
    second = stats.get()

    assert (first.cache, second.cache) == ("MISS", "HIT")
    assert first.stats == second.stats
    assert first.stats.total == 1


def test_a_miss_stores_the_result_with_the_thirty_second_ttl(
    stats: StatsService, cache: FakeCache
) -> None:
    stats.get()

    assert cache.sets == [(CACHE_KEY, 30)]


def test_every_category_and_priority_is_present_with_zero_when_empty(stats: StatsService) -> None:
    result = stats.get().stats

    assert result.total == 0
    assert set(result.by_category) == set(Category) and set(result.by_priority) == set(Priority)
    assert not any(result.by_category.values()) and not any(result.by_priority.values())


def test_after_a_new_complaint_the_next_call_is_a_miss_that_counts_it(
    stats: StatsService, complaints: ComplaintService, cache: FakeCache
) -> None:
    stats.get()  # cached: total 0
    assert stats.get().cache == "HIT"

    complaints.create(DATA)  # invalidates on write
    after = stats.get()

    assert after.cache == "MISS"
    assert after.stats.total == 1
    assert after.stats.by_category[Category.WATER] == 1
    assert cache.deletes == 1


def test_the_entry_expires_after_thirty_seconds_without_any_sleeping(
    stats: StatsService, cache: FakeCache
) -> None:
    stats.get()

    cache.advance(29.9)
    still_cached = stats.get().cache
    cache.advance(0.2)  # 30.1 seconds after the store
    expired = stats.get().cache

    assert (still_cached, expired) == ("HIT", "MISS")


def test_the_ttl_covers_a_lost_invalidation(unit_of_work: FakeUnitOfWork, cache: FakeCache) -> None:
    """Why both exist: if the delete is lost (Redis down at that moment), the TTL still ends
    the staleness at 30 seconds."""
    stats = StatsService(unit_of_work, cache)
    complaints = ComplaintService(unit_of_work, StubTriager(), after_create=stats.invalidate)
    stats.get()  # caches total 0
    cache.down = True
    complaints.create(DATA)  # the invalidation fails; the complaint is still created
    cache.down = False

    assert stats.get().stats.total == 0  # stale, served from the cache
    cache.advance(30.5)
    assert stats.get().stats.total == 1  # the TTL brought it back


def test_a_status_change_does_not_invalidate_the_counts_by_category_and_priority(
    stats: StatsService, complaints: ComplaintService, cache: FakeCache
) -> None:
    from app.domain import Status

    created = complaints.create(DATA)
    stats.get()
    deletes = cache.deletes

    complaints.change_status(str(created.id), Status.IN_PROGRESS)

    assert cache.deletes == deletes
    assert stats.get().cache == "HIT"


def test_when_redis_is_down_the_answer_comes_from_the_database_as_a_miss(
    stats: StatsService, complaints: ComplaintService, cache: FakeCache
) -> None:
    complaints.create(DATA)
    cache.down = True

    first = stats.get()
    second = stats.get()

    assert (first.cache, second.cache) == ("MISS", "MISS")
    assert first.stats.total == second.stats.total == 1


def test_creating_a_complaint_succeeds_when_the_invalidation_fails(
    complaints: ComplaintService, cache: FakeCache
) -> None:
    cache.down = True

    record = complaints.create(DATA)

    assert record.id is not None


def test_a_malformed_cache_entry_is_ignored_and_replaced(
    stats: StatsService, cache: FakeCache
) -> None:
    cache.set(CACHE_KEY, "{not json", 30)

    result = stats.get()

    assert result.cache == "MISS"
    assert json.loads(cache.get(CACHE_KEY) or "{}")["total"] == 0


def test_an_entry_of_the_wrong_shape_is_ignored(stats: StatsService, cache: FakeCache) -> None:
    cache.set(CACHE_KEY, json.dumps({"total": "many"}), 30)

    assert stats.get().cache == "MISS"

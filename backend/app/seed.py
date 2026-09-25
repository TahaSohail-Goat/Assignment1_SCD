"""Idempotent demo complaints: run `python -m app.seed` after Alembic migration."""

import os
import uuid

from app.database import create_db_engine, create_session_factory
from app.domain import Category, Priority
from app.repositories.complaints import NewComplaint, SqlComplaintRepository

SEED_NAMESPACE = uuid.UUID("2fcad73d-f7cb-4698-952c-c26416552a23")

# Synthetic places only. Each category has five complaints and all priorities occur.
SEED_ROWS: tuple[tuple[Category, Priority, str, str], ...] = (
    (
        Category.WATER,
        Priority.HIGH,
        "Main pipe burst near our gali, water is flowing since morning.",
        "Ward 2, Gali 4",
    ),
    (
        Category.WATER,
        Priority.NORMAL,
        "Tap water is very muddy after yesterday's repair, please check.",
        "Ward 5, Block B",
    ),
    (
        Category.WATER,
        Priority.LOW,
        "Public hand pump is leaking slowly, kindly send a mechanic.",
        "Ward 1, Bazaar Lane",
    ),
    (
        Category.WATER,
        Priority.HIGH,
        "No water in the whole mohalla for three days, tanks are empty.",
        "Ward 3, School Road",
    ),
    (
        Category.WATER,
        Priority.NORMAL,
        "Water pressure becomes very low every evening in our street.",
        "Ward 4, Canal Colony",
    ),
    (
        Category.ELECTRICITY,
        Priority.HIGH,
        "Electric wire is sparking above the bus stop, please come urgently.",
        "Ward 6, Bus Stop",
    ),
    (
        Category.ELECTRICITY,
        Priority.NORMAL,
        "Transformer keeps tripping at night and the lane goes dark.",
        "Ward 2, Gali 7",
    ),
    (
        Category.ELECTRICITY,
        Priority.LOW,
        "Meter box door at the public park is loose, kindly fix it.",
        "Ward 1, Park Gate",
    ),
    (
        Category.ELECTRICITY,
        Priority.HIGH,
        "Power pole is leaning after rain and may fall onto the road.",
        "Ward 5, Link Road",
    ),
    (
        Category.ELECTRICITY,
        Priority.NORMAL,
        "Street feeder has voltage fluctuation; fans stop again and again.",
        "Ward 3, Block C",
    ),
    (
        Category.SANITATION,
        Priority.HIGH,
        "Sewer is overflowing outside the clinic, dirty water is on the path.",
        "Ward 4, Clinic Street",
    ),
    (
        Category.SANITATION,
        Priority.NORMAL,
        "Garbage truck missed our gali twice this week, bags are piling up.",
        "Ward 2, Gali 2",
    ),
    (
        Category.SANITATION,
        Priority.LOW,
        "Dustbin lid at the market is broken, please replace when possible.",
        "Ward 1, Market Gate",
    ),
    (
        Category.SANITATION,
        Priority.HIGH,
        "Blocked drain is sending sewage into the school entrance.",
        "Ward 6, School Lane",
    ),
    (
        Category.SANITATION,
        Priority.NORMAL,
        "Open manhole smells badly near the community hall, kindly cover it.",
        "Ward 5, Hall Road",
    ),
    (
        Category.ROADS,
        Priority.HIGH,
        "Large pothole is making bikes fall at the main chowk after rain.",
        "Ward 3, Main Chowk",
    ),
    (
        Category.ROADS,
        Priority.NORMAL,
        "Road surface is broken near the bus stand; rickshaws move slowly.",
        "Ward 6, Bus Stand",
    ),
    (
        Category.ROADS,
        Priority.LOW,
        "Footpath tiles are uneven near the library, kindly repair them.",
        "Ward 1, Library Walk",
    ),
    (
        Category.ROADS,
        Priority.HIGH,
        "Bridge approach has a deep crack and traffic is swerving suddenly.",
        "Ward 4, Bridge Road",
    ),
    (
        Category.ROADS,
        Priority.NORMAL,
        "Rainwater has washed away the shoulder on our colony road.",
        "Ward 5, Canal Colony",
    ),
    (
        Category.STREETLIGHTS,
        Priority.HIGH,
        "All lights outside the hospital gate are off at night.",
        "Ward 2, Hospital Gate",
    ),
    (
        Category.STREETLIGHTS,
        Priority.NORMAL,
        "Three street lights in our gali have not worked since Eid.",
        "Ward 3, Gali 9",
    ),
    (
        Category.STREETLIGHTS,
        Priority.LOW,
        "One lamp at the park gate flickers, please inspect it.",
        "Ward 1, Park Gate",
    ),
    (
        Category.STREETLIGHTS,
        Priority.HIGH,
        "Dark crossing near the school needs its broken lights repaired.",
        "Ward 6, School Crossing",
    ),
    (
        Category.STREETLIGHTS,
        Priority.NORMAL,
        "Pole light near the vegetable bazaar turns off every evening.",
        "Ward 4, Vegetable Bazaar",
    ),
    (
        Category.OTHER,
        Priority.HIGH,
        "Public playground wall is falling toward the walking path.",
        "Ward 5, Playground",
    ),
    (
        Category.OTHER,
        Priority.NORMAL,
        "Stray animals are blocking the entrance to the public market.",
        "Ward 2, Market Road",
    ),
    (
        Category.OTHER,
        Priority.LOW,
        "Community notice board is damaged and papers fall in the rain.",
        "Ward 1, Community Hall",
    ),
    (
        Category.OTHER,
        Priority.HIGH,
        "Tree branch is hanging over the bus shelter after the storm.",
        "Ward 6, Shelter Lane",
    ),
    (
        Category.OTHER,
        Priority.NORMAL,
        "Public park gate is jammed, bachay cannot use the playground.",
        "Ward 3, Park Road",
    ),
)


def seed_items() -> list[NewComplaint]:
    """Fixed UUIDs make the same row safe to insert on every run."""
    return [
        NewComplaint(
            id=uuid.uuid5(SEED_NAMESPACE, text),
            text=text,
            location=location,
            reporter_contact=None,
            category=category,
            priority=priority,
            ai_summary=None,
            triaged_by="rules",
            triage_latency_ms=0,
        )
        for category, priority, text, location in SEED_ROWS
    ]


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required to run the seed")
    engine = create_db_engine(database_url)
    try:
        session_factory = create_session_factory(engine)
        with session_factory.begin() as session:
            inserted = SqlComplaintRepository(session).add_many_if_absent(seed_items())
    finally:
        engine.dispose()
    print(f"Seed complete: {inserted} new complaints; {len(SEED_ROWS)} defined")


if __name__ == "__main__":
    main()

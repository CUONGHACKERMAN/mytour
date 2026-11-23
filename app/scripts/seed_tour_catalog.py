"""
Seed tour categories and catalog services.

Usage (from repo root, with DATABASE_URL set):
  python -m app.scripts.seed_tour_catalog
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from schema.tour import Service, ServiceType, TourCategory

CATEGORIES = [
    ("Adventure", "Active outdoor and adventure experiences"),
    ("Luxury", "Premium stays and exclusive experiences"),
    ("Cultural", "Heritage, history, and local culture"),
    ("City Break", "Short urban getaways"),
    ("Eco Tour", "Nature-focused and sustainable travel"),
    ("Family", "Family-friendly itineraries"),
]

SERVICES = [
    ("3-Star Hotel", ServiceType.HOTEL, "Standard hotel accommodation"),
    ("4-Star Hotel", ServiceType.HOTEL, "Upscale hotel accommodation"),
    ("5-Star Resort", ServiceType.HOTEL, "Luxury resort stay"),
    ("Airport Pickup", ServiceType.TRANSFER, "Private airport arrival transfer"),
    ("Airport Drop-off", ServiceType.TRANSFER, "Private airport departure transfer"),
    ("Intercity Transport", ServiceType.TRANSFER, "Coach or van between destinations"),
    ("Breakfast Daily", ServiceType.MEAL, "Daily breakfast included"),
    ("Lunch Set Menu", ServiceType.MEAL, "Set lunch at local restaurants"),
    ("Dinner Banquet", ServiceType.MEAL, "Group dinner banquet"),
    ("City Walking Tour", ServiceType.ACTIVITY, "Guided walking tour of the city"),
    ("Boat Cruise", ServiceType.ACTIVITY, "Scenic boat cruise experience"),
    ("Cooking Class", ServiceType.ACTIVITY, "Hands-on local cooking class"),
    ("English Speaking Guide", ServiceType.GUIDE, "Licensed English-speaking tour guide"),
    ("Local Specialist Guide", ServiceType.GUIDE, "Local specialist for cultural sites"),
]


async def seed(session: AsyncSession) -> None:
    now = datetime.utcnow()

    existing_categories = {
        row.name
        for row in (
            await session.execute(
                select(TourCategory.name).where(TourCategory.deleted_at.is_(None))
            )
        ).scalars()
    }
    for name, description in CATEGORIES:
        if name in existing_categories:
            continue
        session.add(
            TourCategory(
                id=uuid.uuid4(),
                name=name,
                description=description,
                created_at=now,
                updated_at=now,
            )
        )

    existing_services = {
        row.name
        for row in (
            await session.execute(select(Service.name).where(Service.deleted_at.is_(None)))
        ).scalars()
    }
    for name, service_type, description in SERVICES:
        if name in existing_services:
            continue
        session.add(
            Service(
                id=uuid.uuid4(),
                name=name,
                service_type=service_type,
                description=description,
                created_at=now,
                updated_at=now,
            )
        )

    await session.commit()


async def main() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        await session.execute(text("SELECT 1"))
        await seed(session)
    await engine.dispose()
    print("Seeded tour categories and services.")


if __name__ == "__main__":
    asyncio.run(main())

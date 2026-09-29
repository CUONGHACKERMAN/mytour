from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from .repositories import (
    TourTemplateRepository,
    TourCategoryRepository,
    TourDepartureRepository,
)


class TourService:
    def __init__(self, session: AsyncSession):
        self.__template_repo = TourTemplateRepository(session)
        self.__category_repo = TourCategoryRepository(session)
        self.__departure_repo = TourDepartureRepository(session)

    async def create_template(self, template_data: dict) -> dict:
        created = await self.__template_repo.create(template_data)
        return created.to_dict()

    async def get_template_by_id(self, template_id: UUID) -> Optional[dict]:
        template = await self.__template_repo.find_one({"id": template_id})
        return template.to_dict() if template else None

    async def find_templates(self, filters: Dict[str, Any] = dict()) -> List[dict]:
        clean_filters = {k: v for k, v in filters.items() if v is not None}
        templates = await self.__template_repo.find_many(clean_filters)
        return [t.to_dict() for t in templates] if templates else []

    async def update_template(self, template_id: UUID, template_data: dict) -> Optional[dict]:
        clean_data = {k: v for k, v in template_data.items() if v is not None}
        if not clean_data:
            template = await self.__template_repo.find_one({"id": template_id})
            return template.to_dict() if template else None
        updated = await self.__template_repo.update(template_id, clean_data)
        return updated.to_dict() if updated else None

    async def delete_template(self, template_id: UUID) -> Optional[dict]:
        deleted = await self.__template_repo.delete({"id": template_id})
        return deleted.to_dict() if deleted else None

    async def create_category(self, category_data: dict) -> dict:
        created = await self.__category_repo.create(category_data)
        return created.to_dict()

    async def get_category_by_id(self, category_id: UUID) -> Optional[dict]:
        category = await self.__category_repo.find_one({"id": category_id})
        return category.to_dict() if category else None

    async def find_categories(self, filters: Dict[str, Any] = dict()) -> List[dict]:
        clean_filters = {k: v for k, v in filters.items() if v is not None}
        categories = await self.__category_repo.find_many(clean_filters)
        return [c.to_dict() for c in categories] if categories else []

    async def update_category(self, category_id: UUID, category_data: dict) -> Optional[dict]:
        clean_data = {k: v for k, v in category_data.items() if v is not None}
        if not clean_data:
            category = await self.__category_repo.find_one({"id": category_id})
            return category.to_dict() if category else None
        updated = await self.__category_repo.update(category_id, clean_data)
        return updated.to_dict() if updated else None

    async def delete_category(self, category_id: UUID) -> Optional[dict]:
        deleted = await self.__category_repo.delete({"id": category_id})
        return deleted.to_dict() if deleted else None

    async def create_departure(self, departure_data: dict) -> dict:
        created = await self.__departure_repo.create(departure_data)
        return created.to_dict()

    async def get_departure_by_id(self, departure_id: UUID) -> Optional[dict]:
        departure = await self.__departure_repo.find_one({"id": departure_id})
        return departure.to_dict() if departure else None

    async def find_departures(self, filters: Dict[str, Any] = dict()) -> List[dict]:
        clean_filters = {k: v for k, v in filters.items() if v is not None}
        departures = await self.__departure_repo.find_many(clean_filters)
        return [d.to_dict() for d in departures] if departures else []

    async def update_departure(self, departure_id: UUID, departure_data: dict) -> Optional[dict]:
        clean_data = {k: v for k, v in departure_data.items() if v is not None}
        if not clean_data:
            departure = await self.__departure_repo.find_one({"id": departure_id})
            return departure.to_dict() if departure else None
        updated = await self.__departure_repo.update(departure_id, clean_data)
        return updated.to_dict() if updated else None

    async def delete_departure(self, departure_id: UUID) -> Optional[dict]:
        deleted = await self.__departure_repo.delete({"id": departure_id})
        return deleted.to_dict() if deleted else None

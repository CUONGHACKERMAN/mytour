from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from .repositories import (
    TourTemplateRepository,
    TourCategoryRepository,
    TourDepartureRepository,
)
import re
import uuid

class TourService:
    def __init__(self, session: AsyncSession):
        self.__template_repo = TourTemplateRepository(session)
        self.__category_repo = TourCategoryRepository(session)
        self.__departure_repo = TourDepartureRepository(session)
    
    def _extract_prefix(self, name: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9]", "", name or "")
        if len(clean) >= 4:
            return clean[:4].upper()
        return clean.ljust(4, "A").upper()
    async def create_template(self, template_data: dict) -> dict:
        ### generate code
        template_id = template_data.get("id") or uuid.uuid4()
        template_data["id"] = template_id
        prefix = self._extract_prefix(template_data.get("name", "TOUR"))
        template_data["template_code"] = f"{prefix}_{template_id.hex[:6]}"
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
        deleted = await self.__template_repo.delete(template_id)
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
        deleted = await self.__category_repo.delete(category_id)
        return deleted.to_dict() if deleted else None

    async def create_departure(self, departure_data: dict) -> dict:
        # 1. Tìm template cha để lấy tiền tố hoặc tên tour
        parent_template = await self.__template_repo.find_one(
            {"id": departure_data["template_id"]}
        )
        if not parent_template:
            raise ValueError("Template not found")

        # Lấy prefix từ template_code có sẵn (VD: 'DANA_0ad9m1' -> 'DANA')
        # hoặc gọi self._extract_prefix(parent_template.name)
        prefix = parent_template.template_code.split("_")[0]

        # 2. Sinh UUID cho departure
        departure_id = departure_data.get("id") or uuid.uuid4()
        departure_data["id"] = departure_id

        # 3. Ghép mã code theo format: PREFIX_xxxxxx
        departure_data["code"] = f"{prefix}_{departure_id.hex[:6]}"

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
        deleted = await self.__departure_repo.delete(departure_id)
        return deleted.to_dict() if deleted else None

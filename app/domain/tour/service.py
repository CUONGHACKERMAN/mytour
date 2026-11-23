from typing import Dict, Any, List, Optional
from math import ceil
from uuid import UUID
from datetime import datetime
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncSession
from schema.tour import TourTemplate, TourTemplateService
from .repositories import (
    TourTemplateRepository,
    TourCategoryRepository,
    TourDepartureRepository,
    TourServiceCatalogRepository,
)
import json
import re
import uuid


class TourService:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__template_repo = TourTemplateRepository(session)
        self.__category_repo = TourCategoryRepository(session)
        self.__departure_repo = TourDepartureRepository(session)
        self.__service_repo = TourServiceCatalogRepository(session)

    def _extract_prefix(self, name: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9]", "", name or "")
        if len(clean) >= 4:
            return clean[:4].upper()
        return clean.ljust(4, "A").upper()

    @staticmethod
    def _encode_gallery_urls(urls: Optional[List[str]]) -> Optional[str]:
        if urls is None:
            return None
        cleaned = [str(url).strip() for url in urls if str(url).strip()]
        return json.dumps(cleaned)

    @staticmethod
    def _decode_gallery_urls(raw: Optional[str]) -> List[str]:
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(url) for url in parsed if str(url).strip()]
        except json.JSONDecodeError:
            # Backward-compatible fallback for comma/newline separated text
            return [part.strip() for part in re.split(r"[\n,]", raw) if part.strip()]
        return []

    def _prepare_template_scalar_fields(self, template_data: dict) -> dict:
        data = dict(template_data)
        if "gallery_image_urls" in data:
            data["gallery_image_urls"] = self._encode_gallery_urls(data.get("gallery_image_urls"))
        if "hero_image_url" in data and data["hero_image_url"] is not None:
            data["hero_image_url"] = str(data["hero_image_url"]).strip() or None
        return data

    def _serialize_template(self, template: TourTemplate) -> dict:
        data = template.to_dict()
        data["gallery_image_urls"] = self._decode_gallery_urls(
            getattr(template, "gallery_image_urls", None)
        )

        # Avoid lazy IO in async context (MissingGreenlet). Only read relations
        # that were already eagerly loaded (e.g. find_one_with_relations).
        state = sa_inspect(template)
        if "categories" in state.unloaded:
            data["categories"] = []
        else:
            categories = getattr(template, "categories", None) or []
            data["categories"] = [
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                }
                for category in categories
                if getattr(category, "deleted_at", None) is None
            ]

        if "services" in state.unloaded:
            data["services"] = []
        else:
            services = getattr(template, "services", None) or []
            data["services"] = []
            for link in services:
                if getattr(link, "deleted_at", None) is not None:
                    continue
                link_state = sa_inspect(link)
                service = None
                if "service" not in link_state.unloaded:
                    service = getattr(link, "service", None)
                data["services"].append(
                    {
                        "id": str(link.id),
                        "service_id": str(link.service_id),
                        "is_included": bool(link.is_included),
                        "service": None
                        if service is None
                        else {
                            "id": str(service.id),
                            "name": service.name,
                            "service_type": service.service_type.value
                            if hasattr(service.service_type, "value")
                            else str(service.service_type),
                            "description": service.description,
                        },
                    }
                )
        return data

    async def _sync_template_relations(
        self,
        template: TourTemplate,
        *,
        category_ids: Optional[List[UUID]] = None,
        services: Optional[List[dict]] = None,
    ) -> None:
        if category_ids is not None:
            categories = await self.__template_repo.find_categories_by_ids(category_ids)
            found_ids = {category.id for category in categories}
            missing = [str(cid) for cid in category_ids if cid not in found_ids]
            if missing:
                raise ValueError(f"Unknown category ids: {', '.join(missing)}")
            # Preserve requested order where possible
            by_id = {category.id: category for category in categories}
            template.categories = [by_id[cid] for cid in category_ids if cid in by_id]

        if services is not None:
            service_ids = [item["service_id"] for item in services]
            unique_ids = list(dict.fromkeys(service_ids))
            found_services = []
            for service_id in unique_ids:
                service = await self.__service_repo.find_one({"id": service_id})
                if service:
                    found_services.append(service)
            found_ids = {service.id for service in found_services}
            missing = [str(sid) for sid in unique_ids if sid not in found_ids]
            if missing:
                raise ValueError(f"Unknown service ids: {', '.join(missing)}")

            now = datetime.utcnow()
            for link in list(template.services or []):
                if link.deleted_at is None:
                    link.deleted_at = now

            for item in services:
                self.__session.add(
                    TourTemplateService(
                        id=uuid.uuid4(),
                        template_id=template.id,
                        service_id=item["service_id"],
                        is_included=bool(item.get("is_included", True)),
                    )
                )

        await self.__session.commit()

    async def create_template(self, template_data: dict) -> dict:
        category_ids = template_data.pop("category_ids", None)
        services = template_data.pop("services", None)
        template_data = self._prepare_template_scalar_fields(template_data)

        template_id = template_data.get("id") or uuid.uuid4()
        template_data["id"] = template_id
        prefix = self._extract_prefix(template_data.get("name", "TOUR"))
        template_data["template_code"] = f"{prefix}_{template_id.hex[:6]}"
        created = await self.__template_repo.create(template_data)

        detailed = await self.__template_repo.find_one_with_relations(created.id)
        if detailed is None:
            return created.to_dict()

        await self._sync_template_relations(
            detailed,
            category_ids=category_ids if category_ids is not None else [],
            services=services if services is not None else [],
        )
        refreshed = await self.__template_repo.find_one_with_relations(created.id)
        return self._serialize_template(refreshed) if refreshed else created.to_dict()

    async def get_template_by_id(self, template_id: UUID) -> Optional[dict]:
        template = await self.__template_repo.find_one_with_relations(template_id)
        if not template:
            return None
        return self._serialize_template(template)

    async def find_templates(
        self,
        filters: Dict[str, Any] = dict(),
        *,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        clean_filters = {k: v for k, v in filters.items() if v is not None}
        page = max(1, page)
        limit = max(1, min(limit, 100))
        total = await self.__template_repo.count(clean_filters)
        pages = ceil(total / limit) if total > 0 else 0
        if pages > 0 and page > pages:
            page = pages
        offset = (page - 1) * limit
        templates = await self.__template_repo.find_many(
            clean_filters, offset=offset, limit=limit
        )
        return {
            "items": [self._serialize_template(t) for t in templates] if templates else [],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }

    async def update_template(self, template_id: UUID, template_data: dict) -> Optional[dict]:
        category_ids = template_data.pop("category_ids", None)
        services = template_data.pop("services", None)
        clear_hero = "hero_image_url" in template_data
        template_data = self._prepare_template_scalar_fields(template_data)
        # Keep explicit None for internal_notes if provided; allow empty gallery list
        clean_data = {k: v for k, v in template_data.items() if v is not None}
        if clear_hero and "hero_image_url" not in clean_data:
            clean_data["hero_image_url"] = None

        if clean_data:
            updated = await self.__template_repo.update(template_id, clean_data)
            if not updated:
                return None

        detailed = await self.__template_repo.find_one_with_relations(template_id)
        if not detailed:
            return None

        if category_ids is not None or services is not None:
            await self._sync_template_relations(
                detailed,
                category_ids=category_ids,
                services=services,
            )
            detailed = await self.__template_repo.find_one_with_relations(template_id)
            if not detailed:
                return None

        return self._serialize_template(detailed)

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

    async def create_service(self, service_data: dict) -> dict:
        created = await self.__service_repo.create(service_data)
        return created.to_dict()

    async def get_service_by_id(self, service_id: UUID) -> Optional[dict]:
        service = await self.__service_repo.find_one({"id": service_id})
        return service.to_dict() if service else None

    async def find_services(self, filters: Dict[str, Any] = dict()) -> List[dict]:
        clean_filters = {k: v for k, v in filters.items() if v is not None}
        services = await self.__service_repo.find_many(clean_filters)
        return [s.to_dict() for s in services] if services else []

    async def update_service(self, service_id: UUID, service_data: dict) -> Optional[dict]:
        clean_data = {k: v for k, v in service_data.items() if v is not None}
        if not clean_data:
            service = await self.__service_repo.find_one({"id": service_id})
            return service.to_dict() if service else None
        updated = await self.__service_repo.update(service_id, clean_data)
        return updated.to_dict() if updated else None

    async def delete_service(self, service_id: UUID) -> Optional[dict]:
        deleted = await self.__service_repo.delete(service_id)
        return deleted.to_dict() if deleted else None

    async def create_departure(self, departure_data: dict) -> dict:
        parent_template = await self.__template_repo.find_one(
            {"id": departure_data["template_id"]}
        )
        if not parent_template:
            raise ValueError("Template not found")

        prefix = parent_template.template_code.split("_")[0]
        departure_id = departure_data.get("id") or uuid.uuid4()
        departure_data["id"] = departure_id
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

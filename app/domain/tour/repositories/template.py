from typing import Optional, List
from uuid import UUID
from core import BaseRepository
from schema.tour import TourTemplate, TourTemplateService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class TourTemplateRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(TourTemplate, session)
        self._session = session

    async def find_one_with_relations(self, template_id: UUID) -> Optional[TourTemplate]:
        stmt = (
            select(TourTemplate)
            .where(TourTemplate.id == template_id, TourTemplate.deleted_at.is_(None))
            .options(
                selectinload(TourTemplate.categories),
                selectinload(TourTemplate.services).selectinload(TourTemplateService.service),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_categories_by_ids(self, category_ids: List[UUID]):
        from schema.tour import TourCategory

        if not category_ids:
            return []
        stmt = select(TourCategory).where(
            TourCategory.id.in_(category_ids),
            TourCategory.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

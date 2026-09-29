from core import BaseRepository
from schema.tour import TourCategory
from sqlalchemy.ext.asyncio import AsyncSession


class TourCategoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(TourCategory, session)
        self._session = session

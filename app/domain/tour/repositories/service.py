from core import BaseRepository
from schema.tour import Service
from sqlalchemy.ext.asyncio import AsyncSession


class TourServiceCatalogRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Service, session)
        self._session = session

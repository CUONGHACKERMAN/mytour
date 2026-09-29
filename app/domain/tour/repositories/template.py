from core import BaseRepository
from schema.tour import TourTemplate
from sqlalchemy.ext.asyncio import AsyncSession


class TourTemplateRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(TourTemplate, session)
        self._session = session

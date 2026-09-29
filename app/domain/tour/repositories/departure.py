from core import BaseRepository
from schema.tour import TourDeparture
from sqlalchemy.ext.asyncio import AsyncSession


class TourDepartureRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(TourDeparture, session)
        self._session = session

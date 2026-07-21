from core import BaseRepository
from schema.user import Organization

class OrganizationRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Organization, session)

from core import BaseRepository
from schema.user import User

class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(User, session)

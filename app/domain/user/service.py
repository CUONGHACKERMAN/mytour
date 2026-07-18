from .user import UserRepository
from .organization import OrganizationRepository
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, session: AsyncSession):
        self.__user_repo = UserRepository(session)
        self.__organization_repo = OrganizationRepository(session)
    


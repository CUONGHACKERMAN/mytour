from .repositories import UserRepository, OrganizationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

class UserService:
    def __init__(self, session: AsyncSession):
        self.__user_repo = UserRepository(session)
        self.__organization_repo = OrganizationRepository(session)

    async def create_user(self, user_data: dict):
        created_user = await self.__user_repo.create(user_data)
        return created_user.to_dict()

    async def find_user_by_id(self, user_id: str):
        pass

    async def find_user(self, filters: Dict[str, Any]):
        pass

    async def update_user(self, user_data: dict):
        pass

    async def delete_user(self, user_id: str):
        pass

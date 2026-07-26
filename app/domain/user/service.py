from .repositories import UserRepository, OrganizationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from uuid import UUID

class UserService:
    def __init__(self, session: AsyncSession):
        self.__user_repo = UserRepository(session)
        self.__organization_repo = OrganizationRepository(session)

    async def create_user(self, user_data: dict):
        created_user = await self.__user_repo.create(user_data)
        return created_user.to_dict()

    async def update_user(self, user_id: UUID, user_data: dict):
        updated_user = await self.__user_repo.update(user_id, user_data)
        return updated_user.to_dict()

    async def find_user_by_id(self, user_id: str):
        pass

    async def find_user_by_email(self, email: str):
        user = await self.__user_repo.find_one({"email": email})
        return user.to_dict() if user else None

    async def find_user(self, filters: Dict[str, Any] = dict()):
        users = await self.__user_repo.find_many(filters)
        return [user.to_dict() for user in users]


    async def delete_user(self, user_id: str):
        pass

from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .service import UserService
from .dto import CreateUserDto, UpdateUserDto
from uuid import UUID

router = APIRouter(prefix='/user', tags=["User"])

def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)

@router.post(
    "/create-new-user",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: CreateUserDto,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(payload.model_dump())

@router.get(
    "/users",
    status_code=status.HTTP_200_OK
)
async def get_user(
    service: UserService = Depends(get_user_service)
):
    return await service.find_user()

@router.put(
    "/update-user/{user_id}",
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: UUID,
    payload: UpdateUserDto,
    service: UserService = Depends(get_user_service)
):
    return await service.update_user(user_id, payload.model_dump())

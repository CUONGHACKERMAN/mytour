from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .service import UserService
from core.database import get_db

router = APIRouter(prefix='/user', tags=["User"])

@router.post(
    "/create-new-user",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.create_user(payload)


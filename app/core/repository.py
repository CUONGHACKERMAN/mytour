from typing import Type, List, Optional, Any, Dict
from .database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from uuid import UUID
from datetime import datetime
class BaseRepository:
    def __init__(self, model: Type[Base], session: AsyncSession):
        self.__model = model
        self.__session = session

    async def create(self, item: Dict[str, Any]):
        db_obj = self.__model(**item)
        self.__session.add(db_obj)
        await self.__session.commit()
        await self.__session.refresh(db_obj)
        return db_obj

    async def find_one(self, filters: Dict[str, Any]) -> Optional[Any]:
        stmt = select(self.__model).filter_by(**filters, deleted_at=None)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_many(self, filters: Dict[str, Any]) -> Optional[List[Any]]:
        stmt = select(self.__model).filter_by(**filters, deleted_at=None)
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def update(self, item_id: UUID, item: Dict[str, Any]) -> Optional[Any]:
        stmt = (
            update(self.__model)
            .where(self.__model.id == item_id, self.__model.deleted_at.is_(None))
            .values(**item)
            .returning(self.__model)
        )
        result = await self.__session.execute(stmt)
        await self.__session.commit()
        return result.scalar_one_or_none()

    async def delete(self, item_id: UUID) -> Optional[Any]:
        stmt = (
            update(self.__model)
            .where(self.__model.id == item_id, self.__model.deleted_at.is_(None))
            .values(deleted_at=datetime.utcnow())
            .returning(self.__model)
        )
        result = await self.__session.execute(stmt)
        await self.__session.commit()
        return result.scalar_one_or_none()

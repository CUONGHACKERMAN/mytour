from .database import Base
import datetime
from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class DomainBaseModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
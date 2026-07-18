from core import DomainBaseModel
from sqlalchemy.ext.declarative import declared_attr
import uuid
from sqlalchemy import Uuid, String, Integer, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

class UserBase:
    @declared_attr
    def __table_args__(cls):
        return {"schema": "user"}
        
class User(UserBase, DomainBaseModel):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    memberships: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="user", cascade="all, delete-orphan"
    )

class Organization(UserBase, DomainBaseModel):
    __tablename__ = "organization"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)

    members: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="organization", cascade="all, delete-orphan"
    )

class Role(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class OrganizationMember(UserBase, DomainBaseModel):
    __tablename__ = "organization_member"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    role: Mapped[Role] = mapped_column(SAEnum(Role), default=Role.MEMBER, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.organization.id", ondelete = "CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.user.id", ondelete = "CASCADE"), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="members"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="memberships"
    )

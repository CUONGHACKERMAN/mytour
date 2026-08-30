import uuid
from typing import List, Optional
from datetime import date
from enum import Enum as PyEnum
from sqlalchemy import String, Text, Numeric, ForeignKey, Column, Table, Date, Enum as SAEnum, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from core import DomainBaseModel

class TourCategory(TourBase, DomainBaseModel):
    __tablename__ = "tour_category"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    templates: Mapped[List["TourTemplate"]] = relationship(
        secondary=template_category_assoc, back_populates="categories"
    )


class Destination(TourBase, DomainBaseModel):
    __tablename__ = "destination"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    templates: Mapped[List["TourTemplate"]] = relationship(
        secondary=template_destination_assoc, back_populates="destinations"
    )


class TourTemplate(TourBase, DomainBaseModel):
    __tablename__ = "tour_template"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)   
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    duration_days: Mapped[int] = mapped_column(nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[TourStatus] = mapped_column(SAEnum(TourStatus), default=TourStatus.DRAFT, nullable=False)
    
    inclusions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    exclusions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    categories: Mapped[List["TourCategory"]] = relationship(
        secondary=template_category_assoc, back_populates="templates"
    )
    destinations: Mapped[List["Destination"]] = relationship(
        secondary=template_destination_assoc, back_populates="templates"
    )
    departures: Mapped[List["TourDeparture"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )
    itinerary_days: Mapped[List["ItineraryDay"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )


class TourDeparture(TourBase, DomainBaseModel):
    __tablename__ = "tour_departure"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    
    # Notice the foreign key specifies the 'tour' schema explicitly
    template_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), nullable=False)
    
    start_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    max_capacity: Mapped[int] = mapped_column(nullable=False)
    current_bookings: Mapped[int] = mapped_column(default=0, nullable=False)

    template: Mapped["TourTemplate"] = relationship(back_populates="departures")


class ItineraryDay(TourBase, DomainBaseModel):
    __tablename__ = "itinerary_day"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), nullable=False)
    
    day_number: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    template: Mapped["TourTemplate"] = relationship(back_populates="itinerary_days")
    services: Mapped[List["TourService"]] = relationship(
        back_populates="itinerary_day", cascade="all, delete-orphan"
    )


class TourService(TourBase, DomainBaseModel):
    __tablename__ = "tour_service"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    itinerary_day_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tour.itinerary_day.id", ondelete="CASCADE"), nullable=False)
    
    service_type: Mapped[ServiceType] = mapped_column(SAEnum(ServiceType), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    itinerary_day: Mapped["ItineraryDay"] = relationship(back_populates="services")

class TourBase(DomainBaseModel):
    __abstract__ = True
    @declared_attr
    def __table_args__(cls):
        return {"schema": "tour"}
class TourStatus(str, PyEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class ServiceType(str, PyEnum):
    HOTEL = "HOTEL"
    TRANSFER = "TRANSFER"
    MEAL = "MEAL"
    ACTIVITY = "ACTIVITY"
    GUIDE = "GUIDE"


template_category_assoc = Table(
    "template_category",
    DomainBaseModel.metadata,
    Column("template_id", Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Uuid, ForeignKey("tour.tour_category.id", ondelete="CASCADE"), primary_key=True),
    schema="tour"
)

template_destination_assoc = Table(
    "template_destination",
    DomainBaseModel.metadata,
    Column("template_id", Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), primary_key=True),
    Column("destination_id", Uuid, ForeignKey("tour.destination.id", ondelete="CASCADE"), primary_key=True),
    schema="tour"
)
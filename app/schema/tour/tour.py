import uuid
from typing import List, Optional
from datetime import date
from sqlalchemy import String, Text, Numeric, ForeignKey, Column, Table, Date, Enum as SAEnum, Uuid, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .types import TourStatus, ServiceType
from .base import TourBase
from core import DomainBaseModel



class TourTemplate(TourBase):
    __tablename__ = "tour_template"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    template_code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    duration_days: Mapped[int] = mapped_column(nullable=False)
    total_days: Mapped[int] = mapped_column(nullable=False)
    total_nights: Mapped[int] = mapped_column(nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[TourStatus] = mapped_column(SAEnum(TourStatus), default=TourStatus.DRAFT, nullable=False)

    # TODO: Tour boundary type enum (e.g. TourBoundaryType):
    # - DOMESTIC: Domestic travelers within their home country
    # - INBOUND: Foreign travelers coming into the country (Destination Management Company / DMC)
    # - OUTBOUND: Local resident travelers traveling abroad
    # - CROSS_BORDER / REGIONAL: Tours spanning multiple international countries
    # boundary_type: Mapped[TourBoundaryType] = mapped_column(SAEnum(TourBoundaryType), nullable=False)

    internal_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    categories: Mapped[List["TourCategory"]] = relationship(
        secondary="tour.template_category", back_populates="templates"
    )
    departures: Mapped[List["TourDeparture"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )
    itinerary_days: Mapped[List["ItineraryDay"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )
    services: Mapped[List["TourTemplateService"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )

class TourCategory(TourBase):
    __tablename__ = "tour_category"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    templates: Mapped[List["TourTemplate"]] = relationship(
        secondary="tour.template_category", back_populates="categories"
    )

class TourDeparture(TourBase):
    __tablename__ = "tour_departure"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    # Notice the foreign key specifies the 'tour' schema explicitly
    template_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), nullable=False)

    start_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    # TODO: actual_price shouldn't be in departure, but in its own price table (tour_departure_price)
    actual_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    max_capacity: Mapped[int] = mapped_column(nullable=False)
    current_bookings: Mapped[int] = mapped_column(default=0, nullable=False)

    template: Mapped["TourTemplate"] = relationship(back_populates="departures")


class ItineraryDay(TourBase):
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


class TourService(TourBase):
    __tablename__ = "tour_service"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    itinerary_day_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tour.itinerary_day.id", ondelete="CASCADE"), nullable=False)

    service_type: Mapped[ServiceType] = mapped_column(SAEnum(ServiceType), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    itinerary_day: Mapped["ItineraryDay"] = relationship(back_populates="services")


class Service(TourBase):
    __tablename__ = "service"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    service_type: Mapped[ServiceType] = mapped_column(SAEnum(ServiceType), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    template_services: Mapped[List["TourTemplateService"]] = relationship(
        back_populates="service", cascade="all, delete-orphan"
    )


class TourTemplateService(TourBase):
    __tablename__ = "tour_template_service"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), nullable=False
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tour.service.id", ondelete="CASCADE"), nullable=False
    )
    is_included: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    template: Mapped["TourTemplate"] = relationship(back_populates="services")
    service: Mapped["Service"] = relationship(back_populates="template_services")




# template_category_assoc = Table(
#     "template_category",
#     DomainBaseModel.metadata,
#     Column("template_id", Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), primary_key=True),
#     Column("category_id", Uuid, ForeignKey("tour.tour_category.id", ondelete="CASCADE"), primary_key=True),
#     schema="tour"
# )

# template_destination_assoc = Table(
#     "template_destination",
#     DomainBaseModel.metadata,
#     Column("template_id", Uuid, ForeignKey("tour.tour_template.id", ondelete="CASCADE"), primary_key=True),
#     Column("destination_id", Uuid, ForeignKey("tour.destination.id", ondelete="CASCADE"), primary_key=True),
#     schema="tour"
# )

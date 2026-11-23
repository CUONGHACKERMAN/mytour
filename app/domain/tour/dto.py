from typing import Optional, Any, List
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from schema.tour import TourStatus, TourBoundaryType, CurrencyType, ServiceType


class PaginatedTourTemplatesDto(BaseModel):
    items: List[dict[str, Any]]
    total: int
    page: int
    limit: int
    pages: int


class TemplateServiceLinkDto(BaseModel):
    service_id: UUID = Field(..., description="Catalog service ID to attach")
    is_included: bool = Field(True, description="Whether the service is included in the tour")


class CreateTourTemplateDto(BaseModel):
    name: str = Field(..., max_length=200, description="Name of the tour template")
    duration_days: int = Field(..., gt=0, description="Duration of the tour in days")
    total_days: int = Field(..., gt=0, description="Total days")
    total_nights: int = Field(..., ge=0, description="Total nights")
    base_price: Decimal = Field(..., ge=0, description="Base price for the tour")
    status: TourStatus = Field(default=TourStatus.DRAFT, description="Tour status")
    boundary_type: TourBoundaryType = Field(..., description="Tour boundary type (DOMESTIC, INBOUND, OUTBOUND, CROSS_BORDER)")
    internal_notes: Optional[str] = Field(None, description="Internal notes for operations")
    currency_type: CurrencyType = Field(..., description="Currency type")
    hero_image_url: Optional[str] = Field(None, max_length=255, description="Hero image public URL")
    gallery_image_urls: List[str] = Field(
        default_factory=list,
        description="Gallery image public URLs",
    )
    category_ids: List[UUID] = Field(default_factory=list, description="Tour category IDs to attach")
    services: List[TemplateServiceLinkDto] = Field(
        default_factory=list,
        description="Services linked to this template",
    )


class UpdateTourTemplateDto(BaseModel):
    name: Optional[str] = Field(None, max_length=200, description="Name of the tour template")
    duration_days: Optional[int] = Field(None, gt=0, description="Duration of the tour in days")
    total_days: Optional[int] = Field(None, gt=0, description="Total days")
    total_nights: Optional[int] = Field(None, ge=0, description="Total nights")
    base_price: Optional[Decimal] = Field(None, ge=0, description="Base price for the tour")
    status: Optional[TourStatus] = Field(None, description="Tour status")
    boundary_type: Optional[TourBoundaryType] = Field(None, description="Tour boundary type")
    internal_notes: Optional[str] = Field(None, description="Internal notes for operations")
    currency_type: Optional[CurrencyType] = Field(None, description="Currency type")
    hero_image_url: Optional[str] = Field(None, max_length=255, description="Hero image public URL")
    gallery_image_urls: Optional[List[str]] = Field(
        None,
        description="Replace gallery image URLs when provided",
    )
    category_ids: Optional[List[UUID]] = Field(None, description="Replace attached category IDs when provided")
    services: Optional[List[TemplateServiceLinkDto]] = Field(
        None,
        description="Replace linked services when provided",
    )


class CreateTourCategoryDto(BaseModel):
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


class UpdateTourCategoryDto(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


class CreateServiceDto(BaseModel):
    name: str = Field(..., max_length=150, description="Service name")
    service_type: ServiceType = Field(..., description="Service type")
    description: Optional[str] = Field(None, description="Service description")


class UpdateServiceDto(BaseModel):
    name: Optional[str] = Field(None, max_length=150, description="Service name")
    service_type: Optional[ServiceType] = Field(None, description="Service type")
    description: Optional[str] = Field(None, description="Service description")


class CreateTourDepartureDto(BaseModel):
    template_id: UUID = Field(..., description="Associated tour template ID")
    start_date: date = Field(..., description="Start date of departure")
    end_date: date = Field(..., description="End date of departure")
    max_capacity: int = Field(..., gt=0, description="Maximum seating/booking capacity")

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date must be greater than or equal to start_date")
        return v


class UpdateTourDepartureDto(BaseModel):
    start_date: Optional[date] = Field(None, description="Start date of departure")
    end_date: Optional[date] = Field(None, description="End date of departure")
    max_capacity: Optional[int] = Field(None, gt=0, description="Maximum seating/booking capacity")

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, v: Optional[date], info) -> Optional[date]:
        if v is not None and "start_date" in info.data and info.data["start_date"] is not None:
            if v < info.data["start_date"]:
                raise ValueError("end_date must be in or after start_date")
        return v

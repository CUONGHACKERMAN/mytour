from typing import Optional
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from schema.tour import TourStatus, TourBoundaryType

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

class CreateTourCategoryDto(BaseModel):
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


class UpdateTourCategoryDto(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")


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

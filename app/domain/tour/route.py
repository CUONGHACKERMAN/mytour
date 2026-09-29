from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.tour import TourStatus, TourBoundaryType
from .service import TourService
from .dto import (
    CreateTourTemplateDto,
    UpdateTourTemplateDto,
    CreateTourCategoryDto,
    UpdateTourCategoryDto,
    CreateTourDepartureDto,
    UpdateTourDepartureDto,
)

router = APIRouter(prefix="/tour", tags=["Tour"])


def get_tour_service(session: AsyncSession = Depends(get_db)) -> TourService:
    return TourService(session)

@router.post(
    "/templates",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tour template"
)
async def create_template(
    payload: CreateTourTemplateDto,
    service: TourService = Depends(get_tour_service)
):
    return await service.create_template(payload.model_dump())


@router.get(
    "/templates",
    status_code=status.HTTP_200_OK,
    summary="List tour templates with optional filters"
)
async def get_templates(
    status_filter: Optional[TourStatus] = Query(None, alias="status", description="Filter by status (DRAFT, ACTIVE, CLOSED)"),
    boundary_type: Optional[TourBoundaryType] = Query(None, description="Filter by boundary type"),
    service: TourService = Depends(get_tour_service)
):
    filters = {}
    if status_filter:
        filters["status"] = status_filter
    if boundary_type:
        filters["boundary_type"] = boundary_type
    return await service.find_templates(filters)


@router.get(
    "/templates/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Get tour template details by ID"
)
async def get_template(
    template_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    template = await service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour template '{template_id}' not found"
        )
    return template


@router.put(
    "/templates/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a tour template"
)
async def update_template(
    template_id: UUID,
    payload: UpdateTourTemplateDto,
    service: TourService = Depends(get_tour_service)
):
    updated = await service.update_template(
        template_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour template '{template_id}' not found"
        )
    return updated


@router.delete(
    "/templates/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tour template"
)
async def delete_template(
    template_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    deleted = await service.delete_template(template_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour template '{template_id}' not found"
        )
    return {"message": "Tour template deleted successfully", "id": template_id}

@router.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    summary="Create a tour category"
)
async def create_category(
    payload: CreateTourCategoryDto,
    service: TourService = Depends(get_tour_service)
):
    return await service.create_category(payload.model_dump())


@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    summary="List all tour categories"
)
async def get_categories(
    service: TourService = Depends(get_tour_service)
):
    return await service.find_categories()


@router.get(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Get tour category by ID"
)
async def get_category(
    category_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    category = await service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour category '{category_id}' not found"
        )
    return category


@router.put(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a tour category"
)
async def update_category(
    category_id: UUID,
    payload: UpdateTourCategoryDto,
    service: TourService = Depends(get_tour_service)
):
    updated = await service.update_category(
        category_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour category '{category_id}' not found"
        )
    return updated


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tour category"
)
async def delete_category(
    category_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour category '{category_id}' not found"
        )
    return {"message": "Tour category deleted successfully", "id": category_id}

@router.post(
    "/departures",
    status_code=status.HTTP_201_CREATED,
    summary="Create a tour departure"
)
async def create_departure(
    payload: CreateTourDepartureDto,
    service: TourService = Depends(get_tour_service)
):
    template = await service.get_template_by_id(payload.template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour template '{payload.template_id}' not found"
        )
    return await service.create_departure(payload.model_dump())


@router.get(
    "/departures",
    status_code=status.HTTP_200_OK,
    summary="List tour departures, optionally filtered by template_id"
)
async def get_departures(
    template_id: Optional[UUID] = Query(None, description="Filter departures by tour template ID"),
    service: TourService = Depends(get_tour_service)
):
    filters = {}
    if template_id:
        filters["template_id"] = template_id
    return await service.find_departures(filters)


@router.get(
    "/departures/{departure_id}",
    status_code=status.HTTP_200_OK,
    summary="Get tour departure by ID"
)
async def get_departure(
    departure_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    departure = await service.get_departure_by_id(departure_id)
    if not departure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour departure '{departure_id}' not found"
        )
    return departure


@router.put(
    "/departures/{departure_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a tour departure"
)
async def update_departure(
    departure_id: UUID,
    payload: UpdateTourDepartureDto,
    service: TourService = Depends(get_tour_service)
):
    updated = await service.update_departure(
        departure_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour departure '{departure_id}' not found"
        )
    return updated


@router.delete(
    "/departures/{departure_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tour departure"
)
async def delete_departure(
    departure_id: UUID,
    service: TourService = Depends(get_tour_service)
):
    deleted = await service.delete_departure(departure_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tour departure '{departure_id}' not found"
        )
    return {"message": "Tour departure deleted successfully", "id": departure_id}

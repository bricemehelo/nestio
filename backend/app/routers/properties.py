# app/routers/properties.py
#
# PURPOSE: Defines all HTTP endpoints for the Property resource.
# This is the entry point for every property-related API request.
#
# LAYERED RULE: This layer handles HTTP only — status codes, request params,
# and responses. It knows nothing about database queries or business rules.
# It only calls the service layer and returns the result.
#
# PATTERN: Decorator — @router.get(), @router.post() etc. tell FastAPI
# which function handles which URL and HTTP method.

from fastapi import APIRouter, Depends, Query
from sqlachemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.property_service import PropertyService
from app.schemas.property import (
    PropertyCreate, 
    PropertyUpdate, 
    PropertyListResponse, 
    PropertyResponse 
)

# APIRouter groups all property routes together under the /properties prefix
# This router is registered in main.py — keeping routes modular and organised
router = APIRouter(
    prefix="/properties",
    tags=["properties"], # Groups endpoints together in /docs
)

def get_service(db: Session = Depends(get_db)) -> PropertyService:
    """
    Dependency function that creates a PropertyService instance per request.
    Depends(get_db) tells FastAPI to inject a fresh DB session automatically.
    The service receives the session and creates its own repository internally.
    """
    return PropertyService(db)

@router.get("/", response_model=PropertyListResponse)
def get_all_properties (
    skip: int = Query(default=0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of records to return"),
    city: Optional[str] = Query(default=None, description="Filter by city name"),
    property_type: Optional[str] = Query(default=None, description="Filter by type e.g. apartment, house"),
    status: Optional[str] = Query(default=None, description="Filter by status e.g. for_sale, for_rent"),
    search: Optional[str] = Query(default=None, description="Search across title and description"),
    min_price: Optional[float] = Query(default=None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(default=None, ge=0, description="Maximum price filter"),
    service: PropertyService = Depends(get_service),
):
    """
    Fetch all properties with optional filters and pagination.
    Used by the map view to load and filter property markers.
    """
    return service.get_all_properties(
        skip=skip,
        limit=limit,
        city=city,
        property_type=property_type,
        status=status,
        search=search,
        min_price=min_price,
        max_price=max_price,
    )

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property_by_id(
    property_id: int,
    service: PropertyService = Depends(get_service),
):
    """
    Fetch a single property by its ID.
    Used by the property detail page to load all information about a specific property.
    """
    return service.get_property_by_id(property_id)

@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(
    property_data: PropertyCreate,
    service: PropertyService = Depends(get_service),
):
    """
    Create a new property.
    Used by the admin panel to add new properties to the system.
    """
    return service.create_property(property_data)


@router.patch("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    service: PropertyService = Depends(get_service),
):
    """
    Partially update an existing property.
    PATCH is used instead of PUT — only send the fields you want to change.
    Returns 404 if the property does not exist.
    """
    return service.update_property(property_id, property_data)


@router.delete("/{property_id}", status_code=200)
def delete_property(
    property_id: int,
    service: PropertyService = Depends(get_service),
):
    """
    Delete a property by ID.
    Returns 404 if the property does not exist.
    Returns a confirmation message on success.
    """
    return service.delete_property(property_id)
# app/services/property_service.py
#
# PURPOSE: Handles all business logic for the Property resource.
# Sits between the router (HTTP layer) and the repository (database layer).
#
# LAYERED RULE: This layer knows about repositories and schemas only.
# It knows nothing about HTTP status codes, requests, or SQL queries.
#
# PATTERN: Service Layer — centralises business rules so they are never
# duplicated across routes. If a rule changes, it changes in one place.

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.property_repo import PropertyRepository
from app.schemas.property import HTTPException

from app.repositories.property_repo import PropertyRepository
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyListResponse, PropertyResponse
from typing import Optional


class PropertyService:
    """
    Service class for all Property business logic.
    Receives a SQLAlchemy Session and creates its own repository instance.
    """

    def __init__(self, db: Session):
        # Service creates the repository — the router only creates the service
        # This keeps the router clean — it never touches the repository directly
        self.repository = PropertyRepository(db)

    
    def get_all_properties(
        self,
        skip: int = 0,
        limit: int = 100,
        city: Optional[str] = None,
        property_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> PropertyListResponse:
        """
        Fetch all properties with optional filters.
        Business rule: limit cannot exceed 100 — prevents abuse and DB overload.
        """

        # Business rule — cap the limit regardless of what the client sends
        # A client requesting limit=10000 would be capped at 100
        if limit > 100:
            limit = 100

        properties, total = self.repository.get_all(
            skip=skip,
            limit=limit,
            city=city,
            property_type=property_type,
            status=status,
            search=search,
            min_price=min_price,
            max_price=max_price,
        )

        # Return a structured response with total count and list of properties
        return PropertyListResponse(total=total, properties=properties)

    def get_property_by_id(self, property_id: int) -> PropertyResponse:
        """
        Fetch a single property by ID.
        Business rule: raise 404 if not found — never return None to the router.
        """

        property = self.repository.get_by_id(property_id)

        # Business rule — if not found, raise an HTTP exception
        # The router catches this automatically and returns a 404 response
        # This is why the service imports HTTPException — it owns this decision
        if not property:
            raise HTTPException(
                status_code=404,
                detail=f"Property with id {property_id} not found"
            )

        return property

    def create_property(self, property_data: PropertyCreate) -> PropertyResponse:
        """
        Create a new property listing.
        Business rule: coordinates must be valid for map rendering.
        Pydantic already validates ranges but we add a meaningful error here.
        """

        # Business rule — coordinates are required for MapLibre map markers
        # Without valid coordinates the property cannot appear on the map
        if property_data.latitude == 0 and property_data.longitude == 0:
            raise HTTPException(
                status_code=422,
                detail="Invalid coordinates — latitude and longitude cannot both be zero"
            )

        return self.repository.create(property_data)

    def update_property(self, property_id: int, property_data: PropertyUpdate) -> PropertyResponse:
        """
        Update an existing property — partial update supported.
        Business rule: raise 404 if property does not exist.
        """

        # First confirm the property exists — raises 404 if not
        # We reuse get_property_by_id so the not-found rule lives in one place
        self.get_property_by_id(property_id)

        updated = self.repository.update(property_id, property_data)

        return updated

    def delete_property(self, property_id: int) -> dict:
        """
        Delete a property by ID.
        Business rule: raise 404 if property does not exist.
        Returns a confirmation message — never return the deleted object.
        """

        # Confirm exists first — raises 404 if not found
        self.get_property_by_id(property_id)

        self.repository.delete(property_id)

        # Return a simple confirmation — the deleted object no longer exists
        # so returning it would be misleading
        return {"message": f"Property {property_id} deleted successfully"}
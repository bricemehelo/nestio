# app/repositories/property_repo.py
#
# PURPOSE: Handles all database queries for the Property resource.
# This is the ONLY place in the application that directly touches PostgreSQL.
#
# PATTERN: Repository — wraps all data access behind a clean interface.
# The service layer calls methods on this class without knowing anything
# about SQLAlchemy, SQL syntax, or how the database is structured.
#
# LAYERED RULE: This layer knows about the database and models only.
# It knows nothing about HTTP, business rules, or API responses.

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate

class PropertyRepository:
    """
    Repository class for all Property database operations.
    Receives a SQLAlchemy Session via dependency injection —
    it does not create or manage the session itself.
    """

    def __init__(self, db: Session):
        # The session is injected — this class never opens or closes it.
        # Opening and closing is handled by the get_db() dependency in database.py.
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        city: Optional[str] = None,
        property_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> tuple[list[Property]]:
        """
        Fetch all properties with optional filtering and pagination.
        Returns a tuple of (list of properties, total count).
        The total count is used by the frontend to display "Showing X properties".
        """

        # Start with the base query for all properties
        query = self.db.query(Property)

        # Filter by city if provided — case-insensitive using ilike
        # ilike is PostgreSQL's case-insensitive LIKE — "lagos" matches "Lagos"
        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))

         # Filter by property type if provided — exact match
        if property_type:
            query = query.filter(Property.property_type == property_type)

        # Filter by status if provided — exact match e.g. "for_sale"
        if status:
            query = query.filter(Property.status == status)

        # Filter by search term if provided — case-insensitive using ilike
        if search:
            query = query.filter(
                or_(
                    Property.title.ilike(f"%{search}%"),
                    Property.description.ilike(f"%{search}%")
                )
            )

        # Filter by price range if provided
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)

        # Count total results BEFORE applying pagination
        # This gives the frontend the real total, not just the page size
        total = query.count()

        # Apply pagination — skip is the offset, limit is the page size
        # e.g. skip=0, limit=20 = first page. skip=20, limit=20 = second page
        properties = query.offset(skip).limit(limit).all()

        return properties, total
    
    def get_by_id(self, property_id: int) -> Optional[Property]:
        """
        Fetch a single property by its primary key.
        Returns None if not found — the service layer decides what to do with that.
        """
        return self.db.query(Property).filter(Property.id == property_id).first()

    def create(self, property_data: PropertyCreate) -> Property:
        """
        Insert a new property into the database.
        Accepts a validated Pydantic schema — converts it to a SQLAlchemy model.
        """

        # model_dump() converts the Pydantic schema to a plain Python dict
        # ** unpacks the dict as keyword arguments into the Property constructor
        db_property = Property(**property_data.model_dump())

        # Stage the new record — tells SQLAlchemy to prepare this INSERT
        self.db.add(db_property)

        # Commit the transaction — writes to PostgreSQL permanently
        self.db.commit()

        # Refresh the instance — fetches the DB-generated values back into the object
        # This is how we get the auto-generated id, created_at, updated_at
        self.db.refresh(db_property)

        return db_property

    def update(self, property_id: int, property_data: PropertyUpdate) -> Optional[Property]:
        """
        Update an existing property — partial update supported.
        Only updates fields that were actually sent in the request (not None).
        Returns None if the property does not exist.
        """

        db_property = self.get_by_id(property_id)

        # If property not found, return None — service layer handles the 404
        if not db_property:
            return None

        # model_dump(exclude_unset=True) returns only fields the client actually sent
        # This enables partial updates — sending just {"price": 500000} only
        # updates price, leaving all other fields untouched
        update_data = property_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_property, field, value)

        self.db.commit()
        self.db.refresh(db_property)

        return db_property

    def delete(self, property_id: int) -> bool:
        """
        Delete a property by ID.
        Returns True if deleted, False if not found.
        """

        db_property = self.get_by_id(property_id)

        if not db_property:
            return False

        self.db.delete(db_property)
        self.db.commit()

        return True
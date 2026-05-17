# app/models/property.py
# This file contains the Property model, which represents a real estate property in the application.
from sqlalchemy import Column, Integer, String, Text, Numeric, Float, DateTime
from sqlalchemy.sql import func

# Import Base from database.py — every model must inherit from this
# so SQLAlchemy can register it and map it to a table
from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    
    # --- Identity ---
    # Primary key — auto-incremented by PostgreSQL
    # index=True adds a DB index for faster lookups by ID
    id = Column(Integer, primary_key=True, index=True)

    # --- Core Details ---
    # title — short name for the listing e.g. "3 Bedroom Flat in Lekki"
    # nullable=False means this column is required — cannot be empty
    # index=True because we will search/filter by title
    title = Column(String(255), nullable=False, index=True)

    # description — longer text about the property
    # Text allows unlimited length unlike String which has a cap
    # nullable=True — description is optional on a listing
    description = Column(Text, nullable=True)

    # price — using Numeric for financial values, not Float
    # Float has floating point precision issues (e.g. 1000.00 becomes 999.9999...)
    # Numeric(12, 2) = up to 12 digits total, 2 decimal places — e.g. 999999999.99
    # nullable=False — every listing must have a price
    price = Column(Numeric(12, 2), nullable=False)

    # --- Location ---
    # address — full street address e.g. "12 Admiralty Way, Lekki Phase 1"
    address = Column(String(500), nullable=False)

    # city — used for filtering properties by city
    # index=True because filtering by city will be a common query
    city = Column(String(100), nullable=False, index=True)

    # latitude and longitude — critical for MapLibre GL JS map markers
    # Float is acceptable here — coordinate precision at Float level is
    # accurate to ~1cm which is more than enough for map pins
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # --- Classification ---
    # property_type — e.g. "apartment", "house", "land", "commercial"
    # index=True because users will filter by property type
    property_type = Column(String(50), nullable=False, index=True)

    # status — e.g. "for_sale", "for_rent", "sold", "rented"
    # index=True because filtering by status will be very common
    status = Column(String(50), nullable=False, index=True)

    # --- Metadata ---
    # created_at — automatically set to current timestamp when row is inserted
    # server_default=func.now() means PostgreSQL sets this, not Python
    # This is safer than Python's datetime.now() which depends on app server time
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # updated_at — automatically updated every time the row changes
    # onupdate=func.now() tells SQLAlchemy to refresh this on every UPDATE
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        # __repr__ gives a readable string when you print a Property instance
        # Useful for debugging — e.g. print(property) shows something meaningful
        return f"<Property id={self.id} title={self.title} city={self.city}>"

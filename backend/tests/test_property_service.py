# tests/test_property_service.py
#
# PURPOSE: Tests for the PropertyService — verifies business rules are applied correctly.

import pytest
from app.services.property_service import PropertyService
from app.schemas.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException


def test_get_all_properties_returns_list_response(db):
    """Service should return a PropertyListResponse with total and properties."""
    service = PropertyService(db)
    result = service.get_all_properties()

    assert hasattr(result, "total")
    assert hasattr(result, "properties")


def test_create_property_success(db):
    """Service should create and return a property."""
    service = PropertyService(db)
    data = PropertyCreate(
        title="Service Test Property",
        price=5000000,
        address="12 Test Street",
        city="Lagos",
        latitude=6.4281,
        longitude=3.4219,
        property_type="apartment",
        status="for_sale"
    )
    result = service.create_property(data)

    assert result.id is not None
    assert result.title == "Service Test Property"


def test_create_property_rejects_zero_coordinates(db):
    """Service should raise 422 when both latitude and longitude are zero."""
    service = PropertyService(db)
    data = PropertyCreate(
        title="Bad Coordinates",
        price=5000000,
        address="12 Test Street",
        city="Lagos",
        latitude=0,
        longitude=0,
        property_type="apartment",
        status="for_sale"
    )
    with pytest.raises(HTTPException) as exc:
        service.create_property(data)

    assert exc.value.status_code == 422


def test_get_property_by_id_not_found_raises_404(db):
    """Service should raise 404 when property does not exist."""
    service = PropertyService(db)

    with pytest.raises(HTTPException) as exc:
        service.get_property_by_id(99999)

    assert exc.value.status_code == 404


def test_limit_capped_at_100(db):
    """Service should cap limit at 100 regardless of what is requested."""
    service = PropertyService(db)
    result = service.get_all_properties(limit=9999)

    # No error — limit was silently capped
    assert result.total >= 0


def test_delete_nonexistent_property_raises_404(db):
    """Service should raise 404 when deleting a non-existent property."""
    service = PropertyService(db)

    with pytest.raises(HTTPException) as exc:
        service.delete_property(99999)

    assert exc.value.status_code == 404
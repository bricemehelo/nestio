# tests/test_property_repository.py
#
# PURPOSE: Tests for the PropertyRepository — verifies all DB queries work correctly.

from app.repositories.property_repo import PropertyRepository
from app.schemas.property import  PropertyCreate, PropertyUpdate

def test_create_property(db):
        """Repository should insert a property and return it with an auto-generated ID."""
        repo = PropertyRepository(db)
        property_in = PropertyCreate(
            title="Test Property",
            description="A lovely test property.",
            address="12 Test Street",
            city="Lagos",
            price=123456.78,
            latitude=6.5244,
            longitude=3.3792,
            property_type="Apartment",
            status="for_sale"
        )
        
        created_property = repo.create(property_in)

        assert created_property.id is not None
        assert created_property.title == property_in.title
        assert created_property.city == property_in.city

def test_get_all_properties(db):
        """Repository should return all properties with correct filtering."""
        repo = PropertyRepository(db)

        # Create multiple properties for testing
        properties = [
            PropertyCreate(
                title="Test Property 1",
                description="A lovely test property.",
                city="Lagos",
                address="13 Test Street",
                price=100000.00,
                latitude=6.5244,
                longitude=3.3792,
                property_type="Apartment",
                status="for_sale"
            ),
            PropertyCreate(
                title="Test Property 2",
                description="Another lovely test property.",
                city="Abuja",
                price=200000.00,
                address="14 Test Street",
                latitude=9.0578,
                longitude=7.4958,
                property_type="House",
                status="for_rent"
            )
        ]

        for prop in properties:
            repo.create(prop)

        # Test fetching all properties without filters
        all_properties, total = repo.get_all()
        assert total  == 2  # At least the two we just created

        # Test filtering by city
        lagos_properties, total_lagos = repo.get_all(city="Lagos")
        assert total_lagos == 1
        for prop in lagos_properties:
            assert "lagos" in prop.city.lower()
def test_get_by_id(db):
    """Repository should return the correct property by ID."""
    repo = PropertyRepository(db)
    data = PropertyCreate(
        title="Test Property",
        price=5000000,
        address="12 Test Street",
        city="Lagos",
        latitude=6.4281,
        longitude=3.4219,
        property_type="apartment",
        status="for_sale"
    )
    created = repo.create(data)
    result = repo.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id


def test_get_by_id_not_found(db):
    """Repository should return None for a non-existent ID."""
    repo = PropertyRepository(db)
    result = repo.get_by_id(99999)

    assert result is None


def test_update_property(db):
    """Repository should update only the provided fields."""
    repo = PropertyRepository(db)
    data = PropertyCreate(
        title="Original Title",
        price=5000000,
        address="12 Test Street",
        city="Lagos",
        latitude=6.4281,
        longitude=3.4219,
        property_type="apartment",
        status="for_sale"
    )
    created = repo.create(data)
    updated = repo.update(created.id, PropertyUpdate(title="Updated Title"))

    assert updated.title == "Updated Title"
    assert updated.price == created.price  # Unchanged fields stay the same


def test_delete_property(db):
    """Repository should delete a property and return True."""
    repo = PropertyRepository(db)
    data = PropertyCreate(
        title="Test Property",
        price=5000000,
        address="12 Test Street",
        city="Lagos",
        latitude=6.4281,
        longitude=3.4219,
        property_type="apartment",
        status="for_sale"
    )
    created = repo.create(data)
    result = repo.delete(created.id)

    assert result is True
    assert repo.get_by_id(created.id) is None


def test_delete_nonexistent_property(db):
    """Repository should return False when deleting a non-existent property."""
    repo = PropertyRepository(db)
    result = repo.delete(99999)

    assert result is False
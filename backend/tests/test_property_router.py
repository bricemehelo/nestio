# tests/test_property_router.py
#
# PURPOSE: Tests for the properties HTTP endpoints.
# Tests HTTP status codes, response shapes, and error handling.
# Uses FastAPI's TestClient — no real HTTP server needed.

def test_create_property_returns_201(client, sample_property_data):
    """POST /api/properties/ should return 201 and the created property."""
    response = client.post("/api/properties/", json=sample_property_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_property_data["title"]
    assert data["city"] == sample_property_data["city"]
    assert "id" in data  # Ensure the created property has an ID
    assert "created_at" in data  # Ensure the created property has a timestamp

def test_get_all_properties_returns_200(client, sample_property_data):
    """GET /api/properties/ should return 200 and a list with total count."""
    # First, create a property to ensure there's at least one in the database
    client.post("/api/properties/", json=sample_property_data)

    response = client.get("/api/properties/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data  # Should include total count
    assert "properties" in data  # Should include the list of properties
    assert data["total"] >= 1  # There should be at least one property

def test_get_property_by_id_return_200(client, sample_property_data):
    """GET /api/properties/{id} should return the correct property."""
    # First, create a property to get its ID
    created_property = client.post("/api/properties/", json=sample_property_data).json()

    response = client.get(f"/api/properties/{created_property['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_property["id"]

def test_get_property_not_found_returns_404(client):
    """GET /api/properties/{id} for a non-existent ID should return 404."""
    response = client.get("/api/properties/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert "Property with id 9999 not found" in data["detail"]

def test_update_property_returns_200(client, sample_property_data):
    """PATCH /api/properties/{id} should update and return the modified property."""
    created = client.post("/api/properties/", json=sample_property_data).json()

    response = client.patch(
        f"/api/properties/{created['id']}",
        json={"title": "Updated Title", "price": 6000000}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_property_returns_200(client, sample_property_data):
    """DELETE /api/properties/{id} should return 200 and delete the property."""
    # First, create a property to get its ID
    created_property = client.post("/api/properties/", json=sample_property_data).json()

    response = client.delete(f"/api/properties/{created_property['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data["message"]  # Ensure the response indicates deletion

    # Verify that the property is actually deleted
    get_response = client.get(f"/api/properties/{created_property['id']}")
    assert get_response.status_code == 404

def test_delete_nonexistent_property_returns_404(client):
    """DELETE /api/properties/99999 should return 404."""
    response = client.delete("/api/properties/99999")

    assert "not found" in response.json()["detail"]
    assert response.status_code == 404
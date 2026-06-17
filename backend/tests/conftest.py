# tests/conftest.py
#
# PURPOSE: Shared test configuration and fixtures for all pytest tests.
# Fixtures defined here are automatically available to every test file.
#
# conftest.py is pytest's convention for shared setup — no imports needed
# in test files to access these fixtures.

import pytest
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

load_dotenv()  # Load environment variables from .env file

# Separate test database so we never touch the development database in tests
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://lovehope@localhost:5432/nestio_test_db")

# Create a test engine pointing to the test database
test_engine = create_engine(TEST_DATABASE_URL)

#create a session factory for tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def db():
    """
    Creates a fresh database session for each test function.
    Drops and recreates all tables before each test — guarantees clean state.
    scope="function" means this runs fresh for every single test.
    """
    # Drop all tables and recreate — clean slate for every test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()
    try:
        yield session  # Provide the session to the test
    finally:
        session.close()  # Ensure the session is closed after the test

@pytest.fixture(scope="function")
def client(db):
    """
    Creates a FastAPI TestClient with the test database injected.
    Overrides the get_db dependency so the app uses the test DB, not the real one.
    """
    def override_get_db():
        try:
            yield db  # Use the test database session
        finally:
            pass  # Ensure the session is closed after the test

    # Override FastApi's database dependency with our test database session
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client  # Provide the test client to the test

    # Clean up the override after the test
    app.dependency_overrides.clear()

@pytest.fixture
def sample_property_data():
    """
    Reusable sample property data for creating test records.
    Centralised here so all test files use consistent data.
    """
    return {
        "title": "Test Property in Lagos",
        "description": "A test property for automated testing",
        "price": 5000000,
        "address": "12 Test Street, Lekki",
        "city": "Lagos",
        "latitude": 6.4281,
        "longitude": 3.4219,
        "property_type": "apartment",
        "status": "for_sale"
    }
 
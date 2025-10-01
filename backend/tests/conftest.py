import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from datetime import timedelta
import os


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(scope="session")
def admin_token():
    """Generate a test admin token."""
    token_data = {
        "sub": "test-admin-id",
        "email": "admin@test.com",
        "role": "admin"
    }
    return create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture(scope="session")
def employee_token():
    """Generate a test employee token."""
    token_data = {
        "sub": "test-employee-id",
        "email": "employee@test.com",
        "role": "employee"
    }
    return create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture
def admin_headers(admin_token):
    """Generate headers with admin authentication."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def employee_headers(employee_token):
    """Generate headers with employee authentication."""
    return {"Authorization": f"Bearer {employee_token}"}


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    os.environ.setdefault("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
    os.environ.setdefault("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
    os.environ.setdefault("SECRET_KEY", os.getenv("SECRET_KEY", "test-secret-key"))
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    yield


@pytest.fixture
def sample_customer_data():
    """Provide sample customer data for tests."""
    return {
        "dni": "12345678",
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-01-15",
        "gender": "male",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "address": "123 Test Street",
        "emergency_contact_name": "Jane Doe",
        "emergency_contact_phone": "+0987654321",
        "status": "active"
    }


@pytest.fixture
def sample_biometric_data():
    """Provide sample biometric data for tests."""
    return {
        "client_id": "test-client-id",
        "biometric_type": "face"
    }

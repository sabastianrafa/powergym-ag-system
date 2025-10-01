import pytest
from fastapi import status


@pytest.mark.auth
class TestAuthEndpoints:
    """Test suite for authentication endpoints."""

    def test_login_success(self, test_client):
        """Test successful login with valid credentials."""
        login_data = {
            "username": "admin@powergym.com",
            "password": "Admin123!"
        }

        response = test_client.post("/auth/login", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, test_client):
        """Test login with invalid credentials."""
        login_data = {
            "username": "invalid@test.com",
            "password": "wrongpassword"
        }

        response = test_client.post("/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_missing_fields(self, test_client):
        """Test login with missing required fields."""
        response = test_client.post("/auth/login", data={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_protected_endpoint_without_token(self, test_client):
        """Test accessing protected endpoint without authentication token."""
        response = test_client.get("/protected")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_invalid_token(self, test_client):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = test_client.get("/protected", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_valid_token(self, test_client, admin_headers):
        """Test accessing protected endpoint with valid authentication token."""
        response = test_client.get("/protected", headers=admin_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "user" in data

    def test_employee_access_to_employee_endpoint(self, test_client, employee_headers):
        """Test employee can access employee-level endpoints."""
        response = test_client.get("/customers", headers=employee_headers)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_access_to_admin_endpoint(self, test_client, admin_headers):
        """Test admin can access admin-level endpoints."""
        response = test_client.get("/customers", headers=admin_headers)

        assert response.status_code == status.HTTP_200_OK

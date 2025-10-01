import pytest
from fastapi import status
from io import BytesIO
from faker import Faker

fake = Faker()


@pytest.mark.biometrics
class TestBiometricEndpoints:
    """Test suite for biometric endpoints."""

    def test_list_biometrics_unauthorized(self, test_client):
        """Test listing biometrics without authentication."""
        response = test_client.get("/biometrics")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_biometrics_with_auth(self, test_client, employee_headers):
        """Test listing biometrics with valid authentication."""
        response = test_client.get("/biometrics", headers=employee_headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_list_biometrics_filter_by_client_id(self, test_client, employee_headers):
        """Test listing biometrics filtered by client_id."""
        client_id = "test-client-id"
        response = test_client.get(
            f"/biometrics?client_id={client_id}",
            headers=employee_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_list_biometrics_filter_by_type(self, test_client, employee_headers):
        """Test listing biometrics filtered by type."""
        response = test_client.get(
            "/biometrics?biometric_type=face",
            headers=employee_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_create_biometric_success(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test creating a biometric record with valid data."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"fake-image-content-for-testing")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "face"
        }

        response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["client_id"] == customer_id
        assert result["type"] == "face"
        assert "hash_checksum" in result
        assert result["is_active"] is True

    def test_create_biometric_invalid_type(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test creating biometric with invalid type."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"fake-image-content")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "invalid_type"
        }

        response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_biometric_customer_not_found(self, test_client, employee_headers):
        """Test creating biometric for non-existent customer."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        fake_image = BytesIO(b"fake-image-content")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": fake_id,
            "biometric_type": "face"
        }

        response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_biometric_missing_file(self, test_client, employee_headers):
        """Test creating biometric without file upload."""
        data = {
            "client_id": "test-client-id",
            "biometric_type": "face"
        }

        response = test_client.post(
            "/biometrics",
            data=data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_biometric_by_id(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test retrieving a specific biometric record by ID."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"fake-image-content-unique")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "fingerprint"
        }

        create_response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )
        biometric_id = create_response.json()["id"]

        response = test_client.get(
            f"/biometrics/{biometric_id}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == biometric_id
        assert result["client_id"] == customer_id

    def test_get_biometric_not_found(self, test_client, employee_headers):
        """Test retrieving a non-existent biometric record."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.get(
            f"/biometrics/{fake_id}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_biometric_success(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test updating a biometric record."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"original-image-content")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "face"
        }

        create_response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )
        biometric_id = create_response.json()["id"]
        original_hash = create_response.json()["hash_checksum"]

        updated_image = BytesIO(b"updated-image-content")
        updated_image.name = "updated.jpg"

        update_files = {"file": ("updated.jpg", updated_image, "image/jpeg")}

        response = test_client.put(
            f"/biometrics/{biometric_id}",
            files=update_files,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == biometric_id
        assert result["hash_checksum"] != original_hash

    def test_update_biometric_not_found(self, test_client, employee_headers):
        """Test updating a non-existent biometric record."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        fake_image = BytesIO(b"updated-image-content")
        fake_image.name = "updated.jpg"

        files = {"file": ("updated.jpg", fake_image, "image/jpeg")}

        response = test_client.put(
            f"/biometrics/{fake_id}",
            files=files,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_biometric_success(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test soft deleting a biometric record (setting is_active to false)."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"image-to-delete")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "face"
        }

        create_response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )
        biometric_id = create_response.json()["id"]

        response = test_client.delete(
            f"/biometrics/{biometric_id}",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = test_client.get(
            f"/biometrics/{biometric_id}",
            headers=employee_headers
        )
        assert get_response.json()["is_active"] is False

    def test_delete_biometric_not_found(self, test_client, admin_headers):
        """Test deleting a non-existent biometric record."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.delete(
            f"/biometrics/{fake_id}",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_biometric_without_admin_role(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test that non-admin users cannot delete biometric records."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"image-content")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "face"
        }

        create_response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )
        biometric_id = create_response.json()["id"]

        response = test_client.delete(
            f"/biometrics/{biometric_id}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_biometric_data_endpoint(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test retrieving biometric data including base64 encoded content."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        customer_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = customer_response.json()["id"]

        fake_image = BytesIO(b"biometric-data-content")
        fake_image.name = "test.jpg"

        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        data = {
            "client_id": customer_id,
            "biometric_type": "face"
        }

        create_response = test_client.post(
            "/biometrics",
            files=files,
            data=data,
            headers=employee_headers
        )
        biometric_id = create_response.json()["id"]

        response = test_client.get(
            f"/biometrics/{biometric_id}/data",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert "data" in result
        assert "hash_checksum" in result
        assert result["id"] == biometric_id
        assert result["client_id"] == customer_id

    def test_get_biometric_data_not_found(self, test_client, employee_headers):
        """Test retrieving data for non-existent biometric record."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.get(
            f"/biometrics/{fake_id}/data",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

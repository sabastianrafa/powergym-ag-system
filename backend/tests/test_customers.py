import pytest
from fastapi import status
from faker import Faker

fake = Faker()


@pytest.mark.customers
class TestCustomerEndpoints:
    """Test suite for customer CRUD endpoints."""

    def test_list_customers_unauthorized(self, test_client):
        """Test listing customers without authentication."""
        response = test_client.get("/customers")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_customers_with_auth(self, test_client, employee_headers):
        """Test listing customers with valid authentication."""
        response = test_client.get("/customers", headers=employee_headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_list_customers_with_pagination(self, test_client, employee_headers):
        """Test listing customers with pagination parameters."""
        response = test_client.get(
            "/customers?skip=0&limit=10",
            headers=employee_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10

    def test_create_customer_success(self, test_client, admin_headers, sample_customer_data):
        """Test creating a new customer with valid data."""
        unique_dni = fake.random_number(digits=8, fix_len=True)
        unique_email = fake.email()

        sample_customer_data["dni"] = str(unique_dni)
        sample_customer_data["email"] = unique_email

        response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["dni"] == str(unique_dni)
        assert data["email"] == unique_email
        assert data["first_name"] == sample_customer_data["first_name"]
        assert data["last_name"] == sample_customer_data["last_name"]
        assert "id" in data
        assert "created_at" in data

    def test_create_customer_without_admin_role(self, test_client, employee_headers, sample_customer_data):
        """Test that non-admin users cannot create customers."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_customer_missing_required_fields(self, test_client, admin_headers):
        """Test creating customer with missing required fields."""
        incomplete_data = {
            "first_name": "John"
        }

        response = test_client.post(
            "/customers",
            json=incomplete_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_customer_duplicate_dni(self, test_client, admin_headers, sample_customer_data):
        """Test creating customer with duplicate DNI."""
        unique_dni = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["dni"] = unique_dni
        sample_customer_data["email"] = fake.email()

        test_client.post("/customers", json=sample_customer_data, headers=admin_headers)

        sample_customer_data["email"] = fake.email()
        response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_customer_with_date_serialization(self, test_client, admin_headers, sample_customer_data):
        """Test creating customer with birth_date to verify date serialization fix."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()
        sample_customer_data["birth_date"] = "1995-06-15"

        response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "birth_date" in data
        assert data["birth_date"] == "1995-06-15"

    def test_get_customer_by_id(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test retrieving a specific customer by ID."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        response = test_client.get(
            f"/customers/{customer_id}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == customer_id
        assert data["dni"] == sample_customer_data["dni"]

    def test_get_customer_not_found(self, test_client, employee_headers):
        """Test retrieving a non-existent customer."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.get(
            f"/customers/{fake_id}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_customer_success(self, test_client, admin_headers, sample_customer_data):
        """Test updating customer information."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        update_data = {
            "phone": "+9999999999",
            "address": "456 New Address"
        }

        response = test_client.put(
            f"/customers/{customer_id}",
            json=update_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["phone"] == update_data["phone"]
        assert data["address"] == update_data["address"]

    def test_update_customer_with_date_serialization(self, test_client, admin_headers, sample_customer_data):
        """Test updating customer birth_date to verify date serialization fix."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        update_data = {
            "birth_date": "1992-03-20"
        }

        response = test_client.put(
            f"/customers/{customer_id}",
            json=update_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["birth_date"] == "1992-03-20"

    def test_update_customer_not_found(self, test_client, admin_headers):
        """Test updating a non-existent customer."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        update_data = {"phone": "+9999999999"}

        response = test_client.put(
            f"/customers/{fake_id}",
            json=update_data,
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_customer_without_admin_role(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test that non-admin users cannot update customers."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        update_data = {"phone": "+9999999999"}
        response = test_client.put(
            f"/customers/{customer_id}",
            json=update_data,
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_customer_success(self, test_client, admin_headers, sample_customer_data):
        """Test soft deleting a customer (status change to inactive)."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        response = test_client.delete(
            f"/customers/{customer_id}",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = test_client.get(
            f"/customers/{customer_id}",
            headers=admin_headers
        )
        assert get_response.json()["status"] == "inactive"

    def test_delete_customer_not_found(self, test_client, admin_headers):
        """Test deleting a non-existent customer."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.delete(
            f"/customers/{fake_id}",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_search_customers_by_name(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test searching customers by name."""
        unique_first_name = f"SearchTest{fake.random_number(digits=4)}"
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()
        sample_customer_data["first_name"] = unique_first_name

        test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )

        response = test_client.get(
            f"/customers/search?query={unique_first_name}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert any(c["first_name"] == unique_first_name for c in data)

    def test_search_customers_by_dni(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test searching customers by DNI."""
        unique_dni = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["dni"] = unique_dni
        sample_customer_data["email"] = fake.email()

        test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )

        response = test_client.get(
            f"/customers/search?query={unique_dni}",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert any(c["dni"] == unique_dni for c in data)

    def test_search_customers_missing_query(self, test_client, employee_headers):
        """Test search endpoint without query parameter."""
        response = test_client.get(
            "/customers/search",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_customer_biometrics(self, test_client, admin_headers, employee_headers, sample_customer_data):
        """Test retrieving biometrics for a specific customer."""
        sample_customer_data["dni"] = str(fake.random_number(digits=8, fix_len=True))
        sample_customer_data["email"] = fake.email()

        create_response = test_client.post(
            "/customers",
            json=sample_customer_data,
            headers=admin_headers
        )
        customer_id = create_response.json()["id"]

        response = test_client.get(
            f"/customers/{customer_id}/biometrics",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_get_customer_biometrics_not_found(self, test_client, employee_headers):
        """Test retrieving biometrics for non-existent customer."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = test_client.get(
            f"/customers/{fake_id}/biometrics",
            headers=employee_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

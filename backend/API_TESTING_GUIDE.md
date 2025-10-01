# API Testing Guide

This guide provides comprehensive documentation for testing the Gym Management System API endpoints.

## Table of Contents

1. [Setup](#setup)
2. [Authentication](#authentication)
3. [Customer Endpoints](#customer-endpoints)
4. [Biometric Endpoints](#biometric-endpoints)
5. [Subscription Endpoints](#subscription-endpoints)
6. [Payment Endpoints](#payment-endpoints)
7. [Attendance Endpoints](#attendance-endpoints)

## Setup

### Environment Configuration

Ensure your `.env` file contains the following variables:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running the API Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

### Login

**Endpoint:** `POST /auth/login`

**Request Body (form-data):**
```
username: admin@gym.com
password: admin123
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@gym.com&password=admin123"
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage:**
Use the `access_token` in the Authorization header for subsequent requests:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Customer Endpoints

### List All Customers

**Endpoint:** `GET /customers`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `skip` (optional, default: 0): Number of records to skip
- `limit` (optional, default: 100): Maximum number of records to return

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/customers?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Success Response (200 OK):**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "dni": "12345678",
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-01-15",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+0987654321",
    "status": "active",
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-01T10:00:00Z"
  }
]
```

### Search Customers

**Endpoint:** `GET /customers/search`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `query` (required): Search term (searches DNI, first name, last name, email)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/customers/search?query=John" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Customer by ID

**Endpoint:** `GET /customers/{customer_id}`

**Authentication:** Required (Employee or Admin)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/customers/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Customer

**Endpoint:** `POST /customers`

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
  "dni": "87654321",
  "first_name": "Jane",
  "last_name": "Smith",
  "birth_date": "1995-06-20",
  "gender": "female",
  "email": "jane.smith@example.com",
  "phone": "+1234567890",
  "address": "456 Oak Avenue",
  "emergency_contact_name": "John Smith",
  "emergency_contact_phone": "+0987654321",
  "status": "active"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "87654321",
    "first_name": "Jane",
    "last_name": "Smith",
    "birth_date": "1995-06-20",
    "gender": "female",
    "email": "jane.smith@example.com",
    "phone": "+1234567890",
    "address": "456 Oak Avenue",
    "emergency_contact_name": "John Smith",
    "emergency_contact_phone": "+0987654321",
    "status": "active"
  }'
```

**Success Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "dni": "87654321",
  "first_name": "Jane",
  "last_name": "Smith",
  "birth_date": "1995-06-20",
  "gender": "female",
  "email": "jane.smith@example.com",
  "phone": "+1234567890",
  "address": "456 Oak Avenue",
  "emergency_contact_name": "John Smith",
  "emergency_contact_phone": "+0987654321",
  "status": "active",
  "created_at": "2025-01-01T11:00:00Z",
  "updated_at": "2025-01-01T11:00:00Z"
}
```

### Update Customer

**Endpoint:** `PUT /customers/{customer_id}`

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
  "phone": "+9999999999",
  "address": "789 New Street",
  "status": "active"
}
```

**Example cURL:**
```bash
curl -X PUT "http://localhost:8000/customers/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+9999999999",
    "address": "789 New Street"
  }'
```

### Delete Customer (Soft Delete)

**Endpoint:** `DELETE /customers/{customer_id}`

**Authentication:** Required (Admin only)

**Example cURL:**
```bash
curl -X DELETE "http://localhost:8000/customers/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Success Response (204 No Content)**

### Get Customer Biometrics

**Endpoint:** `GET /customers/{customer_id}/biometrics`

**Authentication:** Required (Employee or Admin)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/customers/123e4567-e89b-12d3-a456-426614174000/biometrics" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Biometric Endpoints

### List All Biometrics

**Endpoint:** `GET /biometrics`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `client_id` (optional): Filter by customer ID
- `biometric_type` (optional): Filter by type (face, fingerprint)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/biometrics?biometric_type=face" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Biometric by ID

**Endpoint:** `GET /biometrics/{biometric_id}`

**Authentication:** Required (Employee or Admin)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/biometrics/123e4567-e89b-12d3-a456-426614174002" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Biometric

**Endpoint:** `POST /biometrics`

**Authentication:** Required (Employee or Admin)

**Request Body (multipart/form-data):**
- `client_id`: Customer UUID
- `biometric_type`: Type (face or fingerprint)
- `file`: Image file (max 10MB)

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/biometrics" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "client_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "biometric_type=face" \
  -F "file=@/path/to/face_image.jpg"
```

**Success Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174002",
  "client_id": "123e4567-e89b-12d3-a456-426614174000",
  "type": "face",
  "hash_checksum": "a3c5f7d9e2b4a6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6",
  "encryption_method": "SHA256",
  "is_active": true,
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z",
  "meta_info": null
}
```

### Update Biometric

**Endpoint:** `PUT /biometrics/{biometric_id}`

**Authentication:** Required (Employee or Admin)

**Request Body (multipart/form-data):**
- `file`: New image file (max 10MB)

**Example cURL:**
```bash
curl -X PUT "http://localhost:8000/biometrics/123e4567-e89b-12d3-a456-426614174002" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/new_face_image.jpg"
```

### Delete Biometric (Soft Delete)

**Endpoint:** `DELETE /biometrics/{biometric_id}`

**Authentication:** Required (Admin only)

**Example cURL:**
```bash
curl -X DELETE "http://localhost:8000/biometrics/123e4567-e89b-12d3-a456-426614174002" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Biometric Data

**Endpoint:** `GET /biometrics/{biometric_id}/data`

**Authentication:** Required (Employee or Admin)

**Description:** Returns the base64 encoded biometric data.

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/biometrics/123e4567-e89b-12d3-a456-426614174002/data" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Subscription Endpoints

### List Subscriptions

**Endpoint:** `GET /subscriptions`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `customer_id` (optional): Filter by customer ID
- `status_filter` (optional): Filter by status

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/subscriptions?status_filter=active" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Subscription

**Endpoint:** `POST /subscriptions`

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "plan_id": "123e4567-e89b-12d3-a456-426614174010",
  "start_date": "2025-01-01"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/subscriptions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "plan_id": "123e4567-e89b-12d3-a456-426614174010",
    "start_date": "2025-01-01"
  }'
```

## Payment Endpoints

### List Payments

**Endpoint:** `GET /payments`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `customer_id` (optional): Filter by customer ID
- `subscription_id` (optional): Filter by subscription ID

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/payments?customer_id=123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Payment

**Endpoint:** `POST /payments`

**Authentication:** Required (Employee or Admin)

**Request Body (JSON):**
```json
{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "subscription_id": "123e4567-e89b-12d3-a456-426614174020",
  "amount": 50.00,
  "payment_method": "cash",
  "payment_date": "2025-01-01T10:00:00Z",
  "status": "completed",
  "notes": "Monthly payment"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/payments" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "subscription_id": "123e4567-e89b-12d3-a456-426614174020",
    "amount": 50.00,
    "payment_method": "cash",
    "payment_date": "2025-01-01T10:00:00Z",
    "status": "completed"
  }'
```

## Attendance Endpoints

### List Attendances

**Endpoint:** `GET /attendances`

**Authentication:** Required (Employee or Admin)

**Query Parameters:**
- `customer_id` (optional): Filter by customer ID
- `date_filter` (optional): Filter by date (YYYY-MM-DD)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/attendances?date_filter=2025-01-01" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Today's Attendances

**Endpoint:** `GET /attendances/today`

**Authentication:** Required (Employee or Admin)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/attendances/today" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Attendance (Check-in)

**Endpoint:** `POST /attendances`

**Authentication:** Required (Employee or Admin)

**Request Body (JSON):**
```json
{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "check_in_time": "2025-01-01T08:00:00Z",
  "notes": "Regular check-in"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/attendances" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "check_in_time": "2025-01-01T08:00:00Z"
  }'
```

## Error Responses

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate entry (e.g., DNI or email already exists)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Example Error Response:
```json
{
  "detail": "Customer with this DNI or email already exists"
}
```

## Testing with Postman

### Import Collection

1. Open Postman
2. Click "Import"
3. Select "Raw text"
4. Copy the example requests from this guide
5. Set up environment variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: Your JWT token

### Authentication Setup

1. Send a login request to get your access token
2. In your collection, go to Authorization tab
3. Select "Bearer Token"
4. Use `{{access_token}}` as the token value

## Running Automated Tests

### Using pytest

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_customers.py

# Run tests with specific marker
pytest -m auth
pytest -m customers
pytest -m biometrics

# Run tests with verbose output
pytest -v

# Run tests and show print statements
pytest -s
```

### Test Coverage

The test suite covers:
- Authentication and authorization
- Customer CRUD operations
- Date serialization fixes
- Biometric data management
- Search functionality
- Pagination
- Error handling
- Role-based access control

## Notes

- All date fields should be in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- The date serialization bug has been fixed in customer endpoints
- File uploads for biometrics must be less than 10MB
- Soft deletes are used for customers and biometrics (status changes, not actual deletion)
- Admin tokens are required for create, update, and delete operations
- Employee tokens can access read operations

# Testing Guide

This document provides instructions for running tests on the Gym Management System API.

## Overview

The testing suite includes:
- **Pytest-based unit and integration tests** for automated testing
- **Manual testing documentation** with cURL examples
- **Automated test runner script** for quick endpoint verification

## Prerequisites

Install testing dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Running Pytest Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Authentication tests
pytest tests/test_auth.py

# Customer endpoint tests
pytest tests/test_customers.py

# Biometric endpoint tests
pytest tests/test_biometrics.py
```

### Run Tests by Marker

```bash
# Run only authentication tests
pytest -m auth

# Run only customer tests
pytest -m customers

# Run only biometric tests
pytest -m biometrics
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Print Statements

```bash
pytest -s
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=html
```

## Using the Automated Test Runner

The automated test runner (`test_runner.py`) provides a quick way to test all endpoints with colored console output.

### Basic Usage

```bash
# Run with default URL (http://localhost:8000)
python test_runner.py

# Run with custom URL
python test_runner.py http://your-server:8000
```

### Features

- Colored console output (green for pass, red for fail)
- Sequential endpoint testing
- Automatic test customer creation and cleanup
- Summary report with success rate
- Failed test details

### Example Output

```
======================================================================
                 GYM MANAGEMENT SYSTEM API TESTER
======================================================================

Base URL: http://localhost:8000
Date: 2025-01-01 10:00:00

>>> Testing Authentication
[PASS] Login with valid credentials
      Token obtained
[PASS] Login with invalid credentials
      Status: 401
[PASS] Access protected endpoint
      Status: 200

>>> Testing Customer Endpoints
[PASS] List all customers
      Found 5 customers
[PASS] Create customer
      Customer ID: 123e4567-e89b-12d3-a456-426614174000
[PASS] Get customer by ID
      Status: 200
[PASS] Update customer
      Status: 200
[PASS] Search customers
      Found 3 results

======================================================================
                           TEST SUMMARY
======================================================================

Total Tests: 15
Passed: 15
Failed: 0
Success Rate: 100.0%
```

## Manual Testing

Refer to the `API_TESTING_GUIDE.md` for detailed manual testing instructions including:
- cURL command examples for each endpoint
- Request/response formats
- Authentication setup
- Postman collection setup

## Test Configuration

### Environment Setup

Tests use the same environment variables as the main application. Ensure your `.env` file contains:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Pytest Configuration

The `pytest.ini` file contains test configuration:
- Test discovery patterns
- Async test mode
- Custom markers
- Output formatting

### Test Fixtures

The `tests/conftest.py` file provides shared fixtures:
- `test_client`: FastAPI test client
- `admin_token`: Admin authentication token
- `employee_token`: Employee authentication token
- `admin_headers`: Headers with admin token
- `employee_headers`: Headers with employee token
- `sample_customer_data`: Sample customer data for tests
- `sample_biometric_data`: Sample biometric data for tests

## Test Coverage

### Current Test Coverage

- **Authentication**: Login, token validation, protected endpoints
- **Customers**: CRUD operations, search, pagination, date serialization
- **Biometrics**: Create, read, update, delete, file upload
- **Authorization**: Role-based access control (admin/employee)
- **Error Handling**: Invalid data, missing fields, duplicates, not found

### What's Tested

1. **Authentication & Authorization**
   - Valid/invalid login credentials
   - Token-based authentication
   - Role-based access control
   - Protected endpoint access

2. **Customer Management**
   - List customers with pagination
   - Create customer with all fields
   - Create customer with date serialization (bug fix verification)
   - Get customer by ID
   - Update customer fields
   - Update customer birth_date (bug fix verification)
   - Delete customer (soft delete)
   - Search customers by name/DNI/email
   - Duplicate DNI/email handling
   - Missing required fields validation

3. **Biometric Management**
   - List biometrics with filters
   - Create biometric with file upload
   - Get biometric by ID
   - Update biometric file
   - Delete biometric (soft delete)
   - Invalid biometric type handling
   - File size validation
   - Get biometric data with base64

4. **Error Cases**
   - 401 Unauthorized
   - 403 Forbidden
   - 404 Not Found
   - 409 Conflict
   - 422 Validation Error

## Bug Fixes Verified by Tests

### Date Serialization Bug

**Issue**: `Object of type date is not JSON serializable` error when creating/updating customers with birth_date field.

**Fix**: Added `.isoformat()` conversion for date fields in:
- `app/routers/customers.py:86` (create endpoint)
- `app/routers/customers.py:124` (update endpoint)

**Tests**:
- `test_customers.py::TestCustomerEndpoints::test_create_customer_with_date_serialization`
- `test_customers.py::TestCustomerEndpoints::test_update_customer_with_date_serialization`

These tests verify that date fields are properly serialized to ISO format strings before sending to the database.

## Continuous Integration

The test suite is designed to be CI/CD friendly and can be integrated with:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

Example GitHub Actions workflow:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest -v
```

## Troubleshooting

### Tests Failing Due to Database Connection

Ensure your Supabase credentials are correct in the `.env` file and that the Supabase instance is accessible.

### Authentication Tests Failing

Make sure the default admin credentials exist in your database:
- Email: `admin@gym.com`
- Password: `admin123`

### Test Customer Creation Failing

The tests create customers with unique DNI and email addresses using timestamps. If tests fail due to duplicates, ensure the test cleanup is running properly.

## Best Practices

1. **Run tests before committing**: Always run the test suite before pushing changes
2. **Write tests for new features**: Add tests when implementing new endpoints
3. **Update tests when fixing bugs**: Add regression tests for bug fixes
4. **Keep tests isolated**: Each test should be independent and not rely on other tests
5. **Use fixtures**: Leverage pytest fixtures for common setup tasks
6. **Mock external services**: Use mocks for external API calls to avoid flaky tests

## Future Improvements

- Add subscription endpoint tests
- Add payment endpoint tests
- Add attendance endpoint tests
- Add performance/load testing
- Add integration tests with real database
- Add end-to-end tests
- Increase test coverage to 90%+

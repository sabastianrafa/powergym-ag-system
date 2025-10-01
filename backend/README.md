# Backend - Project Bolt

This folder contains the backend API for Project Bolt. The backend is built with Python and FastAPI, and provides RESTful endpoints for managing customers, biometrics, payments, plans, subscriptions, and attendance.

## Features
- FastAPI-based REST API
- Supabase integration for database operations
- JWT authentication and security middleware
- Modular architecture (routers, models, services)
- Automated testing with pytest

## Getting Started

### Prerequisites
- Python 3.10+
- Supabase account and credentials
- (Optional) Docker

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   ```
2. Navigate to the backend folder:
   ```sh
   cd backend
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using Poetry:
   ```sh
   poetry install
   ```

### Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```sh
cp .env.example .env
```

### Running the API
Start the FastAPI server:
```sh
uvicorn app.main:app --reload
```

Or with Docker Compose:
```sh
docker-compose up backend
```

### Testing
Run tests with pytest:
```sh
pytest
```

## Project Structure
```
backend/
  app/
    core/           # Config, dependencies, security
    database/       # Supabase client
    middleware/     # Custom middleware
    models/         # Pydantic models
    routers/        # API endpoints
    services/       # Business logic
    main.py         # FastAPI app entrypoint
  tests/            # Pytest test cases
  seed.py           # Seed script
  test_runner.py    # Test runner
  pyproject.toml    # Project config
  ...
```

## API Documentation
Once running, access the interactive docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License
MIT

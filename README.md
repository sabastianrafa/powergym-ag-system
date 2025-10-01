# Project Bolt - Full Stack

Project Bolt is a full stack application for managing customers, biometrics, payments, plans, subscriptions, and attendance. It consists of a FastAPI backend and a React/TypeScript frontend, integrated with Supabase for database operations.

## Features
- FastAPI backend with RESTful endpoints
- React + TypeScript frontend SPA
- Supabase integration
- JWT authentication
- Modular architecture
- Automated testing (pytest)
- Docker support

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account
- Docker (optional)

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   ```
2. Copy environment variables:
   ```sh
   cp .env.example .env
   ```

#### Backend Setup
1. Navigate to backend:
   ```sh
   cd backend
   ```
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   or
   ```sh
   poetry install
   ```
3. Run the API server:
   ```sh
   uvicorn app.main:app --reload
   ```

#### Frontend Setup
1. Navigate to frontend:
   ```sh
   cd frontend
   ```
2. Install Node dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```

#### Docker Compose
To run both services with Docker Compose:
```sh
docker-compose up
```

## Project Structure
```
project/
  backend/    # FastAPI backend
  frontend/   # React frontend
  supabase/   # Database migrations
  docker-compose.yml
```

## API Documentation
Once running, access the backend docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License
MIT

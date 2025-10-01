# Frontend - Project Bolt

This folder contains the frontend application for Project Bolt. The frontend is built with React, TypeScript, and Vite, and provides a modern user interface for managing customers, biometrics, payments, plans, subscriptions, and attendance.

## Features
- React + TypeScript SPA
- Vite for fast development and build
- Tailwind CSS for styling
- Context API for authentication state
- Modular components and pages
- API integration with backend

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   ```
2. Navigate to the frontend folder:
   ```sh
   cd frontend
   ```
3. Install dependencies:
   ```sh
   npm install
   ```
   or
   ```sh
   yarn install
   ```

### Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```sh
cp .env.example .env
```

### Running the App
Start the development server:
```sh
npm run dev
```

### Building for Production
```sh
npm run build
```

## Project Structure
```
frontend/
  src/
    components/     # Reusable UI components
    context/        # React context providers
    hooks/          # Custom hooks
    pages/          # Application pages
    services/       # API service layer
    types/          # TypeScript types
    App.tsx         # Main app component
    main.tsx        # Entry point
  public/           # Static assets
  index.html        # HTML template
  package.json      # Project config
  ...
```

## License
MIT

# IntelliBuild AI - Autonomous Building Intelligence Platform

An AI-powered enterprise platform that continuously monitors, reasons, and optimizes smart building energy consumption using an NVIDIA AI Decision Engine and EnergyPlus as a Digital Twin.

## Architecture

The platform uses a clean, feature-based microservice architecture split into two main components:

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (asyncpg)
- **Orchestration**: LangGraph, NVIDIA AI Client
- **Simulation**: EnergyPlus Integration Engine
- **Task Scheduling**: APScheduler

### Frontend
- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS & shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query
- **Visualization**: Apache ECharts & Framer Motion

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.12+ (for local backend development)

### Running the Application

The entire platform is orchestrated using Docker Compose.

1. Create a `.env` file in the `backend/` directory by copying `.env.example`.
2. From the root directory, run:
```bash
docker compose up --build
```
3. The platform will start:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **Swagger Docs**: http://localhost:8000/docs
   - **Database**: PostgreSQL on port 5432

### Demo Guide
For the Honeywell Hackathon demo, the application will initialize with mock telemetry data and allow seamless interactions with the AI Copilot to generate decision goals and queue simulations. The AI planner will construct execution plans viewable in the Decision Center.

# IntelliBuild AI 🏢🧠

**AI-Powered Autonomous Building Intelligence Platform**

IntelliBuild AI is an autonomous AI platform that continuously monitors, reasons, and optimizes smart building energy consumption using EnergyPlus as a Digital Twin and an Open-Source LLM.

## Architecture

This backend implements a scalable, modern feature-based architecture optimized for AI integration and complex simulations:

- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with SQLAlchemy 2 (async) and Alembic
- **Package Management**: Poetry
- **Logging**: Enterprise-grade JSON logging via Structlog

---

## 🚀 Quick Start & Environment Setup

We strictly enforce **Poetry** as our environment manager to guarantee 100% reproducibility across Mac, Linux, and Windows. **Do not use standard `venv` or `Anaconda` directly.**

### Prerequisites
- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installation) (version 1.7+)
- Docker & Docker Compose

### 1. Clone & Configure Environment
First, configure Poetry to create the virtual environment inside the project folder. This ensures your IDE detects it automatically.

```bash
cd backend
poetry config virtualenvs.in-project true
```

### 2. Install Dependencies
Install all required and development packages exactly as locked in `poetry.lock`.

```bash
poetry install
```

### 3. Verify Active Interpreter
Ensure that your terminal hasn't defaulted to Anaconda or a system Python. It **must** point to the local `.venv`.

```bash
# This MUST output a path ending in: backend/.venv/bin/python
poetry run which python
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
```

---

## 🛠️ Developer Workflow

**CRITICAL RULE**: Every python command **MUST** be prefixed with `poetry run` to ensure you are executing inside the isolated environment, avoiding `ModuleNotFoundError`.

### Running Quality Gates
We enforce strict code quality using `Black` and `Ruff`.

```bash
# 1. Format code
poetry run black .

# 2. Lint code
poetry run ruff check .

# 3. Run all tests
poetry run pytest
```
*Expected Output*: Black formats without error, Ruff returns no violations, and Pytest passes 100%.

### Starting the Backend Locally
To boot the FastAPI application:

```bash
poetry run uvicorn app.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`. 
Swagger UI is accessible at `http://127.0.0.1:8000/docs`.

### Running Database Migrations
```bash
poetry run alembic upgrade head
```

---

## Simulation Orchestration

Milestone 4 adds a non-AI Simulation Orchestration Engine for creating,
queuing, starting, cancelling, and tracking simulation jobs. The orchestrator
executes jobs in the background and still routes simulation work through
`SimulationController` and the `SimulationAdapter` abstraction.

REST endpoints:

- `POST /api/simulations`
- `GET /api/simulations`
- `GET /api/simulations/{id}`
- `POST /api/simulations/{id}/start`
- `POST /api/simulations/{id}/cancel`

---

## Decision Engine

Milestone 5 adds a deterministic rule-based Decision Engine. It converts
high-level building goals into ordered simulation plans and creates the
underlying simulation jobs through the Simulation Orchestrator. It does not use
LLMs, MCP, reinforcement learning, autonomous reasoning, or optimization
algorithms.

REST endpoints:

- `POST /api/decision/goals`
- `GET /api/decision/goals`
- `GET /api/decision/goals/{id}`
- `POST /api/decision/goals/{id}/plan`
- `GET /api/decision/plans/{id}`

---

## AI Intelligence Layer

Milestone 6 adds a natural-language AI layer that converts user requests into
deterministic `DecisionGoal` objects through the NVIDIA Cloud AI API. The AI never executes
simulations and never communicates with EnergyPlus. All execution continues
through the existing Decision Engine.

Configuration:

- `AI_PROVIDER` (default: `nvidia`)
- `NVIDIA_API_KEY` (required: your NVIDIA API Key)
- `NVIDIA_MODEL` (default: `meta/llama-3.1-70b-instruct`)
- `NVIDIA_BASE_URL` (default: `https://integrate.api.nvidia.com/v1`)
- `AI_TEMPERATURE` (default: `0.2`)
- `AI_MAX_TOKENS` (default: `2048`)
- `AI_TIMEOUT` (default: `120.0`)

REST endpoints:

- `POST /api/ai/chat`
- `POST /api/ai/plan`
- `GET /api/ai/health`

See [AI Intelligence Layer Design](design/ai-intelligence-layer.md) for full
architecture details.

---

## 💻 IDE Configuration

To ensure your IDE (VS Code or PyCharm) resolves imports like `structlog` and `app.*` without errors, you must point it to the Poetry `.venv`.

### VS Code
1. Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`).
2. Select **Python: Select Interpreter**.
3. Choose the interpreter located at `./backend/.venv/bin/python`.

### PyCharm
1. Open **Settings / Preferences** > **Project** > **Python Interpreter**.
2. Click **Add Interpreter** > **Add Local Interpreter**.
3. Select **Poetry Environment** and point it to the project base. Alternatively, select **Existing environment** and navigate to `./backend/.venv/bin/python`.

---

## 🐳 Docker Deployment

To spin up the entire stack (API and PostgreSQL Database) without local dependencies:

```bash
docker-compose up --build -d

# View logs
docker-compose logs -f api
```

---

## 🛣️ Roadmap
- [x] Implement foundational architecture
- [x] Database schema for buildings and sensors
- [x] Connect EnergyPlus Engine through the `SimulationAdapter` abstraction
- [x] Implement the PyEnergyPlus-backed `EnergyPlusAdapter`
- [x] Implement Simulation Orchestration Engine
- [x] Implement deterministic Decision Engine
- [x] Integrate Open-Source LLM (Ollama/Qwen3)
- [ ] MCP Server Implementation
- [ ] Real-time WebSockets setup

# Project Roadmap

## Phase 1: Foundation (Completed)
- FastAPI Architecture Setup
- Dependency Injection Patterns
- Database Configs & Structlog setup

## Phase 2: Digital Twin (Completed)
- Simulation interfaces and Data Models
- Digital Twin Manager & Repository

## Phase 3: EnergyPlus Integration (Completed)
- `EnergyPlusAdapter` concrete implementation of `SimulationAdapter`
- `EnergyPlusConfig` with `EPLUS_` env-var overrides
- `IDFLoader` and `WeatherManager` for asset validation
- `OutputManager` for simulation output routing
- `CallbackManager` for zone timestep callback registration
- `EnergyPlusRuntime` for background thread C-engine orchestration
- Custom exception hierarchy (`errors.py`)
- Full unit test coverage with mocked PyEnergyPlus API

## Phase 4: AI & Orchestration
- Simulation job model and lifecycle status tracking
- Background Simulation Orchestrator for create, queue, start, cancel, run, cleanup
- Simulation job repository for execution metadata and history
- REST management endpoints under `/api/simulations`

## Phase 5: Decision Engine (Completed)
- Deterministic `DecisionGoal` and `ExecutionPlan` models
- Rule-based plan generation for energy, peak load, comfort, HVAC, lighting, occupancy, carbon, water, and diagnostics goals
- Integration with the Simulation Orchestrator for ordered simulation job creation
- REST management endpoints under `/api/decision`
- Unit and API coverage for validation, rule ordering, repositories, and error handling

## Phase 6: AI Intelligence Layer (Completed)
- Ollama client with health check, model listing, chat completion, timeout, and retry handling
- Reusable prompt templates for all supported goal types
- AI planner that converts natural language into deterministic `DecisionGoal` objects
- JSON parser with schema and goal-type validation
- REST endpoints under `/api/ai`
- Unit and API coverage with mocked Ollama responses

## Phase 7: Multi-Agent Orchestration (Future)
- LangGraph integration
- Supervisor and autonomous agent workflows
- Advanced prompt chains beyond goal parsing

## Phase 8: Production Readiness
- Dashboard APIs
- Real-time WebSockets
- Security audits and payload limits

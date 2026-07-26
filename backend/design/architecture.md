# Overall System Architecture

IntelliBuild AI is designed as an autonomous, event-driven, AI-powered digital twin platform aimed at optimizing building energy consumption. The architecture follows a strict decoupled, feature-based service layer pattern to separate AI reasoning from the underlying physics simulations.

## Layer Responsibilities

### 1. Presentation & API Layer (FastAPI)
The topmost layer exposed to external clients (e.g., dashboards, MCP servers). It handles HTTP/WebSocket connections, Request ID injection, structlog tracing, and delegates input to the respective controllers.

### 2. Orchestration Layer
The planning and decision layer of the system.
- **AI Intelligence Layer**: Converts natural language into deterministic `DecisionGoal` objects through Ollama. It never executes simulations or communicates with EnergyPlus.
- **AI Planner**: Builds prompts, calls Ollama, validates structured JSON, and submits goals to the Decision Engine.
- **Decision Engine**: Deterministic rule engine that validates goals, generates ordered execution plans, and creates simulation jobs through the `SimulationOrchestrator`.
- **Supervisor**: Future coordinator for higher-level multi-agent workflows.

### 3. Digital Twin Layer
Maintains the latest representation of the physical (or simulated) building in memory. It prevents the Orchestration layer from directly waiting on physics simulations.
- **Manager**: Controls state updates.
- **Repository**: Thread-safe in-memory store for instant state lookup.

### 4. Adapter & Simulation Layer
The integration layer bridging IntelliBuild AI to EnergyPlus or any substitute simulator.
- **SimulationOrchestrator**: Owns simulation job creation, queueing, background execution, lifecycle status, cancellation, and execution history.
- **SimulationController**: Wraps adapter lifecycle.
- **SimulationAdapter (ABC)**: Enforces a strict interface contract.
- **EnergyPlusAdapter**: The concrete production implementation using PyEnergyPlus. Manages the C-engine in a background thread via `EnergyPlusRuntime`, registers zone timestep callbacks via `CallbackManager`, and validates IDF/EPW assets via `IDFLoader` and `WeatherManager`.

## Data Flow & Dependency Flow

1. **Natural Language -> Goal**: The `AIPlanner` receives a user message, builds a prompt, calls Ollama, validates structured JSON, and creates a `DecisionGoal` through the `DecisionEngine`.
2. **Goal -> Plan**: The `DecisionEngine` receives a `DecisionGoal`, validates it, applies deterministic rules, and creates an ordered `ExecutionPlan`.
2. **Plan -> Jobs**: The `DecisionEngine` creates simulation jobs through the `SimulationOrchestrator`; it never calls `SimulationController`, `SimulationAdapter`, or EnergyPlus directly.
3. **Job Execution**: The `SimulationOrchestrator` starts simulation jobs asynchronously and invokes the `SimulationController`; it never bypasses `SimulationAdapter`.
4. **Simulation -> Twin**: The `EnergyPlusAdapter` receives zone timestep callbacks from the C-engine. The `CallbackManager` invokes `_update_internal_state()` to pull variable values. The `SimulationController` then calls `get_state()` and `get_sensor_data()` and writes them into the `DigitalTwinManager`.
5. **Twin -> Future AI**: Future AI planners and supervisors consume orchestration summaries and twin snapshots through their own layer instead of directly importing adapters.

## Dependency Flow Constraints
The core principle is strict Dependency Injection (DI) and the Open-Closed Principle.
`API Layer -> AI Intelligence Layer -> Decision Engine -> Simulation Orchestration Layer -> Simulation Controller -> Adapter Layer`
Future multi-agent supervisors **must never** import or depend directly on the Adapter layer. They submit goals to the Decision Engine, which uses the Simulation Orchestrator.
The AI Intelligence Layer **must never** communicate directly with EnergyPlus or simulation adapters.

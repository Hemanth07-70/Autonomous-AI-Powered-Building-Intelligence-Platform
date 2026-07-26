# Agent Architecture Design

The AI orchestration layer of IntelliBuild AI uses a multi-agent framework designed to emulate human-like building management reasoning, while retaining deterministic safety guarantees.

## Core Components

### Supervisor
The central authority in the orchestrator.
- Evaluates total system state against high-level goals.
- Delegates tasks to the Planner or Decision Engine based on the severity of the building's deviations from ideal performance.

### Decision Engine
The tactical reasoning center.
- Ingests `SimulationSnapshot` (temperatures, occupancy, energy usage).
- Uses prompt flows (to be implemented via LangGraph/Ollama) to synthesize immediate `ControlAction` payloads (e.g., adjusting HVAC setpoints in response to sudden occupancy spikes).

### Planner
The strategic reasoning center.
- Forecasts long-term implications of weather patterns and historical load profiles.
- Emits broad operational directives to guide the Decision Engine's boundaries.

## Tool Layer
Agents are provided tools (functions) strictly scoped to their authorization level.
- `get_current_state()`
- `get_forecast()`
- `apply_setpoint_override()`

## Future MCP Integration
IntelliBuild AI will eventually expose an MCP (Model Context Protocol) server, allowing external advanced LLMs to act as the Supervisor, passing contexts fluidly and executing tool calls directly into the `SimulationController` boundary.

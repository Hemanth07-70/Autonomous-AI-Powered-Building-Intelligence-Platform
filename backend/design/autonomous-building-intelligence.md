# Autonomous Building Intelligence

This document details the LangGraph Multi-Agent System orchestration layer implemented in Milestone 7.

## Architecture

The orchestration layer uses `LangGraph` and `LangChain Core` to execute a state machine graph composed of intelligent agent nodes.

### Flow

1. **User Input**: Reaches `POST /api/agents/run`.
2. **Graph Initiation**: Initial state (containing the request) is piped into the `PlannerAgentNode`.
3. **Planner**: Parses the request via Ollama to generate a `DecisionGoal`, then delegates to the underlying **Decision Engine** to create an `ExecutionPlan`.
4. **Analytics & Diagnostics**: (Parallel Execution)
   - **AnalyticsAgentNode**: Computes deterministic KPIs (Cost, Carbon, Comfort) from the simulation state without LLM hallucination.
   - **DiagnosticsAgentNode**: Evaluates the simulated results and `DecisionGoal` for inefficiencies and schedules anomalies.
5. **Recommendation**: Terminal node combining all contexts into actionable `Recommendation` structures.

## LangGraph State Model

The state passed through the graph is defined via `TypedDict` and includes reducers (e.g., `operator.add` for lists, custom dict reducer for timestamps) to handle parallel branching:
- `user_request`
- `decision_goal`
- `execution_plan`
- `analytics`
- `diagnostics`
- `recommendations`
- `timestamps`

## Future Extensibility

- **Memory / Checkpoints**: Can add LangGraph persistence for long-running workflows.
- **Supervisor Edge Conditional Routing**: Expand the Supervisor to evaluate the `recommendations` and possibly iterate the simulation loop before finalizing.
- **MCP**: Model Context Protocol can act as a wrapper on top of this graph to allow external systems to control the simulation endpoints securely.

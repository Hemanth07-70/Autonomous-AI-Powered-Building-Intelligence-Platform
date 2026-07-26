# System Architecture Report

## Objective
IntelliBuild AI implements a closed-loop autonomous building optimization system that reads building telemetry, generates control decisions with an LLM-driven agentic layer, applies control parameter updates, and validates impact through simulation.

## Tool-Calling Architecture
The system is organized around a Python FastAPI backend with explicit feature modules and orchestration boundaries:

- API Layer: Receives user and machine requests (AI copilot prompts, simulation actions, decision endpoints).
- Agent Orchestration Layer: Coordinates multi-step decision flow using planner, diagnostics, analytics, and recommendation agents.
- Digital Twin Layer: Maintains synchronized building operational state for decision context.
- EnergyPlus Adapter Layer: Bridges abstract simulation interfaces to concrete EnergyPlus execution.
- Scheduler/Execution Layer: Queues and runs simulation jobs, tracks state transitions, and records outputs.

Primary implementation areas:
- backend/app/api
- backend/app/agents
- backend/app/energyplus
- backend/app/scheduler

## Prompt Engineering Strategy
The AI decision flow is structured to keep prompts deterministic and auditable:

- Role-scoped prompts: Planner and specialist agents each receive bounded responsibility.
- Context shaping: Building telemetry, constraints, and goals are passed as structured fields.
- Output contracts: Agent responses are transformed into typed decision goals and execution plans.
- Validation gates: Downstream layers enforce schema and state constraints before simulation execution.

This design reduces free-form ambiguity and supports reproducible runs.

## Prompt Latency Management
Latency is handled using a layered strategy:

- Async HTTP handlers and non-blocking orchestration.
- Separation of immediate response vs long-running simulation execution.
- Scheduler-based job lifecycle (queued, running, completed/failed) to avoid blocking user requests.
- Lightweight frontend polling/state refresh via query hooks for responsive UX.

Operationally, users receive quick acknowledgment while heavy simulation tasks run asynchronously.

## Handling Lengthy Simulation Logs
Simulation outputs can be large and noisy; the architecture addresses this by:

- Isolating simulation state and output management into dedicated modules.
- Capturing job progress and summarized status for dashboard consumption.
- Persisting simulation outputs by job so post-run analytics can be computed without rerunning.
- Exposing only essential operational signals to user-facing endpoints.

This keeps the control loop robust under extended simulation horizons and high log volume.

## Closed-Loop Sequence
1. Telemetry and building context are collected.
2. User/system goal is sent to AI copilot/decision layer.
3. Planner returns a structured decision goal.
4. Execution plan and simulation jobs are created.
5. EnergyPlus simulation runs with updated parameters.
6. Results are analyzed against energy and comfort constraints.
7. Recommendations and next control actions are fed back into the loop.

## Reliability and Extensibility
- Modular feature boundaries simplify maintenance and testing.
- Strong typing/schema contracts reduce runtime ambiguity.
- Adapter abstractions allow simulator replacement or expansion.
- Agent decomposition supports future supervisor and policy layers.

## Conclusion
IntelliBuild AI provides a production-oriented blueprint for autonomous building intelligence: an LLM-guided decision layer integrated with simulation-driven validation and an auditable operational feedback loop focused on energy savings while preserving comfort constraints.

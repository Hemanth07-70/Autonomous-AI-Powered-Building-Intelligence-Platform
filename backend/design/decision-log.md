# Architectural Decision Log

This log records major architectural decisions (ADRs) made during the lifecycle of IntelliBuild AI.

## ADR-001: Strict Simulation Decoupling
- **Date**: 2026-07-25
- **Decision**: Abstract the physics engine (EnergyPlus) behind an interface (`SimulationAdapter`).
- **Rationale**: Prevents AI orchestration from becoming tightly coupled to EnergyPlus specific idiosyncrasies. Allows drop-in replacements for testing or alternative engines.

## ADR-002: In-Memory Digital Twin Repository
- **Date**: 2026-07-25
- **Decision**: Use an in-memory python dictionary locked via `threading.RLock()` for the active digital twin instead of a database (like Redis or Postgres).
- **Rationale**: Millisecond read latency is required for AI agents performing real-time reasoning. The overhead of network IO for intra-tick state queries is unacceptable.

## ADR-003: Structlog for Telemetry
- **Date**: 2026-07-25
- **Decision**: Mandate Structlog across the entire codebase.
- **Rationale**: Enables JSON-structured logging critical for parsing telemetry and AI reasoning trajectories in Datadog or ELK stacks.

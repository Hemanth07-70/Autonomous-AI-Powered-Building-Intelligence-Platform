# Folder Structure

The repository follows a clean, feature-based bounded-context organization.

```text
backend/
├── app/
│   ├── ai/             # AI Intelligence Layer (Ollama client, planner, parser, prompts).
│   ├── api/            # External interface (FastAPI routers & endpoints).
│   ├── config/         # System configurations & env parsing.
│   ├── core/           # Core cross-cutting implementations (Exceptions, Logging Contexts).
│   ├── energyplus/     # The Simulation Adapter and Digital Twin Layer.
│   ├── monitoring/     # System health and diagnostics services.
│   ├── orchestrator/   # Decision Engine and execution planning.
│   ├── scheduler/      # Background loops, polling mechanisms, and task queues.
│   ├── shared/         # Universally utilized constants, types, and enums.
│   └── telemetry/      # Performance metrics and data collectors.
├── design/             # Architecture and design documentation.
├── development/        # SDLC documentation and engineering milestones.
├── tests/              # Segmented test suites (unit, integration, mocks).
├── .github/            # GitHub Actions CI/CD pipelines.
```

**Rule of Thumb:**
Code belonging to a specific bounded context (e.g., telemetry) stays in that folder. Code shared across multiple contexts goes into `shared` or `core`.

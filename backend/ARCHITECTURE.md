# System Architecture Overview

IntelliBuild AI is structured utilizing a **Layered Feature-Based Architecture**, emphasizing strict Dependency Injection and SOLID principles.

## Core Layers
1. **API / Transport Layer**: Built on FastAPI, this handles external HTTP requests, WebSockets, and structured logging context injection.
2. **Orchestration Layer**: The AI engine consisting of the AI Intelligence Layer, Decision Engine, and future Supervisor.
3. **Digital Twin Layer**: The ultra-fast, thread-safe in-memory representation of the physics engine.
4. **Adapter Layer**: The bridge connecting the abstract twin interfaces to concrete simulators like EnergyPlus.

For deep technical specifications, refer to the documentation in the `/design/` directory:
- [Architecture Details](../design/architecture.md)
- [AI Intelligence Layer](../design/ai-intelligence-layer.md)
- [Agent Design](../design/agent-design.md)
- [Digital Twin](../design/digital-twin.md)

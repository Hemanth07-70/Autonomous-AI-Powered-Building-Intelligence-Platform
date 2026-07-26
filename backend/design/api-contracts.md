# API Contracts & Networking

## Versioning Strategy
All APIs are versioned via the URI (e.g., `/api/v1/`). Backwards breaking changes require a new version integer.

## Future REST APIs

### Analytics & Reporting
- `GET /api/v1/analytics/history`
  - Returns aggregated energy usage over specified time windows.
- `GET /api/v1/simulation/state`
  - Returns the JSON equivalent of `SimulationSnapshot`.

### Simulation Control
- `POST /api/v1/simulation/start`
- `POST /api/v1/simulation/pause`
- `POST /api/v1/simulation/stop`

## Future WebSocket APIs
For real-time dashboard telemetry, a WebSocket connection will be established at `ws://<host>/api/v1/ws/telemetry`.

**Schema Definition**:
Payloads over WS will strictly follow the `SimulationSnapshot` Pydantic models serialized to JSON, pushed at the completion of every simulation `step`.

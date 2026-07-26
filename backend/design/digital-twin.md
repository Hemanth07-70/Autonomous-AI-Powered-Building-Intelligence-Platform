# Digital Twin Architecture

The Digital Twin is the central nervous system of IntelliBuild AI. It is an ultra-fast, in-memory proxy representation of the physics engine.

## State Management

The Twin abstracts away the asynchronous latency of physics simulations. When the AI requires the current temperature, it asks the Twin, which retrieves it from RAM in O(1) time without blocking or asking the physics engine.

## Snapshots

The Twin generates a `SimulationSnapshot` at the end of every simulation step. A snapshot is immutable and fully encapsulates:
- `BuildingState` (Time, occupancy, overall simulation status).
- `SensorData` (Zone-by-zone metrics like Temp, CO2, Power).
- `ControlAction` (The last action applied).

## Repositories

**SimulationRepository**:
- Utilizes `threading.RLock()` to guarantee thread safety during state mutations by the `SimulationController`.
- Holds the single latest source of truth for the building state.
- Retains a configured list of history `SimulationSnapshot` elements to allow the AI planner to observe trend lines.

## Synchronization

The `SimulationController` owns the synchronization loop. Upon advancing the simulator one tick, it sequentially pulls data, creates Pydantic representations, and injects them into the `DigitalTwinManager`.

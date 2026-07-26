# Testing Strategy

We rely on Pytest for the execution framework.

## 1. Unit Tests (`tests/unit/`)
- Must isolate the class under test using mocks (e.g., `unittest.mock`).
- No database access.
- No file I/O (unless using `tmp_path`).
- Expected coverage: 90%+ for core domain logic.

## 2. Integration Tests (`tests/integration/`)
- Tests the interaction between components (e.g., Database + Controller).
- Requires Docker Compose spin-up.

## 3. Mock Boundaries (`tests/mocks/`)
- Real simulators (EnergyPlus) are NEVER run in the test suite. We provide a `MockSimulationAdapter` that emits deterministic dummy physics data.

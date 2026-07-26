# Acceptance Criteria Guidelines

Acceptance Criteria (AC) must be rigidly defined before a feature enters `In Progress`.

## Format
We prefer the BDD (Behavior-Driven Development) format for functional criteria:
- **Given** [initial context]
- **When** [action occurs]
- **Then** [expected outcome]

For non-functional architecture criteria (like telemetry), use strict bullets:
- e.g., "All SimulationController methods emit exactly one `duration_s` metric."

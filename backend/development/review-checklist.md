# Code Review Checklist

Reviewers must verify the following before approving:

- [ ] Does the code satisfy the Acceptance Criteria?
- [ ] Is the architecture strictly decoupled (no new direct dependencies between AI and Simulator)?
- [ ] Are new classes properly injected via dependency injection?
- [ ] Do all methods and classes have descriptive docstrings?
- [ ] Are type hints complete and accurate?
- [ ] Are all new paths covered by unit tests?
- [ ] Are metrics (telemetry) appropriately emitted for new critical paths?
- [ ] Does the PR title conform to conventional commits?

# Branching Strategy

We enforce a strict Git Flow methodology.

- `main`: Reflects the production state. Protected branch.
- `develop`: Integration branch. Protected branch.
- `feature/<ticket-id>-<description>`: Branched from `develop`. Used for new features.
- `bugfix/<ticket-id>-<description>`: Branched from `develop`.
- `hotfix/<ticket-id>-<description>`: Branched from `main`. Only for critical production bugs.

## Commits
Use Conventional Commits (e.g., `feat: added digital twin manager`).

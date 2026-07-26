# Contributing to IntelliBuild AI

Thank you for your interest in contributing! This document outlines the process for submitting patches, features, and bug fixes to the IntelliBuild AI platform.

## 1. Local Setup
Ensure you have Python 3.12, Poetry, and Docker installed.
Review `README.md` for local setup instructions.

## 2. Branching Strategy
We use Git Flow variant:
- `main`: Production-ready code.
- `develop`: Integration branch for ongoing milestones.
- `feature/<name>`: New features.
- `bugfix/<name>`: Fixes for non-production environments.

## 3. Pull Request Process
1. Ensure your code passes the CI pipeline (Ruff, Black, Pytest).
2. Update the `CHANGELOG.md` under the `Unreleased` section.
3. Submit a PR against `develop`.
4. Ensure at least one code owner approves your PR.

## 4. Testing
All new features must include unit tests. Integration tests are required for any adapter or external API modifications.

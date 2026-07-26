# Code Style Guidelines

We enforce strict automated formatting using Black and Ruff.

## 1. Automated Tools
- **Black**: Enforces deterministic PEP8 formatting with an 88 character line limit.
- **Ruff**: Runs comprehensive linting and syntax checking.

*Note: All code must pass `.pre-commit-config.yaml` checks before being merged.*

## 2. Typing
- All variables, function parameters, and return types must be fully typed (Python 3.12 syntax).
- Avoid `Any`. Use generic types and unions explicitly.

## 3. Docstrings
- Every public class and function must include a docstring.
- Docstrings should explain the *why*, not the *how*.

## 4. Error Handling
- Do not catch generic `Exception` unless absolutely necessary (and if you do, re-raise it or log it exhaustively).
- Use the enterprise exception hierarchy defined in `app/shared/exceptions.py`.

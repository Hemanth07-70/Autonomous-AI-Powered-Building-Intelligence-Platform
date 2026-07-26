# Coding Standards

## 1. Type Hinting
Every function signature MUST contain complete Python 3.12 type hints.
- Use `Optional[X]` rather than `X | None` for backwards compatibility readability, or standard modern union `X | None` if strictly enforcing Python 3.10+. (We standardize on 3.12, so either is acceptable, but be consistent).
- Use `Any` sparingly.

## 2. Dependency Injection
Hardcoding instantiations inside business logic is forbidden. Use constructors to pass dependencies.
```python
# Bad
class Service:
    def __init__(self):
        self.repo = MyRepository()

# Good
class Service:
    def __init__(self, repo: MyRepository):
        self.repo = repo
```

## 3. SOLID Principles
- **Single Responsibility**: Classes must have only one reason to change.
- **Open/Closed**: Architect using abstract interfaces (`abc.ABC`) so behaviors can be extended without modifying existing source code.

## 4. Documentation
All public classes and methods must possess a descriptive docstring explaining *intent*, not just re-stating the code.

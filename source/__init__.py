"""
Feline Finder source package.

This project follows Clean Architecture principles with a domain-centric
structure inspired by Domain-Driven Design (DDD).

Each bounded context (e.g., scraping, repository, monitoring) is organized
as a vertical slice with four layers:

- `entities`: Core business models and rules
- `use_cases`: Application-specific business workflows
- `adapters`: Interfaces (abstract contracts) for external dependencies
- `infrastructure`: Concrete implementations

Dependencies flow inward: outer layers depend on inner ones, never the
reverse. This promotes modularity, testability, and maintainability.
"""

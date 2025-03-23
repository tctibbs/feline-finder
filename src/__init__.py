"""
Source package for the application.

This package is organized according to the principles of Clean Architecture.
Each layer of the architecture is separated into its own subpackage:

- `entities`: Core business models and logic
- `use_cases`: Application-specific business rules
- `interfaces`: Gateways and interfaces
- `infrastructure`: Implementation details

Dependencies should point inward only.
"""

from . import entities
from . import use_cases
from . import adapters
from . import infrastructure

__all__ = ["entities", "use_cases", "adapters", "infrastructure"]

"""Domain policies package (validation-only policies).

Policies live under `app.domain.policies` to group validation alongside domain logic.
"""

__all__ = [
    "BasePolicy",
    "UserPolicy",
    "TransactionPolicy",
    "CategoryPolicy",
    "FinancialCalculationsPolicy",
]

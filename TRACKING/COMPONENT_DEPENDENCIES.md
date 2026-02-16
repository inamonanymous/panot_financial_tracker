# Component / Class Dependency Tracker

This document describes prerequisites and connections between layers (routes → use-cases → policies/services → domain entities → repositories/ORM).

- Naming: `module.Class` or `path/to/file` for clarity.

## Examples (current important links)

- `r_users.py` → `CheckLoginUseCase` → `p_UserPolicy` → `m_Users` (Users table)
  - Prereq: `m_Users` DB schema and `UOW.users` repository available

- `r_expense.py` → `CreateExpenseUseCase` → `p_TransactionPolicy` → `domain.entities.expense` → `expenses repository` → `m_Expenses` ORM
  - Prereq: valid `category_id` owned by user (enforced by `UOW.categories`)

- `CreateDebtPaymentUseCase` → `uow.debts`, `uow.categories`, `uow.expenses`, `uow.debt_payments` + `p_FinancialCalculationsPolicy` and `p_CategoryPolicy`
  - Important: will create a category when not present

- `DashboardReportingUseCase` → `UOW.incomes` + `UOW.expenses` + `SavingTransactions` (uses raw SQL join on `Income.id`)

## How to keep this updated
- When adding a new use-case, add a `Prereqs` section referencing domain entities and policies.
- Run `python scripts/generate_trackers.py` to auto-list use-cases and basic cross-references.

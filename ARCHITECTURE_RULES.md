# Architecture Rules (Step 1)

Last updated: 2026-02-25

This document is the working contract for redesign. Every refactor step must preserve these rules.

## 1) Layer Responsibilities

- Routes (`app/routes`): HTTP-only concerns (request parsing, auth/session checks, response/redirect rendering).
- Use Cases (`app/use_cases`): business workflow orchestration and transaction boundaries.
- Policies (`app/domain/policies`): input sanitation + request-context validation.
- Domain Entities (`app/domain/entities`): invariant business rules that must always hold.
- Repositories (`app/repositories` + `app/persistence/repositories`): all database reads/writes and query composition.
- Unit of Work (`app/persistence/unit_of_work.py`): commit/rollback and atomic write orchestration.

## 2) Dependency Direction (Allowed)

- `routes -> use_cases`
- `use_cases -> policies, domain services, repositories via uow`
- `repositories (impl) -> ORM models`
- `domain entities/services -> no route/use-case imports`

## 3) Forbidden Dependencies

- Use cases importing ORM models (`app/model/*`) directly.
- Routes performing business orchestration beyond request mapping.
- Policies calling repositories/ORM.
- Domain entities importing route or persistence modules.

## 4) Route Contract

Every route handler should do only:

1. Extract request input.
2. Inject user/session context.
3. Call one use case/service entry point.
4. Map success/error to HTTP response.

No domain branching or data joins in routes.

## 5) Use Case Contract

Use cases may:

- Validate via policies.
- Read/write using `uow.<repo>` methods.
- Open `with self.uow.transaction()` for write operations.

Use cases must not:

- Query ORM models directly.
- Build SQLAlchemy joins directly.
- Return raw ORM objects to routes.

## 6) Repository Contract

- All data access belongs here, including read models for UI (e.g., list views with category names and timestamps).
- Repository methods should return domain entities or stable DTO dictionaries.
- If only one implementation exists, prefer simple concrete repository classes over deep interface hierarchies.

## 7) Validation Strategy (Chosen)

Single source of truth split:

- Domain entities: core invariants (e.g., amount > 0, valid payment method set).
- Policies: endpoint/form validation and contextual checks (required fields, ownership checks, edit/delete preconditions).

Guideline: avoid duplicating the exact same rule in both layers.

## 8) Current Violations to Fix Next

1. Use-case ORM leakage
   - `app/use_cases/income/get_user_income.py` imports `app.model.m_Income`.
   - `app/use_cases/expense/get_user_expense.py` imports `app.model.m_Expenses`.

2. Route orchestration duplication
   - `app/routes/r_income.py` and `app/routes/r_expense.py` repeat error handling and redirect plumbing.

3. Over-abstract repository stack for single backend
   - `app/repositories/repository.py` + per-entity interfaces add indirection with only one concrete implementation path.

4. Validation overlap
   - Similar transaction field constraints exist in both `app/domain/policies/p_TransactionPolicy.py` and domain entities (`income.py`, `expense.py`).

## 9) Refactor Sequence Guardrail

Perform refactors in this order:

1. Thin routes.
2. Remove use-case ORM leakage.
3. Standardize use-case return DTOs.
4. Consolidate validation responsibilities.
5. Simplify repository abstractions.

Do not remove `UnitOfWork.transaction()` from multi-write workflows.
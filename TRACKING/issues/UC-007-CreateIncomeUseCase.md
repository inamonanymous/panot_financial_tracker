Title: [UC-007] CreateIncomeUseCase — Insert income (validate category)

Summary
- Insert income record ensuring category ownership and validity.

Acceptance criteria
- [ ] Valid input saved to `UOW.incomes`.
- [ ] Category belongs to user.

References
- `app/use_cases/income/create_income.py`
- `app/routes/r_income.py` (/insert_income)

Components / Prereqs
- `TransactionPolicy`, `domain.entities.income`, `UOW.categories`, `UOW.incomes`

Labels: use-case, backend, income
Assignee:

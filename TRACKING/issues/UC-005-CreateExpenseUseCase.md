Title: [UC-005] CreateExpenseUseCase — Insert expense (validate category ownership)

Summary
- Insert a new expense for a user; ensure category belongs to the user.

Acceptance criteria
- [ ] Category exists and belongs to user; otherwise error.
- [ ] Expense is saved via `UOW.expenses`.

References
- `app/use_cases/expense/create_expense.py`
- `app/routes/r_expense.py` (/insert_expense)

Components / Prereqs
- `TransactionPolicy`, `domain.entities.expense`, `UOW.categories`, `UOW.expenses`

Labels: use-case, backend, expense
Assignee:

Title: [UC-006] GetUserExpenseUseCase — Return enriched expense list

Summary
- Return user's expenses with category name and `created_at` metadata.

Acceptance criteria
- [ ] Returns list with `category_name` and `created_at` for each expense.
- [ ] Handles missing category gracefully.

References
- `app/use_cases/expense/get_user_expense.py`
- `app/routes/r_expense.py` (/expense)

Components / Prereqs
- `UOW.expenses`, `UOW.categories`, `m_Expenses`

Labels: use-case, backend, expense
Assignee:

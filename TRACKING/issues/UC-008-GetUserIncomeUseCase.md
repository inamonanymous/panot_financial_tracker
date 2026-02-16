Title: [UC-008] GetUserIncomeUseCase — Return enriched income list

Summary
- Return user's incomes with category name and `created_at` metadata.

Acceptance criteria
- [ ] Returns list with `category_name` and `created_at` for each income.
- [ ] Handles missing category gracefully.

References
- `app/use_cases/income/get_user_income.py`
- `app/routes/r_income.py` (/income)

Components / Prereqs
- `UOW.incomes`, `UOW.categories`, `m_Income`

Labels: use-case, backend, income
Assignee:

Title: [UC-009] GetUserCategoriesUseCase — Return categories for UI dropdowns

Summary
- Return categories filtered by user and optional type (income/expense/etc.).

Acceptance criteria
- [ ] Returns only categories that belong to requesting user.
- [ ] Optional `category_type` filter is applied correctly.

References
- `app/use_cases/get_user_categories.py`
- `app/routes/r_income.py`, `app/routes/r_expense.py` (used to populate UI modals)

Components / Prereqs
- `UOW.categories`

Labels: use-case, backend, categories
Assignee:

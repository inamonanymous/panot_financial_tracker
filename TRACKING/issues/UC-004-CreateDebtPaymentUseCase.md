Title: [UC-004] CreateDebtPaymentUseCase — Debt payment (creates expense + debt_payment)

Summary
- Create an expense from a debt payment and a debt_payment record; create a generated category if missing.

Acceptance criteria
- [ ] Debt exists and belongs to user; otherwise fail.
- [ ] Expense saved and `debt_payments` entry created transactionally.
- [ ] Category is auto-created when missing.

References
- `app/use_cases/create_debt_payment.py`
- `app/routes/r_users.py` (/debt_payment)

Components / Prereqs
- `TransactionPolicy`, `CategoryPolicy`, `FinancialCalculationsPolicy`
- `UOW.debts`, `UOW.expenses`, `UOW.categories`, `UOW.debt_payments`

Labels: use-case, backend, debt
Assignee:

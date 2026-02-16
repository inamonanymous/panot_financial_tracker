Title: [UC-003] DashboardReportingUseCase — Aggregate dashboard metrics

Summary
- Calculate total income, total expense, total saving deposits and net user value.

Acceptance criteria
- [ ] Returns correct sums for income, expense and saving deposits.
- [ ] Uses `UOW.incomes` / `UOW.expenses` and `SavingTransactions` consistency.
- [ ] Edge-cases (no records) return zeros, not nulls.

References
- `app/use_cases/dashboard_reporting.py`
- `app/routes/r_users.py` (/dashboard)

Components / Prereqs
- `m_Income`, `m_Expenses`, `m_SavingTransactions`
- DB query used in `_calculate_total_saving_deposits`

Labels: use-case, backend, reporting
Assignee:

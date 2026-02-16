# Use Case Tracker (auto-generated)

| ID | Use case | File | Route(s) | Short description | Status | Components |
|---:|---|---|---|---|---|---|
| UC-001 | CheckLoginUseCase | `app\use_cases\check_login.py` | r_users.py:/,/login,/dashboard,/debt_payment,/logout,/registration | Authenticates user login with email and password. | Backlog | p_UserPolicy, m_Users |
| UC-002 | CreateDebtPaymentUseCase | `app\use_cases\create_debt_payment.py` | r_users.py:/,/login,/dashboard,/debt_payment,/logout,/registration | Orchestrates creating a debt payment (category -> expense -> debt_payment)

The use-case expects repositories to be provided via a UnitOfWork instance
that exposes `debts`, `categories`, `expenses`, a | Backlog | p_TransactionPolicy, p_CategoryPolicy, p_FinancialCalculations, m_DebtPayments |
| UC-003 | CreateUserUseCase | `app\use_cases\create_user.py` | r_users.py:/,/login,/dashboard,/debt_payment,/logout,/registration | Orchestrates user registration with validation and atomic transaction. | Backlog | p_UserPolicy, m_Users |
| UC-004 | DashboardReportingUseCase | `app\use_cases\dashboard_reporting.py` | r_users.py:/,/login,/dashboard,/debt_payment,/logout,/registration | Aggregates dashboard metrics using repositories and domain services. | Backlog | m_Income, m_Expenses, m_SavingTransactions |
| UC-005 | GetUserCategoriesUseCase | `app\use_cases\get_user_categories.py` | r_expense.py:/insert_expense,/expense, r_income.py:/insert_income,/income |  | Backlog |  |
| UC-006 | CreateExpenseUseCase | `app\use_cases\expense\create_expense.py` | r_expense.py:/insert_expense,/expense |  | Backlog | p_TransactionPolicy |
| UC-007 | GetUserExpenseUseCase | `app\use_cases\expense\get_user_expense.py` | r_expense.py:/insert_expense,/expense |  | Backlog | m_Expenses |
| UC-008 | CreateIncomeUseCase | `app\use_cases\income\create_income.py` | r_income.py:/insert_income,/income |  | Backlog | p_TransactionPolicy |
| UC-009 | GetUserIncomeUseCase | `app\use_cases\income\get_user_income.py` | r_income.py:/insert_income,/income |  | Backlog | m_Income |
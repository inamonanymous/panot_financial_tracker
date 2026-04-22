# Finance Project Blueprint (Current + Planned)

Last Updated: 2026-04-22
Project Type: Web App (Flask + SQLAlchemy + Jinja + MySQL)
Architecture: Route → Use Case → Policy/Domain Service → Repository → ORM Model

## 1) Product Vision
Build a personal finance tracker where a user can manage income, expenses, categories, debts, and savings, then view useful financial summaries and reports.

## 2) Scope Definition
### In Scope (Implemented)
- Authentication: register, login, logout
- Session-protected dashboard summary
- Income: create, list, edit
- Expense: create, list, edit
- Categories: create, edit (income/expense contexts)
- Category description field support
- Debt payment flow (creates expense + debt payment record)
- Debt page + edit flow (partial debt CRUD)
- **Saving goal payment flow** (creates expense + saving transaction)
  - `AddSavingGoalPaymentUseCase` orchestration
  - Dynamic current amount calculation from transaction history
  - Automatic category generation for saving goal deposits
- **Saving goal progress/current amount calculation in persistence layer** (repository/UOW)
- **Debt current amount/progress calculation in persistence layer** (repository/UOW)
- **Fixed saving goal payment flow** to set expense_id after expense save

### In Scope (Planned / Not Fully Wired)
- Transaction deletion (income/expense)
- Category delete with reference protection
- Full debt CRUD module
- Savings goals CRUD pages/routes (payment flow implemented)
- Reporting & analytics dashboards
- Charts (trend/composition/payoff)
- Export (CSV/PDF)
- Budget planning and notifications

### Out of Scope (Current Sprint)
- Enterprise multi-tenancy
- Third-party banking integrations
- Advanced IAM/SSO

## 3) Users and Core Journeys
### Primary User
- Individual account owner tracking personal finances

### Core User Journeys
1. Register/login and access dashboard
2. Add income/expense with category
3. Edit income/expense and categories
4. Record debt payments
5. Track totals and net financial position

### Planned Journeys
- Delete transaction safely
- Manage debt records fully
- Set/track savings goals (payment flow exists, CRUD UI needed)
- Record and monitor multiple deposits to a single saving goal
- View monthly/yearly analytics

## 4) Functional Requirements (Module View)
### Auth
- FR-A1: Register user with validated fields
- FR-A2: Login user with session
- FR-A3: Logout clears session

### Income
- FR-I1: Create income with required `name` + `source`
- FR-I2: List incomes by user
- FR-I3: Edit income owned by user

### Expense
- FR-E1: Create expense with required `name` + `payee`
- FR-E2: List expenses by user
- FR-E3: Edit expense owned by user

### Category
- FR-C1: Create category by type (`income` or `expense`)
- FR-C2: Edit category name/description
- FR-C3: Enforce ownership checks
- FR-C4 (Planned): Delete with reference checks

### Dashboard
- FR-D1: Show total income/expense/savings/debt impact summary

### Debt
- FR-DB1: Record debt payment
- FR-DB2: List and edit owned debt records
- FR-DB3 (Planned): Delete debt record

### Savings / Reporting
- FR-S1: Add saving goal payment (Implemented)
- FR-S2: Calculate saving goal current amount from transaction history (Implemented)
- FR-S3 (Planned): Savings goal CRUD pages/routes
- FR-S4 (Planned): View savings goal progress and timeline
- FR-R1 (Planned): Monthly/yearly reports and charts

## 5) Non-Functional Requirements
- Security: input validation by policy layer, hashed passwords, session-guarded routes
- Maintainability: layered architecture + use-case centric logic
- Data integrity: user ownership checks, UoW transaction boundaries
- Performance: route-level data retrieval by user scope
- Observability (Needed): structured logging and error tracing

## 6) Technical Architecture (Current)
### Backend Stack
- Python + Flask
- Flask-SQLAlchemy, Flask-Migrate, Flask-Session
- MySQL (SQLAlchemy models)

### Layering
- Routes: HTTP concerns and rendering/redirects
- Use Cases: orchestration and application rules
- Policies: validation and business guards
- Domain Services: calculations and financial logic
- Repositories/UoW: persistence and transaction control

### UI
- Server-rendered templates (Jinja)
- Bootstrap-based pages, modals, cards, tables
- Shared page scripts in static JS

## 7) Data Domain (High-Level Entities)
- User
- Category
- Income
- Expense
- Debt
- DebtPayment
- SavingGoal
- SavingTransaction

## 8) API/Route Surface (Current)
### Users
- `GET /`
- `GET|POST /login`
- `GET|POST /registration`
- `GET /dashboard`
- `POST /debt_payment`
- `GET /logout`

### Income
- `GET /income`
- `POST /insert_income`
- `GET /api/income/<income_id>`
- `POST /update_income/<income_id>`
- `POST /insert_income_category`
- `POST /update_income_category/<category_id>`
- `GET /api/income/categories/<category_id>`

### Expense
- `GET /expense`
- `POST /insert_expense`
- `GET /api/expense/<expense_id>`
- `POST /update_expense/<expense_id>`
- `POST /insert_expense_category`
- `POST /update_expense_category/<category_id>`
- `GET /api/expense/categories/<category_id>`

### Saving Goals
- `GET /saving_goals` (List - route exists, UI enhanced)
- `GET /saving_goal_details/<goal_id>` (Details page with progress and history)
- `POST /add_saving_goal_payment/<goal_id>` (Implemented)
- `POST /insert_saving_goal` (Planned)
- `POST /update_saving_goal/<goal_id>` (Planned)
- `POST /delete_saving_goal/<goal_id>` (Planned)

## 9) Current Gaps / Risks
- No automated test suite yet
- Some planned modules exist in domain/model but not exposed in routes/UI
- Security hardening and auth behavior still in active tuning
- Documentation is strong, but execution consistency needs tighter change control

## 10) Delivery Plan (Recommended Next Iterations)
### Iteration 1 (Savings Goals Completion) ← NEXT
- Create `CreateSavingGoalUseCase` and route
- Create `EditSavingGoalUseCase` and route
- Create `DeleteSavingGoalUseCase` with safety checks
- Build saving goals list page with progress indicators and payment button (Enhanced)
- Test multi-transaction tracking per goal

### Iteration 2 (CRUD Completeness)
- Income/expense delete flows
- Category delete with dependency protection
- Debt CRUD pages/routes/use-cases
- Monthly/yearly summaries
- Category and trend charts
- Export CSV/PDF baseline

## 11) Definition of Done (Per Feature)
- Route + use case + policy + repository coverage complete
- User ownership checks enforced
- Manual test scenario checklist passed
- Error paths handled with clear user feedback
- Docs updated (`README`, roadmap, guide)

## 12) Suggested Project Artifacts Status
- Vision/Scope: Available
- Architecture: Available
- Data model: Partially documented
- API contract: Partially documented (route map present)
- Test strategy: Missing (needs creation)
- Security baseline: Partial
- Release checklist: Partial

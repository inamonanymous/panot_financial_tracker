# Finance Project — Personal Finance Tracker

Flask web app for tracking personal finances with a layered architecture (Routes → Use Cases → Policies/Domain Services → Repositories → SQLAlchemy models).

**Status (February 18, 2026):** Active development. Core auth, dashboard, income, expense, debt payment, and category management are implemented with create + edit flows.

## What Works Right Now

- User registration and login/logout
- Session-protected dashboard
- Income list + create + edit income
- Expense list + create + edit expense
- Category create/edit APIs for both income and expense pages
- Shared category modal/card UI reused across pages
- Debt payment flow that records both an expense and a debt payment entry
- Server-side sessions and MySQL persistence

## In Progress / Not Fully Wired

- Standalone category blueprint (`app/routes/r_category.py`) exists but is not registered in app factory yet
- Savings goals pages/routes are not exposed yet
- Reports and analytics pages are still planned
- Automated tests are not set up yet

## Recent Changelog

### 2026-02-18
- Added category description support end-to-end (model, policy, repository, UI)
- Added income and expense name support, while keeping source/payee fields
- Added income and expense edit flows (routes, APIs, use-cases, edit modals)
- Unified category UI by reusing shared category modal/card components across income and expense pages
- Updated project documentation (README, project guide, roadmap) to reflect current state

---

## Quick Start

From project root:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open: `http://127.0.0.1:5000`

> Note: run command is `python run.py` (no trailing slash).

---

## Environment Variables

Create a `.env` file in project root with:

```env
DATABASE_URI=mysql+mysqldb://<user>:<password>@<host>/<database>
SECRET_KEY=your_secret_key
SESSION_TYPE=sqlalchemy
SESSION_PERMANENT=false
SESSION_USE_SIGNER=true
PERMANENT_SESSION_LIFETIME=3600
```

The app reads these in `app/config.py`.

---

## Current Route Map

### Users (`app/routes/r_users.py`)
- `GET /` → redirect to login
- `GET|POST /login`
- `GET|POST /registration`
- `GET /dashboard` (requires session)
- `POST /debt_payment` (requires session)
- `GET /logout`

### Income (`app/routes/r_income.py`)
- `GET /income` (requires session)
- `POST /insert_income` (requires session)
- `GET /api/income/<income_id>` (requires session)
- `POST /update_income/<income_id>` (requires session)
- `POST /insert_income_category` (requires session)
- `POST /update_income_category/<category_id>` (requires session)
- `GET /api/income/categories/<category_id>` (requires session)

### Expense (`app/routes/r_expense.py`)
- `GET /expense` (requires session)
- `POST /insert_expense` (requires session)
- `GET /api/expense/<expense_id>` (requires session)
- `POST /update_expense/<expense_id>` (requires session)
- `POST /insert_expense_category` (requires session)
- `POST /update_expense_category/<category_id>` (requires session)
- `GET /api/expense/categories/<category_id>` (requires session)

---

## How the App Works (Request Flow)

Typical write flow (example: insert income):

1. Route collects form data and injects current `user_id`
2. Use case validates input using `TransactionPolicy`
3. Use case verifies ownership/state with repositories (e.g., category belongs to user)
4. Use case creates entity/ORM via repository
5. Persistence happens inside `UnitOfWork.transaction()`
6. Route redirects to page on success, or with `error_message` on failure

This keeps responsibilities separated:

- **Routes**: HTTP and redirects/templates
- **Policies**: input validation and guard rules
- **Use cases**: orchestration/business flow
- **Domain services**: pure calculations (net worth, debt math, savings analysis)
- **Repositories + UoW**: data access and transaction safety

---

## Architecture Snapshot

```
HTTP Request
    ↓
Blueprint Routes (app/routes)
    ↓
Use Cases (app/use_cases)
    ↓
Policies (app/domain/policies) + Domain Services (app/domain/services)
    ↓
Repository Interfaces (app/repositories)
    ↓
Repository Implementations (app/persistence/repositories)
    ↓
SQLAlchemy Models (app/model) + MySQL
```

`app/service/__init__.py` exposes a pre-wired shared `UOW` instance created by `app.persistence.create_unit_of_work()`.

---

## Key Files

- `run.py` — app entry point
- `app/__init__.py` — app factory, extension setup, blueprint registration
- `app/config.py` — environment-based configuration
- `app/persistence/unit_of_work.py` — transaction manager
- `app/use_cases/` — app-level workflows (auth, income, expense, dashboard, debt payment)
- `app/domain/policies/` — validation policies
- `app/domain/services/` — pure finance calculators/analyzers

---

## Implemented Templates

- `app/templates/public/login.html`
- `app/templates/public/register.html`
- `app/templates/auth/pages/dashboard.html`
- `app/templates/auth/pages/income.html`
- `app/templates/auth/pages/expense.html`
- Shared category templates:
    - `app/templates/auth/modals/add_category.html`
    - `app/templates/auth/modals/edit_category.html`
    - `app/templates/auth/cards/categories_card.html`
- Transaction edit templates:
    - `app/templates/auth/modals/edit_income.html`
    - `app/templates/auth/modals/edit_expense.html`

---

## Database & Migrations

- ORM: Flask-SQLAlchemy / SQLAlchemy
- Migrations: Alembic in `migrations/`
- App currently also calls `db.create_all()` during startup (`generate_tables`) to ensure missing tables are created

---

## Development Notes

- No formal test suite yet
- If you add a new feature, follow this pattern:
  1. Add/extend policy validation
  2. Implement use case
  3. Add repository method (if needed)
  4. Add route/template
  5. Keep DB writes inside `uow.transaction()`

For detailed design and roadmap, see `PROJECT_GUIDE.md` and `DEVELOPMENT_ROADMAP.md`.

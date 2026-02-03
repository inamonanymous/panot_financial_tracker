# Finance Project — Personal Finance Tracker

A Flask-based web application for tracking income, expenses, debts, and savings goals. Built with a clean layered architecture separating validation, business rules, orchestration, and persistence.

## Quick Start

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Visit `http://127.0.0.1:5000` and register or log in.

---

## Architecture Overview

This project uses **Clean Architecture** with these key layers:

```
HTTP Request
    ↓
Routes (app/routes)
    ↓
Use Cases (app/use_cases) — orchestration & business flows
    ↓
Policies (app/domain/policies) — input validation
Domain Services (app/domain/services) — pure business logic & calculations
    ↓
Repositories (app/repositories) + UnitOfWork (app/persistence/unit_of_work.py)
    ↓
Database (SQLAlchemy ORM models in app/model)
```

### Core Concepts

- **Policies** (`app/domain/policies`): Input validation only. No DB access. No business calculations. Just type/format/constraint checks.
- **Domain Services** (`app/domain/services`): Pure, stateless business functions (debt math, financial ratios, net worth). Unit-testable.
- **Use Cases** (`app/use_cases`): Orchestrate request flows. Validate input → run DB/state checks → call domain services → persist via repositories inside a transaction.
- **Repositories** (`app/repositories`): Data access. Abstraction over SQLAlchemy ORM models.
- **UnitOfWork** (`app/persistence/unit_of_work.py`): Transaction manager. Exposes repositories and commit/rollback semantics.

---

## Directory Structure

```
app/
├── domain/
│   ├── entities/          # Plain constructors (Category, Expense, Income, Debt, etc.)
│   ├── policies/          # Input validation (BasePolicy + specific policies)
│   └── services/          # Business rules (FinancialCalculator, DebtCalculator, etc.)
├── use_cases/             # Application orchestration (CreateUserUseCase, CreateDebtPaymentUseCase, etc.)
├── routes/                # Flask HTTP endpoints (r_users.py, r_income.py, etc.)
├── repositories/          # Data access layer (user_repository.py, expense_repository.py, etc.)
├── persistence/           # UnitOfWork and transaction handling
├── model/                 # SQLAlchemy ORM models (m_Users.py, m_Debts.py, etc.)
├── validators/            # Low-level format validators (date_validator, email_validator, etc.)
├── utils/                 # Utilities and exceptions
├── templates/             # Jinja2 templates
├── static/                # CSS, JS, images
├── ext.py                 # Flask extensions (db, etc.)
├── config.py              # Configuration
└── __init__.py            # App factory (create_app)
```

---

## Data Flow (Request → Response)

### Example: Creating an Income Record

1. **Route** (`app/routes/r_income.py`) receives HTTP POST `/income` with JSON data.
2. **Route** calls the use-case: `CreateIncomeUseCase.execute(income_data)`.
3. **Use Case** calls `TransactionPolicy.validate_insert_income(income_data)`.
4. **Policy** validates input only (required fields, types, formats, ranges). Returns cleaned data or raises `PolicyError`.
5. **Use Case** performs DB/state checks using repositories:
   - Does the category exist?
   - Does the user own this category?
6. **Use Case** calls domain service for any calculations (if needed).
7. **Use Case** persists using `UnitOfWork`:
   ```python
   with uow.transaction():
       saved_income = uow.incomes.save(income_entity)
   ```
8. **Route** returns the response (JSON or redirect).

---

## Where to Add New Code

### Pure Business Logic (Calculations, Analysis)
→ Add functions to `app/domain/services/*.py`

**Example:**
```python
# app/domain/services/my_calculator.py
class MyCalculator:
    @staticmethod
    def calculate_something(value: float) -> float:
        return value * 0.1  # Pure math, no DB access
```

### Input Validation
→ Add methods to `app/domain/policies/*.py` (inherit from `BasePolicy`)

**Example:**
```python
# app/domain/policies/p_MyPolicy.py
class MyPolicy(BasePolicy):
    def validate_my_input(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["field1", "field2"],
            allowed=["field1", "field2", "field3"]
        )
        clean["field1"] = self.validate_string(clean["field1"], "Field 1", min_len=3)
        return clean
```

### Business Flows & Orchestration
→ Add use-cases to `app/use_cases/*.py`

**Example:**
```python
# app/use_cases/create_my_thing.py
from app.domain.policies.p_MyPolicy import MyPolicy
from app.domain.services.my_calculator import MyCalculator

class CreateMyThingUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.policy = MyPolicy()
    
    def execute(self, data: dict):
        clean_data = self.policy.validate_my_input(data)
        
        # Perform state checks
        existing = self.uow.my_repo.find_by_name(clean_data["field1"])
        if existing:
            raise Exception("Already exists")
        
        # Call domain service
        computed = MyCalculator.calculate_something(clean_data["amount"])
        
        # Persist
        with self.uow.transaction():
            my_entity = MyEntity(**clean_data)
            saved = self.uow.my_repo.save(my_entity)
        
        return saved
```

### Data Access (DB Queries)
→ Add methods to `app/repositories/*.py`

**Example:**
```python
# app/repositories/my_repository.py
class MyRepository(Repository):
    def find_by_name(self, name: str):
        return self.session.query(MyORM).filter_by(name=name).first()
```

### HTTP Endpoints
→ Add routes to `app/routes/*.py`

**Example:**
```python
# app/routes/r_my_route.py
from flask import request, jsonify
from app.use_cases.create_my_thing import CreateMyThingUseCase
from app.persistence.unit_of_work import UnitOfWork

@app.route('/my-endpoint', methods=['POST'])
def my_endpoint():
    uow = UnitOfWork()
    use_case = CreateMyThingUseCase(uow)
    try:
        result = use_case.execute(request.json)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
```

---

## Key Patterns

### BasePolicy
All policies inherit from `BasePolicy` which provides:
- `create_resource(data, required=[], allowed=[])` — validates required fields, normalizes strings, filters allowed fields
- `update_resource(data, allowed=[])` — for edit operations
- `validate_string(value, field, min_len)` — string validation
- `validate_numeric_values(value, field, allow_zero=False)` — money-safe number validation
- `validate_date_value(value, field, allow_future, allow_past)` — date validation
- `validate_email_string(email)` — email validation
- `validate_password_string(password, confirm, min_len)` — password validation

### UnitOfWork Pattern
```python
from app.persistence.unit_of_work import UnitOfWork

uow = UnitOfWork()
with uow.transaction():
    user = uow.users.save(user_entity)
    income = uow.incomes.save(income_entity)
    # If all succeeds → commits
    # If any fails → rolls back
```

### Error Handling
- **PolicyError**: raised by policies when input validation fails
- **Exception**: raised by use-cases for business logic violations
- Routes catch and translate into HTTP responses

---

## Features

- ✅ User registration & authentication (email, password hashing)
- ✅ Income tracking (add, edit, delete)
- ✅ Expense tracking with categories
- ✅ Debt management with due dates
- ✅ Savings goals
- ✅ Dashboard with summaries
- ⏳ Reports (planned)
- ⏳ Charts & analytics (planned)

---

## Database

- **Engine**: MySQL
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Migrations**: Alembic (in `migrations/` folder)

All financial values (totals, ratios) are **computed on-demand** using SQL aggregations. No cached monetary fields.

---

## Development Notes

### Running Tests
Not yet set up. Unit tests should test domain services independently; integration tests should test use-cases with mocked UnitOfWork.

### Adding a New Feature
1. Define the domain entity (if new) in `app/domain/entities/`
2. Add validation rules to `app/domain/policies/`
3. Add business logic to `app/domain/services/`
4. Create a use-case in `app/use_cases/`
5. Add a repository method in `app/repositories/`
6. Add a route in `app/routes/`
7. Create a template if needed

### Code Style
- Use type hints where possible
- Keep policies stateless and side-effect-free
- Keep domain services pure (no I/O, no mutations)
- Use UnitOfWork for all DB transactions

---

## Contact & License

- **Author**: Stephen Joaquin Aguilar
- **Project**: Finance Tracker 2025-2026
- **License**: Educational/Personal Use

# Finance Project — Complete Project Guide

**Last Updated:** February 18, 2026  
**Author:** Stephen Joaquin Aguilar  
**Status:** Active Development

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Design Principles](#architecture--design-principles)
3. [Technology Stack](#technology-stack)
4. [Directory Structure](#directory-structure)
5. [Core Concepts & Patterns](#core-concepts--patterns)
6. [Data Models](#data-models)
7. [Features](#features)
8. [Development Workflow](#development-workflow)
9. [Adding New Features](#adding-new-features)
10. [Common Patterns & Examples](#common-patterns--examples)
11. [Troubleshooting](#troubleshooting)
12. [Future Enhancements](#future-enhancements)

---

## Project Overview

**Finance Project** is a personal finance tracker web application built with Flask and SQLAlchemy. It helps users:
- Track income and expenses
- Manage debts with interest calculations
- Set and monitor savings goals
- View financial dashboards and summaries
- Categorize transactions by type

### Why This Project Exists

The original project had mixed concerns — business logic scattered across multiple "service" classes, no clear separation between validation and business rules, and tightly coupled persistence logic. This refactored version reorganizes the codebase using **Clean Architecture** principles:

- **Policies** handle input validation only
- **Domain Services** contain pure business rules
- **Use Cases** orchestrate workflows and transactions
- **Repositories** abstract data access
- **UnitOfWork** manages transactions

---

## Architecture & Design Principles

### Layered Architecture

```
┌─────────────────────────────┐
│    HTTP Routes (Flask)      │  app/routes
├─────────────────────────────┤
│    Use Cases (Orchestration)│  app/use_cases
├─────────────────────────────┤
│ Policies (Validation)       │  app/domain/policies
│ Domain Services (Logic)     │  app/domain/services
├─────────────────────────────┤
│ Repositories (Data Access)  │  app/repositories
│ UnitOfWork (Transactions)   │  app/persistence
├─────────────────────────────┤
│ ORM Models (SQLAlchemy)     │  app/model
├─────────────────────────────┤
│      Database (MySQL)       │
└─────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**
   - Policies: Input validation only (no DB, no calculations)
   - Domain Services: Pure business logic (stateless, deterministic)
   - Use Cases: Orchestration and transaction management
   - Repositories: Data access abstraction

2. **Dependency Injection**
   - Use cases receive a `UnitOfWork` instance
   - Routes pass `UnitOfWork` to use cases
   - Policies are instantiated within use cases

3. **No Circular Dependencies**
   - Routes → Use Cases → Policies, Services, Repositories
   - Never: Use Cases → Routes, Repositories → Routes

4. **Fail-Fast Validation**
   - Policies validate input before any DB operations
   - Invalid input raises `PolicyError` immediately

5. **Transaction Safety**
   - All DB operations wrapped in `UnitOfWork.transaction()`
   - Automatic rollback on exception

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Flask | 3.1.2 |
| **Database** | MySQL | 8.0+ |
| **ORM** | SQLAlchemy | (from Flask-SQLAlchemy) |
| **Sessions** | Flask-Session | 0.8.0 |
| **Migrations** | Alembic | |
| **Python** | Python | 3.10+ |
| **Password Hash** | Werkzeug | 3.1.3 |

### Python Dependencies

See `requirements.txt` for full list. Key packages:
- `Flask` — web framework
- `Flask-SQLAlchemy` — ORM and DB integration
- `Flask-Session` — server-side sessions
- `Werkzeug` — password hashing, WSGI utilities
- `Alembic` — database migrations

---

## Directory Structure

```
Finance Project/app/
│
├── README.md                      # Quick start & overview
├── PROJECT_GUIDE.md              # This file
├── ARCHITECTURE_README.md         # Architecture summary
├── requirements.txt              # Python dependencies
├── run.py                        # Entry point
│
├── app/
│   ├── __init__.py              # Factory function: create_app()
│   ├── config.py                # Configuration (DB, SECRET_KEY, etc.)
│   ├── ext.py                   # Flask extensions (db)
│   │
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── category.py
│   │   │   ├── debt.py
│   │   │   ├── expense.py
│   │   │   ├── income.py
│   │   │   ├── saving_goal.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── policies/
│   │   │   ├── BasePolicy.py       # Base class with validation helpers
│   │   │   ├── p_CategoryPolicy.py
│   │   │   ├── p_FinancialCalculations.py
│   │   │   ├── p_TransactionPolicy.py
│   │   │   ├── p_UserPolicy.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/
│   │   │   ├── debt_calculator.py
│   │   │   ├── financial_calculator.py
│   │   │   ├── net_worth_calculator.py
│   │   │   ├── saving_goal_analyzer.py
│   │   │   ├── transaction_analyzer.py
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── use_cases/
│   │   ├── check_login.py
│   │   ├── create_debt_payment.py
│   │   ├── create_user.py
│   │   ├── dashboard_reporting.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   ├── category_repository.py
│   │   ├── debt_payments_repository.py
│   │   ├── debt_repository.py
│   │   ├── expense_repository.py
│   │   ├── income_repository.py
│   │   ├── repository.py          # Base Repository class
│   │   ├── saving_goal_repository.py
│   │   ├── saving_transactions_repository.py
│   │   ├── user_repository.py
│   │   ├── exceptions.py
│   │   └── __init__.py
│   │
│   ├── persistence/
│   │   ├── unit_of_work.py       # UnitOfWork transaction manager
│   │   └── __init__.py
│   │
│   ├── model/
│   │   ├── m_Admin.py
│   │   ├── m_Categories.py
│   │   ├── m_DebtPayments.py
│   │   ├── m_Debts.py
│   │   ├── m_Expenses.py
│   │   ├── m_Income.py
│   │   ├── m_SavingGoals.py
│   │   ├── m_SavingTransactions.py
│   │   ├── m_Users.py
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── r_income.py
│   │   ├── r_users.py
│   │   ├── functions.py           # Shared route utilities
│   │   └── __init__.py
│   │
│   ├── validators/
│   │   ├── date_validator.py
│   │   ├── email_validator.py
│   │   ├── numeric_validator.py
│   │   ├── string_validator.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── exceptions/
│   │   │   ├── PolicyError.py
│   │   │   ├── ServiceError.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── pages/
│   │   │       ├── income.html
│   │   │       ├── expenses.html
│   │   │       ├── debts.html
│   │   │       ├── savings.html
│   │   │       └── dashboard.html
│   │   └── public/
│   │       └── ...
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   ├── scss/
│   │   └── vendor/
│   │       ├── bootstrap/
│   │       ├── fontawesome/
│   │       ├── jquery/
│   │       └── ...
│   │
│   └── service/
│       ├── __init__.py            # Helper functions (password hashing, etc.)
│       └── (legacy service wrappers — removed during refactoring)
│
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 337101cc7d91_...py
│       ├── 61f19152c4f3_...py
│       ├── ...
│       └── __pycache__/
│
└── venv/                          # Python virtual environment
```

---

## Core Concepts & Patterns

### 1. Policies (Input Validation)

**Location:** `app/domain/policies/`

**Purpose:** Validate user input. No database access. No side effects.

**Base Class:** `BasePolicy` provides:
- `create_resource(data, required=[], allowed=[])` — validate required fields, strip whitespace, filter allowed fields
- `update_resource(data, allowed=[])` — for PATCH/PUT operations
- `validate_string(value, field, min_len)` — string type & length
- `validate_numeric_values(value, field, allow_zero=False)` — safe number validation
- `validate_date_value(value, field, allow_future, allow_past)` — date validation
- `validate_email_string(email)` — email format
- `validate_password_string(password, confirm, min_len)` — password strength

**Example:**

```python
# app/domain/policies/p_TransactionPolicy.py
class TransactionPolicy(BasePolicy):
    def validate_insert_income(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["user_id", "category_id", "source", "amount", "payment_method", "received_date"],
            allowed=[...same fields...]
        )
        clean["amount"] = self.validate_numeric_values(
            clean["amount"], "Amount", allow_zero=False
        )
        return clean
```

**When to Use:**
- Always validate user input from routes
- Call policy methods in use cases BEFORE any DB operations
- Raise `PolicyError` on validation failure

---

### 2. Domain Services (Business Logic)

**Location:** `app/domain/services/`

**Purpose:** Pure, deterministic business calculations. Testable without database.

**Characteristics:**
- No database access
- No side effects
- Accept plain values, return computed results
- Stateless (can be static methods or classes with no state)

**Example:**

```python
# app/domain/services/debt_calculator.py
class DebtCalculator:
    @staticmethod
    def monthly_payment(principal: float, interest_rate: float, months: int) -> float:
        """Calculate monthly debt payment using standard amortization formula."""
        if months == 0:
            return principal
        monthly_rate = interest_rate / 100 / 12
        if monthly_rate == 0:
            return principal / months
        return principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    
    @staticmethod
    def days_until_due(due_date) -> int:
        """Calculate days from today until due date."""
        from datetime import date
        today = date.today()
        return (due_date - today).days
```

**Current Services:**
- `debt_calculator.py` — interest, monthly payment, days/months until due
- `financial_calculator.py` — balance, available balance, ratios
- `net_worth_calculator.py` — total assets vs. liabilities
- `transaction_analyzer.py` — income/expense analysis
- `saving_goal_analyzer.py` — savings progress metrics

**When to Use:**
- Extract any complex calculations from use cases into domain services
- Add new metrics/analysis logic here
- Unit-test these independently

---

### 3. Use Cases (Orchestration)

**Location:** `app/use_cases/`

**Purpose:** Orchestrate request flows. Combine validation, state checks, business logic, and persistence.

**Typical Flow:**
1. Receive input data
2. Call policy to validate
3. Use repositories to check state (e.g., "does resource exist?")
4. Call domain services for calculations
5. Persist via UnitOfWork transaction
6. Return result

**Example:**

```python
# app/use_cases/create_debt_payment.py
class CreateDebtPaymentUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
    
    def execute(self, debt_data: dict, expense_data: dict):
        # Step 1: Validate
        clean_debt = self.tx_policy.validate_insert_debt_payment(debt_data)
        
        # Step 2: Check state
        debt = self.uow.debts.get_by_id_and_user_id(clean_debt["debt_id"], clean_debt["user_id"])
        if debt is None:
            raise Exception("Debt not found")
        
        # Step 3: Compute (if needed)
        # ...
        
        # Step 4: Persist
        with self.uow.transaction():
            saved_debt_payment = self.uow.debt_payments.save(...)
        
        return saved_debt_payment
```

**Existing Use Cases:**
- `check_login.py` — authenticate user
- `create_user.py` — register new user
- `create_debt_payment.py` — record debt payment
- `dashboard_reporting.py` — aggregate financial summaries

**When to Create New Use Cases:**
- New endpoint or workflow
- Multi-step process (validate → check → compute → persist)
- Complex orchestration that mixes multiple entities

---

### 4. Repositories (Data Access)

**Location:** `app/repositories/`

**Purpose:** Abstract database queries. Hide SQLAlchemy details.

**Base Class:** `Repository`

```python
# app/repositories/repository.py
class Repository:
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class
    
    def save(self, entity) -> object:
        """Save (insert or update) an entity."""
        self.session.add(entity)
        self.session.flush()
        return entity
    
    def delete(self, entity) -> None:
        """Delete an entity."""
        self.session.delete(entity)
        self.session.flush()
    
    def get_by_id(self, id: int) -> object:
        """Get entity by primary key."""
        return self.session.query(self.model_class).filter_by(id=id).first()
```

**Specific Repositories:**
- `user_repository.py` — load/save users
- `category_repository.py` — category CRUD
- `income_repository.py` — income CRUD
- `expense_repository.py` — expense CRUD
- `debt_repository.py` — debt CRUD
- etc.

**When to Add Methods:**
- New query needed in a use case → add query method to repository
- Complex filter logic → hide it in repository
- Reusable query across multiple use cases → definitely in repository

**Example:**

```python
# app/repositories/user_repository.py
class UserRepository(Repository):
    def find_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()
    
    def find_all_by_active(self, active: bool = True):
        return self.session.query(User).filter_by(is_active=active).all()
```

---

### 5. UnitOfWork (Transaction Manager)

**Location:** `app/persistence/unit_of_work.py`

**Purpose:** Manage transactions. Expose repositories. Ensure atomicity.

**Key Methods:**
- `transaction()` — context manager for ACID transactions
- `commit()` — commit current transaction
- `rollback()` — rollback changes

**Exposed Repositories:**
- `uow.users`
- `uow.categories`
- `uow.incomes`
- `uow.expenses`
- `uow.debts`
- `uow.saving_goals`
- etc.

**Usage:**

```python
from app.persistence.unit_of_work import UnitOfWork

uow = UnitOfWork()

# Method 1: Explicit context manager
with uow.transaction():
    user = uow.users.get_by_id(1)
    user.name = "New Name"
    saved = uow.users.save(user)  # Auto-commits on exit

# Method 2: Manual
uow.begin()
try:
    user = uow.users.get_by_id(1)
    uow.commit()
except Exception:
    uow.rollback()
    raise
```

---

## Data Models

### User

```python
# app/model/m_Users.py
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Relationships:**
- Has many `Categories` (user-specific)
- Has many `Income` records
- Has many `Expense` records
- Has many `Debts`
- Has many `SavingGoals`

---

### Category

```python
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum('income', 'expense'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Rules:**
- User-specific (each user has their own categories)
- Type-restricted ('income' or 'expense')
- Cannot delete if in use

---

### Income

```python
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    received_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Enum('cash', 'gcash', 'bank', 'card', 'other'), default='cash')
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### Expense

```python
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    payee = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Enum('cash', 'gcash', 'bank', 'card', 'other'), default='cash')
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### Debt

```python
class Debts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lender = db.Column(db.String(255), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # Annual percentage
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Business Rules:**
- Principal >= 100 PHP
- Interest rate 0-6%
- Due date must be in future

---

### DebtPayment

```python
class DebtPayments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    debt_id = db.Column(db.Integer, db.ForeignKey('debts.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    pymt_type = db.Column(db.Enum('deposit', 'withdraw'), default='deposit')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### SavingGoal

```python
class SavingGoals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    target_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## Features

### ✅ Implemented

- **User Management**
  - Registration with email & password
  - Password hashing (Werkzeug)
  - Login/logout with sessions
    - Session-protected routes and dashboard access

- **Transaction Tracking**
    - Income create/list/edit
    - Expense create/list/edit
    - Validation requires separate fields:
        - Income: `name` + `source`
        - Expense: `name` + `payee`
    - User-owned category checks before save/update
    - Multiple payment methods

- **Debt Management**
  - Debt payment recording (creates expense)

- **Category Management**
    - Category create/edit in both income and expense pages
    - Category description support
    - Shared category modal/card components reused across pages

- **Dashboard**
    - Financial summary (total income, expenses, savings deposits)
    - Net value calculation

---

### ⏳ Planned

- **Transaction Deletion Flows**
    - Income/expense delete use cases + routes + UI confirm modals

- **Debt CRUD Module**
    - Debt create/list/edit/delete pages and use cases

- **Savings Module**
    - Savings goal and saving transaction routes/pages

- **Analytics & Reports**
  - Monthly/yearly summaries
  - Spending trends
  - Category breakdowns

- **Charts**
  - Pie charts for expense distribution
  - Line charts for income/expense over time
  - Debt payoff timeline

- **Export**
  - PDF reports
  - CSV export

- **Budget Planning**
  - Set monthly budgets
  - Budget vs. actual comparison

- **Notifications**
  - Upcoming debt due dates
  - Savings goal milestones

---

## Development Workflow

### 1. Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database and run migrations (if needed)
flask db upgrade
```

### 2. Running the App

```powershell
python run.py
```

Visit `http://127.0.0.1:5000`

### 3. Making Changes

Follow this workflow:

1. **Define the feature request** — what user action, input, output?
2. **Create/update domain entity** — if new type of data
3. **Write policy validation** — input validation rules
4. **Write domain service** — business logic (if applicable)
5. **Write use case** — orchestrate workflow
6. **Add repository methods** — DB queries needed
7. **Create/update route** — HTTP endpoint
8. **Create/update template** — UI (if applicable)
9. **Test manually** — run app and test the flow

### 4. Common Tasks

#### Add a New Field to User

1. Create migration:
   ```powershell
   flask db migrate -m "Add field_name to users"
   ```

2. Edit migration file to define the change

3. Apply migration:
   ```powershell
   flask db upgrade
   ```

4. Update model in `app/model/m_Users.py`

5. Update policy in `app/domain/policies/p_UserPolicy.py` (if validation needed)

#### Add a New Repository Method

1. Open the repository file (e.g., `app/repositories/expense_repository.py`)
2. Add method:
   ```python
   def find_by_user_and_date_range(self, user_id: int, start_date, end_date):
       return self.session.query(Expenses).filter(
           Expenses.user_id == user_id,
           Expenses.expense_date >= start_date,
           Expenses.expense_date <= end_date,
       ).all()
   ```

#### Add a New Use Case

1. Create `app/use_cases/my_new_use_case.py`:
   ```python
   from app.domain.policies.p_MyPolicy import MyPolicy
   
   class MyNewUseCase:
       def __init__(self, unit_of_work):
           self.uow = unit_of_work
           self.policy = MyPolicy()
       
       def execute(self, data: dict):
           clean = self.policy.validate_input(data)
           # ... orchestrate ...
           return result
   ```

2. Create `app/routes/r_my_route.py`:
   ```python
   from app.use_cases.my_new_use_case import MyNewUseCase
   from app.persistence.unit_of_work import UnitOfWork
   
   @app.route('/my-endpoint', methods=['POST'])
   def my_endpoint():
       try:
           uow = UnitOfWork()
           use_case = MyNewUseCase(uow)
           result = use_case.execute(request.form.to_dict())
           return redirect('/')
       except Exception as e:
           return render_template('error.html', error=str(e)), 400
   ```

---

## Common Patterns & Examples

### Example 1: Creating an Income Record

**Flow:**
```
Route (/insert_income) 
  → Use Case (validate, check state, persist)
    → Policy (validate_insert_income)
    → Repository (find category, save income)
    → UnitOfWork (transaction)
```

**Route Code:**

```python
# app/routes/r_income.py
@income.route('/insert_income', methods=['POST'])
def insert_income_route():
    try:
        user = get_current_user()
        form_data = request.form.to_dict()
        form_data["user_id"] = user.id
        use_case = CreateIncomeUseCase(UOW)
        income = use_case.execute(form_data)
        return redirect(url_for('income.income_page'))
    except Exception as e:
        return redirect(url_for('income.income_page', error_message=str(e)))
```

**Use Case Code:**

```python
# app/use_cases/income/create_income.py
class CreateIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
    
    def execute(self, data: dict):
        # Validate
        clean = self.tx_policy.validate_insert_income(data)
        
        # Check state
        category = self.uow.categories.get_by_id(clean["category_id"])
        if not category or category.user_id != clean["user_id"]:
            raise Exception("Category not found or doesn't belong to user")
        
        # Persist
        with self.uow.transaction():
            income = Income(
                user_id=clean["user_id"],
                category_id=clean["category_id"],
                name=clean["name"],
                source=clean["source"],
                amount=clean["amount"],
                received_date=clean["received_date"],
                payment_method=clean["payment_method"],
                remarks=clean.get("remarks", "")
            )
            saved = self.uow.incomes.save(income)
        
        return saved
```

---

### Example 2: Computing Debt Monthly Payment

**Domain Service:**

```python
# app/domain/services/debt_calculator.py
class DebtCalculator:
    @staticmethod
    def monthly_payment(principal: float, annual_rate: float, months: int) -> float:
        """Calculate monthly payment using amortization formula."""
        if months == 0:
            return principal
        monthly_rate = annual_rate / 100 / 12
        if monthly_rate == 0:
            return principal / months
        numerator = monthly_rate * (1 + monthly_rate) ** months
        denominator = (1 + monthly_rate) ** months - 1
        return principal * (numerator / denominator)
```

**Use Case Usage:**

```python
from app.domain.services.debt_calculator import DebtCalculator

class ViewDebtDetailsUseCase:
    def execute(self, debt_id: int):
        debt = self.uow.debts.get_by_id(debt_id)
        months_until_due = DebtCalculator.months_until_due(debt.due_date)
        monthly_payment = DebtCalculator.monthly_payment(
            debt.principal, debt.interest_rate, months_until_due
        )
        return {
            "debt": debt,
            "monthly_payment": monthly_payment,
            "months_until_due": months_until_due
        }
```

---

### Example 3: Validating Input

**Policy:**

```python
# app/domain/policies/p_TransactionPolicy.py
class TransactionPolicy(BasePolicy):
    def validate_insert_expense(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["user_id", "category_id", "payee", "amount", "expense_date", "payment_method"],
            allowed=[...same...]
        )
        
        clean["payee"] = self.validate_string(clean["payee"], "Payee", min_len=1)
        clean["amount"] = self.validate_numeric_values(clean["amount"], "Amount", allow_zero=False)
        clean["expense_date"] = self.validate_date_value(
            clean["expense_date"], "Expense Date", allow_future=False, allow_past=True
        )
        clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        
        return clean
```

**Raises `PolicyError` on validation failure.**

---

## Troubleshooting

### Issue: `NameError: name 'IS_INS' is not defined`

**Cause:** Legacy service variable reference.

**Solution:** 
- Remove or replace with use case / repository method
- Example: `IS_INS.get_all_income_by_user(user_id)` → `uow.incomes.find_by_user_id(user_id)`

---

### Issue: `ModuleNotFoundError: No module named 'app.policies'`

**Cause:** Old import from deleted package.

**Solution:**
- Update imports from `app.policies.X` to `app.domain.policies.X`

---

### Issue: Database constraint errors

**Cause:** Violating uniqueness, foreign key, or business rule.

**Solution:**
- Check that policy/use case validates constraints BEFORE persisting
- Ensure use case checks state (e.g., "does category exist?")
- Use `UnitOfWork.transaction()` to rollback on error

---

### Issue: Session/authentication errors

**Cause:** Flask-Session not properly configured.

**Solution:**
- Check `app/config.py` for `SESSION_TYPE`, `SESSION_SQLALCHEMY_TABLE`
- Ensure database has `flask_sessions` table
- Verify `session[key] = value` in login route

---

## Future Enhancements

### Phase 2: Reports & Analytics

- **Income/Expense Summary** by month/year
- **Category Breakdown** (pie charts)
- **Spending Trends** (line charts over time)
- **Savings Progress** visualization

**Implementation:**
- Add domain services in `app/domain/services/report_generator.py`
- Create use cases: `GenerateMonthlyReportUseCase`, etc.
- Create routes: `/reports`, `/analytics`

### Phase 3: Budgeting

- Set monthly budgets per category
- Track budget vs. actual
- Alerts when exceeding budget

**Implementation:**
- New model: `m_Budgets.py`
- New policy: `p_BudgetPolicy.py`
- New service: `budget_analyzer.py`

### Phase 4: Notifications & Reminders

- Email/SMS notifications
- Upcoming debt due dates
- Savings goal milestones

**Implementation:**
- Task queue (Celery + Redis)
- Notification service
- Email templates

### Phase 5: Mobile & API

- REST API for mobile app
- JWT authentication
- Mobile UI

**Implementation:**
- Flask-RESTful or Flask-RESTX
- Separate blueprint for `/api/v1/`
- JWT auth middleware

---

## Code Style & Guidelines

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Class | PascalCase | `UserPolicy`, `DebtCalculator` |
| Function | snake_case | `validate_email_string`, `monthly_payment` |
| Variable | snake_case | `user_id`, `clean_data` |
| Constant | UPPER_SNAKE | `MAX_DEBT_RATE`, `DEFAULT_PAYMENT_METHOD` |
| Private | \_leading_underscore | `_compute_balance` |

### Docstring Format

```python
def validate_numeric_values(self, value, field_name: str = "Amount", *, allow_zero: bool = False) -> float:
    """
    Validate numeric input for money fields.
    
    Args:
        value: The value to validate (int, float, or numeric string)
        field_name: Name of the field (for error messages)
        allow_zero: If True, allows zero; if False, requires > 0
    
    Returns:
        float: Normalized numeric value
    
    Raises:
        PolicyError: If validation fails
    """
```

### Type Hints

Always use type hints:

```python
def execute(self, data: dict) -> Users:
    ...

def get_by_id(self, id: int) -> Optional[User]:
    ...
```

### Error Handling

```python
# In policies/validators
raise PolicyError("Human-readable message")

# In use cases
raise Exception("Business logic error")

# In routes
except PolicyError as e:
    return render_template('error.html', error=str(e)), 400
except Exception as e:
    return render_template('error.html', error="An error occurred"), 500
```

---

## Contact & Support

**Project Owner:** Stephen Joaquin Aguilar  
**Status:** Active Development  
**Last Updated:** February 2026

For questions or issues, refer to this guide or check the repository structure and docstrings in the code.

---

**End of Project Guide**

# Finance Tracker

A personal **Finance Tracker web application** built with **Flask** and **SQLAlchemy**, designed to help users manage income, expenses, debts, and savings goals with a clean service-based architecture.

---

## 📌 Features

### ✅ Phase 1 (Core)

* User registration & authentication
* Income tracking (add / edit / delete)
* Expense tracking with categories
* Debt management with due dates
* Savings goals with transactions
* Dashboard with financial summaries

### ⏳ Phase 2 (Planned)

* Monthly & yearly reports
* Advanced analytics & charts
* Export reports (PDF/CSV)

---

## 🧱 Architecture Overview

This project follows a **layered architecture**:

```
Routes (Controllers)
   ↓
Services (Application Layer)
   ↓
Policies (Business Rules/Validation Layer)
   ↓
Models (Persistence Layer)
   ↓
Database
```

### Why this design?

* Clean separation of concerns
* Easier testing and maintenance
* Use cases or Application layer (Services) stay out of HTTP Requests (Routes)
* Business rules and validations (Policies) stay out of Use Cases or Application layer (Services) 


---

## 📂 Project Structure

```
app/
│
├── models/              # SQLAlchemy models
├── policies/            # Business rules and Validation logic (BasePolicy pattern)
├── routes/              # Flask routes / controllers
├── services/            # Use Cases or Application logic (BaseService pattern)

├── utils/
│   └── exceptions/      # Custom ServiceError, PolicyError, RoutesError
├── templates/           # Jinja2 templates
├── static/              # CSS / JS
├── ext.py               # db, etc.
├── config.py            # App Configurations
└── app.py               # App factory
```

---

## 🧠 Service Layer Pattern

Each domain entity has a corresponding service class (1:1 with models), responsible for orchestrating application workflows.

All services inherit from BaseService, which provides:

safe_execute() – centralized error handling & transaction safety

create_resource() – request data normalization and filtering

_save() / _delete() – database persistence helpers

### Example

```python
class IncomeService(BaseService):
    def create_income(self, data: dict):
        clean = self.create_resource(
            data,
            required=["source", "amount", "category_id"],
            allowed=["source", "amount", "remarks", "category_id", "user_id"]
        )

        IncomePolicy.validate_create(clean)

        income = Income(**clean)
        return self.safe_execute(lambda: self._save(income))

```

## 🧩 Policy Layer (Business Rules)
The Policy layer enforces all domain-specific rules and validations.
Responsibilities:
   * Validate business constraints
   * Enforce data ownership
   * Prevent invalid state transitions
   * Centralize reusable validation logic
Examples of enforced rules:
   * Users can only access their own data
   * Categories are user-specific and type-restricted
   * Categories in use cannot be deleted
   * Income and expense amounts must be greater than zero
   * Debt payments cannot exceed remaining balance
   * Savings withdrawals cannot exceed current savings balance
Policies are stateless, reusable, and have no persistence logic.

## 🔐 Validation & Error Handling
* Business rule violations raise PolicyError
* Application-level failures raise ServiceError
* Routes catch errors and translate them into HTTP responses or UI messages
* Database errors are never exposed directly to users

Example:

```python
raise ServiceError("Email already exists")
```

---

## 📊 Financial Calculations

All financial values are derived, not stored.

Examples:
* Total income
* Total expenses
* Outstanding debt
* Available balance

Calculations are performed efficiently using SQL aggregation:
```python
func.coalesce(func.sum(Income.amount), 0)

```

## 📊 Dashboard Calculations

Totals are calculated efficiently using SQL aggregation:

```python
func.sum(Income.amount)
```
✔ No cached monetary fields
✔ No Python loops
✔ Consistent and scalable

Savings are intentionally excluded from the available balance calculation.
---



## 🗃️ Database

* **Database**: MySQL
* **ORM**: SQLAlchemy (Flask-SQLAlchemy)
* **Transactions** stored as normalized tables

No cached monetary values are stored to avoid inconsistency.

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/inamonanymous/panot_financial_tracker.git
cd panot_financial_tracker
```

### 2️⃣ Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### 5️⃣ Run the app

```bash
flask run
```

---

## 🧪 Testing (Future)

Planned:

* Unit tests for policy rules
* Service-level tests for use cases
* Route integration tests

---

## 📈 Roadmap

* [#] Complete Expenses & Income modules
* [ ] Complete dashboard summaries
* [ ] Charts & analytics
* [ ] Reports (monthly/yearly)
* [ ] Budgeting module (Phase 2)
---

## 👤 Author

**Stephen Joaquin Aguilar**
Finance Tracker Project 2025-26

---

## 📄 License

This project is for educational and personal use.

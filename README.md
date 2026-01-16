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
Services (Business Logic)
   ↓
Models (SQLAlchemy ORM)
   ↓
Database
```

### Why this design?

* Clean separation of concerns
* Easier testing and maintenance
* Business rules stay out of routes

---

## 📂 Project Structure

```
app/
│
├── models/              # SQLAlchemy models
├── services/            # Business logic (BaseService pattern)
├── routes/              # Flask routes / controllers
├── utils/
│   └── exceptions/      # Custom ServiceError
├── templates/           # Jinja2 templates
├── static/              # CSS / JS
├── extensions.py        # db, login, etc.
└── app.py               # App factory
```

---

## 🧠 Service Layer Pattern

All services inherit from `BaseService`, which provides:

* `safe_execute()` – centralized error handling
* `create_resource()` – input validation & cleaning
* `_save()` / `_delete()` – database persistence

### Example

```python
class IncomeService(BaseService):
    def insert_income(self, data: dict):
        clean = self.create_resource(
            data,
            required=["source", "amount"],
            allowed=["source", "amount", "remarks", "user_id"]
        )
        income = Income(**clean)
        return self.safe_execute(lambda: self._save(income))
```

---

## 🔐 Validation & Error Handling

* All validation errors raise `ServiceError`
* Database constraint errors (e.g., duplicate email) are mapped to user-friendly messages
* Routes catch errors and render messages to HTML

Example:

```python
raise ServiceError("Email already exists")
```

---

## 📊 Dashboard Calculations

Totals are calculated efficiently using SQL aggregation:

```python
func.sum(Income.amount)
```

✔ No Python loops
✔ Scales well with large datasets

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
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
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

* Unit tests for services
* Validation tests
* Integration tests for routes

---

## 📈 Roadmap

* [ ] Complete Expenses & Income modules
* [ ] Dashboard charts
* [ ] Reports (monthly/yearly)
* [ ] Performance optimizations

---

## 👤 Author

**Stephen Joaquin Aguilar**
Finance Tracker Project

---

## 📄 License

This project is for educational and personal use.

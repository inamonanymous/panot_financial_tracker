# Finance Project — Development Roadmap & Task List

**Last Updated:** February 2026

---

## Phase 1: Core Features (In Progress)

### ✅ Completed
- [x] User registration & login
- [x] Dashboard with summaries
- [x] Debt payment creation

### 🔄 In Progress
- [ ] **Income Page** (View all income in table)
  - Create `GetUserIncomeUseCase` in `app/use_cases/`
  - Update `app/routes/r_income.py` → `income_page()` route
  - Fix template to display income list
  - **Status:** Template ready, needs use case + route update

### 📋 Next Priority (Do These in Order)

---

## Phase 1.5: Complete Transaction Management

### Income Management (After Income Page)
```
┌─────────────────────────────────────────┐
│ Priority: HIGH - Blocks other features  │
└─────────────────────────────────────────┘
```

**1.1 Create Income Use Case**
   - File: `app/use_cases/create_income.py`
   - Create `CreateIncomeUseCase`
   - Input: `income_data` dict with category_id, source, amount, etc.
   - Process:
     - Validate using `TransactionPolicy.validate_insert_income()`
     - Check category exists and belongs to user
     - Create and persist Income entity
   - Return: saved income object
   - **Estimated time:** 30 minutes
   - **Similar to:** `create_debt_payment.py`

**1.2 Update Income Route**
   - File: `app/routes/r_income.py`
   - Add `POST /income` route that:
     - Gets form data
     - Calls `CreateIncomeUseCase`
     - Redirects on success or shows error
   - **Similar to:** login route in `r_users.py`

**1.3 Update Income Template**
   - File: `app/templates/auth/pages/income.html`
   - Fix modal form to POST to `/income`
   - Add fields: category_id, source, amount, received_date, payment_method, remarks
   - **Estimated time:** 15 minutes

**1.4 Get Expense Page (View all expenses)**
   - Similar pattern to income page
   - File: `app/use_cases/get_user_expenses.py`
   - **Estimated time:** 20 minutes

**1.5 Create Expense Use Case**
   - File: `app/use_cases/create_expense.py`
   - Similar to create_income
   - **Estimated time:** 30 minutes

**1.6 Update Expense Route & Template**
   - Similar to income
   - **Estimated time:** 20 minutes

---

## Phase 2: Category Management

```
┌─────────────────────────────────────────┐
│ Priority: HIGH - Needed for transactions│
└─────────────────────────────────────────┘
```

**2.1 Create Category Use Case**
   - File: `app/use_cases/create_category.py`
   - Input: user_id, type ("income"/"expense"), name
   - Process:
     - Validate using `CategoryPolicy.validate_insert_category()`
     - Check no duplicate category name for user
     - Create and persist
   - **Estimated time:** 30 minutes

**2.2 Get Categories Use Case**
   - File: `app/use_cases/get_user_categories.py`
   - Return all categories for a user, grouped by type
   - **Estimated time:** 20 minutes

**2.3 Update Category Use Case**
   - File: `app/use_cases/update_category.py`
   - Input: category_id, user_id, new_name
   - **Estimated time:** 25 minutes

**2.4 Delete Category Use Case**
   - File: `app/use_cases/delete_category.py`
   - Check category is not in use (no income/expense records)
   - Delete if safe
   - **Estimated time:** 25 minutes

**2.5 Category Management Page & Routes**
   - Create `app/routes/r_categories.py`
   - Routes: GET (list), POST (create), PUT/POST (update), DELETE
   - Template: `app/templates/auth/pages/categories.html`
   - **Estimated time:** 45 minutes

---

## Phase 3: Debt Management

```
┌─────────────────────────────────────────┐
│ Priority: MEDIUM - Core feature        │
└─────────────────────────────────────────┘
```

**3.1 Create Debt Use Case**
   - File: `app/use_cases/create_debt.py`
   - Input: user_id, lender, principal, interest_rate, start_date, due_date
   - Validate using `FinancialCalculationsPolicy`
   - **Estimated time:** 30 minutes

**3.2 Get Debts Use Case**
   - File: `app/use_cases/get_user_debts.py`
   - Enrich with calculated data:
     - Monthly payment (from `DebtCalculator.monthly_payment()`)
     - Days until due
     - Is overdue?
   - **Estimated time:** 25 minutes

**3.3 Update Debt Use Case**
   - File: `app/use_cases/update_debt.py`
   - Allow editing: lender, principal, interest_rate
   - Validate constraints
   - **Estimated time:** 25 minutes

**3.4 Delete Debt Use Case**
   - File: `app/use_cases/delete_debt.py`
   - Check no debt payments exist
   - **Estimated time:** 20 minutes

**3.5 Debt Management Page & Routes**
   - Create `app/routes/r_debts.py`
   - Template: `app/templates/auth/pages/debts.html`
   - Show table with: lender, principal, monthly payment, due date, days until due
   - **Estimated time:** 60 minutes

---

## Phase 4: Savings Goals

```
┌─────────────────────────────────────────┐
│ Priority: MEDIUM - Feature extension   │
└─────────────────────────────────────────┘
```

**4.1 Create Saving Goal Use Case**
   - File: `app/use_cases/create_saving_goal.py`
   - Input: user_id, name, target_amount, target_date
   - **Estimated time:** 25 minutes

**4.2 Get Saving Goals Use Case**
   - File: `app/use_cases/get_user_saving_goals.py`
   - Enrich with:
     - Current amount (sum of transactions)
     - Progress percentage
     - Days remaining
   - Use `SavingGoalAnalyzer` domain service
   - **Estimated time:** 30 minutes

**4.3 Add Saving Transaction Use Case**
   - File: `app/use_cases/add_saving_transaction.py`
   - Input: saving_goal_id, amount, type ("deposit"/"withdraw")
   - Update goal's current_amount
   - **Estimated time:** 25 minutes

**4.4 Savings Page & Routes**
   - Create `app/routes/r_savings.py`
   - Template: `app/templates/auth/pages/savings.html`
   - Show progress bars, target vs. current
   - **Estimated time:** 60 minutes

---

## Phase 5: Reports & Analytics

```
┌─────────────────────────────────────────┐
│ Priority: MEDIUM-LOW - Enhancement     │
└─────────────────────────────────────────┘
```

**5.1 Monthly Summary Use Case**
   - File: `app/use_cases/get_monthly_summary.py`
   - Input: user_id, year, month
   - Return: total income, total expense, net, by category breakdown
   - **Estimated time:** 40 minutes

**5.2 Yearly Summary Use Case**
   - File: `app/use_cases/get_yearly_summary.py`
   - Input: user_id, year
   - Return: monthly data points for charts
   - **Estimated time:** 35 minutes

**5.3 Category Analysis Use Case**
   - File: `app/use_cases/get_category_analysis.py`
   - Input: user_id, category_type ("income"/"expense")
   - Return: breakdown by category with percentages
   - **Estimated time:** 30 minutes

**5.4 Reports Page**
   - Template: `app/templates/auth/pages/reports.html`
   - Shows tables and summaries
   - **Estimated time:** 60 minutes

**5.5 Charts (with Chart.js)**
   - Template: `app/templates/auth/pages/charts.html`
   - Pie chart: expense by category
   - Line chart: income/expense over time
   - Bar chart: monthly comparison
   - **Estimated time:** 90 minutes

---

## Phase 6: Advanced Features

```
┌─────────────────────────────────────────┐
│ Priority: LOW - Optional enhancements  │
└─────────────────────────────────────────┘
```

**6.1 Budget Planning**
   - Create `SetBudgetUseCase`, `GetBudgetUseCase`
   - Check budget vs. actual spending
   - **Estimated time:** 60 minutes

**6.2 Scheduled Transactions (Recurring)**
   - Support weekly/monthly recurring income/expense
   - **Estimated time:** 90 minutes

**6.3 Export Reports**
   - PDF export (using `reportlab`)
   - CSV export
   - **Estimated time:** 120 minutes

**6.4 Notifications**
   - Email notifications for:
     - Upcoming debt due date
     - Budget exceeded
     - Savings goal reached
   - Background task runner (Celery)
   - **Estimated time:** 180 minutes

---

## Build Order Recommendation

For **smooth progression** and to **avoid blockers**, build in this order:

```
1. ✅ User Auth (DONE)
2. ✅ Dashboard (DONE)
3. → Income Page (You are here - 1 hour)
4. → Create Income + Expense (2 hours)
5. → Category Management (2 hours)
6. → Debt Management (2.5 hours)
7. → Savings Goals (2.5 hours)
8. → Reports & Analytics (3 hours)
9. → Advanced Features (parallel)
```

**Total estimated time for core features:** ~15-16 hours

---

## Quick Reference: Use Case Template

Every new use case follows this structure:

```python
# app/use_cases/my_use_case.py
class MyUseCase:
    """Brief description of what this does."""
    
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        # Initialize policies if validation needed
        self.policy = MyPolicy()
    
    def execute(self, param1, param2):
        """
        Main orchestration method.
        
        Args:
            param1: Description
            param2: Description
        
        Returns:
            Result object or dict
            
        Raises:
            PolicyError: If validation fails
            Exception: If business logic violated
        """
        # Step 1: Validate (if input)
        clean = self.policy.validate_input({"param1": param1, ...})
        
        # Step 2: Check state (if needed)
        entity = self.uow.my_repo.get_by_id(id)
        if entity is None:
            raise Exception("Not found")
        
        # Step 3: Compute (if needed)
        # compute_result = SomeDomainService.calculate(...)
        
        # Step 4: Persist (if modifying)
        with self.uow.transaction():
            saved = self.uow.my_repo.save(entity)
        
        # Step 5: Return (enriched if needed)
        return saved
```

---

## Quick Reference: Route Template

```python
from flask import Blueprint, request, render_template, redirect, url_for
from app.use_cases.my_use_case import MyUseCase
from app.service import UOW
from app.routes.functions import require_user_session, get_current_user

my_routes = Blueprint('my_routes', __name__)

@my_routes.route('/my-page', methods=['GET'])
@require_user_session
def view_page():
    user = get_current_user()
    
    use_case = MyUseCase(UOW)
    data = use_case.execute(user.id)
    
    return render_template('auth/pages/my_page.html', user=user, data=data)

@my_routes.route('/my-page', methods=['POST'])
@require_user_session
def create_item():
    user = get_current_user()
    form_data = request.form.to_dict()
    
    try:
        use_case = MyUseCase(UOW)
        result = use_case.execute(form_data)
        return redirect(url_for('my_routes.view_page'))
    except Exception as e:
        return render_template('auth/pages/my_page.html', error=str(e)), 400
```

---

## How to Self-Check Your Work

After implementing each use case:

- [ ] Use case created in `app/use_cases/`
- [ ] Route updated in `app/routes/`
- [ ] Template updated/created
- [ ] Tested manually in browser
- [ ] Forms validate and show errors
- [ ] Data persists and displays correctly
- [ ] Relationships load (like category names)

---

## Key Files You'll Edit Most

- `app/use_cases/*.py` — New use cases (1 per feature)
- `app/routes/r_*.py` — Routes (1 per module or shared)
- `app/templates/auth/pages/*.html` — Templates (1 per page)
- `app/domain/policies/*.py` — Validation (add methods as needed)
- `app/domain/services/*.py` — Business logic (add calculators as needed)
- `app/repositories/*_impl.py` — Repository methods (only if new query types needed)

---

## Questions to Ask Yourself When Building

1. **What does the user want to do?**
   - View data? Create? Edit? Delete?

2. **What data do I need?**
   - From which repositories?
   - Do I need to enrich/join data from multiple sources?

3. **What validation is needed?**
   - Use existing policy or create new method?

4. **What business rules apply?**
   - Check in use case or add domain service?

5. **Should this be a new use case or route?**
   - Separate use case = reusable, testable
   - Routes = HTTP handling (keep thin)

---

End of Roadmap

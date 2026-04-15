# Finance Project — Development Roadmap & Task List

**Last Updated:** April 15, 2026

---

## Current Snapshot

### ✅ Completed (Implemented and Working)
- [x] User registration, login, logout
- [x] Dashboard totals reporting
- [x] Income create + list + edit
- [x] Expense create + list + edit
- [x] Category create + edit for income and expense contexts
- [x] Shared category card/modal UI reused across income and expense pages
- [x] Debt payment flow (creates expense + debt payment record)
- [x] Debt list + edit page + use case
- [x] `name` support added to income and expense models
- [x] Validation now requires both:
  - Income: `name` and `source`
  - Expense: `name` and `payee`
- [x] **Saving goal payment flow** (creates expense + saving transaction)
- [x] **Dynamic saving goal current amount calculation** from transaction history
- [x] **Saving transaction validation policies**
- [x] **AddSavingGoalPaymentUseCase orchestration**
- [x] **Route for `/add_saving_goal_payment/<goal_id>` (POST)**

### 🔄 In Progress
- [ ] Cleanup/refactor pass for duplicated table/modal JS (optional quality task)
- [ ] Consistent timestamp/date formatting in all table views
- [ ] Saving goal list/create/edit/delete pages and routes (payment infrastructure complete)

---

## Phase 2: Near-Term Priorities

### 1) Saving Goals CRUD & UI Completion
**Priority:** High (Payment infrastructure exists, UI/CRUD missing)

- Create `CreateSavingGoalUseCase` and route
- Create `EditSavingGoalUseCase` and route  
- Create `DeleteSavingGoalUseCase` with safety checks
- Build saving goals list page with progress indicators
- Integrate payment flow button into goal view
- Test transaction tracking across multiple payments

### 2) Delete Flows for Transactions
**Priority:** High

- Add `DeleteIncomeUseCase` and route/action
- Add `DeleteExpenseUseCase` and route/action
- Add delete confirmation modal and in-use safety checks

### 3) Category Lifecycle Completion
**Priority:** High

- Add category delete use case and route
- Prevent deletion when referenced by income/expense
- Show clear user-facing error messaging

### 4) Debt Management Module (CRUD)
**Priority:** Medium

- Add debt create/list/edit/delete routes + use-cases (delete remains pending)
- Reuse existing debt calculators for enriched listing
- Add debt page templates (table + modal forms)

---

## Phase 3: Reporting & Analytics

**Priority:** Medium-Low

- Monthly and yearly summaries
- Category breakdown reporting
- Chart.js views for trends and composition

---

## Phase 4: Optional Enhancements

**Priority:** Low

- Budget planning module
- Recurring transactions
- Export to CSV/PDF
- Notifications and reminders

---

## Recommended Next Session Start

1. Build saving goals list page and CRUD (create/edit/delete) routes
2. Complete transaction delete flows (income + expense)
3. Add category delete with protection checks

This order finalizes savings goals (critical path) while maintaining momentum on core CRUD completeness.

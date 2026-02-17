# Finance Project — Development Roadmap & Task List

**Last Updated:** February 18, 2026

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
- [x] `name` support added to income and expense models
- [x] Validation now requires both:
  - Income: `name` and `source`
  - Expense: `name` and `payee`

### 🔄 In Progress
- [ ] Cleanup/refactor pass for duplicated table/modal JS (optional quality task)
- [ ] Consistent timestamp/date formatting in all table views

---

## Phase 2: Near-Term Priorities

### 1) Delete Flows for Transactions
**Priority:** High

- Add `DeleteIncomeUseCase` and route/action
- Add `DeleteExpenseUseCase` and route/action
- Add delete confirmation modal and in-use safety checks

### 2) Category Lifecycle Completion
**Priority:** High

- Add category delete use case and route
- Prevent deletion when referenced by income/expense
- Show clear user-facing error messaging

### 3) Debt Management Module (CRUD)
**Priority:** Medium

- Add debt create/list/edit/delete routes + use-cases
- Reuse existing debt calculators for enriched listing
- Add debt page templates (table + modal forms)

---

## Phase 3: Savings Goals Module

**Priority:** Medium

- Implement saving goal CRUD use-cases and routes
- Implement saving transaction create flow
- Add savings page with progress and timeline indicators

---

## Phase 4: Reporting & Analytics

**Priority:** Medium-Low

- Monthly and yearly summaries
- Category breakdown reporting
- Chart.js views for trends and composition

---

## Phase 5: Optional Enhancements

**Priority:** Low

- Budget planning module
- Recurring transactions
- Export to CSV/PDF
- Notifications and reminders

---

## Recommended Next Session Start (Tomorrow)

1. Implement transaction delete flow (income + expense)
2. Add category delete with protection checks
3. Start debt CRUD pages/routes

This order keeps momentum on core CRUD completeness before moving into analytics.

# Finance Project — Development Roadmap & Task List

**Last Updated:** April 16, 2026

---

## Current Snapshot

### ✅ Recently Completed (Implemented and Working)
- [x] Saving goal progress/current amount calculation moved to persistence layer (repository/UOW)
- [x] Debt current amount/progress calculation moved to persistence layer (repository/UOW)
- [x] Fixed saving goal payment expense ID bug (expense_id now set after expense save)

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

# Feature Tracker

High-level features mapped to use-cases and components.

| Feature ID | Feature | Related use-cases | Status | Priority | Notes |
|---:|---|---|---|---:|---|
| F-001 | Authentication & User management | UC-001, UC-002 | Implemented | High | Add unit + integration tests for registration/login flows |
| F-002 | Dashboard & Reporting | UC-003 | Implemented | High | Consider performance tests / caching |
| F-003 | Income management (CRUD) | UC-007, UC-008 | Implemented | High | Add input validation tests |
| F-004 | Expense management (CRUD) | UC-005, UC-006 | Implemented | High | Add pagination and edge-case tests |
| F-005 | Debt handling & payments | UC-004 | Implemented | Medium | Ensure category creation edge-cases handled |
| F-006 | Categories & lookup | UC-009 | Implemented | Medium | Ensure category ownership is enforced |
| F-007 | Saving goals & transactions | (partial) | In Progress | Medium | Add missing use-cases if any |

Prioritization and TODOs
- Move items from Backlog → In Progress when work starts; mark Done when PR merged.
- Use `TRACKING/WORKBOARD.md` for sprint-specific cards.

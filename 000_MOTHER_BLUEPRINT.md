# 000 — Mother Blueprint (Read This First)

Status: Mandatory first document before planning, coding, refactoring, or design changes.
Owner: Product + Engineering
Last Updated: 2026-02-18

## 1) Why This Exists
This is the single source of truth for how projects start and execute.
If a task is not aligned to this blueprint, it does not start.

## 2) Rule #1 (Start Order)
You must read and complete this order before writing code:
1. Product Vision and Business Goal
2. Scope (MVP + Non-goals)
3. Core User Flows and Acceptance Criteria
4. Data Model + API Contract
5. Architecture + Security Baseline
6. Sprint Plan + Definition of Done

Only after these 6 are complete can implementation begin.

## 3) Timeline (What To Do First)

### Day 0–1: Discovery + Scope Lock
- Define problem statement and target users
- Write success metrics (KPIs)
- Define MVP boundaries and explicit non-goals
- Create initial backlog (epics only)

Deliverables:
- `docs/product/01_Product_Vision.md`
- `docs/product/02_Scope_and_Requirements.md`

### Day 2–3: Design Baseline
- Define user flows and acceptance criteria
- Create domain/data model
- Define API contracts and error format
- Produce architecture/container diagrams

Deliverables:
- `docs/product/03_User_Flows_and_Use_Cases.md`
- `docs/architecture/04_Architecture_Decisions.md`
- `docs/architecture/05_Data_Model.md`
- `docs/architecture/06_API_Contracts.md`

### Day 4: Risk + Quality Planning
- Define security baseline (session/auth/csrf/secrets/logging)
- Define test strategy and quality gates
- Define deployment and rollback expectations

Deliverables:
- `docs/delivery/07_Security_and_Risk.md`
- `docs/delivery/08_Test_Strategy.md`
- `docs/delivery/10_Operations_Runbook.md`

### Day 5: Sprint 0 Setup + Execution Plan
- Finalize roadmap and milestone order
- Break epics into user stories
- Estimate first sprint
- Confirm DoR/DoD and release criteria

Deliverables:
- `docs/delivery/09_Delivery_Roadmap.md`
- Sprint board with story priorities

### Week 2+: Build in Agile Increments
- Implement only stories that pass Definition of Ready
- One vertical slice at a time (route + use case + policy + repo + UI + test)
- Demo each sprint and update docs continuously

## 4) Required Diagram Order
Create these diagrams in this exact sequence:
1. Context Diagram (C4 L1)
2. Container Diagram (C4 L2)
3. ERD / Domain Model Diagram
4. Key Sequence Diagrams (login, create transaction, update transaction)
5. Deployment Diagram (before production release)

## 5) SDLC (Agile-Friendly)

### Phase A — Initiation
- Vision, stakeholders, scope assumptions
- Output: Vision + Scope docs

### Phase B — Planning
- Backlog setup, architecture baseline, release milestones
- Output: ADR + Roadmap + epic priorities

### Phase C — Design
- Contracts, diagrams, acceptance criteria
- Output: API/Data/Flow docs with review sign-off

### Phase D — Implementation
- Sprint-based feature development
- Output: production-ready increments

### Phase E — Verification
- Unit/integration/manual/UAT checks
- Output: quality sign-off per increment

### Phase F — Deployment
- Release notes, migration steps, rollback plan
- Output: controlled release

### Phase G — Maintenance
- Monitoring, incidents, postmortems, backlog refinements
- Output: stable operations + iterative improvements

## 6) Governance Rules (No Vibe Coding)
- No code starts without scope + acceptance criteria.
- No architecture change mid-sprint without updating ADR.
- New requests become backlog items, not instant code changes.
- Every feature update must include:
  - docs update
  - test/update checklist
  - rollback note if DB/API changes

## 7) Definition of Ready (DoR)
A story is ready when:
- User value is clear
- Acceptance criteria are testable
- Data/API impacts are known
- Dependencies are identified
- Estimate is agreed

## 8) Definition of Done (DoD)
A story is done when:
- Implementation complete and reviewed
- Validation/policy rules covered
- Regression checks passed
- Docs and roadmap updated
- Demo accepted

## 9) How To Use This in Every New Project
1. Copy this file into the new project root as `000_MOTHER_BLUEPRINT.md`
2. Create the `/docs` tree and required 10 documents
3. Run Week 1 timeline exactly
4. Begin coding only after Design Baseline sign-off

## 10) Current Project Mapping
For this Finance Project, supporting blueprints are:
- `PROJECT_BLUEPRINT_CURRENT.md`

But this file (`000_MOTHER_BLUEPRINT.md`) is the first required read and workflow authority.

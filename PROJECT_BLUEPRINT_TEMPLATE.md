# Project Blueprint Template (SDLC + Agile)

Use this as a starter before writing code.

## A) What Real-World Teams Do First (Practical Sequence)
1. Problem framing (why this product, why now)
2. Business goals and success metrics (north-star + constraints)
3. Scope boundary (MVP vs later phases)
4. Architecture and data design
5. Delivery plan (epics/sprints/releases)
6. Risk/security/compliance planning
7. Build with short feedback loops (Agile increments)

---

## B) Document Pack You Should Create First
Create these documents in this order:

1. `01_Product_Vision.md`
   - Problem statement
   - Target users/personas
   - Value proposition
   - Success metrics (KPIs)

2. `02_Scope_and_Requirements.md`
   - In scope / out of scope
   - Functional requirements (FR-1, FR-2...)
   - Non-functional requirements (performance, security, reliability)

3. `03_User_Flows_and_Use_Cases.md`
   - Top user journeys
   - Alternate/error flows
   - Acceptance criteria per flow

4. `04_Architecture_Decisions.md`
   - Tech stack choices
   - Layering/module boundaries
   - ADRs (Architecture Decision Records)

5. `05_Data_Model.md`
   - Entities and relationships
   - Ownership and lifecycle rules
   - Migration/versioning strategy

6. `06_API_Contracts.md`
   - Endpoints, request/response DTOs
   - Error contract
   - Auth/authorization rules

7. `07_Security_and_Risk.md`
   - Threat model (lightweight)
   - Secrets/session/CSRF strategy
   - Logging and audit requirements

8. `08_Test_Strategy.md`
   - Test pyramid (unit/integration/e2e)
   - Critical path tests
   - Regression policy and quality gates

9. `09_Delivery_Roadmap.md`
   - Epics, milestones, release phases
   - Dependencies and risks

10. `10_Operations_Runbook.md`
   - Environments and configs
   - Deployment rollback plan
   - Monitoring/alerting + incident steps

---

## C) Diagram Set You Should Produce First
Create diagrams in this order (start simple):

1. Context Diagram (C4 Level 1)
   - System, users, external dependencies

2. Container Diagram (C4 Level 2)
   - Web app, DB, cache, queue, external services

3. Domain Model / ERD
   - Core entities and relationships

4. Key Sequence Diagrams
   - Login/auth flow
   - Main transaction/create flow
   - Critical write path with validation + persistence

5. Deployment Diagram (optional early, mandatory before release)
   - Runtime nodes, networking, environment topology

6. State Diagram (if needed)
   - Lifecycle-heavy objects (orders, approvals, subscriptions)

---

## D) SDLC Phases with Agile Mapping

### 1) Initiation / Discovery
Outputs:
- Vision, scope draft, stakeholder map, risk assumptions
Agile mapping:
- Create initial product backlog + MVP hypothesis

### 2) Planning
Outputs:
- Prioritized epics, release plan, architecture baseline, estimation
Agile mapping:
- Story mapping + sprint 0 (setup/guardrails)

### 3) Design
Outputs:
- UX wireframes, API/data contracts, diagrams, ADRs
Agile mapping:
- Definition of Ready (DoR) for first sprint stories

### 4) Implementation
Outputs:
- Incremental feature slices with tests and docs
Agile mapping:
- Sprint cycles (plan → dev → test → review → retro)

### 5) Verification
Outputs:
- Test reports, UAT sign-off, defect triage
Agile mapping:
- Continuous QA in each sprint + release hardening sprint if needed

### 6) Deployment
Outputs:
- Release notes, migration scripts, rollback plan
Agile mapping:
- Small batch releases per sprint/release train

### 7) Maintenance
Outputs:
- Monitoring dashboards, incidents, postmortems, backlog updates
Agile mapping:
- Operate + improve loop (SRE + product backlog refinement)

---

## E) Agile Execution Model (Simple and Effective)

### Team Cadence
- Sprint length: 1–2 weeks
- Ceremonies:
  - Backlog refinement (1–2x/week)
  - Sprint planning
  - Daily stand-up
  - Sprint review/demo
  - Retrospective

### Backlog Hierarchy
- Theme → Epic → Feature → User Story → Tasks

### Story Template
- As a [user], I want [capability], so that [benefit].
- Acceptance criteria: Given/When/Then
- Non-functional checks: security/performance/logging

### Definition of Ready (DoR)
Story is ready when:
- Scope clear
- Dependencies identified
- API/data impacts identified
- Acceptance criteria testable

### Definition of Done (DoD)
Story is done when:
- Code + tests pass
- Security checks applied
- Docs updated
- Demo accepted by PO/stakeholder

---

## F) Governance and Change Control (Avoid “Vibe Coding”)
- Freeze MVP scope for the sprint
- No architecture changes mid-sprint without ADR update
- Every new requirement gets backlog item + priority decision
- Use feature flags for risky unfinished work
- Keep a `DECISIONS.md` to track why decisions were made

---

## G) Suggested Folder for Planning Artifacts

```text
/docs
  /product
    01_Product_Vision.md
    02_Scope_and_Requirements.md
    03_User_Flows_and_Use_Cases.md
  /architecture
    04_Architecture_Decisions.md
    05_Data_Model.md
    06_API_Contracts.md
    diagrams/
  /delivery
    07_Security_and_Risk.md
    08_Test_Strategy.md
    09_Delivery_Roadmap.md
    10_Operations_Runbook.md
```

---

## H) First 2-Week Sprint Plan (Template)
Week 1:
- Finalize scope + architecture baseline
- Build skeleton modules + CI + lint + test harness
- Implement one vertical slice end-to-end (small but complete)

Week 2:
- Implement 2–3 high-priority stories
- Add regression tests for the vertical slice
- Demo + retro + replan

---

## I) Quick Checklist Before Coding
- [ ] Vision and MVP scope approved
- [ ] Data model and API contracts reviewed
- [ ] Security baseline defined
- [ ] Test strategy documented
- [ ] Sprint backlog prioritized and estimated
- [ ] Definition of Done agreed by team

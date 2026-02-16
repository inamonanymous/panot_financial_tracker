Title: [UC-002] CreateUserUseCase — Register new user

Summary
- Validate registration payload, create user within transaction, handle duplicate email.

Acceptance criteria
- [ ] Valid data creates user record.
- [ ] Duplicate email returns friendly error.
- [ ] Password confirmation enforced.

References
- `app/use_cases/create_user.py`
- `app/routes/r_users.py` (/registration)
- `app/domain/policies/p_UserPolicy.py`
- `app/model/m_Users.py`

Components / Prereqs
- DB constraints for `email` unique
- `UOW.users` repository

Labels: use-case, backend, auth
Assignee:

Title: [UC-001] CheckLoginUseCase — Authenticate user login

Summary
- Validate login by email & password; set session on success.

Acceptance criteria
- [ ] Valid credentials authenticate and set `session['user_email']`.
- [ ] Invalid credentials return user-facing error.
- [ ] Uses `p_UserPolicy` for validation.

References
- `app/use_cases/check_login.py`
- `app/routes/r_users.py` (/login)
- `app/domain/policies/p_UserPolicy.py`
- `app/model/m_Users.py`

Components / Prereqs
- `UOW.users` repository
- `Users` DB model exists

Labels: use-case, backend, auth
Assignee:

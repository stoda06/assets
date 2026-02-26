# Code Review: IT Asset Management App (Django) — 3/10

## What it is
A Django app for "Red Education" to track laptop and mobile device assets — add records, validate inputs, auto-detect hardware via PowerShell, and display data via an AdminLTE dashboard.

## What works
- **Basic CRUD is functional** — The laptop and mobile data entry views do achieve the goal of saving records to the database.
- **Some input validation exists** — RAM range checks, HDD size validation with unit awareness (GB/TB) show the developer was thinking about data quality.
- **Duplicate detection** — The `Q` object OR-based check to prevent duplicate asset IDs or usernames is a reasonable approach.
- **AdminLTE integration** — The templates produce a usable UI with a sidebar, forms, and data tables.

## Major issues

### Security (critical)
- `@csrf_exempt` on `Laptops_data` — disables Django's built-in CSRF protection on a data-writing POST endpoint. This is a serious vulnerability.
- `views1.py:228` — `subprocess.check_output(['pwsh', '-ExecutionPolicy', 'Bypass', '-Command', powershell_script])` — executes PowerShell with execution policy bypass. The variable `powershell_script` is also undefined (the parameter is named `script`) so this would crash, but if fixed, the inline script approach is fragile and risky.
- No authentication decorators on any view — `asset()` checks `user.is_authenticated` in the template but not the view, meaning unauthenticated users still hit the database queries.
- `from .models import *` — wildcard imports throughout make it unclear what's in scope and can mask bugs.

### Bugs
- `views1.py:169,171-172` — MAC HDD validation compares `MAC_HDD` (the string value) instead of `MAC_HDDType` against `'GB'`/`'TB'`. This means the HDD validation for Mac laptops is broken and will never trigger correctly.
- `views1.py:284` — `run_powershell_command(request, string)` references an undefined variable `string` (should be `script`). This view would crash on every request.
- `views1.py:226-229` — The function parameter is `script` but the body references `powershell_script`. NameError guaranteed.
- `serializers.py` — References `YourModel` which doesn't exist. This is clearly a placeholder that was never completed.
- `urls.py:14` — References `views.start_vm` which doesn't exist in `views.py`. The app would fail to start.
- `Mobile_data` returns success even on GET requests (no else branch guarding the return).

### Code quality
- Massive amounts of commented-out code — `views.py` has a full duplicate of `Laptops_data` commented out (lines 115-173). `views1.py` has the same. `models.py` has a commented-out model. `admin.py` has commented-out registrations. `urls.py` has commented-out routes. This is what version control is for.
- **4 backup/versioned files** in the repo: `views.py.bak`, `views1.py`, `views_14SEP2023.py`, `views_25SEP2023.py`. These should not be in the repository — this is what git history provides.
- `print()` statements everywhere for debugging. Use `logging` instead.
- `today = date.today()` at module level — this gets evaluated once at import time, so it's stale after the first day the server runs.
- Inconsistent naming conventions throughout: mixing PascalCase, camelCase, snake_case, and Hungarian-notation-style prefixes.
- `Laptops_info` model exists but is never used anywhere.
- Every single `CharField` has `max_length=200` regardless of what it stores. RAM should be an `IntegerField`, not a `CharField`.
- The `Lappurchasedate` default is `default=""` which is an invalid date.
- No `__str__` methods on any model.
- Template HTML doesn't use Django template inheritance properly — `base.html` exists but other templates duplicate the entire layout instead of extending it.
- Hardcoded values like `'2023-03-27'` for purchase date in `views1.py:391`.
- The `apps.py` class is named `PollsConfig` — clearly copied from the Django tutorial and never renamed.

### Architecture
- No Django Forms or ModelForms — all validation is manual, repetitive, and error-prone.
- No use of Django REST Framework despite importing it in `serializers.py` and `urls.py`.
- No tests whatsoever (`tests.py` is the default empty file).
- No migrations management — there's both `migrations/` and `migrations_old/` with no explanation.

## Score Breakdown

| Category | Score |
|---|---|
| Functionality | 3/10 |
| Security | 1/10 |
| Code quality | 2/10 |
| Architecture | 2/10 |
| Testing | 0/10 |
| **Overall** | **3/10** |

## Summary
The code reads like a first attempt by someone learning Django, with significant copy-paste development and no code review process. It would not be safe to deploy — the CSRF exemption, lack of auth guards, and multiple NameErrors that would crash in production are the most urgent concerns. The developer shows some understanding of Django's ORM and Q objects, which is positive, but the fundamentals (security, testing, naming, version control hygiene) need substantial work.

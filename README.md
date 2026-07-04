# LangNation Dictionary Test Automation

Standalone Python + pytest automation for LangNation Dictionary.

This folder is intentionally outside the application source so the app directory is not changed.

## Included

- Python `pytest` test runner
- `pytest-playwright` browser automation
- Page Object Model under `tests_py/pages/`
- API smoke tests
- UI smoke tests with mocked dictionary lookup responses
- GitHub Actions example workflow under `.github/workflows/python-pytest.yml`

## Target app

By default, tests use this local app path:

```text
C:\Users\sheik\My_Porject\LangNation Dictionary\Web\langnation-dictionary-v19
```

You can override it:

```powershell
$env:LANGNATION_PROJECT_ROOT="C:\path\to\langnation-dictionary-v19"
```

Or run against an already running app:

```powershell
pytest --base-url http://localhost:3000
pytest --base-url https://your-staging-url.example
```

## Local setup

```powershell
cd "C:\Users\sheik\Documents\Codex\2026-07-04\te\testing"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-test.txt
python -m playwright install chromium
pytest
```

## Useful commands

```powershell
pytest -m smoke
pytest -m api
pytest -m ui --headed
pytest tests_py/test_dictionary_ui.py --browser chromium
```

Visual demo command:

```powershell
pytest -m ui --headed --slowmo 700
```

Page smoke tests:

```powershell
pytest -m pages
```

Auth/login tests:

```powershell
pytest -m auth
```

## Test coverage structure

- `tests_py/test_api_smoke.py` checks core API health/config/validation.
- `tests_py/test_dictionary_ui.py` checks dictionary search, direction toggle, and auth modal opening.
- `tests_py/test_pages_smoke.py` checks that every main public/admin HTML route renders.
- `tests_py/test_page_functions.py` checks page-level functions like reset-password validation and Amtsdeutsch consent/decode gating.
- `tests_py/test_auth_ui.py` checks sign-in behavior using mocked backend responses and reusable login test data.

## Login test data

Save login test data here:

```text
tests_py/test_data/
```

Commit only this template:

```text
tests_py/test_data/login_users.example.json
```

For real local credentials, create this file and keep it private:

```text
tests_py/test_data/login_users.local.json
```

Then run:

```powershell
$env:LANGNATION_LOGIN_DATA="C:\Users\sheik\My_Porject\LangNation Dictionary\Web\Testing\tests_py\test_data\login_users.local.json"
pytest -m auth
```

`.gitignore` already excludes `*.local.json`, so real passwords stay out of GitHub.

## Notes for GitHub

If you want this to run in GitHub Actions, place this `testing` folder in your repository, or keep the workflow file from `.github/workflows/python-pytest.yml` in the repository root and adjust its `working-directory` values if needed.

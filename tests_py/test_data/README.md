# Test Data

Use this folder for test data that is safe to share.

```text
tests_py/test_data/login_users.local.json
```

Then run tests with:

```powershell
$env:LANGNATION_LOGIN_DATA="Testing\tests_py\test_data\login_users.local.json"
pytest -m auth
```

Do not commit real passwords, tokens, or production user data.

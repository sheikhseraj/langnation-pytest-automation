# Test Data

Use this folder for test data that is safe to share.

Keep `login_users.example.json` in GitHub as a template only. For real local credentials, create a private file:

```text
tests_py/test_data/login_users.local.json
```

Then run tests with:

```powershell
$env:LANGNATION_LOGIN_DATA="C:\Users\sheik\My_Porject\LangNation Dictionary\Web\Testing\tests_py\test_data\login_users.local.json"
pytest -m auth
```

Do not commit real passwords, tokens, or production user data.

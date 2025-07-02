Run acceptance tests:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate.bat
pytest -v tests/test_acceptance.py
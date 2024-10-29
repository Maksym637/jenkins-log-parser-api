### jenkins-log-parser-api
- - -
Prepared by __Maksym Oliinyk__
- - -
### Description
...
- - -
### Technologies
. . .
- - -
### Project structure
. . .
- - -
### Project execution
1. Install app
2. Launch app
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
3. Launch tests
```bash
pytest tests
```
4. See tests coverage
withou threshold
```bash
pytest --cov=app
```
with threshold
```bash
pytest --cov=app --cov-fail-under=90
```
- - -
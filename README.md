## jenkins-log-parser-api
- - -
Prepared by __Maksym Oliinyk__
- - -
### Description
This application handles unparsed Jenkins logs from external API
- - -
### Technologies
_Python 3.12.1_ is used as the programming language and _MongoDB v8.0.3_ is used as the database
- - -
### Project structure
The project has the following structure:
- _app_
    - _crud_ - contains functions for interacting with the MongoDB collections, including creating, reading, updating, and deleting records for `users`, `jenkins-logs`, and `jenkins-histories`
    - _models_ - defines the data models used by the application, such as [`User`, ...], [`JenkinsLog`, ...], and [`JenkinsHistory`, ...], which correspond to the collections in MongoDB
    - _routers_ - contains the FastAPI router definitions that handle the API endpoints for interacting with `users`, `jenkins-logs`, and `jenkins-histories`
    - _schemas_ - defines Pydantic schemas for data validation and serialization used in API requests and responses 
    - _utils_ - includes utility functions that assist with tasks like data processing, authorization, or timing
- _tests_ - contains test cases for verifying the functionality of different components within the application, using pytest for automated testing
- - -
### Project execution
1. Create and activate `venv`
2. Install all dependencies
```bash
pip install -r requirements.txt
```
3. Create `.env` file and put your MongoDB URI
4. Start application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
5. Execute tests
```bash
pytest tests
```
6. Execute tests with coverage
```bash
pytest --cov=app
```
7. Execute tests with coverage _threshold_
```bash
pytest --cov=app --cov-fail-under=90
```
- - -
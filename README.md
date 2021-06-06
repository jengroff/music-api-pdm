# music-api

API for the everyton music service.
Built in Python.
Uses FastAPI, Tortoise ORM, Pydantic, and Postgres on the backend.
Packaged with Docker.

## Run the app

```
cd project && uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

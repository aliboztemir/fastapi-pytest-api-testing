# Task Management API

A professional FastAPI task management service demonstrating clean architecture, comprehensive test coverage across multiple test layers, and containerised deployment with PostgreSQL.

## Tech Stack

- **FastAPI** — async-ready Python web framework
- **SQLAlchemy 2.x** — ORM with `Mapped` column syntax
- **Pydantic v2** — request/response validation
- **SQLite** (dev/test) / **PostgreSQL** (production)
- **pytest** — unit, component, integration and end-to-end test suites
- **Docker + Docker Compose** — containerised deployment

## Project Structure

```
+-- app/
¦   +-- main.py          # FastAPI application entry point
¦   +-- database.py      # SQLAlchemy engine and session
¦   +-- models.py        # ORM models
¦   +-- schemas.py       # Pydantic request/response schemas
¦   +-- routers/
¦       +-- tasks.py     # Task CRUD endpoints
+-- tests/
¦   +-- conftest.py      # Shared fixtures (TestClient, db_session)
¦   +-- unit/            # Schema validation tests
¦   +-- component/       # Endpoint tests with in-memory SQLite
¦   +-- integration/     # Direct database operation tests
¦   +-- e2e/             # Full workflow tests
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the interactive API documentation.

## Running Tests

```bash
# All tests
pytest -v

# By layer
pytest -v -m unit
pytest -v -m component
pytest -v -m integration
pytest -v -m e2e

# With coverage
pytest --cov=app --cov-report=html
```

## Running with Docker

```bash
docker-compose up --build
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/tasks/` | List all tasks |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{id}` | Get a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

# Task Management API

This project focuses on demonstrating API testing practices using pytest across multiple test layers rather than providing a production-ready task management application.

## Overview

A portfolio project demonstrating multi-layer API testing of a FastAPI service using pytest, SQLAlchemy, and Pydantic. The emphasis is on test architecture, test readability, and multi-layer API testing.

## Tech Stack

- **FastAPI** — async-ready Python web framework
- **SQLAlchemy 2.x** — ORM with `Mapped` column syntax
- **Pydantic v2** — request/response validation
- **SQLite** (dev/test) / **PostgreSQL** (production)
- **pytest** — unit, component, integration and end-to-end test suites
- **Docker + Docker Compose** — containerised deployment

## Project Structure

```
app/
├── main.py          # FastAPI application entry point
├── database.py      # SQLAlchemy engine and session
├── models.py        # ORM models
├── schemas.py       # Pydantic request/response schemas
└── routers/
    └── tasks.py     # Task CRUD endpoints
tests/
├── conftest.py      # Shared fixtures (TestClient, db_session)
├── unit/            # Schema validation tests
│   └── test_task_schema_validation.py
├── component/       # Endpoint tests with in-memory SQLite
│   └── test_task_repository_component.py
├── integration/     # Direct database operation tests
│   └── test_task_api_integration.py
└── e2e/             # Full workflow tests
    └── test_task_crud_workflow_e2e.py
Dockerfile
docker-compose.yml
requirements.txt
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

## Test Markers

Tests are tagged with markers for selective execution:

| Marker | File | Meaning |
|---|---|---|
| `unit` | `test_task_schema_validation.py` | Isolated schema/validation tests (no I/O) |
| `component` | `test_task_repository_component.py` | Endpoint tests with in-memory SQLite |
| `integration` | `test_task_api_integration.py` | Direct database operation tests |
| `e2e` | `test_task_crud_workflow_e2e.py` | Full workflow tests |

## Test Coverage Matrix

| Feature | Unit | Component | Integration | E2E |
|---|---|---|---|---|
| Create Task | ✓ | ✓ | ✓ | ✓ |
| Get Task | — | ✓ | ✓ | ✓ |
| Update Task | — | ✓ | ✓ | ✓ |
| Delete Task | — | ✓ | ✓ | ✓ |
| Validation | ✓ | ✓ | — | — |

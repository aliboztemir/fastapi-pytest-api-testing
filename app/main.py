from fastapi import FastAPI
from app.database import Base, engine
from app.routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A FastAPI task management service with SQLAlchemy and PostgreSQL.",
    version="1.0.0",
)

app.include_router(tasks.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Task Management API is running"}
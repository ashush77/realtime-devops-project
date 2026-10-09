import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "dbname": os.getenv("DB_NAME", "devopsdb"),
    "user": os.getenv("DB_USER", "devopsuser"),
    "password": os.getenv("DB_PASSWORD", "devops-dev-only"),
    "connect_timeout": 5,
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
    yield


app = FastAPI(
    title="Real-Time DevOps API",
    description="FastAPI, PostgreSQL, and Docker Compose",
    version="2.0.0",
    lifespan=lifespan,
)


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Real-Time DevOps Project!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        )


@app.get("/items")
def list_items():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM items ORDER BY id"
            )
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "created_at": row[2].isoformat(),
        }
        for row in rows
    ]


@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO items (name) VALUES (%s) "
                "RETURNING id, name, created_at",
                (item.name,),
            )
            row = cursor.fetchone()

    return {
        "id": row[0],
        "name": row[1],
        "created_at": row[2].isoformat(),
    }

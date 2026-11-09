from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.redis_client import redis_client, close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()
    await engine.dispose()

app = FastAPI(
    title = "Scientific Reviews API",
    description = (
        "Система сбора и анализа пользовательских отзывов о научных публикациях"
    ),
    version = "1.0.0",
    lifespan = lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Scientific Reviews API",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }

@app.get("/health/database")
async def database_health():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }

@app.get("/health/redis")
async def redis_health():
    await redis_client.ping()

    return {
        "redis": "connected"
    }

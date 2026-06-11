from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.redis import redis_client
from app.middleware.error_handler import register_error_handlers
from app.middleware.logging import request_logging_middleware
from app.middleware.rate_limit import limiter
from app.models import *  # noqa: F403
from app.routers import applications, auth, contacts, resumes, stats, tags


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Validate settings and create local SQLite tables during development."""
    settings.validate_for_startup()
    if settings.database_url.startswith("sqlite"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_logging_middleware)
register_error_handlers(app)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(applications.router, prefix=settings.api_prefix)
app.include_router(tags.router, prefix=settings.api_prefix)
app.include_router(contacts.router, prefix=settings.api_prefix)
app.include_router(resumes.router, prefix=settings.api_prefix)
app.include_router(stats.router, prefix=settings.api_prefix)


@app.get("/health")
async def health() -> dict[str, bool | str]:
    """Return basic service health."""
    return {"ok": True, "service": settings.app_name}


@app.get("/health/db")
async def health_db() -> dict[str, bool]:
    """Return database connectivity health."""
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: True)
    return {"ok": True}


@app.get("/health/redis")
async def health_redis() -> dict[str, bool]:
    """Return Redis connectivity health."""
    await redis_client.ping()
    return {"ok": True}

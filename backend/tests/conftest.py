from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_job_tracker.db"


@pytest_asyncio.fixture()
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a clean test database and session."""
    engine = create_async_engine(TEST_DATABASE_URL)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with session_factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture()
def client(test_session: AsyncSession) -> Generator[TestClient, None, None]:
    """Return a TestClient using the test session."""

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client: TestClient) -> dict[str, str]:
    """Register and login a test user."""
    payload = {"email": "test@example.com", "name": "Test User", "password": "password123"}
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

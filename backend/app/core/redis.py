from datetime import timedelta
from typing import Any

from app.core.config import settings


class InMemoryRedis:
    """Small async Redis-compatible fallback for local development and tests."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    async def setex(self, key: str, seconds: int | timedelta, value: Any) -> None:
        """Set a value with an ignored TTL in the in-memory fallback."""
        self._store[key] = value

    async def get(self, key: str) -> Any | None:
        """Get a value from the in-memory fallback."""
        return self._store.get(key)

    async def delete(self, key: str) -> None:
        """Delete a key."""
        self._store.pop(key, None)

    async def ping(self) -> bool:
        """Return connectivity status."""
        return True


redis_client: Any = InMemoryRedis()

if settings.redis_url:
    try:
        from redis.asyncio import from_url

        redis_client = from_url(settings.redis_url, decode_responses=True)
    except Exception:
        redis_client = InMemoryRedis()


async def blacklist_jti(jti: str, seconds: int) -> None:
    """Blacklist a JWT ID."""
    await redis_client.setex(f"blacklist:{jti}", seconds, "1")


async def is_jti_blacklisted(jti: str) -> bool:
    """Check whether a JWT ID has been blacklisted."""
    return bool(await redis_client.get(f"blacklist:{jti}"))


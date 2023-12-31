import httpx
import asyncio
from asgi_lifespan import LifespanManager

import pytest
import pytest_asyncio


from main import app


@pytest_asyncio.fixture
async def test_client() -> httpx.AsyncClient:
    # app.dependency_overrides
    async with httpx.AsyncClient(
        app=app, base_url="http://localhost:8000"
    ) as test_client:
        yield test_client

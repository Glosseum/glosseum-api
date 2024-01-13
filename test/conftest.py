import httpx
import pytest
import asyncio
from datetime import datetime, timedelta
from jose import jwt

import pytest_asyncio
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from main import app
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from data.db import database
from data.db.models import User

from config import CREDENTIAL_SECRET_KEY, CREDENTIAL_ALGORITHM

TEST_USERNAME = "test"
TEST_USERMAIL = "test@test.com"
TEST_PASSWORD = "test"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client() -> httpx.AsyncClient:  # Test Client
    # app.dependency_overrides
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://localhost:8000"
        ) as test_client:
            yield test_client


@pytest_asyncio.fixture(scope="session")
def db() -> dict:
    try:
        engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
        session = async_sessionmaker(bind=engine, expire_on_commit=False)
        alembic_config = AlembicConfig("alembic.ini")

        alembic_config.set_main_option("sqlalchemy_url", "sqlite+aiosqlite:///:memory:")

        alembic_upgrade(alembic_config, "head")

        _db = {"engine": engine, "session": session}

        yield _db

    finally:
        engine.dispose()


@pytest_asyncio.fixture
async def test_headers():
    user = User(username=TEST_USERNAME, email=TEST_USERMAIL, password=TEST_PASSWORD)

    payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(
        payload, CREDENTIAL_SECRET_KEY, algorithm=CREDENTIAL_ALGORITHM
    )

    yield {"Authorization": f"Bearer {access_token}"}

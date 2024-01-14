import os

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


from data.db import database
from data.db.models import User, Base

from test.utils.common import random_lower_string

from config import CREDENTIAL_SECRET_KEY, CREDENTIAL_ALGORITHM

TEST_USERNAME = f"{random_lower_string(10)}"
TEST_USERMAIL = f"{random_lower_string(10)}@test.com"
TEST_PASSWORD = "test"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


@pytest_asyncio.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
    finally:
        loop.close()
        print("Ends Here")
        os.remove("test.db")


@pytest_asyncio.fixture
async def test_client() -> httpx.AsyncClient:  # Test Client
    # app.dependency_overrides
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://localhost:8000"
        ) as test_client:
            yield test_client


@pytest_asyncio.fixture(scope="session")
async def db(event_loop) -> dict:
    engine = create_async_engine(url="sqlite+aiosqlite:///test.db")
    session = async_sessionmaker(bind=engine, expire_on_commit=False)

    _db = {"engine": engine, "session": session}

    yield _db

    await engine.dispose()


@pytest_asyncio.fixture
async def test_headers(db):
    user = User(username=TEST_USERNAME, email=TEST_USERMAIL, password=TEST_PASSWORD)
    async with db["session"]() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(
        payload, CREDENTIAL_SECRET_KEY, algorithm=CREDENTIAL_ALGORITHM
    )

    yield {"Authorization": f"Bearer {access_token}"}

import os
import asyncio
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from pymongo import MongoClient
from app.main import app
from app.utils.constants import Dependencies as DP
from mongoengine import connect, disconnect


load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    database: MongoClient = connect(db=DP.DB_NAME, host=os.getenv("MONGO_URI"))

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    database.drop_database(name_or_database=DP.DB_NAME)
    disconnect()

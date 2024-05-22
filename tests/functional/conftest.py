import asyncio
from http import HTTPMethod
from typing import Mapping

import aiohttp
import pytest_asyncio
from redis.asyncio import Redis

from tests.functional.config import test_settings


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def make_request(client_session: aiohttp.ClientSession):
    async def inner(method: HTTPMethod, uri: str, body: Mapping = None, params: Mapping = None):
        url = test_settings.service_url + uri

        async with client_session.request(method, url, json=body, params=params) as response:
            body = await response.json()
            status = response.status

            return body, status

    return inner


@pytest_asyncio.fixture(scope="session")
async def flashdb_redis():
    redis: Redis = Redis.from_url(test_settings.redis_url)
    await redis.flushdb()
    await redis.close()

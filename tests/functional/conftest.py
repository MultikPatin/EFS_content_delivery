import json
from json import JSONDecodeError

import pytest
import aiohttp

from tests.functional.settings import settings

pytest_plugins = (
    "tests.functional.fixtures.connections",
    "tests.functional.fixtures.db_operations",
)


@pytest.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(path: str, query_data: dict = None):
        url = settings.get_api_host + "/api/v1" + path
        async with session.get(url, params=query_data) as response:
            body = await response.read()
        try:
            body = json.loads(body)
        except JSONDecodeError:
            pass
        status = response.status
        return body, status

    return inner

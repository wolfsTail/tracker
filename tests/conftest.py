import asyncio
import pytest


pytest_plugins = [
    "tests.fixtures.auth.auth_fixtures",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repo_fixture",
    "tests.fixtures.infrastructure_settings",
    "tests.fixtures.users.user_model",
    "tests.fixtures.users.users_fixtures",
]

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

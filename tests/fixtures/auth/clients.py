from dataclasses import dataclass

import factory, factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory
import pytest
import httpx

from app.core import settings
from app.schemas.auth import GoogleUserData, YandexUserData
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_EMAIL, EXISTS_GOOGLE_USER_ID


faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        return google_user_info_data()
    
    async def _get_user_access_token(self, code: str) -> str:
        return f"access_token_not_real_with_{code}"    


@dataclass
class FakeYandexClient:
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        return yandex_user_info_data()
        
    async def _get_user_access_token(self, code: str):
        return f"yandex_access_token_with_code_{code}"

@pytest.fixture
def google_client():
    return FakeGoogleClient(async_client=httpx.AsyncClient(), settings=settings)

@pytest.fixture
def yandex_client():
    return FakeYandexClient(async_client=httpx.AsyncClient(), settings=settings)

def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL,
        verified_email=True,
        name=faker.name(),
        access_token=faker.sha256(),
    )

def yandex_user_info_data() -> YandexUserData:
    return YandexUserData(
        id=faker.random_int(),
        default_email=faker.email(),
        login="bumshakalaka",
        real_name=faker.name(),
        access_token=faker.sha256(),
    )

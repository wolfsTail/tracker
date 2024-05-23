from dataclasses import dataclass

import pytest
import httpx

from app.core import settings


@dataclass
class FakeGoogleClient:
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code)
        return {"access_token": access_token}
    
    async def _get_user_access_token(self, code: str) -> str:
        return f"access_token_not_real_with_{code}"    


@dataclass
class FakeYandexClient:
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code)
        return {"access_token": access_token}
        
    async def _get_user_access_token(self, code: str):
        return f"yandex_access_token_with_code_{code}"

@pytest.fixture
def google_client():
    return FakeGoogleClient(async_client=httpx.AsyncClient(), settings=settings)

@pytest.fixture
def yandex_client():
    return FakeYandexClient(async_client=httpx.AsyncClient(), settings=settings)

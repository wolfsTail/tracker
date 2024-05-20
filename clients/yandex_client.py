from dataclasses import dataclass

import httpx

from schemas import YandexUserData
from core.settings import settings


@dataclass
class YandexClient():
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code)
        async with self.async_client() as client:
            user_info = await client.get(
                url="https://login.yandex.ru/info?format=json",
                headers={"Authorization": f"Oauth {access_token}"}
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    
    async def _get_user_access_token(self, code: str):
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            "grant_type": "authorization_code",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with self.async_client() as client:
            response = await client.post(
                url=self.settings.YANDEX_REDIRECT_URL, data=data, headers=headers
                )
        access_token = response.json()["access_token"]

        return access_token
from dataclasses import dataclass

import httpx

from app.schemas import GoogleUserData
from app.core.settings import settings


@dataclass
class GoogleClient:
    async_client: httpx.AsyncClient
    settings: settings

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code)
        async with self.async_client as client:
            user_info = await client.get(
                url="https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
                )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    
    async def _get_user_access_token(self, code: str):
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with self.async_client() as client:
            response = await client.post(
                url=self.settings.GOOGLE_TOKEN_URL, data=data
                )
        access_token = response.json()["access_token"]

        return access_token    
    
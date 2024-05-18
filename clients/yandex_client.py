from dataclasses import dataclass

import requests

from schemas import YandexUserData
from core.settings import settings


@dataclass
class YandexClient():
    settings = settings

    def get_user_info(self, code: str) -> dict:
        access_token = self._get_user_access_token(code)
        user_info = requests.get(
            url="https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"Oauth {access_token}"}
        )
        return YandexUserData(**user_info.json(), access_token=access_token)

    
    def _get_user_access_token(self, code: str):
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            "grant_type": "authorization_code",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            url=self.settings.YANDEX_REDIRECT_URL, data=data, headers=headers
            )
        access_token = response.json()["access_token"]

        return access_token
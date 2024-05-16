from dataclasses import dataclass

import requests

from schemas import GoogleUserData
from core.settings import settings


@dataclass
class GoogleClient():
    settings = settings

    def get_user_info(self, code: str) -> dict:
        access_token = self._get_user_access_token(code)
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return GoogleUserData(**user_info.json())

    
    def _get_user_access_token(self, code: str):
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_iri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(
            url=self.settings.GOOGLE_TOKEN_URL, data=data
            )
        access_token = response.json()["access_token"]

        return access_token
    
    
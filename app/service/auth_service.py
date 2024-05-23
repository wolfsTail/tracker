from datetime import timedelta, datetime
from dataclasses import dataclass

from jose import jwt, JWTError
from app.clients import GoogleClient, YandexClient


from app.core.settings import settings
from app.schemas import UserLoginSchema, UserCreateSchema
from app.repository import UserRepository
from app.utils import UserNotFoundException, UserNotAwailable, TokenExpireError, TokenNotValidError


@dataclass
class AuthService:
    yandex_client: YandexClient
    google_client: GoogleClient
    user_repo: UserRepository

    async def get_login_google_redirect(self) -> str:
        return settings.GOOGLE_REDIRECT_URL
      
    async def get_yandex_redirect(self) -> str:
        return settings.YANDEX_REDIRECT_URL

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)

        if user := await self.user_repo.get_user_by_email(email=user_data.email):
            access_token = await self.dummy_generate_access_token(iser_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)            

        create_user_data = UserCreateSchema(
             google_access_token=user_data.access_token,
             email=user_data.email,
             name=user_data.name
         )
        created_user = await self.user_repo.create_user(create_user_data)
        access_token = await self.dummy_generate_access_token(iser_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
    
    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code)

        if user := await self.user_repo.get_user_by_email(email=user_data.default_email):
            access_token = await self.dummy_generate_access_token(iser_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)            

        create_user_data = UserCreateSchema(
             yandex_access_token=user_data.access_token,
             email=user_data.default_email,
             name=user_data.name
         )
        created_user = await self.user_repo.create_user(create_user_data)
        access_token = await self.dummy_generate_access_token(iser_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def login(
            self, username: str, password: str
        ) -> UserLoginSchema:
        current_user = await self.user_repo.get_user_by_username(username)

        if not current_user:
            raise UserNotFoundException
        if current_user.password != password:
            raise UserNotAwailable
        
        access_token = await self.dummy_generate_access_token(iser_id=current_user.id)

        return UserLoginSchema(
                user_id=current_user.id, access_token=access_token
                )

    async def get_user_id_from_access_token(
            self, token: str
    ) -> int:
        payload = await self.decode_access_token(token)
        if payload["expire"] < datetime.utcnow().timestamp():
            raise TokenExpireError
        return payload["user_id"]
        
    @staticmethod
    async def dummy_generate_access_token(user_id: int) -> str:
        expired_date_unix = (datetime.utcnow() + timedelta(seconds=300)).timestamp()
        claims = {
            "user_id": user_id,
            "expire": expired_date_unix,
            }
        token = jwt.encode(
            claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM,
        )
        return token
    
    @staticmethod
    async def decode_access_token(token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM,])
        except JWTError:
            raise TokenNotValidError
        
        return payload

from datetime import timedelta, datetime
from dataclasses import dataclass

from jose import jwt

from core.settings import settings
from schemas import UserLoginSchema
from repository import UserRepository
from utils import UserNotFoundException, UserNotAwailable


@dataclass
class AuthService:
    user_repo = UserRepository

    async def login(
            self, username: str, password: str
        ) -> UserLoginSchema:
        current_user = await self.user_repo.get_user_by_username(username)

        if not current_user:
            raise UserNotFoundException
        if current_user.password != password:
            raise UserNotAwailable
        
        access_token = self.dummy_generate_access_token(iser_id=current_user.id)

        return UserLoginSchema(
                user_id=current_user.id, access_token=access_token
                )
        
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

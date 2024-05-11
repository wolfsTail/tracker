import string, random
from dataclasses import dataclass

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
        
        return UserLoginSchema(
                user_id=current_user.id, access_token=current_user.access_token
                )        

from dataclasses import dataclass

from schemas import UserLoginSchema
from repository import UserRepository
from service.auth_service import AuthService


@dataclass
class UserService:
    user_repo = UserRepository
    auth_service = AuthService

    async def create_user(
            self, 
            username: str, 
            password: str,            
            ) -> UserLoginSchema:
        user = await self.user_repo.create_user(username, password)
        access_token = await self.auth_service.dummy_generate_access_token(user.id)

        return UserLoginSchema(user_id=user.id, access_token=access_token)

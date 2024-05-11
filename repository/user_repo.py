from repository.base_repo import BaseRepo

from database.database import async_session_maker
from database.models import User


class UserRepository(BaseRepo):
    model_name = User
    current_session = async_session_maker

    @classmethod
    async def create_user(
        cls, username: str, password: str, access_token: str
        ) -> User:
        user_data = {
            "username": username,
            "password": password,
            "access_token": access_token,
        }
        user = await cls.create_one(user_data, cls.current_session())
        return user

    @classmethod
    async def get_user(cls, user_id: int) -> User | None:
        user = await cls.get_one(user_id, cls.current_session())
        return user

    @classmethod
    async def get_user_by_username(cls, username: str) -> User | None:
        filter = {
            "username": username,
        }
        users = await cls.get_by_filter(filter, cls.current_session())
        if users:
            return users[0]
        return None
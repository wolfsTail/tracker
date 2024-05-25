from dataclasses import dataclass

import pytest
from app.models.users import User

from app.schemas.user import UserCreateSchema
from tests.fixtures.users.user_model import UserFactory


@dataclass
class FakeUserRepo:

    @classmethod
    async def create_user(
        cls, *args, **kwargs
        ) -> User:
        return UserFactory()

    @classmethod
    async def get_user(cls, user_id: int) -> User | None:
        user = await cls.get_one(user_id, cls.current_session())
        return user
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> User | None:
        filter = {
            "email": email,
        }
        return None

    @classmethod
    async def get_user_by_username(cls, username: str) -> User | None:
        filter = {
            "username": username,
        }
        users = await cls.get_by_filter(filter, cls.current_session())
        if users:
            return users[0]
        return None
    

@pytest.fixture
def user_repo():
    return FakeUserRepo()

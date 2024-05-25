import pytest

from app.schemas import UserLoginSchema
from app.service.user_service import UserService
from app.schemas import UserLoginSchema


@pytest.mark.asyncio
async def test_create_user__complete(
    user_service: UserService
    ):
    username = "tester"
    password = "password"

    user = await user_service.create_user(username=username, password=password)

    assert isinstance(user, UserLoginSchema)
    assert "user_id" in user.__dict__
    assert "access_token" in user.__dict__

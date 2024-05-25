import pytest

from app.service.user_service import UserService


@pytest.fixture
def user_service(user_repo, auth_service):
    return UserService(
        user_repo=user_repo,
        auth_service=auth_service
        )

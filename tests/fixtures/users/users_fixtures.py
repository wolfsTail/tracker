import pytest

from app.service.user_service import UserService


@pytest.fixture
def user_service(fake_user_repo, mock_auth_service):
    return UserService(
        user_repo=fake_user_repo,
        auth_service=mock_auth_service,
        )

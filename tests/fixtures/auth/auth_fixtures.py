import pytest

from app.repository import UserRepository
from app.service.auth_service import AuthService


@pytest.fixture
def mock_auth_service(yandex_client, google_client, fake_user_repo):
    return AuthService(
        user_repo=fake_user_repo,
        yandex_client=yandex_client,
        google_client=google_client,
    )

@pytest.fixture
def auth_service(yandex_client, google_client, db_session):
    return AuthService(
        user_repo=UserRepository(current_session=db_session),
        yandex_client=yandex_client,
        google_client=google_client,
    )
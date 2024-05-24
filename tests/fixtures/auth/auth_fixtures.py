import pytest

from app.service.auth_service import AuthService


@pytest.fixture
def auth_service(yandex_client, google_client, user_repo):
    return AuthService(
        yandex_client=yandex_client,
        google_client=google_client,
        user_repo=user_repo
    )
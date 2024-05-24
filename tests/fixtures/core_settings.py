import pytest

from app.core.settings import settings as app_settings


@pytest.fixture
def settings():
    return app_settings
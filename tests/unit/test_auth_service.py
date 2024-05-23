import pytest

from app.service.depends import get_auth_service
from app.service.auth_service import AuthService


@pytest.mark.asyncio
async def test_get_google_redirect_url__ok():
    auth_service = await get_auth_service()
    assert isinstance(auth_service, AuthService)


@pytest.mark.asyncio
async def test_get_google_redirect_url__fail():
    ...
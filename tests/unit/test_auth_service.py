from datetime import datetime

import pytest
from jose import jwt

from app.core.settings import Settings
from app.service.auth_service import AuthService
from app.schemas import UserLoginSchema, UserCreateSchema


@pytest.mark.asyncio
async def test_get_google_redirect_url__complete(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.GOOGLE_REDIRECT_URL

    auth_service_google_redirect_url = await auth_service.get_login_google_redirect()

    assert auth_service_google_redirect_url == settings_google_redirect_url
    assert isinstance(auth_service, AuthService)

@pytest.mark.asyncio
async def test_get_google_redirect_url__fail(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.GOOGLE_REDIRECT_URL

    settings_google_redirect_url += "a"
    auth_service_google_redirect_url = await auth_service.get_login_google_redirect()

    assert auth_service_google_redirect_url != settings_google_redirect_url

@pytest.mark.asyncio
async def test_get_yandex_redirect_url__complete(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.YANDEX_REDIRECT_URL

    auth_service_google_redirect_url = await auth_service.get_yandex_redirect()

    assert auth_service_google_redirect_url == settings_google_redirect_url
    assert isinstance(auth_service, AuthService)

@pytest.mark.asyncio
async def test_get_yandex_redirect_url__fail(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.YANDEX_REDIRECT_URL

    settings_google_redirect_url += "a"
    auth_service_google_redirect_url = await auth_service.get_yandex_redirect()

    assert auth_service_google_redirect_url != settings_google_redirect_url

@pytest.mark.asyncio
async def test_generate_access_token__complete(auth_service: AuthService, settings: Settings):
    user_id = 0

    access_token = await auth_service.dummy_generate_access_token(user_id=user_id)
    decoded_token = jwt.decode(
        access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM,]
        )
    
    assert isinstance(access_token, str)
    assert ("user_id" in decoded_token) and ("expire" in decoded_token)
    assert decoded_token.get("user_id", None) == user_id
    assert decoded_token.get("expire", None) >= datetime.utcnow().timestamp()

@pytest.mark.asyncio
async def test_generate_access_token__fail(auth_service: AuthService, settings: Settings):
    user_id = 123

    access_token = await auth_service.dummy_generate_access_token(user_id=user_id)
    decoded_token = jwt.decode(
        access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM,]
        )    

    assert not all(("access_token" not in decoded_token, "expire" not in decoded_token))
    assert decoded_token.get("user_id", None) != user_id + 1
    assert not (decoded_token.get("expire", None) < datetime.utcnow().timestamp())

@pytest.mark.asyncio
async def test_google_auth__complete(auth_service: AuthService, settings: Settings):
    code = "not_real_code"

    user = await auth_service.google_auth(code=code)
    user_id = user.user_id
    access_token = user.access_token
    decoded_token = jwt.decode(
        access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM,]
        )
    user_id_from_decoded_token = decoded_token.get("user_id", "No!")

    assert isinstance(user, UserLoginSchema)
    assert user_id == user_id_from_decoded_token

@pytest.mark.asyncio
async def test_yandex_auth__complete(auth_service: AuthService, settings: Settings):
    code = "not_real_code_for_yandex"

    user = await auth_service.yandex_auth(code=code)
    user_id = user.user_id
    access_token = user.access_token
    decoded_token = jwt.decode(
        access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM,]
        )
    user_id_from_decoded_token = decoded_token.get("user_id", "No!")

    assert isinstance(user, UserLoginSchema)
    assert user_id == user_id_from_decoded_token

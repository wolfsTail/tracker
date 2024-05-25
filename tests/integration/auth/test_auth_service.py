import pytest
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_EMAIL, EXISTS_GOOGLE_USER_ID


@pytest.mark.asyncio
async def test_google_auth__login_not_exist_user(auth_service, db_session):
    code = "code_is_not_real"
    session: AsyncSession = db_session
    
    async with session as session:
        query = select(User)
        users = (await session.execute(query)).scalars().all()
    
    user = await auth_service.google_auth(code)

    assert len(users) == 0

    async with session as session:
        query = select(User).where(User.id == user.user_id)
        google_user = (await session.execute(query)).scalars().first()

    assert google_user


@pytest.mark.asyncio
async def test_google_auth__login_exist_user(auth_service, db_session):
    query = insert(User).values(
        id=EXISTS_GOOGLE_USER_ID, email=EXISTS_GOOGLE_USER_EMAIL,
    )
    session = db_session
    code = "not_real_code_again"

    async with session as session:
        await session.execute(query)
        await session.commit()
        user = await auth_service.google_auth(code)

    async with session as session:
        stmt = select(User).where(User.id == EXISTS_GOOGLE_USER_ID)
        login_user = (await session.execute(stmt)).scalar_onr_or_none()

    assert login_user.user_id == EXISTS_GOOGLE_USER_ID
    assert login_user.email == EXISTS_GOOGLE_USER_EMAIL

@pytest.mark.asyncio
async def test_base_login__complte(auth_service, db_session):
    session = db_session
    username = "user"
    password = "password"
    query = insert(User).values(
        username=username, password=password,
    )

    async with session as session:
        await session.execute(query)
        await session.commit()

    user = await auth_service.login(username=username, password=password)

    async with session as session:
        stmt = select(User).where(User.username == username)
        login_user = (await session.execute(stmt)).scalar_one_or_none()
    
    assert login_user is not None
    assert user.user_id == login_user.user_id

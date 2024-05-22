from fastapi import Depends, HTTPException, security, Security, status
import httpx

from app.clients import GoogleClient, YandexClient
from app.core.settings import settings
from app.service.task_service import TaskService
from app.service.category_service import CategoryService
from app.service.user_service import UserService
from app.service.auth_service import AuthService
from app.utils import AbstractUnitOfWork, UnitOfWork, TokenExpireError, TokenNotValidError


async def get_task_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)

async def get_category_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)

async def get_user_service() -> UserService:
    return UserService()

async def get_auth_service() -> AuthService:
    return AuthService()

reusable_auth = security.HTTPBearer()

async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_auth)
        ) -> int:
    try:
        user_id = await auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpireError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err.detail)
    except TokenNotValidError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err.detail) 
    return user_id

async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient

async def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)):
    return GoogleClient(async_client=async_client, settings=settings)

async def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)):
    return YandexClient(async_client=async_client, settings=settings)

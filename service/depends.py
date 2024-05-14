from fastapi import Depends, HTTPException, Request, security, Security, status

from service.task_service import TaskService
from service.category_service import CategoryService
from service.user_service import UserService
from service.auth_service import AuthService
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork
from utils import UserNotFoundException, UserNotAwailable, TokenExpireError, TokenNotValidError
from repository import TaskCache
from cache import get_redis_connection


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


# def get_task_cache_repo() -> TaskCache:
#     redis_connection = get_redis_connection()
#     return TaskCache(redis_connection)

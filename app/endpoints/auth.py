from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.schemas import UserLoginSchema, UserCreateSchema
from app.service.auth_service import AuthService
from app.service.depends import get_auth_service
from app.utils import UserNotAwailable, UserNotFoundException


router = APIRouter(prefix="/auth", tags=["auth",])


@router.get(
        path="/login/google", response_class=RedirectResponse
)
async def login_goole(
    auth_service: Annotated[AuthService ,Depends(get_auth_service)]
):
    redirect_url = await auth_service.get_login_google_redirect()
    return RedirectResponse(url=redirect_url)


@router.get(
        path="/login/yandex", response_class=RedirectResponse
)
async def login_yandex(
    auth_service: Annotated[AuthService ,Depends(get_auth_service)]
):
    redirect_url = await auth_service.get_yandex_redirect()
    return RedirectResponse(url=redirect_url)


@router.get(
      "/google",  
)
async def google_auth(
        code: str,
        auth_service: Annotated[AuthService ,Depends(get_auth_service)]
):
    return await auth_service.google_auth(code)


@router.get(
      "/yandex",  
)
async def yandex_auth(
        code: str,
        auth_service: Annotated[AuthService ,Depends(get_auth_service)]
):
    return await auth_service.yandex_auth(code)


@router.post(
    path="/login", response_model=UserLoginSchema
)
async def login_user(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService ,Depends(get_auth_service)]
) -> UserLoginSchema:
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotAwailable as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = err.detail
        )
    except UserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.detail
        )

from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from schemas.user import UserLoginSchema, UserCreateSchema
from service.user_service import UserService
from service.depends import get_user_service


router = APIRouter(prefix="/user", tags=["user",])


@router.post(
    path="", response_model=UserLoginSchema
)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService ,Depends(get_user_service)]
) -> UserLoginSchema:
    return await user_service.create_user(body.username, body.password)

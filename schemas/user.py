from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

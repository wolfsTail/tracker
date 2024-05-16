from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str | None
    password: str | None
    email: str | None = None
    google_access_token: str | None = None
    name: str | None = None


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

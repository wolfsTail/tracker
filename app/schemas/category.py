from pydantic import BaseModel


class Category(BaseModel):
    name: str


class ResponseCategory(Category):
    id: int

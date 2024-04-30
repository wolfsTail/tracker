from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response

from fixtures import categories as fixture_categories
from schemas.category import Category, ResponseCategory


router = APIRouter(prefix="/categories", tags=["categories",])


@router.get(
    path="/all",
    response_model=list[ResponseCategory]
)
async def get_all_categories():
    return fixture_categories

@router.head(
    path="/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def check_categories(response: Response):
    response.headers["X-Total-categories"] = str(len(fixture_categories))
    response.headers["last-modified"] = str(fixture_categories[-1]["id"])
    return None


@router.post(
    path="/",
    response_model=ResponseCategory
)
async def create_category(category: Category):
    category.__dict__["id"] = len(fixture_categories)
    fixture_categories.append(category)
    return category

@router.patch(
    path="/{category_id}",
    response_model=ResponseCategory
)
async def update_category(category_id: int, name: str):
    for category in fixture_categories:
        if category["id"] == category_id:
            category["name"] = name
            return category
    raise HTTPException(status_code=404, detail="category not found")


@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(category_id: int):
    for category in fixture_categories:
        if category["id"] == category_id:
            fixture_categories.remove(category)
            return {"message": "category deleted"}
    raise HTTPException(status_code=404, detail="category not found")
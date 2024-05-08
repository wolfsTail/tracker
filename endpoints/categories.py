from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends

from schemas.category import Category, ResponseCategory
from service.depends import CategoryService, get_category_service


router = APIRouter(prefix="/categories", tags=["categories",])


@router.get(
        path="/all", response_model=list[ResponseCategory]
)
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service)
    ):
    categories = await category_service.get_all_categories()
    if not categories:
        raise HTTPException(status_code=404, detail="Не найдено ни одной категории")
    return categories    


@router.head(path="/")
async def check_categories(
    response: Response, category_service: CategoryService = Depends(get_category_service)
    ):
    categories = await category_service.get_all_categories()
    response.headers["X-Total-categories"] = str(len(categories))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    path="/",
    response_model=ResponseCategory
)
async def create_category(
    category: Category, category_service: CategoryService = Depends(get_category_service)
    ):
    return await category_service.create_category(category)


@router.patch(
    path="/{category_id}",
    response_model=ResponseCategory
)
async def update_category(
    category_id: int, 
    category: Category, 
    category_service: CategoryService = Depends(get_category_service)
    ):
    updated_category = await category_service.update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="category not found")
    return updated_category


@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int, category_service: CategoryService = Depends(get_category_service)):
    success = await category_service.delete_one(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="category not found")
    return None

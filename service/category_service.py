from schemas import Category, ResponseCategory

from utils import AbstractUnitOfWork


class CategoryService:
    def __init__(self, uow: AbstractUnitOfWork) -> ResponseCategory:
        self.uow = uow

    async def get_one_category(self, category_id: int):
        async with self.uow:
            if category := self.uow.cache_categories.get_item(category_id):
                return category
            category = await self.uow.category.get_one(category_id, self.uow.session)
            if category:
                response_category = ResponseCategory.model_validate(category)
                self.uow.cache_categories.set_item(response_category)
                return response_category
            return None

    async def get_all_categories(self) -> list[ResponseCategory]:
        async with self.uow:
            if categories := self.uow.cache_categories.get_list_items():
                return categories
            categories = await self.uow.category.get_all(self.uow.session)
            response_categories = []
            if categories:
                response_categories = [ResponseCategory.model_validate(category) for category in categories]
                self.uow.cache_categories.set_list_items(response_categories)
            return response_categories
    
    async def create_category(self, category: Category) -> ResponseCategory:
        category_dict: dict = category.model_dump()
        async with self.uow:
            category = await self.uow.category.create_one(category_dict, self.uow.session)
            category_from_db = ResponseCategory.model_validate(category)
            await self.uow.commit()
            return category_from_db
    
    async def update_category(self, category_id: int, category: Category) ->ResponseCategory:
        category_dict: dict = category.model_dump()
        async with self.uow:
            category_updated = await self.uow.category.update_one(category_id, self.uow.session, category_dict)       

            if category_updated:
                category_from_bd = category_updated.model_validate(category)
                await self.uow.commit()
                return category_from_bd
        
        return None
    
    async def delete_one(self, category_id: int):
        async with self.uow:
            success = self.uow.category.delete_one(category_id, self.uow.session)
            if success:
                self.uow.commit()
                return 1
            return None

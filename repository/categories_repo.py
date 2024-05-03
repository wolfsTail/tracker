from database.models import Categories
from repository.base_repo import BaseRepo


class CategoryRepository(BaseRepo):
    model_name = Categories

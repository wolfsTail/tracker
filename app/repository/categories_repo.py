from app.models import Categories
from app.repository.base_repo import BaseRepo


class CategoryRepository(BaseRepo):
    model_name = Categories

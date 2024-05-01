from database.models import Categories
from repository.base_repo import BaseRepo


class TaskRepository(BaseRepo):
    model_name = Categories
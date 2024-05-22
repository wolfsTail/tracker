from abc import ABC, abstractclassmethod


class BaseCacheRepo(ABC):
    cache = None
    model = None

    @classmethod
    @abstractclassmethod
    async def get_list_items(cls):
        pass

    @classmethod
    @abstractclassmethod
    async def get_item(cls):
        pass

    @classmethod
    @abstractclassmethod
    async def set_item(cls):
        pass

    @classmethod
    @abstractclassmethod
    async def set_list_items(cls):
        pass

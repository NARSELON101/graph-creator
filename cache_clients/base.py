from abc import ABC, abstractmethod
from repositories.singleton import Singleton


class BaseCache(ABC, Singleton):

    def __init__(self, cache_object, **kwargs):
        self.cache_object = cache_object

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

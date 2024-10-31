import asyncio
from functools import wraps

from redis import asyncio as aioredis

from cache_clients.base import BaseCache


def reinit_event_loop(func, cls):
    @wraps(func)
    def inner(*args, **kwargs):
        cls.cache_object = aioredis.Redis(port=6380)
        print(cls.cache_object)
        return func(*args, **kwargs)
    return inner


def verbose_methods(cls):
    methods = {
        name: method
        for name, method in vars(cls).items()
        if not name.startswith("__") and callable(method)
    }
    for name, method in methods.items():
        setattr(cls, name, reinit_event_loop(method, cls))
    return cls


# @verbose_methods
class RedisCache(BaseCache):
    def __init__(self, **kwargs):
        super().__init__(aioredis.Redis(port=6380), **kwargs)

    async def get(self, key: str):
        val: bytes = await self.cache_object.get(key)
        if val:
            val = val.decode('utf-8')
        return val

    async def set(self, key, value):
        r = await self.cache_object.set(key, value)
        return r

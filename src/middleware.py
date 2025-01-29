import functools

from src import config
from src.user_middlewares import MiddlewareExample


class MiddlewareManager:
    def __init__(self, middlewares: list[MiddlewareExample] = None):
        self.middlewares = middlewares or config.MIDDLEWARES

    async def execute(self, data: dict):
        for middleware in self.middlewares:
            data = await middleware.process_crypto(data)

        return data


def enable_middlewares(func):
    @functools.wraps(func)
    async def wrapper(self, message: str, *args, **kwargs):
        data = await func(self, message, *args, **kwargs)

        mm = MiddlewareManager()
        data = await mm.execute(data)

        return data

    return wrapper

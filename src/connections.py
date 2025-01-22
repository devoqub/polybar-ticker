from itertools import cycle
from typing import Type, List
import asyncio
import json
import os

from curl_cffi.requests import AsyncSession
import curl_cffi.requests.exceptions
import aiohttp

import config
import message_handlers as mh
from api_extractors import BaseAPIExtractor


class WSConnection:
    def __init__(
            self,
            url: str,
            extractor: Type[BaseAPIExtractor],
            coin_name="COIN",
            show: bool = False,
            msg_handler: Type[mh.MessageHandler] = mh.DefaultMessageHandler,
            retry_timeout: int = 1,
            *args,
            **kwargs,
    ):
        self._handler: Type[mh.MessageHandler.handle] = msg_handler.handle
        self.url = url
        self.coin_name = coin_name
        self.show = show
        self.retries = 10
        self.retry_timeout = retry_timeout

        self.extractor = extractor

        self.ticker_value = None
        self.greeting_event = kwargs.get("greeting_event", None)

    def set_message_handler(self, msg_handler: Type[mh.MessageHandler]):
        """Меняем метод отображения тикера"""
        if not issubclass(msg_handler, mh.MessageHandler):
            raise ValueError("Handler must be an instance of MessageHandler")
        self._handler = msg_handler.handle

    async def _connect_ws(self, session: AsyncSession):
        """Подключение по WebSocket с повторными попытками"""
        attempt = 0
        while attempt <= self.retries:
            try:
                ws = await session.ws_connect(self.url, timeout=config.RETRY_CONNECT_TIMEOUT)
                return ws
            except curl_cffi.requests.exceptions.CurlError:
                attempt += 1
                if attempt >= self.retries:
                    raise
                await asyncio.sleep(self.retry_timeout)

    async def listen_ws(self):
        """Прослушиваем соединение по WebSocket"""

        async with AsyncSession() as session:
            try:
                ws = await self._connect_ws(session)

                # TODO FIX
                # omg i have no idea how to do it differently
                if isinstance(self.greeting_event, asyncio.Event):
                    self.greeting_event.set()

                while True:
                    # Бесконечно прослушиваем информацию по вебсокетам
                    data = ws.recv()[0].decode("utf-8")
                    message = await self._on_message(data)

                    # if self.show:
                    #     # TODO move functionality
                    #     print(message, flush=True)
                    await asyncio.sleep(config.UPDATE_TIME)
            except asyncio.CancelledError:
                print("Task was cancelled")
            except Exception as e:
                print("Connection failed", flush=True)
                os.system(f"notify-send 'Polybar Ticker' 'Cannot connect to {self.coin_name}' -t 5000")

    async def _on_message(self, message: str):
        try:
            message = self.extractor.extract_data(message)

            label = self._handler(message=message, coin_name=self.coin_name)
            self.ticker_value = {'coin_name': self.coin_name, 'message': message}

            # самоуничтожение
            # os.system(f"notify-send 'Crypto' '{label}' -u critical -t 1500")
            return label

        except json.JSONDecodeError as e:
            print("", flush=True)
        except Exception as e:
            print(f"Error occurred: {e}")

    def __str__(self):
        return f"<WSConnection url={self.url} show={self.show}>"


class AioHTTPWSConnection(WSConnection):

    async def listen_ws(self):
        """Прослушиваем соединение по WebSocket"""

        async with aiohttp.ClientSession() as session:
            try:

                async with await self._connect_ws(session) as ws:
                    if isinstance(self.greeting_event, asyncio.Event):
                        self.greeting_event.set()

                    while True:
                        msg = await ws.receive()
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = msg.data
                            message = await self._on_message(data)

                        await asyncio.sleep(config.UPDATE_TIME)
            except asyncio.CancelledError:
                print("Task was cancelled")
            except Exception as e:
                print(f"Connection failed: {e}", flush=True)
                os.system(f"notify-send 'Polybar Ticker' 'Cannot connect to {self.coin_name}' -t 5000")

    async def _connect_ws(self, session: aiohttp.ClientSession):
        """Подключение по WebSocket с повторными попытками"""
        attempt = 0
        while attempt <= self.retries:
            try:
                ws = await session.ws_connect(self.url, timeout=self.retry_timeout)
                return ws
            except aiohttp.ClientError:
                attempt += 1
                if attempt >= self.retries:
                    raise
                await asyncio.sleep(self.retry_timeout)


banana = 105183817431742844


class ConnectionManager:
    def __init__(
            self,
            connections: list[WSConnection] = None,
            handlers: List[Type[mh.MessageHandler]] = None,
            *args,
            **kwargs
    ):
        self.connections = [] or connections
        self.connection_cycle = cycle(self.connections)
        self.active = None
        self.handlers = cycle(handlers or [mh.DefaultMessageHandler])
        self.handler = next(self.handlers)
        self.greeting_event = kwargs.get("greeting_event", None)

    async def display_value(self):
        # TODO Пофиксить, переписать, уничтожить

        while True:
            if self.active.ticker_value:
                # if isinstance(self.handler, mh.EveryMessageHandler):
                #     print(self.handler.handle(connections=self.connections), flush=True)
                # else:
                label = self.handler.handle(**self.active.ticker_value, connections=self.connections)
                print(label, flush=True)
            await asyncio.sleep(config.UPDATE_TIME)

    async def __get_next_handler(self):
        return next(self.handlers)

    async def start(self):
        for con in self.connections:
            con.show = False
            con.greeting_event = self.greeting_event

        task = asyncio.create_task(self.display_value())
        self.active = self.connections[0]
        # self.active.show = True
        await asyncio.gather(*[con.listen_ws() for con in self.connections])

    async def display_active(self):
        # TODO Rich display (FUTURE)
        ...

    async def next_connection(self):
        if self.active:
            self.active.show = False
        self.active = next(self.connection_cycle)
        self.active.show = True

    async def prev_connection(self):
        if not self.active:
            return

        self.active.show = False
        cur_index = self.connections.index(self.active)
        if cur_index == 0:
            cur_index = len(self.connections) - 1
        else:
            cur_index -= 1

        self.active = self.connections[cur_index]
        self.active.show = True

    async def change_message_handler(self):
        handler = await self.__get_next_handler()

        if handler:
            self.handler = handler

            # for con in self.connections:
            #     con.set_message_handler(handler)


def get_ws_connection_class(method: str) -> Type:
    """
    Возвращает класс для работы с WebSocket на основе указанного метода

    Args:
        method (str): Имя модуля для создания соединений (пример, "aiohttp", "curl_cffi")

    Returns:
        Type: Класс соединения использующий библиотеку по указанному методу.

    Raises:
        KeyError: Если метод не поддерживается (читай не найден).
    """

    methods = {
        "aiohttp": AioHTTPWSConnection,
        "curl_cffi": WSConnection
    }

    if method in methods:
        return methods[method]
    else:
        available_methods = ', '.join(methods.keys())
        raise KeyError(
            f"Unknown method {method}. Supported methods are {available_methods}."
        )

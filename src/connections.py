from itertools import cycle
import asyncio
import json
import os
from abc import ABC, abstractmethod
from typing import Type, Iterable

import aiohttp
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import CurlError
from curl_cffi.requests.websockets import WebSocket

import config
import message_formatters as mh
from api_extractors import BaseAPIExtractor


class BaseWSConnection(ABC):
    def __init__(
            self,
            url: str,
            coin_name: str,
            extractor: Type[BaseAPIExtractor],
            retries: int = 10,
            retry_timeout: int | float = 1,
            retry_connect_timeout: int | float | None = None,
            *args,
            **kwargs,
    ):
        self.url = url
        self.retries = retries
        self.retry_timeout = retry_timeout
        self.retry_connect_timeout = retry_connect_timeout or config.RETRY_CONNECT_TIMEOUT
        self.extractor = extractor
        self.coin_name = coin_name
        self.greeting_event = kwargs.get("greeting_event", None)

        self.ticker_value = None

    @abstractmethod
    async def listen(self):
        raise NotImplementedError("This method must be implemented in subclass.")

    @abstractmethod
    async def _connect(self, session: Type) -> Type:
        raise NotImplementedError("This method must be implemented in subclass.")

    @abstractmethod
    async def _handle_message(self, ws: Type) -> Type:
        raise NotImplementedError("This method must be implemented in subclass.")

    async def _prepare_message(self, message: str):
        try:
            message = self.extractor.extract_data(data=message)
            self.ticker_value = {'coin_name': self.coin_name, 'message': message}

            # самоуничтожение
            # os.system(f"notify-send 'Polybar Ticker' '{label}' -u critical -t 2000")

        except json.JSONDecodeError:
            # Ничего не выводим, при подключении часто передается только часть данных, так что это нормально.
            print("", flush=True)
        except Exception as e:
            print(f"Error: {e}")


class AioHTTPWSConnection(BaseWSConnection):
    async def listen(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with await self._connect(session) as ws:
                        if isinstance(self.greeting_event, asyncio.Event):
                            self.greeting_event.set()

                        await self._handle_message(ws)

                except asyncio.CancelledError:
                    print("Task was cancelled")
                except Exception as e:
                    print(f"Connection failed: {e}", flush=True)
                    os.system(f"notify-send 'Polybar Ticker' 'Cannot connect to {self.coin_name}' -t 5000")

                await asyncio.sleep(1)

    async def _connect(self, session: aiohttp.ClientSession) -> aiohttp.ClientWebSocketResponse:
        attempt = 0

        while attempt <= self.retries:
            try:
                ws = await session.ws_connect(self.url, timeout=self.retry_connect_timeout)
                return ws
            except aiohttp.ClientError:
                attempt += 1
                await asyncio.sleep(self.retry_timeout)

        raise TimeoutError("Не удалось подключится к серверу.")

    async def _handle_message(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        while not ws.closed:

            msg = await ws.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                message = msg.data
                await self._prepare_message(message)
            elif msg.type in (aiohttp.WSMsgType.ERROR, aiohttp.WSMsgType.CLOSED):
                break

            await asyncio.sleep(config.UPDATE_TIME)
            # Сбрасываем накопившиеся сообщения
            await ws.receive()


class CurlCffiWSConnection(BaseWSConnection):
    async def listen(self):
        async with AsyncSession() as session:
            while True:
                try:
                    ws = await self._connect(session)

                    if isinstance(self.greeting_event, asyncio.Event):
                        self.greeting_event.set()

                    await self._handle_message(ws)

                except asyncio.CancelledError:
                    print("Task was cancelled")
                except Exception:
                    print("Connection failed", flush=True)
                    os.system(f"notify-send 'Polybar Ticker' 'Cannot connect to {self.coin_name}' -t 5000")
                await asyncio.sleep(1)

    async def _handle_message(self, ws: WebSocket) -> None:
        while True:
            # Бесконечно прослушиваем информацию по вебсокетам
            message = ws.recv()[0].decode("utf-8")
            await self._prepare_message(message)

            await asyncio.sleep(config.UPDATE_TIME)
            # Сбрасываем накопившиеся сообщения
            ws.recv()

    async def _connect(self, session: AsyncSession) -> WebSocket:
        attempt = 0

        while attempt <= self.retries:
            try:
                ws = await session.ws_connect(self.url, timeout=config.RETRY_CONNECT_TIMEOUT)
                return ws
            except CurlError:
                attempt += 1
                if attempt >= self.retries:
                    raise
                await asyncio.sleep(self.retry_timeout)


class ConnectionManager:
    def __init__(
            self,
            connections: Iterable[BaseWSConnection] = None,
            formatters: Iterable[Type[mh.MessageFormatter]] = None,
            *args,
            **kwargs
    ):
        self.connections = connections or []
        self.connection_cycle = cycle(self.connections)
        self.active = None
        self.formatters = cycle(formatters or [mh.DefaultMessageFormatter])
        self.formatter = next(self.formatters)
        self.greeting_event = kwargs.get("greeting_event", None)

    async def display_ticker(self):
        while True:
            if self.active.ticker_value:
                label = self.formatter.handle(**self.active.ticker_value, connections=self.connections)
                print(label, flush=True)

            await asyncio.sleep(config.UPDATE_TIME)

    async def __get_next_formatter(self):
        return next(self.formatters)

    async def start(self):
        for con in self.connections:
            con.greeting_event = self.greeting_event

        task = asyncio.create_task(self.display_ticker())
        self.active = self.connections[0]

        await asyncio.gather(*[con.listen() for con in self.connections])

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

    async def change_message_formatter(self):
        formatter = await self.__get_next_formatter()

        if formatter:
            self.formatter = formatter


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
        "curl_cffi": CurlCffiWSConnection
    }

    if method in methods:
        return methods[method]
    else:
        available_methods = ', '.join(methods.keys())
        raise KeyError(
            f"Unknown method {method}. Supported methods are {available_methods}."
        )

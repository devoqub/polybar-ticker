from abc import ABC, abstractmethod
from typing import Any
import json

"""Классы для работы с разными поставщиками API"""


class BaseAPIExtractor(ABC):
    """
    Абстрактный базовый класс для API-экстракторов.
    Служит шаблоном для реализации методов извлечения данных.
    """

    @abstractmethod
    def extract_data(self, data: Any) -> Any:
        """
        Метод для извлечения данных о криптовалюте из переданного объекта.
        """

        raise NotImplementedError(
            "Method 'extract_data' must be implemented in subclass."
        )


class GeminiAPIExtractor(BaseAPIExtractor):
    def extract_data(self, data: Any) -> Any:
        data = json.loads(data)
        return data["events"][0]["price"]

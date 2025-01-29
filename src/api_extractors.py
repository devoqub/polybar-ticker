from abc import ABC, abstractmethod
from typing import Any, Type
import json

"""Классы для работы с разными поставщиками API"""


class BaseAPIExtractor(ABC):
    """
    Абстрактный базовый класс для API-экстракторов.
    Служит шаблоном для реализации методов извлечения данных.
    """

    @staticmethod
    @abstractmethod
    def extract_data(data: Any) -> Any:
        """
        Метод для извлечения данных о криптовалюте из переданного объекта.
        """

        raise NotImplementedError(
            "Method 'extract_data' must be implemented in subclass."
        )


class GeminiAPIExtractor(BaseAPIExtractor):
    @staticmethod
    def extract_data(data: str) -> Any:
        try:
            data = json.loads(data)
            price = data["events"][0]["price"]
            return price
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid data format: {e}")


def get_extractor_class(service: str) -> Type[BaseAPIExtractor]:
    services = {
        "gemini": GeminiAPIExtractor,
        # ...
    }

    if service in services:
        return services[service]
    else:
        available_services = ', '.join(services.keys())
        raise KeyError(
            f"Unknown method {service}. Supported api services are {available_services}."
        )

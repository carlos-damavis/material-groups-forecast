import abc
from typing import Any


class Config(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> Any:
        ...

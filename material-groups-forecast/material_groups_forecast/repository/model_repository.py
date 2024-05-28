import abc
from typing import Dict


class ModelRepository(abc.ABC):
    @abc.abstractmethod
    def read(self, file):
        pass

    @abc.abstractmethod
    def write(self, model: Dict, level: str) -> None:
        pass

import abc
from typing import Any


class EnvVarsGetter(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get(config_json_path: str) -> Any:
        pass

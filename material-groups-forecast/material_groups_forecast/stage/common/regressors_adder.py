import abc

from pandas import DataFrame


class RegressorsAdder(abc.ABC):

    @abc.abstractmethod
    def add(self, data: DataFrame) -> DataFrame:
        pass

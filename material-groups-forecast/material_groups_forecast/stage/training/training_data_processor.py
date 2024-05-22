import abc

from pandas import DataFrame


class TrainingDataProcessor(abc.ABC):

    @abc.abstractmethod
    def process(self, training_data: DataFrame) -> DataFrame:
        pass

import abc

from pandas import DataFrame


class TrainingDataGrouper(abc.ABC):

    @abc.abstractmethod
    def group(self, training_data: DataFrame) -> DataFrame:
        pass

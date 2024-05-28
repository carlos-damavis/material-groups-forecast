import abc

from pandas import DataFrame


class ModelsAllGroupsTrainer(abc.ABC):

    @abc.abstractmethod
    def train(self, training_data: DataFrame):
        pass

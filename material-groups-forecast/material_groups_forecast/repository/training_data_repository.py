import abc
from datetime import date

from pandas import DataFrame


class TrainingDataRepository(abc.ABC):

    @abc.abstractmethod
    def get(self, start_date: date, end_date: date) -> DataFrame:
        ...

    def save_data(self, df: DataFrame, table_id: str, override: bool):
        ...

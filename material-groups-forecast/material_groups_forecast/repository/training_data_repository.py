import abc
from datetime import date
from typing import Optional

from pandas import DataFrame


class TrainingDataRepository(abc.ABC):

    @abc.abstractmethod
    def get(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> DataFrame:
        pass

    @abc.abstractmethod
    def save_data(self, df: DataFrame, table_id: str, override: bool) -> None:
        pass

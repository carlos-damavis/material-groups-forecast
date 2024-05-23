import abc
from datetime import date, timedelta
from typing import Optional, Sequence
from pandas import DataFrame


class BigQueryResource(abc.ABC):
    @abc.abstractmethod
    def read(self, table_id: str, date_column_name: Optional[date],
                                  start_date: Optional[date]= None,
                                  end_date: Optional[date]= None) -> DataFrame:

        ...
    @abc.abstractmethod
    def upload(self,
               df: DataFrame,
               table_id: str,
               override: bool,
               expiration_time: Optional[timedelta] = None):
        ...

    @abc.abstractmethod
    def merge(self,
              source_table_id: str,
              target_table_id: str,
              merge_keys: Sequence[str]):
        ...

    @abc.abstractmethod
    def delete(self, table: str):
        ...


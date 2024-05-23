from datetime import date
from pandas import DataFrame
from typing import Optional

from repository.training_data_repository import TrainingDataRepository
from repository.resource.bigquery.bigquery_resource import BigQueryResource
from conf.config import Config


class TrainingDataRepository(TrainingDataRepository):

    def __init__(self,
                 bigquery_resource: BigQueryResource,
                 dataframe_resource: DataFrame,
                 config: Config
                 ):
        self.bigquery_resource_input = bigquery_resource
        self.dataframe_resource = dataframe_resource
        self.config = config

    def get(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> DataFrame:
        return self.bigquery_resource.read(
                                         self.config.get('bigquery_table_id'),
                                         start_date,
                                         end_date)

    def save_data(self, df: DataFrame, override: bool, start_date: Optional[date] = None):
        if override:
            self.bigquery_resource.upload(df,
                                          table_id=self.config.get('bigquery_table_id'),
                                          override=True,
                                          expiration_time=None)
        else:
            self._upsert(df)
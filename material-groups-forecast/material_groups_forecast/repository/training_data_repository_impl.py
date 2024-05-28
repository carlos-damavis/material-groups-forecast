import os
from datetime import date
from pandas import DataFrame
from typing import Optional

from material_groups_forecast.conf.config_getter import ConfigGetter
from material_groups_forecast.repository.resource.bigquery.bigquery_resource import BigQueryResource
from material_groups_forecast.repository.training_data_repository import TrainingDataRepository


class TrainingDataRepositoryImpl(TrainingDataRepository):
    def __init__(self, bigquery_resource: BigQueryResource, trainig_data: str):
        self.bigquery_resource = bigquery_resource
        self.training_data = trainig_data

    def get(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> DataFrame:
        data = self.bigquery_resource.read(self.training_data, start_date, end_date)

        return data

    def save_data(self, df: DataFrame, table_id: str, override: bool):
        self.bigquery_resource.upload(df, table_id=table_id, override=True, expiration_time=None)

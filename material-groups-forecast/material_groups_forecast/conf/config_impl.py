import abc
from typing import Any, Optional
import json, os
from conf.config import Config


class Config(Config):

    def __init__(self,
                 config_json_path: Optional[str] = None,
                 credentials=None):

        if config_json_path is not None:
            with open(config_json_path, 'r') as f:
                env_vars = json.load(f)

            for key, val in env_vars.items():
                if key == 'bigquery_credentials':
                    credentials = val
                    continue
                os.environ[key] = str(val)

        self.values = {
            'bigquery_credentials': credentials,
            'bigquery_read_table_id': os.environ['bigquery_read_table_id'],
            'bigquery_table_month_id': os.environ['bigquery_table_month_id'],
            'bigquery_table_week_id': os.environ['bigquery_table_week_id'],
            'bigquery_table_day_id': os.environ['bigquery_table_day_id'],
            'storage_data_path': os.environ['storage_data_path'],
            'stage_data_path': os.environ['stage_data_path'],
            'bigquery_project_id': os.environ['bigquery_project_id'],
            'bigquery_dataset_id': os.environ['bigquery_dataset_id'],
            'tmp_bigquery_bucket': os.environ['tmp_bigquery_bucket']

        }

    def get(self, key: str) -> Any:
        try:
            return self.values[key]
        except KeyError:
            raise ValueError(f"The value for the key {key} doesn't exists")
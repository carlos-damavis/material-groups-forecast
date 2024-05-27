import abc

import google.cloud.bigquery as bq

class BigQueryClient(abc.ABC):

    @abc.abstractmethod
    def get_table(self, table_id: str) -> bq.Table:
        ...

    @abc.abstractmethod
    def delete_table(self, table_id: str):
        ...

    @abc.abstractmethod
    def query(self, query: str):
        ...

    @abc.abstractmethod
    def create_table(self, table: bq.Table, exists_ok: bool):
        ...

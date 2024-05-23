import google.cloud.bigquery as bq

from repository.resource.bigquery.client.client import BigQueryClient

class BigQueryClientImp(BigQueryClient):

    def __init__(self,
                 credentials: dict):
        try:
            self.client = bq.Client()
        except TypeError:
            self.client = bq.Client.from_service_account_info(credentials)

    def get_table(self, table_id: str) -> bq.Table:
        return self.client.get_table(table_id)

    def delete_table(self, table_id: str):
        self.client.delete_table(table_id)

    def query(self, query: str) -> bq.job.QueryJob:
        return self.client.query(query)

    def create_table(self, table: bq.Table, exists_ok: bool):
        self.client.create_table(table, exists_ok=exists_ok)

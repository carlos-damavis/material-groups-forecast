from datetime import timedelta, datetime
from typing import Optional, List, Dict

from google.cloud.bigquery import Client as BigQueryClient, Table as BigQueryTable
from google.cloud.exceptions import NotFound
from pandas import DataFrame

from material_groups_forecast.repository.resource.bigquery.bigquery_resource import BigQueryResource


class BigQueryResourceImpl(BigQueryResource):

    def __init__(self, credentials: Dict, temporary_bucket: str):
        try:
            self.client = BigQueryClient()
        except TypeError:
            self.client = BigQueryClient.from_service_account_info(credentials)
        self.temporary_bucket = temporary_bucket

    def read(
            self,
            table_id: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date_column_name: Optional[str] = 'fecha_entrada'
    ) -> DataFrame:
        table = self.client.get_table(table_id)

        # FIXME: This is too specific to be a resource. Can we make it more general by passing a list of columns to
        #  filter or dont use it and directly create queries in the repository??
        # FIXME: start_date can be none while end_date is not none. Add other case??
        if start_date and end_date:
            query = f"""
                    SELECT *
                    FROM `{table}`
                    WHERE 
                        `{date_column_name}` >= DATE('{start_date}')
                        AND
                        `{date_column_name}` < DATE('{end_date}')
                    """
        else:
            query = f"""
                    SELECT *
                    FROM `{table}`"""
        response = self.client.query(query).to_dataframe()
        return response

    def merge(self, source_table_id: str, target_table_id: str, merge_keys: List[str]):
        source_table = self.client.get_table(source_table_id)

        columns = [field.name for field in source_table.schema]

        update_clause = "".join(f"{column} = B.{column}, "
                                for column in columns if column not in merge_keys)[:-2]

        values_clause = "(" + "".join((f"{column}, "
                                       for column in columns))[:-2] + ")"

        on_clauses = "".join((f"A.{key} = B.{key} AND "
                              for key in merge_keys))[:-4]

        insert_clauses = "(" + "".join(f"{col}, " for col in columns)[:-2] + ")"

        query = f"""
        MERGE `{target_table_id}` A
        USING `{source_table_id}` B
        ON {on_clauses}
        WHEN MATCHED THEN
            UPDATE SET
                {update_clause}
        WHEN NOT MATCHED THEN
            INSERT {insert_clauses}
            VALUES {values_clause}
        """

        self.client.query(query).result()

    def upload(self, df: DataFrame, table_id: str, override: bool, expiration_time: Optional[timedelta] = None):
        try:
            self.client.get_table(table_id)
        except NotFound:
            # FIXME: Does it work??
            table = BigQueryTable(table_id)

            if expiration_time is not None:
                table.expires = datetime.now() + expiration_time

            self.client.create_table(table, exists_ok=False)

        mode = "overwrite" if override else "append"

        df.write.format('bigquery') \
            .option('table', table_id) \
            .option("temporaryGcsBucket", self.temporary_bucket) \
            .mode(mode) \
            .save()

    def delete(self, table: str):
        self.client.delete_table(table)

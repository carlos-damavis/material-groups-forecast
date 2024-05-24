from itertools import product

from pandas import DataFrame, date_range, ArrowDtype
from pyarrow import table, date32, string, schema

from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainingDataDayGrouperImpl(TrainingDataGrouper):

    @staticmethod
    def _create_full_dates_groups_data_set(data):
        all_dates = date_range(data.fecha_entrada.min(), data.fecha_entrada.max())
        all_groups = [
            group for group in data.dropna(subset=["forecastedGroup"]).forecastedGroup.unique() if group != ""
        ]
        all_groups.sort()

        all_data_schema = {"forecastedGroup": string(), "fecha_entrada": date32()}

        all_data = table(
            DataFrame(product(all_groups, all_dates), columns=["forecastedGroup", "fecha_entrada"]),
            schema=schema(all_data_schema)
        ).to_pandas(types_mapper=ArrowDtype)

        return all_data

    def group(self, training_data: DataFrame) -> DataFrame:
        all_data = self._create_full_dates_groups_data_set(training_data)
        training_data_grouped = training_data \
            .groupby(["forecastedGroup", "fecha_entrada"], as_index=False)[["peso_neto"]].sum()
        all_data = all_data.merge(training_data_grouped, on=["forecastedGroup", "fecha_entrada"], how="left")
        all_data.peso_neto = all_data.peso_neto.fillna(0.0)

        return all_data

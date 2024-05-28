from pandas import DataFrame

from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainingDataMonthGrouperImpl(TrainingDataGrouper):

    def group(self, training_data: DataFrame) -> DataFrame:
        aggregations = {
            "fecha_entrada": "first",
            "peso_neto": "sum",
            "month": "first",
            "problematicDates": "sum",
            "covid": "sum",
            "numWeekendDays": "sum"
        }

        training_data_monthly = training_data.copy()
        training_data_monthly["yearMonth"] = training_data_monthly.fecha_entrada.dt.strftime("%Y-%m")
        training_data_monthly["numWeekendDays"] = training_data_monthly.weekDay >= 6
        training_data_monthly = training_data_monthly \
            .groupby(["forecastedGroup", "yearMonth"], as_index=False).agg(aggregations)
        training_data_monthly = training_data_monthly.drop(columns=["yearMonth"])

        return training_data_monthly

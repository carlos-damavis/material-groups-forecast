from pandas import DataFrame

from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainingDataWeekGrouperImpl(TrainingDataGrouper):

    def group(self, training_data: DataFrame) -> DataFrame:
        aggregations = {
            "fecha_entrada": "first",
            "peso_neto": "sum",
            "month": "first",
            "problematicDates": "max",
            "covid": "max"
        }

        training_data_weekly = training_data.copy()
        training_data_weekly["yearWeek"] = training_data_weekly.fecha_entrada.dt.strftime("%Y-w%V")
        training_data_weekly = training_data_weekly \
            .groupby(["forecastedGroup", "yearWeek"], as_index=False).agg(aggregations)

        return training_data_weekly

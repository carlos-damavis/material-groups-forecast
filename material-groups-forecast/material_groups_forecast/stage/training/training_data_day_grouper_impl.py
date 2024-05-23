from pandas import DataFrame

from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainingDataDayGrouperImpl(TrainingDataGrouper):

    def group(self, training_data: DataFrame) -> DataFrame:
        training_data_grouped = training_data \
            .groupby(["forecastedGroup", "fecha_entrada"], as_index=False)[["peso_neto"]].sum()

        return training_data_grouped

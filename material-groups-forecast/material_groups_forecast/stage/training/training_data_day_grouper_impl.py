from pandas import DataFrame

from material_groups_forecast.stage.common.groups_argument_mapper import GroupsArgumentMapper
from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainingDataDayGrouperImpl(TrainingDataGrouper):
    def __init__(self, groups_argument_mapper: GroupsArgumentMapper, forecasted_group: str):
        self.forecasted_group = groups_argument_mapper.map(forecasted_group)

    def group(self, training_data: DataFrame) -> DataFrame:
        training_data_grouped = training_data \
            .groupby([self.forecasted_group, "fecha_entrada"], as_index=False)[["peso_neto"]].sum()

        return training_data_grouped

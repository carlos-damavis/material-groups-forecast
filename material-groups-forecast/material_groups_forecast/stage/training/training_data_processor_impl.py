from pandas import DataFrame, to_datetime, ArrowDtype
from pyarrow import date32

from material_groups_forecast.stage.common.groups_argument_mapper import GroupsArgumentMapper
from material_groups_forecast.stage.training.training_data_processor import TrainingDataProcessor


class TrainingDataProcessorImpl(TrainingDataProcessor):
    def __init__(self, groups_argument_mapper: GroupsArgumentMapper, forecasted_group: str):
        self.forecasted_group = groups_argument_mapper.map(forecasted_group)

    def process(self, training_data: DataFrame) -> DataFrame:
        training_data.fecha_entrada = to_datetime(training_data.fecha_entrada)
        training_data.fecha_entrada = training_data.fecha_entrada.astype(ArrowDtype(date32()))
        training_data = training_data.rename(columns={self.forecasted_group: "forecastedGroup"})
        training_data = training_data.loc[:, ["forecastedGroup", "fecha_entrada", "peso_neto"]]

        return training_data

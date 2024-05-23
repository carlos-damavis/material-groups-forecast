from pandas import DataFrame, to_datetime

from material_groups_forecast.stage.training.training_data_processor import TrainingDataProcessor


class TrainingDataProcessorImpl(TrainingDataProcessor):

    def process(self, training_data: DataFrame) -> DataFrame:
        training_data.fecha_entrada = to_datetime(training_data.fecha_entrada)

        return training_data

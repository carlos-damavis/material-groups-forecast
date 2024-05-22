from datetime import date

from material_groups_forecast.repository.training_data_repository import TrainingDataRepository
from material_groups_forecast.stage.training.training_data_processor import TrainingDataProcessor


class TrainPipeline:
    def __init__(
            self,
            training_data_repository: TrainingDataRepository,
            training_data_processor: TrainingDataProcessor
    ):
        self.training_data_repository = training_data_repository
        self.training_data_processor = training_data_processor

    def run(self, start_date: date, end_date: date) -> None:

        training_data = self.training_data_repository.get(start_date, end_date)
        training_data = self.training_data_processor.process(training_data)

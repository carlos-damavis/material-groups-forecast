from datetime import date

from material_groups_forecast.repository.training_data_repository import TrainingDataRepository
from material_groups_forecast.stage.common.regressors_adder import RegressorsAdder
from material_groups_forecast.stage.training.models_all_groups_trainer import ModelsAllGroupsTrainer
from material_groups_forecast.stage.training.training_data_processor import TrainingDataProcessor
from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper


class TrainPipeline:
    def __init__(
            self,
            training_data_repository: TrainingDataRepository,
            training_data_processor: TrainingDataProcessor,
            training_data_day_grouper: TrainingDataGrouper,
            regressors_adder: RegressorsAdder,
            training_data_week_grouper: TrainingDataGrouper,
            training_data_month_grouper: TrainingDataGrouper,
            models_all_groups_trainer: ModelsAllGroupsTrainer
    ):
        self.training_data_repository = training_data_repository
        self.training_data_processor = training_data_processor
        self.training_data_day_grouper = training_data_day_grouper
        self.regressors_adder = regressors_adder
        self.training_data_week_grouper = training_data_week_grouper
        self.training_data_month_grouper = training_data_month_grouper
        self.models_all_groups_trainer = models_all_groups_trainer

    def run(self, start_date: date, end_date: date) -> None:

        training_data = self.training_data_repository.get(start_date, end_date)
        training_data = self.training_data_processor.process(training_data)
        training_data_day = self.training_data_day_grouper.group(training_data)
        training_data_day = self.regressors_adder.add(training_data_day)
        training_data_week = self.training_data_week_grouper.group(training_data_day)
        training_data_month = self.training_data_month_grouper.group(training_data_day)

        models_day_level = self.models_all_groups_trainer.train(training_data_day)
        models_week_level = self.models_all_groups_trainer.train(training_data_week)
        models_month_level = self.models_all_groups_trainer.train(training_data_month)

        self.model_repository.write(models_day_level, "day")
        self.model_repository.write(models_week_level, "week")
        self.model_repository.write(models_month_level, "month")

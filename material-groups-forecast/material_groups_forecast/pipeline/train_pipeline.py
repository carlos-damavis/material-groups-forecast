from datetime import date

from material_groups_forecast.repository.training_data_repository import TrainingDataRepository
from material_groups_forecast.stage.common.regressors_adder import RegressorsAdder
from material_groups_forecast.stage.training.training_data_processor import TrainingDataProcessor
from material_groups_forecast.stage.training.training_data_grouper import TrainingDataGrouper

from conf.config import Config


class TrainPipeline:
    def __init__(
            self,
            data_repository: TrainingDataRepository,
            training_data_processor: TrainingDataProcessor,
            training_data_day_grouper: TrainingDataGrouper,
            regressors_adder: RegressorsAdder,
            training_data_week_grouper: TrainingDataGrouper,
            training_data_month_grouper: TrainingDataGrouper,
            config: Config
    ):
        self.data_repository = data_repository
        self.training_data_processor = training_data_processor
        self.training_data_day_grouper = training_data_day_grouper
        self.regressors_adder = regressors_adder
        self.training_data_week_grouper = training_data_week_grouper
        self.training_data_month_grouper = training_data_month_grouper
        self.config = config

    def run(self, start_date: date, end_date: date) -> None:

        training_data = self.data_repository.get(start_date, end_date)
        training_data = self.training_data_processor.process(training_data)
        training_data_day = self.training_data_day_grouper.group(training_data)

        training_data_day = self.regressors_adder.add(training_data_day)
        training_data_week = self.training_data_week_grouper.group(training_data_day)
        training_data_month = self.training_data_month_grouper.group(training_data_day)

        self.data_repository.save_data(training_data_day,
                                       table_id=self.config.get('bigquery_table_day_id'),
                                       override=False)
        self.data_repository.save_data(training_data_week,
                                       table_id=self.config.get('bigquery_table_week_id'),
                                       override=False)
        self.data_repository.save_data(training_data_month,
                                       table_id=self.config.get('bigquery_table_month_id'),
                                       override=False)




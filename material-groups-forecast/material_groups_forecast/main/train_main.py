import json
import os

from material_groups_forecast import ROOT_PATH
from material_groups_forecast.argument.train_arguments import TrainArguments
from material_groups_forecast.conf.env_vars_getter_impl import EnvVarsGetterImpl
from material_groups_forecast.pipeline.train_pipeline import TrainPipeline
from material_groups_forecast.repository.model_repository_impl import ModelRepositoryImpl
from material_groups_forecast.repository.resource.bigquery.bigquery_resource_impl import BigQueryResourceImpl
from material_groups_forecast.repository.training_data_repository_impl import TrainingDataRepositoryImpl
from material_groups_forecast.stage.common.groups_argument_mapper_impl import GroupsArgumentMapperImpl
from material_groups_forecast.stage.common.regressors_adder_impl import RegressorsAdderImpl
from material_groups_forecast.stage.training.prophet_models_all_groups_trainer_impl import \
    ProphetModelsAllGroupsTrainerImpl
from material_groups_forecast.stage.training.training_data_day_grouper_impl import TrainingDataDayGrouperImpl
from material_groups_forecast.stage.training.training_data_month_grouper import TrainingDataMonthGrouperImpl
from material_groups_forecast.stage.training.training_data_processor_impl import TrainingDataProcessorImpl
from material_groups_forecast.stage.training.training_data_week_grouper import TrainingDataWeekGrouperImpl


class TrainMain(TrainArguments):

    def __init__(self):
        super().__init__()
        self.config.read(os.path.join(ROOT_PATH, "conf", "sources.ini"))
        self.start_date = self.args.start_date
        self.end_date = self.args.end_date

    @staticmethod
    def _get_training_data_repository():
        env_vars_getter = EnvVarsGetterImpl().get(f"{ROOT_PATH}/conf/env_variables.json")
        credentials = env_vars_getter["bigquery_credentials"]
        bigquery_resource = BigQueryResourceImpl(credentials, env_vars_getter["tmp_bigquery_bucket"])
        training_data_repository = TrainingDataRepositoryImpl(
            bigquery_resource,
            env_vars_getter["bigquery_training_data_table"]
        )

        return training_data_repository

    def _get_training_data_processor(self):
        groups_argument_mapper = GroupsArgumentMapperImpl()
        training_data_processor = TrainingDataProcessorImpl(groups_argument_mapper, self.args.forecasted_group)

        return training_data_processor

    @staticmethod
    def _get_training_data_day_grouper():
        training_data_day_grouper = TrainingDataDayGrouperImpl()

        return training_data_day_grouper

    @staticmethod
    def _get_regressors_adder():
        regressors_adder = RegressorsAdderImpl()

        return regressors_adder

    @staticmethod
    def _get_training_data_week_grouper():
        training_data_week_grouper = TrainingDataWeekGrouperImpl()

        return training_data_week_grouper

    @staticmethod
    def _get_training_data_month_grouper():
        training_data_month_grouper = TrainingDataMonthGrouperImpl()

        return training_data_month_grouper

    @staticmethod
    def _get_models_all_groups_trainer():
        models_all_groups_trainer = ProphetModelsAllGroupsTrainerImpl()

        return models_all_groups_trainer

    def _get_model_repository(self):
        model_repository = ModelRepositoryImpl(self.config)

        return model_repository

    def run(self):

        train_pipeline = TrainPipeline(
            training_data_repository=self._get_training_data_repository(),
            training_data_processor=self._get_training_data_processor(),
            training_data_day_grouper=self._get_training_data_day_grouper(),
            regressors_adder=self._get_regressors_adder(),
            training_data_week_grouper=self._get_training_data_week_grouper(),
            training_data_month_grouper=self._get_training_data_month_grouper(),
            models_all_groups_trainer=self._get_models_all_groups_trainer(),
            model_repository=self._get_model_repository()
        )

        train_pipeline.run(self.start_date, self.end_date)


def main():
    TrainMain().run()


if __name__ == "__main__":
    main()

import os

from material_groups_forecast import ROOT_PATH
from material_groups_forecast.argument.train_arguments import TrainArguments
from material_groups_forecast.pipeline.train_pipeline import TrainPipeline


class TrainMain(TrainArguments):

    def __init__(self):
        super().__init__()
        self.config.read(os.path.join(ROOT_PATH, "conf", "sources.ini"))

    def run(self):
        args = TrainArguments
        start_date = None if args.is_historic() else args.get_start_date()
        end_date = None if args.is_historic() else args.get_end_date()

        train_pipeline = TrainPipeline(
            training_data_repository,
            training_data_processor,
            training_data_day_grouper,
            regressors_adder,
            training_data_week_grouper,
            training_data_month_grouper,
            models_all_groups_trainer
        )

        train_pipeline.run()


def main():
    TrainMain().run()


if __name__ == "__main__":
    main()

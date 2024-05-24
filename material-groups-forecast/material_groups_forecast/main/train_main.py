import datetime
import os

from material_groups_forecast import ROOT_PATH
from argument.train_arguments import TrainArguments

from repository.resource.bigquery.bigquery_resource_imp import BigQueryResourceImp
import os
from repository.resource.bigquery.client.client_imp import BigQueryClientImp


class TrainMain(TrainArguments):

    def __init__(self):
        super().__init__()
        #self.config.read(os.path.join(ROOT_PATH, "conf", self.args.environment + ".ini"))

    def run(self):
        pass


def main():
    args = TrainArguments
    start_date = None if args.is_historic() else args.get_start_date()
    end_date = None if args.is_historic() else args.get_end_date()


    TrainMain().run()


if __name__ == "__main__":
    main()

import datetime
import os

#from material_groups_forecast import ROOT_PATH
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
    #TrainMain().run()

    bigquery_client = BigQueryClientImp(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

    bq = BigQueryResourceImp(
            bigquery_client,
            'prueba'
        )
    #pd001-datawarehouse-dev.SAP.AI-GESTION-CARGAS
    rows = bq.read(
                    table=os.getenv('BQ_AI_TABLE'),
                    start='2024-01-01',
                    end='2024-05-01')





    #or row in rows:
    #    print(row)


if __name__ == "__main__":
    main()

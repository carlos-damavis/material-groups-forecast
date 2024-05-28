import configparser
from argparse import ArgumentParser
from datetime import datetime


class TrainArguments:
    def __init__(self):
        self.fmt = "%Y-%m-%d"

        self.config = configparser.ConfigParser()

        self.parser = ArgumentParser()
        self.parser.add_argument(
            "--forecasted_group",
            choices=["material", "budget", "budget2"],
            help="Choose Between material, budget and budget2",
            type=str
        )
        self.parser.add_argument(
            "--start_date",
            type=lambda d: datetime.strptime(d, self.fmt).date(),
            required=False,
            help="First date for training. Format yyyy-mmm-dd. If not provided first historic date will be used"
        )
        self.parser.add_argument(
            "--end_date",
            type=lambda d: datetime.strptime(d, self.fmt).date(),
            required=False,
            help="Last date for training. Format yyyy-mmm-dd. If not provided last historic date will be used"
        )

        self.args = self.parser.parse_args()

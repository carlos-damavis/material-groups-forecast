import configparser
from argparse import ArgumentParser
from datetime import datetime


class TrainArguments:
    def __init__(self):
        self.fmt = "%Y-%m-%d"

        self.config = configparser.ConfigParser()

        self.parser = ArgumentParser()
        self.parser.add_argument("--start_date", type=lambda d: datetime.strptime(d, self.fmt).date())
        self.parser.add_argument("--end_date", type=lambda d: datetime.strptime(d, self.fmt).date())

        self.args = self.parser.parse_args()

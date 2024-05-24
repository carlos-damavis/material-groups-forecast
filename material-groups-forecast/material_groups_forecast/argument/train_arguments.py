import configparser
from argparse import ArgumentParser
from datetime import datetime


class TrainArguments:
    def __init__(self):
        self.fmt = "%Y-%m-%d"

        self.config = configparser.ConfigParser()

        self.parser = ArgumentParser()
        self.parser.add_argument("--forecasted_group",
                                 choices=["material", "budget", "budget2"],
                                 help="Choose Between material, budget and budget2",
                                 type=str)
        self.parser.add_argument("--start_date",
                                 type=lambda d: datetime.strptime(d, self.fmt).date(),
                                 required=False,
                                 help="Date to process. Format yyyy-mmm-dd")
        self.parser.add_argument("--end_date",
                                 type=lambda d: datetime.strptime(d, self.fmt).date(),
                                 required=False,
                                 help="Date to process. Format yyyy-mmm-dd")
        self.parser.add_argument("--historic",
                                 type=bool,
                                 required=False,
                                 help="True or False. If true, --date will be ignored")

        self.args = self.parser.parse_args()
    def get_start_date(self):
        args = self.parser.parse_args()
        return self.__parse_date(args.start_date)

    def get_end_date(self):
        args = self.parser.parse_args()
        return self.__parse_date(args.end_date)

    def is_historic(self):
        args = self.parser.parse_args()
        return args.historic == 'true'

    @classmethod
    def __parse_date(date: str):
        pass
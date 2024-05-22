import os

from material_groups_forecast import ROOT_PATH
from material_groups_forecast.argument.train_arguments import TrainArguments


class TrainMain(TrainArguments):

    def __init__(self):
        super().__init__()
        self.config.read(os.path.join(ROOT_PATH, "conf", self.args.environment + ".ini"))

    def run(self):
        pass

def main():
    TrainMain().run()


if __name__ == "__main__":
    main()
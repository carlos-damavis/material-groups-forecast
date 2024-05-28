import pickle
from configparser import ConfigParser
from pathlib import Path
from typing import Dict

from material_groups_forecast import ROOT_PATH
from material_groups_forecast.repository.model_repository import ModelRepository


class ModelRepositoryImpl(ModelRepository):

    def __init__(self, config: ConfigParser):
        self.config = config

    def read(self, file):
        pass

    def write(self, model: Dict, level: str) -> None:
        file_name = self.config["MODELS"][level]
        Path(f"{ROOT_PATH}/models/").mkdir(parents=True, exist_ok=True)
        file_to_write = open(f"{ROOT_PATH}/models/{file_name}", "wb")
        pickle.dump(model, file_to_write)
        file_to_write.close()

import os
import pickle
import shutil
import unittest
from configparser import ConfigParser

from material_groups_forecast import ROOT_PATH
from material_groups_forecast.repository.model_repository_impl import ModelRepositoryImpl


class TestModelRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = ConfigParser()
        config.read(os.path.join(ROOT_PATH, "conf", "sources.ini"))
        cls.config = config
        cls.model_repository = ModelRepositoryImpl(config)
        cls.models_dir = f"{ROOT_PATH}/models/"

    def test_write_1(self):
        if os.path.isdir(self.models_dir):
            shutil.rmtree(self.models_dir)

        model = {"params": "test1"}

        self.model_repository.write(model, "day")

        model_written_file = open(f"{self.models_dir}{self.config['MODELS']['day']}", "rb")
        model_written = pickle.load(model_written_file)

        self.assertDictEqual(model, model_written)
        model_written_file.close()

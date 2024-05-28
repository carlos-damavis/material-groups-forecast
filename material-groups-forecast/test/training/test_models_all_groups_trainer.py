import os
import pickle
import unittest

from pandas import read_csv, ArrowDtype
from pyarrow import schema, table

from material_groups_forecast.schema.mat_loads_with_regressors_monthly_schema import \
    mat_loads_with_regressors_monthly_schema
from material_groups_forecast.schema.mat_loads_with_regressors_schema import mat_loads_with_regressors_schema
from material_groups_forecast.schema.mat_loads_with_regressors_weekly_schema import \
    mat_loads_with_regressors_weekly_schema
from material_groups_forecast.stage.training.prophet_models_all_groups_trainer_impl import \
    ProphetModelsAllGroupsTrainerImpl
from test import ASSETS_TEST_PATH


class TestModelsAllGroupsTrainer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(ASSETS_TEST_PATH, "training", "models_all_groups_trainer")
        cls.models_all_groups_trainer = ProphetModelsAllGroupsTrainerImpl()

    def test_train_1(self):
        data = read_csv(os.path.join(self.data_path, "training_data_day.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        expected_file = open(os.path.join(self.data_path, "result_day_train.pkl"), "rb")
        expected = pickle.load(expected_file)
        expected_file.close()

        result = self.models_all_groups_trainer.train(data)

        self.assertListEqual(list(result.keys()), list(expected.keys()))
        for key in result["RU"].params.keys():
            self.assertTrue((result["RU"].params[key] == expected["RU"].params[key]).all())

    def test_train_2(self):
        data = read_csv(os.path.join(self.data_path, "training_data_week.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_weekly_schema)).to_pandas(types_mapper=ArrowDtype)

        expected_file = open(os.path.join(self.data_path, "result_week_train.pkl"), "rb")
        expected = pickle.load(expected_file)
        expected_file.close()

        result = self.models_all_groups_trainer.train(data)

        self.assertListEqual(list(result.keys()), list(expected.keys()))
        for key in result["RU"].params.keys():
            self.assertTrue((result["RU"].params[key] == expected["RU"].params[key]).all())

    def test_train_3(self):
        data = read_csv(os.path.join(self.data_path, "training_data_month.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_monthly_schema)).to_pandas(types_mapper=ArrowDtype)

        expected_file = open(os.path.join(self.data_path, "result_month_train.pkl"), "rb")
        expected = pickle.load(expected_file)
        expected_file.close()

        result = self.models_all_groups_trainer.train(data)

        self.assertListEqual(list(result.keys()), list(expected.keys()))
        for key in result["RU"].params.keys():
            self.assertTrue((result["RU"].params[key] == expected["RU"].params[key]).all())

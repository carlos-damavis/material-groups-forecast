import os
import unittest
from datetime import date

from pandas import read_csv, ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import schema, table

from material_groups_forecast.schema.mat_loads_with_regressors_schema import mat_loads_with_regressors_schema
from material_groups_forecast.schema.mat_loads_with_regressors_weekly_schema import \
    mat_loads_with_regressors_weekly_schema
from material_groups_forecast.stage.training.training_data_week_grouper import TrainingDataWeekGrouperImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataWeekGrouper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_grouper")
        cls.training_data_week_grouper = TrainingDataWeekGrouperImpl()

    def test_group_1(self):
        """
        If the dates of a week are not all inside the dataframe then the first available date is used as is the case
        with the 7th week in the example
        """
        data = read_csv(os.path.join(self.data_path, "train_data_with_regressors_1.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = {
            "forecastedGroup": ["PVE", "RU", "RU", "RU"],
            "yearWeek": ["2024-w01", "2024-w01", "2024-w07", "2024-w08"],
            "fecha_entrada": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 2, 16), date(2024, 2, 19)],
            "peso_neto": [15645, 11779, 1854, 0],
            "month": [1, 1, 2, 2],
            "problematicDates": [False]*4,
            "covid": [False]*4
        }
        expected = table(
            expected,
            schema=schema(mat_loads_with_regressors_weekly_schema)
        ).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_week_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_2(self):
        data = read_csv(os.path.join(self.data_path, "train_data_with_regressors_2.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = {
            "forecastedGroup": ["PVE", "RU", "RU", "RU"],
            "yearWeek": ["2024-w01", "2024-w01", "2024-w07", "2024-w08"],
            "fecha_entrada": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 2, 16), date(2024, 2, 19)],
            "peso_neto": [15645, 11779, 1854, 0],
            "month": [1, 1, 2, 2],
            "problematicDates": [True]*2 + [False]*2,
            "covid": [True]*3 + [False]
        }
        expected = table(
            expected,
            schema=schema(mat_loads_with_regressors_weekly_schema)
        ).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_week_grouper.group(data)

        assert_frame_equal(result, expected)

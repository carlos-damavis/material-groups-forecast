import os
import unittest
from datetime import date

from pandas import read_csv, ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import schema, table

from material_groups_forecast.schema.mat_loads_with_regressors_monthly_schema import \
    mat_loads_with_regressors_monthly_schema
from material_groups_forecast.schema.mat_loads_with_regressors_schema import mat_loads_with_regressors_schema
from material_groups_forecast.stage.training.training_data_month_grouper import TrainingDataMonthGrouperImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataWeekGrouper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_grouper")
        cls.training_data_month_grouper = TrainingDataMonthGrouperImpl()

    def test_group_1(self):
        """
        If the dates of a month are not all inside the dataframe then the first available date is used as is the case
        with the february in the example. That's why the dataset passed to the function should have all dates for all
        groups with zero weight where needed
        """
        data = read_csv(os.path.join(self.data_path, "train_data_with_regressors_1.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = {
            "forecastedGroup": ["PVE", "RU", "RU"],
            "fecha_entrada": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 2, 16)],
            "peso_neto": [15645, 11779, 1854],
            "month": [1, 1, 2],
            "problematicDates": [0]*3,
            "covid": [0]*3,
            "numWeekendDays": [2, 0, 2]
        }
        expected = table(
            expected,
            schema=schema(mat_loads_with_regressors_monthly_schema)
        ).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_month_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_2(self):
        data = read_csv(os.path.join(self.data_path, "train_data_with_regressors_2.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = {
            "forecastedGroup": ["PVE", "RU", "RU"],
            "fecha_entrada": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 2, 16)],
            "peso_neto": [15645, 11779, 1854],
            "month": [1, 1, 2],
            "problematicDates": [1, 3, 0],
            "covid": [2, 1, 1],
            "numWeekendDays": [2, 0, 2]
        }
        expected = table(
            expected,
            schema=schema(mat_loads_with_regressors_monthly_schema)
        ).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_month_grouper.group(data)

        assert_frame_equal(result, expected)

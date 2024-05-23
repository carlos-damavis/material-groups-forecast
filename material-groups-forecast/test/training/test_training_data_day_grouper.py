import os
import unittest
from datetime import date

from pandas import read_csv, ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import table, schema

from material_groups_forecast.schema.processed_materials_loads_schema import processed_materials_loads_schema
from material_groups_forecast.stage.training.training_data_day_grouper_impl import TrainingDataDayGrouperImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataDayGrouper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_grouper")
        cls.training_data_grouper = TrainingDataDayGrouperImpl()

    def test_group_1(self):
        data = read_csv(os.path.join(self.data_path, "training_processed_data_1.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = table(
            {
                "forecastedGroup": ["RCD", "RECHAZO ENVASES", "RS GII", "RU", "RU"],
                "fecha_entrada": [date(2005, 3, 17), date(2005, 3, 10), date(2005, 3, 28),
                                  date(2005, 3, 12), date(2005, 3, 26)],
                "peso_neto": [4720, 1420, 660, 2680, 500]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_2(self):
        data = read_csv(os.path.join(self.data_path, "training_processed_data_2.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = table(
            {
                "forecastedGroup": ["PVE", "PVE"],
                "fecha_entrada": [date(2005, 3, 10), date(2005, 3, 26)],
                "peso_neto": [1420, 1480]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_3(self):
        data = read_csv(os.path.join(self.data_path, "training_processed_data_3.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = table(
            {
                "forecastedGroup": ["PAPEL-EETT", "RU-PVE", "VIDRIO-GENERAL"],
                "fecha_entrada": [date(2005, 3, 12), date(2005, 3, 26), date(2005, 3, 7)],
                "peso_neto": [3380, 500, 4440]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

import os
import unittest
from datetime import date

from pandas import read_csv, ArrowDtype, date_range
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
                "forecastedGroup": ["RCD"]*22 + ["RECHAZO ENVASES"]*22 + ["RS GII"]*22 + ["RU"]*22,
                "fecha_entrada": [d for d in date_range("2005-03-07", "2005-03-28")]*4,
                "peso_neto": [0]*22*4
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)
        mask = (expected.forecastedGroup == "RCD") & (expected.fecha_entrada == date(2005, 3, 17))
        expected.loc[mask, "peso_neto"] = 4720
        mask = (expected.forecastedGroup == "RECHAZO ENVASES") & (expected.fecha_entrada == date(2005, 3, 10))
        expected.loc[mask, "peso_neto"] = 1420
        mask = (expected.forecastedGroup == "RS GII") & (expected.fecha_entrada == date(2005, 3, 28))
        expected.loc[mask, "peso_neto"] = 660
        mask = (expected.forecastedGroup == "RU") & (expected.fecha_entrada == date(2005, 3, 12))
        expected.loc[mask, "peso_neto"] = 2680
        mask = (expected.forecastedGroup == "RU") & (expected.fecha_entrada == date(2005, 3, 26))
        expected.loc[mask, "peso_neto"] = 500

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_2(self):
        data = read_csv(os.path.join(self.data_path, "training_processed_data_2.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = table(
            {
                "forecastedGroup": ["PVE"]*22,
                "fecha_entrada": date_range("2005-03-07", "2005-03-28"),
                "peso_neto": [0]*3 + [1420] + [0]*15 + [1480] + [0]*2
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

    def test_group_3(self):
        data = read_csv(os.path.join(self.data_path, "training_processed_data_3.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = table(
            {
                "forecastedGroup": ["PAPEL-EETT"]*22 + ["RU-PVE"]*22 + ["VIDRIO-GENERAL"]*22,
                "fecha_entrada": [d for d in date_range("2005-03-07", "2005-03-28")]*3,
                "peso_neto": [0]*22*3
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)
        mask = (expected.forecastedGroup == "PAPEL-EETT") & (expected.fecha_entrada == date(2005, 3, 12))
        expected.loc[mask, "peso_neto"] = 3380
        mask = (expected.forecastedGroup == "RU-PVE") & (expected.fecha_entrada == date(2005, 3, 26))
        expected.loc[mask, "peso_neto"] = 500
        mask = (expected.forecastedGroup == "VIDRIO-GENERAL") & (expected.fecha_entrada == date(2005, 3, 7))
        expected.loc[mask, "peso_neto"] = 4440

        result = self.training_data_grouper.group(data)

        assert_frame_equal(result, expected)

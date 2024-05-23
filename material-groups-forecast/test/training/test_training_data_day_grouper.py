import os
import unittest

from pandas import read_csv, ArrowDtype, to_datetime
from pandas.testing import assert_frame_equal
from pyarrow import table

from material_groups_forecast.stage.common.groups_argument_mapper_impl import GroupsArgumentMapperImpl
from material_groups_forecast.stage.training.training_data_day_grouper_impl import TrainingDataDayGrouperImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataDayGrouper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_grouper")
        groups_argument_mapper = GroupsArgumentMapperImpl()
        cls.training_data_grouper_material = TrainingDataDayGrouperImpl(groups_argument_mapper, "material")
        cls.training_data_grouper_budget = TrainingDataDayGrouperImpl(groups_argument_mapper, "budget")
        cls.training_data_grouper_budget2 = TrainingDataDayGrouperImpl(groups_argument_mapper, "budget2")
        data = read_csv(os.path.join(data_path, "training_processed_data_1.csv"), dtype_backend="pyarrow")
        data.fecha_entrada = to_datetime(data.fecha_entrada)
        cls.data = data

    def test_group_1(self):

        expected = table(
            {
                "grupo": ["RCD", "RECHAZO ENVASES", "RS GII", "RU", "RU"],
                "fecha_entrada": ["2005-03-17", "2005-03-10", "2005-03-28", "2005-03-12", "2005-03-26"],
                "peso_neto": [4720, 1420, 660, 2680, 500]
            }).to_pandas(types_mapper=ArrowDtype)
        expected.fecha_entrada = to_datetime(expected.fecha_entrada)

        result = self.training_data_grouper_material.group(self.data)

        assert_frame_equal(result, expected)

    def test_group_2(self):
        expected = table(
            {
                "grupo_presupuestos": ["PVE", "PVE"],
                "fecha_entrada": ["2005-03-10", "2005-03-26"],
                "peso_neto": [1420, 1480]
            }).to_pandas(types_mapper=ArrowDtype)
        expected.fecha_entrada = to_datetime(expected.fecha_entrada)

        result = self.training_data_grouper_budget.group(self.data)

        assert_frame_equal(result, expected)

    def test_group_3(self):
        expected = table(
            {
                "grupo_presupuestos_v2": ["PAPEL-EETT", "RU-PVE", "VIDRIO-GENERAL"],
                "fecha_entrada": ["2005-03-12", "2005-03-26", "2005-03-07"],
                "peso_neto": [3380, 500, 4440]
            }).to_pandas(types_mapper=ArrowDtype)
        expected.fecha_entrada = to_datetime(expected.fecha_entrada)

        result = self.training_data_grouper_budget2.group(self.data)

        assert_frame_equal(result, expected)

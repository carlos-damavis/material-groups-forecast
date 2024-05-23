import os
import unittest

from pandas import read_csv, ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import table, schema

from material_groups_forecast.schema.materials_loads_schema import materials_loads_schema
from material_groups_forecast.schema.processed_materials_loads_schema import processed_materials_loads_schema
from material_groups_forecast.stage.common.groups_argument_mapper_impl import GroupsArgumentMapperImpl
from material_groups_forecast.stage.training.training_data_processor_impl import TrainingDataProcessorImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.groups_argument_mapper = GroupsArgumentMapperImpl()
        data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_processor")
        data = read_csv(os.path.join(data_path, "training_raw_data_1.csv"), dtype_backend="pyarrow")
        cls.data = table(data, schema=schema(materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

    def test_process_1(self):
        training_data_processor = TrainingDataProcessorImpl(self.groups_argument_mapper, "material")

        expected = self.data.loc[:, ["grupo", "fecha_entrada", "peso_neto"]].copy()
        expected.columns = ["forecastedGroup", "fecha_entrada", "peso_neto"]
        expected = table(expected, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = training_data_processor.process(self.data)

        assert_frame_equal(result, expected)

    def test_process_2(self):
        training_data_processor = TrainingDataProcessorImpl(self.groups_argument_mapper, "budget")

        expected = self.data.loc[:, ["grupo_presupuestos", "fecha_entrada", "peso_neto"]].copy()
        expected.columns = ["forecastedGroup", "fecha_entrada", "peso_neto"]
        expected = table(expected, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = training_data_processor.process(self.data)

        assert_frame_equal(result, expected)

    def test_process_3(self):
        training_data_processor = TrainingDataProcessorImpl(self.groups_argument_mapper, "budget2")

        expected = self.data.loc[:, ["grupo_presupuestos_v2", "fecha_entrada", "peso_neto"]].copy()
        expected.columns = ["forecastedGroup", "fecha_entrada", "peso_neto"]
        expected = table(expected, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        result = training_data_processor.process(self.data)

        assert_frame_equal(result, expected)

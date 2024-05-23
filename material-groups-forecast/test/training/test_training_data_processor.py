import os
import unittest

from pandas import read_csv, to_datetime, ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import table, schema

from material_groups_forecast.schema.materials_loads_schema import materials_loads_schema
from material_groups_forecast.stage.training.training_data_processor_impl import TrainingDataProcessorImpl
from test import ASSETS_TEST_PATH


class TestTrainingDataProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.training_data_processor = TrainingDataProcessorImpl()
        cls.data_path = os.path.join(ASSETS_TEST_PATH, "training", "training_data_processor")

    def test_process_1(self):
        data = read_csv(os.path.join(self.data_path, "training_raw_data_1.csv"), dtype_backend="pyarrow")
        data = table(data, schema=schema(materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)
        expected = data.copy()
        expected.fecha_entrada = to_datetime(expected.fecha_entrada)

        result = self.training_data_processor.process(data)

        assert_frame_equal(result, expected)

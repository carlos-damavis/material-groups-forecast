
import unittest
from datetime import date

from pandas import ArrowDtype
from pandas.testing import assert_frame_equal
from pyarrow import table, schema

from material_groups_forecast.schema.mat_loads_with_regressors_schema import \
    mat_loads_with_regressors_schema
from material_groups_forecast.schema.processed_materials_loads_schema import processed_materials_loads_schema
from material_groups_forecast.stage.common.regressors_adder_impl import RegressorsAdderImpl


class TestRegressorsAdder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.regressors_adder = RegressorsAdderImpl()

    def test_add_1(self):
        training_data = table(
            {
                "forecastedGroup": ["RCD", "RCD", "RU"],
                "fecha_entrada": [date(2024, 8, 19), date(2024, 10, 18), date(2024, 2, 10)],
                "peso_neto": [10, 20, 35]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = training_data.copy()
        expected["weekDay"] = [1, 5, 6]
        expected["month"] = [8, 10, 2]
        expected["problematicDates"] = [0, 0, 0]
        expected["covid"] = [0, 0, 0]
        expected = table(expected, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.regressors_adder.add(training_data)

        assert_frame_equal(result, expected)

    def test_add_2(self):
        training_data = table(
            {
                "forecastedGroup": ["PVE", "PVE", "PVE"],
                "fecha_entrada": [date(2020, 8, 19), date(2015, 10, 18), date(2021, 12, 10)],
                "peso_neto": [10, 20, 35]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = training_data.copy()
        expected["weekDay"] = [3, 7, 5]
        expected["month"] = [8, 10, 12]
        expected["problematicDates"] = [0, 0, 0]
        expected["covid"] = [1, 0, 1]
        expected = table(expected, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.regressors_adder.add(training_data)

        assert_frame_equal(result, expected)

    def test_add_3(self):
        training_data = table(
            {
                "forecastedGroup": ["RCD", "RCD", "RU"],
                "fecha_entrada": [date(2015, 8, 19), date(2015, 10, 18), date(2015, 8, 10)],
                "peso_neto": [10, 20, 35]
            }, schema=schema(processed_materials_loads_schema)).to_pandas(types_mapper=ArrowDtype)

        expected = training_data.copy()
        expected["weekDay"] = [3, 7, 1]
        expected["month"] = [8, 10, 8]
        expected["problematicDates"] = [1, 0, 1]
        expected["covid"] = [0, 0, 0]
        expected = table(expected, schema=schema(mat_loads_with_regressors_schema)).to_pandas(types_mapper=ArrowDtype)

        result = self.regressors_adder.add(training_data)

        assert_frame_equal(result, expected)

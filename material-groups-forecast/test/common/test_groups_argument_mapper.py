import unittest

from material_groups_forecast.stage.common.groups_argument_mapper_impl import GroupsArgumentMapperImpl


class TestGroupsArgumentMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.groups_argument_mapper = GroupsArgumentMapperImpl()

    def test_map_1(self):
        expected = "grupo"
        result = self.groups_argument_mapper.map("material")

        self.assertEqual(result, expected)

    def test_map_2(self):
        expected = "grupo_presupuestos"
        result = self.groups_argument_mapper.map("budget")

        self.assertEqual(result, expected)

    def test_map_3(self):
        expected = "grupo_presupuestos_v2"
        result = self.groups_argument_mapper.map("budget2")

        self.assertEqual(result, expected)

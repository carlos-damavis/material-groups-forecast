from material_groups_forecast.stage.common.groups_argument_mapper import GroupsArgumentMapper


class GroupsArgumentMapperImpl(GroupsArgumentMapper):

    def __init__(self):
        self.group_mapping = {
            "material": "grupo",
            "budget": "grupo_presupuestos",
            "budget2": "grupo_presupuestos_v2"
        }

    def map(self, group_argument: str) -> str:
        mapped_group_argument = self.group_mapping[group_argument]

        return mapped_group_argument

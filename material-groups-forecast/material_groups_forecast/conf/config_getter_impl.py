import json
import os
from typing import Any, Optional, Dict

from material_groups_forecast.conf.config_getter import ConfigGetter


class ConfigGetterImpl(ConfigGetter):

    @staticmethod
    def get(config_json_path: str) -> Dict:
        env_vars_dict = dict()

        if config_json_path:
            with open(config_json_path, 'r') as f:
                env_vars = json.load(f)

            for key, val in env_vars.items():
                if key == 'bigquery_credentials_path':
                    file = open(val)
                    env_vars_dict['bigquery_credentials'] = json.load(file)
                    continue
                env_vars_dict[key] = str(val)

        return env_vars_dict

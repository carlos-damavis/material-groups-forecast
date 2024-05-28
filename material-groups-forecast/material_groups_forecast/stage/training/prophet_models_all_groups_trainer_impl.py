from typing import Dict

import holidays
from pandas import DataFrame, date_range, Categorical
from prophet import Prophet
from pyarrow import bool_

from material_groups_forecast.stage.training.models_all_groups_trainer import ModelsAllGroupsTrainer


class ProphetModelsAllGroupsTrainerImpl(ModelsAllGroupsTrainer):

    @staticmethod
    def _turn_bool_to_categorical(data: DataFrame) -> bool_():
        variables_to_convert = [col for col in data.columns if data.dtypes[col] == "bool[pyarrow]"]
        for col in variables_to_convert:
            data[col] = Categorical(data[col])

        return data

    @staticmethod
    def _create_holidays() -> DataFrame:
        holidays_balearic_islands = holidays.Spain(subdiv='IB')
        holidays_balearic_islands = [
            (date, holidays_balearic_islands[date])
            for date in date_range("2010-01-01", "2040-01-01")
            if date in holidays_balearic_islands
        ]
        holidays_balearic_islands = DataFrame(holidays_balearic_islands, columns=["ds", "holiday"])

        return holidays_balearic_islands

    def train(self, training_data: DataFrame) -> Dict[str, Prophet]:
        all_models = dict()

        formatted_training_data = training_data.copy()
        formatted_training_data = formatted_training_data.rename(columns={"peso_neto": "y", "fecha_entrada": "ds"})
        formatted_training_data = self._turn_bool_to_categorical(formatted_training_data)

        holidays_balearic_islands = self._create_holidays()
        regressors = [col for col in formatted_training_data.columns if col not in ["forecastedGroup", "ds", "y"]]

        for group in formatted_training_data.forecastedGroup.unique():
            model = Prophet(interval_width=0.85, holidays=holidays_balearic_islands)
            for var in regressors:
                model.add_regressor(var)
            model.fit(formatted_training_data.loc[formatted_training_data.forecastedGroup == group, :])
            all_models[group] = model

        return all_models

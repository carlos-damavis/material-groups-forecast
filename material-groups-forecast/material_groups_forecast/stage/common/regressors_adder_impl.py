from datetime import date
from typing import List

from pandas import DataFrame, date_range, ArrowDtype
from pyarrow import bool_

from material_groups_forecast.stage.common.regressors_adder import RegressorsAdder


class RegressorsAdderImpl(RegressorsAdder):

    @staticmethod
    def _get_problematic_dates() -> List[date]:
        prob_dates = [d for d in date_range("2015-08-01", "2015-08-31")]

        return  prob_dates

    def add(self, data: DataFrame) -> DataFrame:
        problematic_dates = self._get_problematic_dates()
        data["weekDay"] = data.fecha_entrada.dt.isocalendar().day
        data["month"] = data.fecha_entrada.dt.month
        data["problematicDates"] = data.fecha_entrada.isin(problematic_dates).astype(ArrowDtype(bool_()))
        data["covid"] = (data.fecha_entrada.dt.year == 2020) | (data.fecha_entrada.dt.year == 2021)

        return data

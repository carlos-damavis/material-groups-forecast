from pyarrow import date32, string, int64, bool_

mat_loads_with_regressors_weekly_schema = {
    "forecastedGroup": string(),
    "yearWeek": string(),
    "fecha_entrada": date32(),
    "peso_neto": int64(),
    "month": int64(),
    "problematicDates": bool_(),
    "covid": bool_()
}
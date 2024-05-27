from pyarrow import date32, string, int64

mat_loads_with_regressors_monthly_schema = {
    "forecastedGroup": string(),
    "yearMonth": string(),
    "fecha_entrada": date32(),
    "peso_neto": int64(),
    "month": int64(),
    "problematicDates": int64(),
    "covid": int64(),
    "numWeekendDays": int64()
}

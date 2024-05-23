from pyarrow import string, int64, date32

processed_materials_loads_schema = {
    "forecastedGroup": string(),
    "fecha_entrada": date32(),
    "peso_neto": int64()
}

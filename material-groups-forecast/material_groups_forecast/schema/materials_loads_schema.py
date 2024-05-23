from pyarrow import string, int64

materials_loads_schema = {
    "grupo": string(),
    "grupo_presupuestos": string(),
    "grupo_presupuestos_v2": string(),
    "fecha_entrada": string(),
    "peso_neto": int64()
}

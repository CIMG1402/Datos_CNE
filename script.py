import requests
import pandas as pd
import time
from datetime import datetime

BASE_URL = "https://api-reportediario.cne.gob.mx/api/EstacionServicio/Petroliferos"

headers = {
    "User-Agent": "Mozilla/5.0"
}

municipios_df = pd.DataFrame({
    "ENTIDAD_ID": [
        1,2,3,4,5,6,7,8,9,10,
        11,12,13,14,15,16,17,18,19,20,
        21,22,23,24,25,26,27,28,29,30,
        31,32
    ],
    "Municipios": [
        12,8,6,14,39,11,125,68,17,40,
        47,86,85,126,126,114,37,21,52,571,
        218,19,12,60,21,73,18,44,61,213,
        107,59
    ]
})

todos_registros = []

for _, row in municipios_df.iterrows():

    entidad_id = int(row["ENTIDAD_ID"])
    total_municipios = int(row["Municipios"])

    print(f"Entidad {entidad_id}")

    for municipio_id in range(1, total_municipios + 1):

        params = {
            "entidadId": str(entidad_id),
            "municipioId": str(municipio_id)
        }

        try:
            resp = requests.get(BASE_URL, params=params, headers=headers, timeout=20)

            if resp.status_code == 200:
                data = resp.json()
                registros = data.get("Value", [])

                if registros:
                    todos_registros.extend(registros)

            time.sleep(0.25)

        except:
            pass

df = pd.DataFrame(todos_registros)

columnas = [
    "Numero",
    "Nombre",
    "Direccion",
    "Producto",
    "SubProducto",
    "PrecioVigente",
    "EntidadFederativaId",
    "MunicipioId"
]

columnas_validas = [c for c in columnas if c in df.columns]
df = df[columnas_validas]

fecha = datetime.now().strftime("%Y%m%d")

archivo = f"precios_gasolineras_mexico_{fecha}.csv"

df.to_csv(archivo, index=False, encoding="utf-8-sig")

print("Archivo creado:", archivo)

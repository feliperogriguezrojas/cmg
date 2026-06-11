import requests
from pathlib import Path
from urllib.parse import quote
import time

ANIO = 2020

MESES = {
    1: ("01_ENERO", "Enero"),
    2: ("02_FEBRERO", "Febrero"),
    3: ("03_MARZO", "Marzo"),
    4: ("04_ABRIL", "Abril"),
    5: ("05_MAYO", "Mayo"),
    6: ("06_JUNIO", "Junio"),
    7: ("07_JULIO", "Julio"),
    8: ("08_AGOSTO", "Agosto"),
    9: ("09_SETIEMBRE", "Setiembre"),
    10: ("10_OCTUBRE", "Octubre"),
    11: ("11_NOVIEMBRE", "Noviembre"),
    12: ("12_DICIEMBRE", "Diciembre")
}

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

carpeta = Path(f"CMG_{ANIO}")
carpeta.mkdir(exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

descargados = 0
fallidos = 0

for mes in range(1, 13):

    carpeta_mes, nombre_mes = MESES[mes]

    ruta = (
        f"Operación/Costos Marginales CP/Revisados/"
        f"{ANIO}/"
        f"{carpeta_mes}/"
        f"02_Reportes Costos Marginales CP/"
        f"Final/"
        f"RptCostoMarginal_{nombre_mes}.xlsx"
    )

    url = BASE_URL + quote(ruta)

    archivo = carpeta / f"{ANIO}_{mes:02d}.xlsx"

    try:

        r = session.get(url, timeout=30)

        if r.status_code == 200 and len(r.content) > 100000:

            with open(archivo, "wb") as f:
                f.write(r.content)

            descargados += 1
            print(f"[OK] {archivo.name}")

        else:

            fallidos += 1
            print(f"[NO EXISTE] {archivo.name}")

    except Exception as e:

        fallidos += 1
        print(f"[ERROR] {archivo.name} -> {e}")

    time.sleep(1)

print("\n============================")
print("PROCESO TERMINADO")
print("============================")
print(f"Descargados : {descargados}")
print(f"Fallidos    : {fallidos}")
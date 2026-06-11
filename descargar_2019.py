import requests
from pathlib import Path
from urllib.parse import quote
import time

ANIO = 2019

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

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

carpeta = Path("CMG_2019")
carpeta.mkdir(exist_ok=True)

session = requests.Session()

for mes, (carpeta_mes, nombre_mes) in MESES.items():

    ruta = (
        f"Operación/Costos Marginales CP/Revisados/"
        f"{ANIO}/"
        f"{carpeta_mes}/"
        f"II. Actualización Costos Marginales CP/"
        f"02_Reportes Costos Marginales CP/"
        f"RptCostoMarginal_{nombre_mes}.xlsx"
    )

    url = BASE_URL + quote(ruta)

    archivo = carpeta / f"{ANIO}_{mes:02d}.xlsx"

    try:

        r = session.get(url, timeout=30)

        if r.status_code == 200:

            with open(archivo, "wb") as f:
                f.write(r.content)

            print(f"[OK] {archivo.name}")

        else:

            print(
                f"[NO ENCONTRADO] "
                f"{archivo.name} "
                f"({r.status_code})"
            )

    except Exception as e:

        print(
            f"[ERROR] "
            f"{archivo.name}: {e}"
        )

    time.sleep(1)

print("Proceso terminado")
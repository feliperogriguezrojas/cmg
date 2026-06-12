import requests
from pathlib import Path
from urllib.parse import quote
import time

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

ANIOS = range(2022, 2026)

session = requests.Session()

for anio in ANIOS:

    carpeta_anio = Path(f"CMG_{anio}")
    carpeta_anio.mkdir(exist_ok=True)

    print(f"\n===== {anio} =====")

    for mes in range(1, 13):

        carpeta_mes, nombre_mes = MESES[mes]

        ruta = (
            f"Operación/Costos Marginales CP/Revisados/"
            f"{anio}/"
            f"{carpeta_mes}/"
            f"02_Reportes Costos Marginales CP/"
            f"Final/"
            f"RptCostoMarginal_{nombre_mes}.xlsx"
        )

        url = BASE_URL + quote(ruta)

        archivo = carpeta_anio / f"{anio}_{mes:02d}.xlsx"

        try:

            r = session.get(url, timeout=30)

            if r.status_code == 200:

                with open(archivo, "wb") as f:
                    f.write(r.content)

                print(f"[OK] {archivo.name}")

            else:

                print(
                    f"[NO EXISTE] "
                    f"{archivo.name}"
                )

        except Exception as e:

            print(
                f"[ERROR] "
                f"{archivo.name}: {e}"
            )

        time.sleep(1)

print("\nProceso terminado")
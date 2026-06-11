import requests
from pathlib import Path
from urllib.parse import quote
import calendar
import time

# ======================================
# CONFIGURACIÓN
# ======================================

ANIO = 2018
PAUSA = 1  # segundos entre descargas

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

MESES = {
    1: "01_ENERO",
    2: "02_FEBRERO",
    3: "03_MARZO",
    4: "04_ABRIL",
    5: "05_MAYO",
    6: "06_JUNIO",
    7: "07_JULIO",
    8: "08_AGOSTO",
    9: "09_SETIEMBRE",
    10: "10_OCTUBRE",
    11: "11_NOVIEMBRE",
    12: "12_DICIEMBRE"
}

# ======================================
# CARPETA DESTINO
# ======================================

base_dir = Path(f"CMG_{ANIO}")
base_dir.mkdir(exist_ok=True)

# ======================================
# SESIÓN
# ======================================

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# ======================================
# DESCARGA
# ======================================

descargados = 0
fallidos = 0

for mes in range(1, 13):

    carpeta_mes = base_dir / f"{ANIO}_{mes:02d}"
    carpeta_mes.mkdir(exist_ok=True)

    dias_mes = calendar.monthrange(ANIO, mes)[1]

    print(f"\n========== {MESES[mes]} ==========")

    for dia in range(1, dias_mes + 1):

        dd = f"{dia:02d}"
        mm = f"{mes:02d}"

        nombre_salida = f"{ANIO}_{mm}_{dd}.xlsx"

        archivo_destino = carpeta_mes / nombre_salida

        if archivo_destino.exists():
            print(f"[YA EXISTE] {nombre_salida}")
            continue

        ruta = (
            f"Operación/Costos Marginales CP/Revisados/"
            f"{ANIO}/"
            f"{MESES[mes]}/"
            f"Día {dd}/"
            f"CMgCP_Revisión_01/"
            f"CMgCP_{dd}{mm}.xlsx"
        )

        url = BASE_URL + quote(ruta)

        try:

            r = session.get(url, timeout=30)

            if r.status_code == 200:

                with open(archivo_destino, "wb") as f:
                    f.write(r.content)

                descargados += 1

                print(f"[OK] {nombre_salida}")

            else:

                fallidos += 1

                print(
                    f"[NO ENCONTRADO] "
                    f"{nombre_salida} "
                    f"({r.status_code})"
                )

        except Exception as e:

            fallidos += 1

            print(
                f"[ERROR] "
                f"{nombre_salida}: {e}"
            )

        time.sleep(PAUSA)

# ======================================
# RESUMEN
# ======================================

print("\n============================")
print("PROCESO TERMINADO")
print("============================")
print(f"Descargados : {descargados}")
print(f"Fallidos    : {fallidos}")
import requests
from pathlib import Path
from urllib.parse import quote
import calendar
import time

# ======================================
# CONFIGURACIÓN
# ======================================

ANIO = 2018
PAUSA = 1

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

# ======================================
# PLANTILLAS VERIFICADAS
# ======================================

PLANTILLAS = {

    # ENERO
    "01":
    "Operación/Costos Marginales CP/Revisados/2018/"
    "01_ENERO/"
    "Día {dia}/"
    "CMgCP_Revisión_01/"
    "CMgCP_{dia}{mes}.xlsx",

    # FEBRERO
    "02":
    "Operación/Costos Marginales CP/Revisados/2018/"
    "02_FEBRERO/"
    "01_Resultados Costos Marginales CP/"
    "Día {dia}/"
    "CMgCP_Revisión_02/"
    "CMgCP_{dia}{mes}.xlsx",

    # MARZO
    # MARZO
    "03":
    "Operación/Costos Marginales CP/Revisados/2018/"
    "03_MARZO/"
    "01_Resultados Costos Marginales CP/"
    "CMgCP_IEOD/"
    "Día {dia}/"
    "CMgCP_{dia}{mes}.xlsx",

    # ABRIL
    # "04": "",

    # MAYO
    # "05": "",

    # JUNIO
    # "06": "",

    # JULIO
    # "07": "",

    # AGOSTO
    # "08": "",

    # SETIEMBRE
    # "09": "",

    # OCTUBRE
    # "10": "",

    # NOVIEMBRE
    # "11": "",

    # DICIEMBRE
    # "12": "",
}

# ======================================
# SESIÓN
# ======================================

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# ======================================
# CARPETA DESTINO
# ======================================

base_dir = Path(f"CMG_{ANIO}")
base_dir.mkdir(exist_ok=True)

# ======================================
# CONTADORES
# ======================================

descargados = 0
existentes = 0
vacios = 0
errores = 0

# ======================================
# DESCARGA
# ======================================

for mes in sorted(PLANTILLAS.keys()):

    carpeta_mes = base_dir / f"{ANIO}_{mes}"
    carpeta_mes.mkdir(exist_ok=True)

    dias_mes = calendar.monthrange(
        ANIO,
        int(mes)
    )[1]

    print("\n" + "=" * 70)
    print(f"PROCESANDO MES {mes}")
    print("=" * 70)

    for dia in range(1, dias_mes + 1):

        dd = f"{dia:02d}"

        nombre_archivo = f"{ANIO}_{mes}_{dd}.xlsx"

        archivo_destino = (
            carpeta_mes / nombre_archivo
        )

        # ----------------------------------
        # SI YA EXISTE Y TIENE DATOS
        # ----------------------------------

        if (
            archivo_destino.exists()
            and archivo_destino.stat().st_size > 5000
        ):

            existentes += 1

            print(
                f"[YA EXISTE] "
                f"{nombre_archivo}"
            )

            continue

        # ----------------------------------
        # CONSTRUIR URL
        # ----------------------------------

        ruta = PLANTILLAS[mes].format(
            dia=dd,
            mes=mes
        )

        url = BASE_URL + quote(ruta)

        try:

            r = session.get(
                url,
                timeout=30
            )

            tamaño = len(r.content)

            print(
                f"{nombre_archivo} "
                f"-> {tamaño:,} bytes"
            )

            if (
                r.status_code == 200
                and tamaño > 5000
            ):

                with open(
                    archivo_destino,
                    "wb"
                ) as f:

                    f.write(r.content)

                descargados += 1

                print("   ✓ OK")

            else:

                vacios += 1

                print(
                    "   ✗ Archivo vacío"
                )

        except Exception as e:

            errores += 1

            print(
                f"   ✗ ERROR: {e}"
            )

        time.sleep(PAUSA)

# ======================================
# RESUMEN
# ======================================

print("\n" + "=" * 70)
print("PROCESO TERMINADO")
print("=" * 70)

print(f"Descargados : {descargados}")
print(f"Existentes  : {existentes}")
print(f"Vacíos      : {vacios}")
print(f"Errores     : {errores}")
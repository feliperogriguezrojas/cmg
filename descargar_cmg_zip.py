import requests
from pathlib import Path
from urllib.parse import quote
import calendar
import zipfile
import io
import time

# ======================================
# CONFIGURACIÓN
# ======================================

ANIO = 2018
PAUSA = 1

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

MESES = {
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
vacios = 0
errores = 0

# ======================================
# DESCARGA
# ======================================

for mes_num, mes_nombre in MESES.items():

    mm = f"{mes_num:02d}"

    carpeta_mes = base_dir / f"{ANIO}_{mm}"

    carpeta_mes.mkdir(exist_ok=True)

    dias_mes = calendar.monthrange(
        ANIO,
        mes_num
    )[1]

    print("\n" + "=" * 70)
    print(f"PROCESANDO {mes_nombre}")
    print("=" * 70)

    for dia in range(1, dias_mes + 1):

        dd = f"{dia:02d}"

        excel_destino = (
            carpeta_mes /
            f"{ANIO}_{mm}_{dd}.xlsx"
        )

        # Ya existe

        if (
            excel_destino.exists()
            and excel_destino.stat().st_size > 5000
        ):

            print(
                f"[YA EXISTE] "
                f"{excel_destino.name}"
            )

            continue

        ruta = (
            f"Post Operación/Reportes/IEOD/"
            f"{ANIO}/"
            f"{mes_nombre}/"
            f"Día {dd}/"
            f"Anexo6_CMgCP_{dd}{mm}.zip"
        )

        url = BASE_URL + quote(ruta)

        try:

            r = session.get(
                url,
                timeout=60
            )

            tamaño = len(r.content)

            print(
                f"{dd}/{mm} "
                f"-> {tamaño:,} bytes"
            )

            if (
                r.status_code != 200
                or tamaño < 1000
            ):

                vacios += 1

                print(
                    "   ✗ ZIP no encontrado"
                )

                continue

            # ==================================
            # LEER ZIP EN MEMORIA
            # ==================================

            zip_memoria = io.BytesIO(
                r.content
            )

            with zipfile.ZipFile(
                zip_memoria
            ) as z:

                archivos = z.namelist()

                excel_zip = None

                for nombre in archivos:

                    if (
                        nombre.lower()
                        .endswith(
                            (
                                ".xlsx",
                                ".xls"
                            )
                        )
                    ):

                        excel_zip = nombre

                        break

                if excel_zip is None:

                    vacios += 1

                    print(
                        "   ✗ No se encontró Excel"
                    )

                    continue

                with z.open(
                    excel_zip
                ) as origen:

                    with open(
                        excel_destino,
                        "wb"
                    ) as destino:

                        destino.write(
                            origen.read()
                        )

                descargados += 1

                print(
                    f"   ✓ Extraído "
                    f"{excel_zip}"
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
print(f"Vacíos      : {vacios}")
print(f"Errores     : {errores}")
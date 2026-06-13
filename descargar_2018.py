import requests
import zipfile
import io
from pathlib import Path
from datetime import datetime, timedelta

# =====================================================
# CONFIGURACION
# =====================================================

ANIO = 2018

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

BASE_URL = "https://www.coes.org.pe/Portal/browser/download?url="

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CARPETA_DESTINO = Path(f"CMG_{ANIO}")
CARPETA_DESTINO.mkdir(exist_ok=True)

# =====================================================
# FECHAS
# =====================================================

inicio = datetime(ANIO, 1, 1)
fin = datetime(ANIO, 12, 31)

fecha = inicio

# =====================================================
# CONTADORES
# =====================================================

existentes = 0
descargados = 0
redescargados = 0

faltantes = []

# =====================================================
# PROCESO
# =====================================================

while fecha <= fin:

    dia = fecha.day
    mes = fecha.month

    nombre_excel = (
        f"CMgCP_{ANIO}_{mes:02d}_{dia:02d}.xlsx"
    )

    destino_excel = CARPETA_DESTINO / nombre_excel

    fecha_txt = fecha.strftime("%Y-%m-%d")

    # =================================================
    # SI YA EXISTE Y TIENE DATOS
    # =================================================

    if destino_excel.exists():

        tamaño = destino_excel.stat().st_size

        if tamaño > 0:

            existentes += 1

            print(
                f"{fecha_txt} -> EXISTE "
                f"({tamaño:,} bytes)"
            )

            fecha += timedelta(days=1)
            continue

        else:

            print(
                f"{fecha_txt} -> "
                f"0 bytes, redescargando"
            )

            redescargados += 1

    else:

        print(f"{fecha_txt} -> Descargando")

    # =================================================
    # URL DEL ZIP
    # =================================================

    ruta_zip = (
        f"Post Operación/Reportes/IEOD/"
        f"{ANIO}/"
        f"{MESES[mes]}/"
        f"Día {dia:02d}/"
        f"Anexo6_CMgCP_{dia:02d}{mes:02d}.zip"
    )

    url = BASE_URL + requests.utils.quote(ruta_zip)

    try:

        respuesta = requests.get(
            url,
            headers=HEADERS,
            timeout=90
        )

        if respuesta.status_code != 200:

            print(
                f"   ✗ HTTP {respuesta.status_code}"
            )

            faltantes.append(fecha_txt)

            fecha += timedelta(days=1)
            continue

        if len(respuesta.content) == 0:

            print("   ✗ ZIP vacío")

            faltantes.append(fecha_txt)

            fecha += timedelta(days=1)
            continue

        # =============================================
        # ABRIR ZIP
        # =============================================

        try:

            with zipfile.ZipFile(
                io.BytesIO(respuesta.content)
            ) as z:

                excels = [
                    x for x in z.namelist()
                    if x.lower().endswith(".xlsx")
                    or x.lower().endswith(".xls")
                ]

                if len(excels) == 0:

                    print(
                        "   ✗ No hay Excel dentro del ZIP"
                    )

                    faltantes.append(fecha_txt)

                    fecha += timedelta(days=1)
                    continue

                excel_zip = excels[0]

                with z.open(excel_zip) as origen:

                    contenido = origen.read()

                if len(contenido) == 0:

                    print(
                        "   ✗ Excel extraído vacío"
                    )

                    faltantes.append(fecha_txt)

                    fecha += timedelta(days=1)
                    continue

                with open(
                    destino_excel,
                    "wb"
                ) as salida:

                    salida.write(contenido)

                tamaño_final = destino_excel.stat().st_size

                if tamaño_final == 0:

                    print(
                        "   ✗ Excel guardado vacío"
                    )

                    faltantes.append(fecha_txt)

                else:

                    descargados += 1

                    print(
                        f"   ✓ {nombre_excel} "
                        f"({tamaño_final:,} bytes)"
                    )

        except zipfile.BadZipFile:

            print("   ✗ ZIP inválido")

            faltantes.append(fecha_txt)

    except Exception as e:

        print(f"   ✗ {e}")

        faltantes.append(fecha_txt)

    fecha += timedelta(days=1)

# =====================================================
# RESUMEN
# =====================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

print(f"Existentes     : {existentes}")
print(f"Descargados    : {descargados}")
print(f"Redescargados  : {redescargados}")
print(f"Faltantes      : {len(faltantes)}")

# =====================================================
# GUARDAR FALTANTES
# =====================================================

archivo_faltantes = f"faltantes_{ANIO}.txt"

with open(
    archivo_faltantes,
    "w",
    encoding="utf-8"
) as f:

    for dia in faltantes:
        f.write(dia + "\n")

print("\nArchivo generado:")
print(archivo_faltantes)

if faltantes:

    print("\nDIAS NO DESCARGADOS:")

    for dia in faltantes:
        print(dia)
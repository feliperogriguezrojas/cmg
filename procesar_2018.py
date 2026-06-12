from pathlib import Path
import pandas as pd
import numpy as np

# =====================================================
# CONFIGURACION
# =====================================================

CARPETA_BASE = Path("CMG_2018")
BARRA_OBJETIVO = "CHILCA500"

resultados = []

# =====================================================
# RECORRER MESES
# =====================================================

for carpeta_mes in sorted(CARPETA_BASE.iterdir()):

    if not carpeta_mes.is_dir():
        continue

    print("\n" + "=" * 70)
    print(f"PROCESANDO MES: {carpeta_mes.name}")
    print("=" * 70)

    archivos_excel = sorted(carpeta_mes.glob("*.xlsx"))

    print(f"Archivos encontrados: {len(archivos_excel)}")

    valores_mes = []

    for i, archivo in enumerate(archivos_excel, start=1):

        print(f"\n[{i}/{len(archivos_excel)}]")
        print(f"Archivo: {archivo.name}")
        print(f"Ruta: {archivo}")

        try:

            # ==========================================
            # LEER EXCEL
            # ==========================================

            df = pd.read_excel(
                archivo,
                sheet_name="Cmg_Barra",
                header=None,
                engine="openpyxl"
            )

            print("✓ Excel leído correctamente")

            # ==========================================
            # BUSCAR BARRA
            # ==========================================

            encabezados = (
                df.iloc[2]
                .astype(str)
                .str.strip()
            )

            if BARRA_OBJETIVO not in encabezados.values:

                print(
                    f"✗ No se encontró "
                    f"{BARRA_OBJETIVO}"
                )

                continue

            col_chilca = encabezados[
                encabezados == BARRA_OBJETIVO
            ].index[0]

            print(
                f"✓ Columna encontrada: "
                f"{col_chilca}"
            )

            # ==========================================
            # EXTRAER DATOS
            # ==========================================

            serie = pd.to_numeric(
                df.iloc[3:, col_chilca],
                errors="coerce"
            ).dropna()

            print(
                f"✓ Registros válidos: "
                f"{len(serie)}"
            )

            valores_mes.extend(
                serie.tolist()
            )

        except Exception as e:

            print(
                f"✗ ERROR EN "
                f"{archivo.name}"
            )

            print(type(e).__name__)
            print(str(e))

    # =================================================
    # PROMEDIO MENSUAL
    # =================================================

    if len(valores_mes) == 0:

        print(
            f"\n⚠ No se encontraron datos "
            f"para {carpeta_mes.name}"
        )

        continue

    promedio_mes = np.mean(valores_mes)

    anio = int(
        carpeta_mes.name.split("_")[0]
    )

    mes = int(
        carpeta_mes.name.split("_")[1]
    )

    resultados.append({
        "Año": anio,
        "Mes": mes,
        "CMg_Promedio_CHILCA500":
            round(promedio_mes, 4)
    })

    print(
        f"\n📊 Promedio mensual "
        f"{anio}-{mes:02d}: "
        f"{promedio_mes:.4f}"
    )

# =====================================================
# EXPORTAR
# =====================================================

resultado = pd.DataFrame(resultados)

if len(resultado) > 0:

    resultado = resultado.sort_values(
        ["Año", "Mes"]
    )

    nombre_salida = (
        "CMG_2018_Mensual_CHILCA500.xlsx"
    )

    resultado.to_excel(
        nombre_salida,
        index=False
    )

    print("\n" + "=" * 70)
    print("PROCESO TERMINADO")
    print("=" * 70)

    print(resultado)

    print(
        f"\nArchivo generado: "
        f"{nombre_salida}"
    )

else:

    print(
        "\n❌ No se generó ningún resultado."
    )
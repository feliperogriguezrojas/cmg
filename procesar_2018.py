from pathlib import Path
import pandas as pd
import numpy as np

# ============================
# CONFIGURACION
# ============================

CARPETA_BASE = Path("CMG_2018")
BARRA_OBJETIVO = "CHILCA500"

resultados = []

# ============================
# RECORRER MESES
# ============================

for carpeta_mes in sorted(CARPETA_BASE.iterdir()):

    if not carpeta_mes.is_dir():
        continue

    print(f"\nProcesando {carpeta_mes.name}")

    valores_mes = []

    for archivo in sorted(carpeta_mes.glob("*.xlsx")):

        try:

            df = pd.read_excel(
                archivo,
                sheet_name="Cmg_Barra",
                header=None
            )

            # fila donde estan los nombres de barras
            encabezados = df.iloc[2].astype(str).str.strip()

            if BARRA_OBJETIVO not in encabezados.values:
                print(f"No se encontró {BARRA_OBJETIVO} en {archivo.name}")
                continue

            col_chilca = encabezados[encabezados == BARRA_OBJETIVO].index[0]

            # datos horarios
            serie = pd.to_numeric(
                df.iloc[3:, col_chilca],
                errors="coerce"
            )

            serie = serie.dropna()

            valores_mes.extend(serie.tolist())

        except Exception as e:
            print(f"Error en {archivo.name}: {e}")

    if len(valores_mes) == 0:
        continue

    promedio_mes = np.mean(valores_mes)

    anio = int(carpeta_mes.name.split("_")[0])
    mes = int(carpeta_mes.name.split("_")[1])

    resultados.append({
        "Año": anio,
        "Mes": mes,
        "CMg_Promedio_CHILCA500": round(promedio_mes, 4)
    })

# ============================
# EXPORTAR
# ============================

resultado = pd.DataFrame(resultados)

resultado = resultado.sort_values(
    ["Año", "Mes"]
)

resultado.to_excel(
    "CMG_2018_Mensual_CHILCA500.xlsx",
    index=False
)

print("\nProceso terminado")
print(resultado)
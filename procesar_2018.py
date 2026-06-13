from pathlib import Path
from datetime import datetime, timedelta

CARPETA = Path("CMG_2018")

fechas_existentes = set()

for archivo in CARPETA.rglob("*.xlsx"):

    # Ignorar archivos vacíos
    if archivo.stat().st_size == 0:
        continue

    try:
        # Ajustar según el nombre real de tus archivos
        fecha = datetime.strptime(archivo.stem, "%Y_%m_%d").date()
        fechas_existentes.add(fecha)

    except:
        pass

inicio = datetime(2018, 1, 1).date()
fin = datetime(2018, 12, 31).date()

faltantes = []

fecha = inicio

while fecha <= fin:

    if fecha not in fechas_existentes:
        faltantes.append(fecha)

    fecha += timedelta(days=1)

print("\nDIAS FALTANTES")
print("=" * 60)

for f in faltantes:
    print(f)

print(f"\nTotal faltantes: {len(faltantes)}")
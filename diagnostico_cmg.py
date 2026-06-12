from pathlib import Path
import zipfile

CARPETA_BASE = Path("CMG_2018")

for carpeta_mes in sorted(CARPETA_BASE.iterdir()):

    if not carpeta_mes.is_dir():
        continue

    print("\n" + "="*60)
    print(f"MES: {carpeta_mes.name}")
    print("="*60)

    archivos = sorted(carpeta_mes.glob("*.xlsx"))

    for archivo in archivos[:3]:  # solo los 3 primeros para no inundar la pantalla

        print(f"\nArchivo: {archivo.name}")

        # Tamaño
        print(f"Tamaño: {archivo.stat().st_size:,} bytes")

        # ¿Es realmente un XLSX?
        try:
            with zipfile.ZipFile(archivo, 'r'):
                print("✓ XLSX válido (ZIP)")
        except Exception:
            print("✗ NO es XLSX válido")

        # Mostrar primeras líneas
        try:
            with open(archivo, "rb") as f:
                cabecera = f.read(50)

            print("Cabecera:", cabecera)

        except Exception as e:
            print("Error leyendo cabecera:", e)
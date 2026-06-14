import requests

url = "https://www.coes.org.pe/Portal/browser/download?url=Operaci%C3%B3n/Costos%20Marginales%20CP/Revisados/2018/02_FEBRERO/01_Resultados%20Costos%20Marginales%20CP/D%C3%ADa%2009/CMgCP_IEOD/CMgCP_0902.xlsx"

archivo_salida = "CMG_2018/CMgCP_2018_02_09.xlsx"

r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=60
)

print("HTTP:", r.status_code)
print("Bytes:", len(r.content))

if r.status_code == 200 and len(r.content) > 1000:

    with open(archivo_salida, "wb") as f:
        f.write(r.content)

    print("✓ Descargado:", archivo_salida)

else:

    print("✗ Error en descarga")
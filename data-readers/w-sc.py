import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urlSat = "https://portal.sat.gob.gt/portal/alza-e-importacion-vehiculos/#1510763502681-dff4b62b-fd76"
baseUrl = "https://portal.sat.gob.gt"
rutaSalida = "./datos/enlaces-importacion-2024_2025.txt"

def obtenerImportacionesZips(url):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    patronZip = re.compile(r"\.zip$", re.I)
    patronImportacion = re.compile(r"/importacion-de-vehiculos/", re.I)

    enlaces = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if (
            patronZip.search(href)
            and ("2024" in href or "2025" in href)
            and patronImportacion.search(href)
        ):
            enlaces.add(urljoin(baseUrl, href))

    return sorted(enlaces)

def guardarEnlacesImportacion(forzar=False):
    if os.path.exists(rutaSalida) and not forzar:
        respuesta = input(f"El archivo '{rutaSalida}' ya existe. ¿Deseas rehacer el proceso? (s/n): ").strip().lower()
        if respuesta != "s":
            print("Proceso cancelado.")
            return

    print("Obteniendo enlaces...")
    enlaces = obtenerImportacionesZips(urlSat)

    os.makedirs(os.path.dirname(rutaSalida), exist_ok=True)

    with open(rutaSalida, "w", encoding="utf-8") as f:
        f.write("\n".join(enlaces))

    print(f"{len(enlaces)} enlaces guardados en {rutaSalida}")

if __name__ == "__main__":
    guardarEnlacesImportacion(forzar=False)

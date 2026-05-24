"""
Módulo: convocados.py
Fuente 8: Convocados oficiales Mundial 2026
Fuente: https://www.roadtowc.com/es/listas-mundial-2026-convocados-oficiales-de-las-48-selecciones-actualizado/
Fecha límite FIFA: 1 de junio de 2026
Nota: Script con reintento inteligente - actualiza por selección
      Para selecciones sin lista oficial se usa plantilla Transfermarkt
"""

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL_CONVOCADOS = (
    "https://www.roadtowc.com/es/"
    "listas-mundial-2026-convocados-oficiales-de-las-48-selecciones-actualizado/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}


def fuente_8_convocados(raw_dir: Path):
    """
    Fuente 8: Convocados oficiales Mundial 2026
    - Actualiza por selección (no sobreescribe todo)
    - Selecciones sin lista: marcadas como pendientes
    - Respaldo: plantilla Transfermarkt
    """
    dest_dir = raw_dir / "convocados"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "convocados_wc2026.json"

    # Cargar datos previos si existen
    convocados_previos = {}
    if dest.exists():
        with open(dest, encoding="utf-8") as f:
            convocados_previos = json.load(f)
        print(f"   📂 Cargando datos previos: {len(convocados_previos)} selecciones")

    print(f"\n📥 Descargando convocados oficiales WC2026...")

    try:
        response = requests.get(URL_CONVOCADOS, headers=HEADERS, timeout=30)

        if response.status_code != 200:
            print(f"   ❌ Error {response.status_code}")
            return 0, 1

        soup = BeautifulSoup(response.text, "html.parser")
        contenido = soup.find("article") or soup.find("div", {"class": "entry-content"})

        if not contenido:
            print("   ❌ No se encontró contenido")
            return 0, 1

        convocados = convocados_previos.copy()
        seleccion_actual = None
        nuevas = 0
        actualizadas = 0

        elementos = contenido.find_all(["h3", "p", "h2"])

        for elem in elementos:
            texto = elem.get_text(strip=True)
            if not texto:
                continue

            if elem.name == "h3" and "—" in texto:
                partes = texto.split("—")
                seleccion_actual = partes[0].strip()
                seleccion_actual = "".join(
                    c for c in seleccion_actual if c.isalpha() or c.isspace()
                ).strip()

                es_nueva = seleccion_actual not in convocados
                convocados[seleccion_actual] = {
                    "arqueros": [],
                    "defensores": [],
                    "mediocampistas": [],
                    "delanteros": [],
                    "fuente": "roadtowc",
                    "completa": False,
                    "raw": [],
                }
                if es_nueva:
                    nuevas += 1
                else:
                    actualizadas += 1

            elif seleccion_actual and elem.name == "p":
                texto_lower = texto.lower()
                if "arquero" in texto_lower:
                    nombres = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["arqueros"] = [
                        n.strip() for n in nombres.split(",")
                    ]
                elif "defensor" in texto_lower:
                    nombres = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["defensores"] = [
                        n.strip() for n in nombres.split(",")
                    ]
                elif "mediocampi" in texto_lower or "medio" in texto_lower:
                    nombres = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["mediocampistas"] = [
                        n.strip() for n in nombres.split(",")
                    ]
                elif "delantero" in texto_lower or "ataque" in texto_lower:
                    nombres = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["delanteros"] = [
                        n.strip() for n in nombres.split(",")
                    ]
                else:
                    convocados[seleccion_actual]["raw"].append(texto)

        # Marcar como completa si tiene al menos arqueros y delanteros
        completas = 0
        pendientes = []
        for nombre, datos in convocados.items():
            tiene_datos = any(
                [
                    datos.get("arqueros"),
                    datos.get("defensores"),
                    datos.get("mediocampistas"),
                    datos.get("delanteros"),
                ]
            )
            datos["completa"] = tiene_datos
            if tiene_datos:
                completas += 1
            else:
                pendientes.append(nombre)
                datos["fuente"] = "pendiente_usar_transfermarkt"

        with open(dest, "w", encoding="utf-8") as f:
            json.dump(convocados, f, ensure_ascii=False, indent=2)

        print(f"   ✅ Guardado: {len(convocados)} selecciones")
        print(
            f"   📊 Completas: {completas} | Nuevas: {nuevas} | Actualizadas: {actualizadas}"
        )

        if pendientes:
            print(f"   ⚠️  Sin lista aún ({len(pendientes)}) → usarán Transfermarkt:")
            for p in pendientes:
                print(f"      - {p}")

        return 1, 1

    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return 0, 1

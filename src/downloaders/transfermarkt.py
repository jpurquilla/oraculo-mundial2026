"""
Módulo: transfermarkt.py
Fuente 7: Transfermarkt - Valor de mercado de plantillas
48 selecciones oficiales del Mundial 2026
IDs extraídos directamente de:
https://www.transfermarkt.com/weltmeisterschaft/startseite/pokalwettbewerb/FIWC
"""

import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# 48 selecciones oficiales Mundial 2026 - IDs 100% verificados desde Transfermarkt
SELECCIONES_WC2026 = {
    "algerien": (3614, "Algeria"),
    "argentinien": (3437, "Argentina"),
    "australien": (3433, "Australia"),
    "osterreich": (3383, "Austria"),
    "belgien": (3382, "Belgium"),
    "bosnien-herzegowina": (3446, "Bosnia-Herzegovina"),
    "brasilien": (3439, "Brazil"),
    "kanada": (3510, "Canada"),
    "kap-verde": (4311, "Cape Verde"),
    "kolumbien": (3816, "Colombia"),
    "kroatien": (3556, "Croatia"),
    "curacao": (32364, "Curaçao"),
    "tschechien": (3445, "Czechia"),
    "demokratische-republik-kongo": (3854, "DR Congo"),
    "ecuador": (5750, "Ecuador"),
    "agypten": (3672, "Egypt"),
    "england": (3299, "England"),
    "frankreich": (3377, "France"),
    "deutschland": (3262, "Germany"),
    "ghana": (3441, "Ghana"),
    "haiti": (14161, "Haiti"),
    "iran": (3582, "Iran"),
    "irak": (3560, "Iraq"),
    "elfenbeinkuste": (3591, "Ivory Coast"),
    "japan": (3435, "Japan"),
    "jordanien": (15737, "Jordan"),
    "mexiko": (6303, "Mexico"),
    "marokko": (3575, "Morocco"),
    "niederlande": (3379, "Netherlands"),
    "neuseeland": (9171, "New Zealand"),
    "norwegen": (3440, "Norway"),
    "panama": (3577, "Panama"),
    "paraguay": (3581, "Paraguay"),
    "portugal": (3300, "Portugal"),
    "katar": (14162, "Qatar"),
    "saudi-arabien": (3807, "Saudi Arabia"),
    "schottland": (3380, "Scotland"),
    "senegal": (3499, "Senegal"),
    "sudafrika": (3806, "South Africa"),
    "sudkorea": (3589, "South Korea"),
    "spanien": (3375, "Spain"),
    "schweden": (3557, "Sweden"),
    "schweiz": (3384, "Switzerland"),
    "tunesien": (3670, "Tunisia"),
    "turkei": (3381, "Turkiye"),
    "vereinigte-staaten": (3505, "United States"),
    "uruguay": (3449, "Uruguay"),
    "usbekistan": (3563, "Uzbekistan"),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def parsear_valor(valor_str: str) -> float:
    """Convierte '€25.00m' o '€500k' a float en euros."""
    if not valor_str or valor_str == "-":
        return 0.0
    v = valor_str.replace("€", "").replace(",", ".")
    if "m" in v:
        return float(v.replace("m", "")) * 1_000_000
    elif "k" in v:
        return float(v.replace("k", "")) * 1_000
    return 0.0


def fuente_7_transfermarkt(raw_dir: Path):
    """
    Fuente 7: Transfermarkt - Valor de mercado de plantillas
    Extrae jugadores y valores de mercado de las 48 selecciones oficiales
    """
    dest_dir = raw_dir / "transfermarkt"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "squad_values.json"

    if dest.exists():
        print(f"   ⚠️  squad_values.json ya existe, omitiendo.")
        return 1, 1

    todos = {}
    ok = 0
    total = len(SELECCIONES_WC2026)

    print(f"\n📥 Scraping Transfermarkt para {total} selecciones oficiales WC2026...")

    for slug, (tm_id, nombre_oficial) in SELECCIONES_WC2026.items():
        url = (
            f"https://www.transfermarkt.com/{slug}"
            f"/kader/verein/{tm_id}/saison_id/2025/plus/1"
        )
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                tabla = soup.find("table", {"class": "items"})

                jugadores = []
                valor_total = 0.0

                if tabla:
                    filas = tabla.find_all("tr", {"class": ["odd", "even"]})
                    for fila in filas:
                        nombre_td = fila.find("td", {"class": "hauptlink"})
                        valor_td = fila.find("td", {"class": "rechts hauptlink"})

                        if nombre_td and valor_td:
                            valor_num = parsear_valor(valor_td.text.strip())
                            valor_total += valor_num
                            jugadores.append(
                                {
                                    "nombre": nombre_td.text.strip(),
                                    "valor": valor_num,
                                    "valor_str": valor_td.text.strip(),
                                }
                            )

                todos[nombre_oficial] = {
                    "jugadores": jugadores,
                    "valor_total": valor_total,
                    "valor_total_str": f"€{valor_total/1_000_000:.1f}m",
                    "num_jugadores": len(jugadores),
                }
                ok += 1
                print(
                    f"\r   {ok}/{total} {nombre_oficial}: "
                    f"{len(jugadores)} jugadores | "
                    f"€{valor_total/1_000_000:.1f}m",
                    end="",
                    flush=True,
                )

            elif response.status_code == 429:
                print(f"\n   ⚠️  Rate limit en {nombre_oficial}, esperando 60s...")
                time.sleep(60)
            else:
                print(f"\n   ❌ Error {response.status_code}: {nombre_oficial}")
                todos[nombre_oficial] = {"error": response.status_code}

        except Exception as e:
            print(f"\n   ❌ Excepción en {nombre_oficial}: {e}")
            todos[nombre_oficial] = {"error": str(e)}

        time.sleep(2)

    print()
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Guardado: squad_values.json ({ok}/{total} selecciones)")
    return 1, 1

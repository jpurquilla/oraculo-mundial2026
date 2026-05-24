"""
Módulo: football_data_api.py
Fuente 5: Football-Data.org API
Top 5 ligas + Champions League
"""

import json
import os
import requests
from pathlib import Path


def fuente_5_football_data_org(raw_dir: Path):
    """
    Fuente 5: Football-Data.org API
    Equipos de Top 5 ligas + Champions League
    """
    token = os.getenv("FOOTBALL_DATA_API_KEY")
    if not token:
        print("   ❌ No se encontró FOOTBALL_DATA_API_KEY en .env")
        return 0, 1

    headers = {"X-Auth-Token": token}
    base_url = "https://api.football-data.org/v4"
    dest_dir = raw_dir / "leagues"
    dest_dir.mkdir(parents=True, exist_ok=True)

    competencias = {
        "PL": "Premier League",
        "PD": "Primera Division",
        "BL1": "Bundesliga",
        "SA": "Serie A",
        "FL1": "Ligue 1",
        "CL": "Champions League",
    }

    ok = 0
    total = len(competencias)

    for codigo, nombre in competencias.items():
        dest = dest_dir / f"{codigo}_squads.json"

        if dest.exists():
            print(f"   ⚠️  {nombre} ya existe, omitiendo.")
            ok += 1
            continue

        print(f"\n📥 Descargando equipos: {nombre}")
        try:
            url = f"{base_url}/competitions/{codigo}/teams"
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                with open(dest, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                equipos = len(data.get("teams", []))
                print(f"   ✅ {nombre}: {equipos} equipos guardados")
                ok += 1
            elif response.status_code == 429:
                print(f"   ⚠️  Límite de peticiones alcanzado")
                break
            else:
                print(f"   ❌ Error {response.status_code}: {nombre}")

        except Exception as e:
            print(f"   ❌ Excepción: {e}")

    return ok, total

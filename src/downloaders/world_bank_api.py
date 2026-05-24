"""
Módulo: world_bank_api.py
Fuente 6: World Bank API
Indicadores socioeconómicos de los 48 países del Mundial 2026
"""

import json
import requests
from pathlib import Path

PAISES_WC2026 = [
    "USA",
    "CAN",
    "MEX",
    "ARG",
    "BRA",
    "URU",
    "COL",
    "ECU",
    "VEN",
    "PER",
    "CHL",
    "PRY",
    "BOL",
    "FRA",
    "GBR",
    "ESP",
    "DEU",
    "PRT",
    "NLD",
    "BEL",
    "ITA",
    "HRV",
    "AUT",
    "CHE",
    "DNK",
    "NOR",
    "SWE",
    "POL",
    "UKR",
    "SRB",
    "ROU",
    "HUN",
    "CZE",
    "SVK",
    "GRC",
    "TUR",
    "MAR",
    "SEN",
    "CMR",
    "CIV",
    "GHA",
    "EGY",
    "NGA",
    "ZAF",
    "DZA",
    "TUN",
    "JPN",
    "KOR",
    "IRN",
    "SAU",
    "AUS",
    "NZL",
    "UZB",
    "QAT",
    "ARE",
    "IDN",
]

INDICADORES = {
    "NY.GDP.PCAP.CD": "gdp_per_capita",
    "SP.POP.TOTL": "population",
    "SE.XPD.TOTL.GD.ZS": "education_spend_pct_gdp",
    "SP.DYN.LE00.IN": "life_expectancy",
}


def fuente_6_world_bank(raw_dir: Path):
    """
    Fuente 6: World Bank API - Indicadores socioeconómicos
    Útil para equipos debutantes con pocos datos históricos
    """
    dest_dir = raw_dir / "socioeconomic"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "world_bank_indicators.json"

    if dest.exists():
        print(f"   ⚠️  world_bank_indicators.json ya existe, omitiendo.")
        return 1, 1

    base_url = "https://api.worldbank.org/v2/country"
    todos = {}
    ok = 0
    total = len(PAISES_WC2026)

    print(f"\n📥 Descargando indicadores World Bank para {total} países...")

    for pais in PAISES_WC2026:
        todos[pais] = {}
        for codigo, nombre in INDICADORES.items():
            url = (
                f"{base_url}/{pais}/indicator/{codigo}" f"?format=json&mrv=1&per_page=1"
            )
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1 and data[1]:
                        todos[pais][nombre] = data[1][0].get("value")
                    else:
                        todos[pais][nombre] = None
            except Exception:
                todos[pais][nombre] = None

        ok += 1
        print(f"\r   Procesando {ok}/{total}: {pais}...", end="", flush=True)

    print()
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Guardado: world_bank_indicators.json ({ok}/{total} países)")
    return 1, 1

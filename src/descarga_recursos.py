"""
Script: descarga_recursos.py
Propósito: Orquestador principal de descarga de datos
Oráculo del Balón - Predicción Mundial 2026

Fuentes:
    1. martj42/international_results (GitHub)
    2. FIFA World Ranking (Kaggle)
    3. FIFA World Cup Matches (Kaggle)
    4. WC2026 Baseline (Kaggle)
    5. Football-Data.org API
    6. World Bank API
    7. Transfermarkt (scraping)
"""

from pathlib import Path
from dotenv import load_dotenv

from downloaders.github_sources import fuente_1_international_results
from downloaders.kaggle_sources import (
    fuente_2_fifa_ranking,
    fuente_3_worldcup_matches,
    fuente_4_wc2026_baseline,
)
from downloaders.football_data_api import fuente_5_football_data_org
from downloaders.world_bank_api import fuente_6_world_bank
from downloaders.transfermarkt import fuente_7_transfermarkt

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


if __name__ == "__main__":
    print("=" * 60)
    print("🌍 ORÁCULO DEL BALÓN - Descarga de Fuentes")
    print("=" * 60)

    resumen = []

    ok, total = fuente_1_international_results(RAW_DIR)
    resumen.append(("Fuente 1 - martj42/international_results", ok, total))

    ok, total = fuente_2_fifa_ranking(RAW_DIR)
    resumen.append(("Fuente 2 - FIFA World Ranking", ok, total))

    ok, total = fuente_3_worldcup_matches(RAW_DIR)
    resumen.append(("Fuente 3 - FIFA World Cup Matches", ok, total))

    ok, total = fuente_4_wc2026_baseline(RAW_DIR)
    resumen.append(("Fuente 4 - WC2026 Baseline", ok, total))

    ok, total = fuente_5_football_data_org(RAW_DIR)
    resumen.append(("Fuente 5 - Football-Data.org (Top 5 ligas)", ok, total))

    ok, total = fuente_6_world_bank(RAW_DIR)
    resumen.append(("Fuente 6 - World Bank (socioeconómico)", ok, total))

    ok, total = fuente_7_transfermarkt(RAW_DIR)
    resumen.append(("Fuente 7 - Transfermarkt (valor plantillas)", ok, total))

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DESCARGA")
    print("=" * 60)
    for nombre, ok, total in resumen:
        estado = "✅" if ok == total else "⚠️ " if ok > 0 else "❌"
        print(f"   {estado} {nombre}: {ok}/{total} archivos")

    print("\n✅ Sesión de descarga terminada.")

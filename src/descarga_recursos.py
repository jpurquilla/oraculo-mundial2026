"""
Script: download_sources.py
Propósito: Descarga fuentes primarias de datos para el Oráculo del Balón
Capa: 1 - Obtención de datos crudos
Fuentes:
    1. martj42/international_results (GitHub) - 49k+ partidos 1872-2024
    2. FIFA World Ranking 1993-2024 (Kaggle)
    3. FIFA World Cup Matches 1974-2022 (Kaggle)
    4. WC2026 Baseline (Kaggle)
    5. Football-Data.org API - Top 5 ligas + Champions League
"""

import requests
import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────


def download_file(url: str, dest_path: Path, description: str) -> bool:
    """Descarga un archivo desde una URL directa."""
    if dest_path.exists():
        print(f"   ⚠️  {dest_path.name} ya existe, omitiendo.")
        return True

    print(f"\n📥 Descargando: {description}")
    print(f"   URL: {url}")
    print(f"   Destino: {dest_path}")

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r   Progreso: {pct:.1f}%", end="", flush=True)

        print(f"\n   ✅ Guardado: {dest_path.name} ({downloaded / 1024:.1f} KB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"\n   ❌ Error: {e}")
        return False


def download_kaggle_dataset(
    dataset: str, dest_dir: Path, description: str, check_file: str
) -> bool:
    """Descarga un dataset de Kaggle usando kaggle CLI."""
    if (dest_dir / check_file).exists():
        print(f"   ⚠️  {check_file} ya existe, omitiendo.")
        return True

    print(f"\n📥 Descargando: {description}")
    print(f"   Dataset: {dataset}")
    print(f"   Destino: {dest_dir}")

    try:
        result = subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                dataset,
                "-p",
                str(dest_dir),
                "--unzip",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"   ✅ Descargado correctamente")
            return True
        else:
            print(f"   ❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False


# ─────────────────────────────────────────────
# FUENTES DE DATOS
# ─────────────────────────────────────────────


def fuente_1_international_results():
    """
    Fuente 1: martj42/international_results (GitHub)
    49,000+ partidos internacionales 1872-2024
    Archivos: results.csv, goalscorers.csv, shootouts.csv
    """
    sources = {
        "results.csv": (
            "https://raw.githubusercontent.com/martj42/international_results"
            "/master/results.csv"
        ),
        "goalscorers.csv": (
            "https://raw.githubusercontent.com/martj42/international_results"
            "/master/goalscorers.csv"
        ),
        "shootouts.csv": (
            "https://raw.githubusercontent.com/martj42/international_results"
            "/master/shootouts.csv"
        ),
    }

    dest_dir = RAW_DIR / "matches"
    resultados = {}

    for filename, url in sources.items():
        dest = dest_dir / filename
        resultados[filename] = download_file(url, dest, f"martj42 - {filename}")

    ok = sum(resultados.values())
    return ok, len(resultados)


def fuente_2_fifa_ranking():
    """
    Fuente 2: FIFA World Ranking 1993-2024 (Kaggle)
    Ranking FIFA histórico mes a mes por selección
    """
    ok = download_kaggle_dataset(
        dataset="cashncarry/fifaworldranking",
        dest_dir=RAW_DIR / "ranking",
        description="FIFA World Ranking 1993-2024",
        check_file="fifa_ranking-2024-04-04.csv",
    )
    return (1 if ok else 0), 1


def fuente_3_worldcup_matches():
    """
    Fuente 3: FIFA World Cup Matches 1974-2022 (Kaggle)
    Partidos individuales de cada mundial con estadísticas
    """
    ok = download_kaggle_dataset(
        dataset="piterfm/fifa-football-world-cup",
        dest_dir=RAW_DIR / "worldcup",
        description="FIFA World Cup Matches 1974-2022",
        check_file="Fifa_world_cup_matches.csv",
    )
    return (1 if ok else 0), 1


def fuente_4_wc2026_baseline():
    """
    Fuente 4: WC2026 Match Probability Baseline (Kaggle)
    Probabilidades base por ELO para fase de grupos 2026
    """
    ok = download_kaggle_dataset(
        dataset="die9origephit/fifa-world-cup-2022-complete-dataset",
        dest_dir=RAW_DIR / "worldcup",
        description="WC2026 Match Probability Baseline",
        check_file="matches_1930_2022.csv",
    )
    return (1 if ok else 0), 1


def fuente_5_football_data_org():
    """
    Fuente 5: Football-Data.org API
    Equipos y jugadores de Top 5 ligas + Champions League
    Nos permite saber qué convocados juegan en ligas de élite
    """
    token = os.getenv("FOOTBALL_DATA_API_KEY")
    if not token:
        print("   ❌ No se encontró FOOTBALL_DATA_API_KEY en .env")
        return 0, 1

    headers = {"X-Auth-Token": token}
    base_url = "https://api.football-data.org/v4"
    dest_dir = RAW_DIR / "leagues"
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
                print(f"   ⚠️  Límite de peticiones alcanzado, espera 1 minuto")
                break
            else:
                print(f"   ❌ Error {response.status_code}: {nombre}")

        except Exception as e:
            print(f"   ❌ Excepción: {e}")

    return ok, total


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("🌍 ORÁCULO DEL BALÓN - Descarga de Fuentes")
    print("=" * 60)

    resumen = []

    ok, total = fuente_1_international_results()
    resumen.append(("Fuente 1 - martj42/international_results", ok, total))

    ok, total = fuente_2_fifa_ranking()
    resumen.append(("Fuente 2 - FIFA World Ranking", ok, total))

    ok, total = fuente_3_worldcup_matches()
    resumen.append(("Fuente 3 - FIFA World Cup Matches", ok, total))

    ok, total = fuente_4_wc2026_baseline()
    resumen.append(("Fuente 4 - WC2026 Baseline", ok, total))

    ok, total = fuente_5_football_data_org()
    resumen.append(("Fuente 5 - Football-Data.org (Top 5 ligas)", ok, total))

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DESCARGA")
    print("=" * 60)
    for nombre, ok, total in resumen:
        estado = "✅" if ok == total else "⚠️ " if ok > 0 else "❌"
        print(f"   {estado} {nombre}: {ok}/{total} archivos")

    print("\n✅ Sesión de descarga terminada.")

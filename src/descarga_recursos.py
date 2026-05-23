"""
Script: download_sources.py
Propósito: Descarga fuentes primarias de datos para el Oráculo del Balón
Capa: 1 - Obtención de datos crudos
"""

import requests
import os
from pathlib import Path

# Directorio base del proyecto (dos niveles arriba de este script)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def download_file(url: str, dest_path: Path, description: str) -> bool:
    """Descarga un archivo con barra de progreso simple."""
    print(f"\n Descargando: {description}")
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

        print(f"\n   Guardado: {dest_path.name} ({downloaded / 1024:.1f} KB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"\n    Error al descargar: {e}")
        return False


def download_international_results():
    """
    Fuente 1: martj42/international_results
    ~49,000 partidos internacionales 1872-2024
    Columnas: date, home_team, away_team, home_score, away_score,
              tournament, city, country, neutral
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
    results = {}

    for filename, url in sources.items():
        dest = dest_dir / filename
        if dest.exists():
            print(f"     {filename} ya existe, omitiendo descarga.")
            results[filename] = True
            continue
        results[filename] = download_file(url, dest, f"martj42 - {filename}")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("- Descarga de Fuentes")
    print("=" * 60)

    # Fuente 1
    r1 = download_international_results()
    ok = sum(r1.values())
    print(f"\n Descargas completadas: {ok}/{len(r1)} archivos descargados")

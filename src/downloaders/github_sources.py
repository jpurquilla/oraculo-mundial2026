"""
Módulo: github_sources.py
Fuente 1: martj42/international_results
49,000+ partidos internacionales 1872-2024
"""

import requests
from pathlib import Path


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


def fuente_1_international_results(raw_dir: Path):
    """
    Fuente 1: martj42/international_results (GitHub)
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

    dest_dir = raw_dir / "matches"
    resultados = {}

    for filename, url in sources.items():
        dest = dest_dir / filename
        resultados[filename] = download_file(url, dest, f"martj42 - {filename}")

    ok = sum(resultados.values())
    return ok, len(resultados)

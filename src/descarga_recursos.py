"""
Script: download_sources.py
Propósito: Descarga fuentes primarias de datos para el Oráculo del Balón
Capa: 1 - Obtención de datos crudos
Fuentes:
    1. martj42/international_results (GitHub) - 49k+ partidos 1872-2024
    2. FIFA World Ranking 1993-2024 (Kaggle)
    3. FIFA World Cup Matches 1974-2022 (Kaggle)
    4. WC2026 Match Probability Baseline (Kaggle)
"""

import requests
import subprocess
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────


def download_file(url: str, dest_path: Path, description: str) -> bool:
    """Descarga un archivo desde una URL directa."""
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


def download_kaggle_dataset(dataset: str, dest_dir: Path, description: str) -> bool:
    """Descarga un dataset de Kaggle usando kaggle CLI."""
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
        if dest.exists():
            print(f"   ⚠️  {filename} ya existe, omitiendo.")
            resultados[filename] = True
            continue
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
    )
    return (1 if ok else 0), 1


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

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DESCARGA")
    print("=" * 60)
    for nombre, ok, total in resumen:
        estado = "✅" if ok == total else "⚠️ " if ok > 0 else "❌"
        print(f"   {estado} {nombre}: {ok}/{total} archivos")

    print("\n✅ Sesión de descarga terminada.")

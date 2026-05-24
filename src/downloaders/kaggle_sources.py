"""
Módulo: kaggle_sources.py
Fuentes 2, 3, 4: Datasets de Kaggle
"""

import subprocess
from pathlib import Path


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


def fuente_2_fifa_ranking(raw_dir: Path):
    """Fuente 2: FIFA World Ranking 1993-2024 (Kaggle)"""
    ok = download_kaggle_dataset(
        dataset="cashncarry/fifaworldranking",
        dest_dir=raw_dir / "ranking",
        description="FIFA World Ranking 1993-2024",
        check_file="fifa_ranking-2024-04-04.csv",
    )
    return (1 if ok else 0), 1


def fuente_3_worldcup_matches(raw_dir: Path):
    """Fuente 3: FIFA World Cup Matches 1974-2022 (Kaggle)"""
    ok = download_kaggle_dataset(
        dataset="piterfm/fifa-football-world-cup",
        dest_dir=raw_dir / "worldcup",
        description="FIFA World Cup Matches 1974-2022",
        check_file="Fifa_world_cup_matches.csv",
    )
    return (1 if ok else 0), 1


def fuente_4_wc2026_baseline(raw_dir: Path):
    """Fuente 4: WC2026 Match Probability Baseline (Kaggle)"""
    ok = download_kaggle_dataset(
        dataset="die9origephit/fifa-world-cup-2022-complete-dataset",
        dest_dir=raw_dir / "worldcup",
        description="WC2026 Match Probability Baseline",
        check_file="matches_1930_2022.csv",
    )
    return (1 if ok else 0), 1

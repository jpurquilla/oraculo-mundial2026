python3 -c "
import pandas as pd

archivos = {
    'results.csv': 'data/raw/matches/results.csv',
    'goalscorers.csv': 'data/raw/matches/goalscorers.csv',
    'shootouts.csv': 'data/raw/matches/shootouts.csv',
}

for nombre, ruta in archivos.items():
    df = pd.read_csv(ruta)
    print(f'\n{'='*60}')
    print(f'📄 {nombre}')
    print(f'   Filas: {len(df):,} | Columnas: {list(df.columns)}')
    print(f'\n--- PRIMERAS 3 FILAS ---')
    print(df.head(3).to_string())
    print(f'\n--- ÚLTIMAS 3 FILAS ---')
    print(df.tail(3).to_string())
    print(f'\n--- NULOS POR COLUMNA ---')
    print(df.isnull().sum().to_string())
"
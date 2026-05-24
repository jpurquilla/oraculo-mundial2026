### 2.3 Limpieza de results_train

Con los partidos separados y nombres estandarizados, ahora limpiamos
el dataset de entrenamiento:

- Convertir `home_score` y `away_score` de float a entero
- Crear columna `result` con el resultado del partido (H/D/A)
- Aplicar Time Decay (peso exponencial por antigüedad)
- Filtrar desde 1993 (cuando inicia el ranking FIFA)

**Resultado esperado (H/D/A):**
- H = Home wins (local gana)
- D = Draw (empate)
- A = Away wins (visitante gana)

### 2.3.1 Time Decay — Justificación Técnica

#### ¿Por qué aplicar decaimiento temporal?
Un partido de Francia en 2010 tiene poco valor predictivo para 2026.
Los equipos cambian: nuevos jugadores, nuevo técnico, nueva táctica.
Necesitamos que el modelo **aprenda más de lo reciente** y 
**olvide gradualmente lo antiguo**.

#### Fórmula utilizada
La función de decaimiento exponencial es estándar en modelos deportivos:

w = 0.5 ^ (días_atrás / half_life)

Donde:
- `w` = peso del partido (entre 0 y 1)
- `días_atrás` = días desde el partido hasta la fecha de corte
- `half_life` = 1,095 días (3 años)

#### ¿Por qué base 0.5?
Significa que cada período (half_life) el peso se reduce a la mitad.
Es intuitivo y estándar en modelos de decaimiento:

| Antigüedad | Cálculo | Peso        |
| ---------- | ------- | ----------- |
| Hoy        | 0.5^0   | 1.00 (100%) |
| 3 años     | 0.5^1   | 0.50 (50%)  |
| 6 años     | 0.5^2   | 0.25 (25%)  |
| 9 años     | 0.5^3   | 0.13 (13%)  |

#### ¿Por qué half_life de 3 años?
Es un ciclo completo de selección nacional:
- Clasificatorias (2 años) + preparación para el Mundial (1 año)
- Menos de 2 años → demasiado agresivo, se descartan datos útiles
- Más de 5 años → demasiado suave, partidos de hace 8 años pesan casi igual

#### Fecha de corte: 10 de junio de 2026
Un día antes del primer partido del Mundial. Así aprovechamos
todos los datos disponibles incluyendo eliminatorias 2025-2026
sin incluir partidos del propio torneo.


## Hallazgos EDA — results_clean.csv

### Distribución de resultados (1993-2026)
- Local gana    : 48.5% (14,795 partidos)
- Visitante gana: 28.1% (8,580 partidos)
- Empate        : 23.3% (7,111 partidos)

**Desbalance de clases:** El modelo deberá manejar este desbalance
usando class_weight o sample_weight en el entrenamiento.

### Dataset final
- Total partidos para entrenar: 30,486
- Rango: 1993-2026
- Columnas: 11

## Limitaciones del modelo

### World Bank — Indicadores Socioeconómicos
- **England y Scotland** comparten los mismos indicadores (GBR - Reino Unido)
  ya que World Bank no tiene datos separados para cada nación.
- **9 equipos** no tienen datos del World Bank inicialmente:
  Bosnia and Herzegovina, Cape Verde, Curaçao, DR Congo, Haiti,
  Iraq, Jordan, Panama, Scotland.
- Para equipos sin datos se imputará con la **mediana de su confederación**
  en el notebook 03 de Feature Engineering.
- Curaçao es territorio autónomo de Países Bajos — se usarán
  datos de Netherlands como proxy.

  ### England y Scotland — World Bank
- World Bank no tiene datos separados para England ni Scotland
- Ambas usan datos de GBR (Reino Unido) como proxy
- Se aplicará en notebook 03 Feature Engineering
## Nomenclatura de archivos data/processed/

### Entrenamiento
- `results_clean.csv`          → partidos limpios 1993-2026
- `results_train.csv`          → partidos para entrenar (sin WC2022)
- `results_historico_1872.csv` → histórico completo para calcular ELO
- `ranking_clean.csv`          → ranking FIFA jun 2024
- `wc_matches_clean.csv`       → mundiales 1930-2018
- `transfermarkt_clean.csv`    → valores de plantilla actuales
- `worldbank_clean.csv`        → indicadores socioeconómicos
- `leagues_players.csv`        → jugadores en ligas top actuales

### Validación (WC2022)
- `wc2022_eval.csv`            → partidos WC2022 para evaluar modelo
- `ranking_wc2022.csv`         → ranking FIFA oct 2022
- `wc2022_enriched.csv`        → WC2022 con xG y tarjetas
- `wc2022_squads.csv`          → plantillas WC2022 con ligas

### Predicción (WC2026)
- `wc2026_grupos.csv`          → 72 partidos fase de grupos
- `convocados_wc2026.csv`      → convocados WC2026 con ligas
## Convocados WC2026 — Estrategia de datos

### Fuente
Web scraping de ESPN Deportes:
https://www.clarin.com/deportes/mundial-2026-listas-convocados-todas-selecciones_0_LOoLvGaypI.html

### Estrategia por tipo de lista
| Tipo                | Acción                                                             |
| ------------------- | ------------------------------------------------------------------ |
| Lista final oficial | Usar datos reales del scraper                                      |
| Pre-lista           | Usar datos reales del scraper como aproximación                    |
| Sin lista           | Proxy: contar jugadores de esa nacionalidad en leagues_players.csv |

### Limitaciones conocidas
- Jugadores en ligas no europeas no aparecen en leagues_players.csv
  (ej: Neymar en Al-Hilal, Cristiano en Al-Nassr, Benzema en Al-Ittihad)
- Para equipos con proxy el conteo puede ser mayor al real
  porque cuenta TODOS los jugadores de esa nacionalidad en ligas top,
  no solo los convocados
- Las pre-listas pueden diferir de las listas definitivas
  (fecha límite FIFA: 1 de junio de 2026)
- Canadá y otros equipos sin lista al momento del scraping
  usan proxy completo

### Fecha del scraping
24 de mayo de 2026 — 8 días antes de la fecha límite FIFA
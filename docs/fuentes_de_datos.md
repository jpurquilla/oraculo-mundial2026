# Fuentes de Datos - Oráculo del Balón 2026

Este documento registra todas las fuentes de datos utilizadas en el proyecto,
incluyendo URLs, método de obtención, fecha de acceso y descripción.

---

## Fuente 1: Resultados Internacionales Históricos
- **Nombre:** International Football Results (1872-2024)
- **Autor:** Mart Jürisoo (@martj42)
- **URL:** https://github.com/martj42/international_results
- **Archivos:**
  - results.csv — 49,000+ partidos internacionales
  - goalscorers.csv — detalle de goles por partido
  - shootouts.csv — partidos definidos por penales
- **Método:** Descarga directa via GitHub Raw URL
- **Formato:** CSV
- **Uso:** Columna vertebral del modelo — historial de partidos,
  goles, localía, torneos

---

## Fuente 2: FIFA World Ranking Histórico
- **Nombre:** FIFA World Ranking 1993-2024
- **Autor:** cashncarry (Kaggle)
- **URL:** https://www.kaggle.com/datasets/cashncarry/fifaworldranking
- **Archivos:**
  - fifa_ranking-2024-04-04.csv
  - fifa_ranking-2024-06-20.csv
  - fifa_ranking-2023-07-20.csv
- **Método:** Descarga via Kaggle API (kaggle CLI)
- **Formato:** CSV
- **Uso:** Feature de ranking FIFA por fecha para cada selección

---

## Fuente 3: Partidos de Mundiales 1974-2022
- **Nombre:** FIFA Football World Cup
- **Autor:** piterfm (Kaggle)
- **URL:** https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup
- **Archivos:**
  - Fifa_world_cup_matches.csv — estadísticas tácticas Mundial 2022
  - matches_1930_2022.csv — todos los partidos mundiales con xG
  - world_cup.csv — resumen histórico por edición
- **Método:** Descarga via Kaggle API (kaggle CLI)
- **Formato:** CSV
- **Uso:** xG histórico, estadísticas tácticas, validación con Mundial 2022

---

## Fuente 4: WC2026 Match Probability Baseline
- **Nombre:** FIFA World Cup 2022 Complete Dataset
- **Autor:** die9origephit (Kaggle)
- **URL:** https://www.kaggle.com/datasets/die9origephit/fifa-world-cup-2022-complete-dataset
- **Archivos:**
  - fifa_ranking_2022-10-06.csv
- **Método:** Descarga via Kaggle API (kaggle CLI)
- **Formato:** CSV
- **Uso:** Probabilidades base ELO para referencia y validación

---

## Fuente 5: Estadísticas de Ligas Domésticas
- **Nombre:** Football-Data.org API
- **URL API:** https://api.football-data.org/v4
- **URL Registro:** https://www.football-data.org/client/register
- **Competencias descargadas:**
  - PL — Premier League (Inglaterra)
  - PD — Primera Division (España)
  - BL1 — Bundesliga (Alemania)
  - SA — Serie A (Italia)
  - FL1 — Ligue 1 (Francia)
  - CL — UEFA Champions League
- **Método:** API REST con token de autenticación (X-Auth-Token header)
- **Formato:** JSON
- **Uso:** Identificar jugadores convocados que juegan en Top 5 ligas

---

## Fuente 6: Indicadores Socioeconómicos
- **Nombre:** World Bank Open Data API
- **URL:** https://api.worldbank.org/v2/country
- **URL Portal:** https://data.worldbank.org
- **Indicadores:**
  - NY.GDP.PCAP.CD — PIB per cápita (USD)
  - SP.POP.TOTL — Población total
  - SE.XPD.TOTL.GD.ZS — Gasto en educación (% PIB)
  - SP.DYN.LE00.IN — Esperanza de vida al nacer
- **Método:** API REST pública sin autenticación
- **Formato:** JSON
- **Uso:** Features socioeconómicos para equipos debutantes
  con pocos datos históricos (Cabo Verde, Curazao, Jordania, Uzbekistán)

---

## Fuente 7: Valor de Mercado de Plantillas
- **Nombre:** Transfermarkt
- **URL Base:** https://www.transfermarkt.com
- **URL Mundial 2026:** https://www.transfermarkt.com/weltmeisterschaft/startseite/pokalwettbewerb/FIWC
- **IDs verificados desde:** https://www.transfermarkt.com/weltmeisterschaft/startseite/pokalwettbewerb/FIWC
- **Método:** Web scraping con requests + BeautifulSoup
- **Formato:** HTML → JSON
- **Uso:** Valor de mercado total de plantilla por selección,
  valor individual por jugador, indicador de calidad de plantilla

---

## ELO Rating (Calculado internamente)
- **Método:** Calculado por nosotros desde Fuente 1 (results.csv)
- **Referencia metodológica:** https://en.wikipedia.org/wiki/Elo_rating_system
- **Referencia fútbol:** https://www.eloratings.net/about
- **Parámetros:**
  - ELO inicial: 1500 para todos los equipos
  - K-factor: 20 (partidos amistosos), 40 (mundiales)
  - Decay temporal: λ = 0.3
- **Uso:** Feature principal del modelo — más dinámico y preciso
  que el Ranking FIFA

---

## Lista Oficial de Clasificados Mundial 2026
- **URL verificación:** https://www.roadtowc.com/es/48-clasificados-mundial-2026-lista-completa-oficial/
- **URL FIFA oficial:** https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026
- **Uso:** Validación de los 48 equipos participantes
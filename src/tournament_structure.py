"""
Estructura oficial del Mundial 2026
Fuente: https://www.bracketmundial2026.com/grupos
Sorteo oficial FIFA: 5 de diciembre de 2025

Formato:
- 48 equipos en 12 grupos de 4 (A-L)
- Clasifican: 2 primeros de cada grupo (24) + 8 mejores terceros = 32
- Fases: Dieciseisavos → Octavos → Cuartos → Semis → 3er lugar → Final
- Total: 104 partidos
"""

# ─────────────────────────────────────────────
# GRUPOS OFICIALES
# ─────────────────────────────────────────────

GRUPOS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Switzerland", "Qatar", "Bosnia-Herzegovina"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkiye"],
    "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Tunisia", "Sweden"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Norway", "Iraq"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Colombia", "Uzbekistan", "DR Congo"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# ─────────────────────────────────────────────
# FIXTURES FASE DE GRUPOS
# ─────────────────────────────────────────────

FIXTURES_GRUPOS = {
    "A": [
        ("Mexico", "South Africa"),
        ("South Korea", "Czechia"),
        ("Czechia", "South Africa"),
        ("Mexico", "South Korea"),
        ("Czechia", "Mexico"),
        ("South Africa", "South Korea"),
    ],
    "B": [
        ("Canada", "Bosnia-Herzegovina"),
        ("Qatar", "Switzerland"),
        ("Switzerland", "Bosnia-Herzegovina"),
        ("Canada", "Qatar"),
        ("Switzerland", "Canada"),
        ("Bosnia-Herzegovina", "Qatar"),
    ],
    "C": [
        ("Brazil", "Morocco"),
        ("Haiti", "Scotland"),
        ("Scotland", "Morocco"),
        ("Brazil", "Haiti"),
        ("Scotland", "Brazil"),
        ("Morocco", "Haiti"),
    ],
    "D": [
        ("United States", "Paraguay"),
        ("Australia", "Turkiye"),
        ("United States", "Australia"),
        ("Turkiye", "Paraguay"),
        ("Turkiye", "United States"),
        ("Paraguay", "Australia"),
    ],
    "E": [
        ("Germany", "Curaçao"),
        ("Ivory Coast", "Ecuador"),
        ("Germany", "Ivory Coast"),
        ("Ecuador", "Curaçao"),
        ("Ecuador", "Germany"),
        ("Curaçao", "Ivory Coast"),
    ],
    "F": [
        ("Netherlands", "Japan"),
        ("Sweden", "Tunisia"),
        ("Netherlands", "Sweden"),
        ("Tunisia", "Japan"),
        ("Japan", "Sweden"),
        ("Tunisia", "Netherlands"),
    ],
    "G": [
        ("Belgium", "Egypt"),
        ("Iran", "New Zealand"),
        ("Belgium", "Iran"),
        ("New Zealand", "Egypt"),
        ("Egypt", "Iran"),
        ("New Zealand", "Belgium"),
    ],
    "H": [
        ("Spain", "Cape Verde"),
        ("Saudi Arabia", "Uruguay"),
        ("Spain", "Saudi Arabia"),
        ("Uruguay", "Cape Verde"),
        ("Cape Verde", "Saudi Arabia"),
        ("Uruguay", "Spain"),
    ],
    "I": [
        ("France", "Senegal"),
        ("Iraq", "Norway"),
        ("France", "Iraq"),
        ("Norway", "Senegal"),
        ("Norway", "France"),
        ("Senegal", "Iraq"),
    ],
    "J": [
        ("Argentina", "Algeria"),
        ("Austria", "Jordan"),
        ("Argentina", "Austria"),
        ("Jordan", "Algeria"),
        ("Algeria", "Austria"),
        ("Jordan", "Argentina"),
    ],
    "K": [
        ("Portugal", "DR Congo"),
        ("Uzbekistan", "Colombia"),
        ("Portugal", "Uzbekistan"),
        ("Colombia", "DR Congo"),
        ("Colombia", "Portugal"),
        ("DR Congo", "Uzbekistan"),
    ],
    "L": [
        ("England", "Croatia"),
        ("Ghana", "Panama"),
        ("England", "Ghana"),
        ("Panama", "Croatia"),
        ("Panama", "England"),
        ("Croatia", "Ghana"),
    ],
}

# ─────────────────────────────────────────────
# REGLAS DE CLASIFICACIÓN
# ─────────────────────────────────────────────

REGLAS_CLASIFICACION = {
    "puntos_victoria": 3,
    "puntos_empate": 1,
    "puntos_derrota": 0,
    "clasifican_por_grupo": 2,  # 1ro y 2do de cada grupo
    "mejores_terceros": 8,  # 8 de 12 terceros pasan
    "total_clasificados": 32,  # 24 directos + 8 terceros
    "criterios_desempate": [
        "puntos",
        "diferencia_goles",
        "goles_marcados",
        "resultado_directo",
        "tarjetas",
        "ranking_fifa",
        "sorteo",
    ],
}

# ─────────────────────────────────────────────
# BRACKET FASE ELIMINATORIA
# ─────────────────────────────────────────────

"""
Dieciseisavos (32 equipos):
- 1A vs 3D/E/F    - 1B vs 3G/H/I
- 1C vs 3J/K/L    - 1D vs 2C
- 1E vs 2F        - 1F vs 2E
- 1G vs 2H        - 1H vs 2G
- 1I vs 2J        - 1J vs 2I
- 1K vs 2L        - 1L vs 2K
+ 4 cruces con mejores terceros

Octavos (16 equipos)
Cuartos (8 equipos)
Semifinales (4 equipos)
Tercer lugar (2 equipos)
Final (2 equipos)
"""

FASES_ELIMINATORIAS = [
    "Dieciseisavos",  # 32 equipos → 16
    "Octavos",  # 16 equipos → 8
    "Cuartos",  # 8 equipos → 4
    "Semifinales",  # 4 equipos → 2
    "Tercer_lugar",  # 2 equipos → 1 (perdedores semis)
    "Final",  # 2 equipos → 1 campeón
]

# Partidos por fase
PARTIDOS_POR_FASE = {
    "Grupos": 72,  # 6 partidos x 12 grupos
    "Dieciseisavos": 16,  # 32 equipos
    "Octavos": 8,  # 16 equipos
    "Cuartos": 4,  # 8 equipos
    "Semifinales": 2,  # 4 equipos
    "Tercer_lugar": 1,
    "Final": 1,
    "TOTAL": 104,
}

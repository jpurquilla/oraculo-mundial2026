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

import json
from pathlib import Path

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
    "clasifican_por_grupo": 2,
    "mejores_terceros": 8,
    "total_clasificados": 32,
    "criterios_desempate": [
        "puntos",
        "diferencia_goles",
        "goles_marcados",
        "fair_play",
        "ranking_fifa",
        "sorteo",
    ],
}

# ─────────────────────────────────────────────
# BRACKET OFICIAL DIECISEISAVOS
# Fuente: CBS Sports, MLS Soccer, Sky Sports
#         Bleacher Report — Sorteo FIFA dic 2025
#
# 4 líderes SIN tercero (cruces fijos):
#   1C vs 2F  (P74)
#   1F vs 2C  (P75)
#   1H vs 2J  (P84)
#   1J vs 2H  (P86)
#
# 8 líderes CON tercero (usan matriz 495):
#   1A(P79) 1B(P85) 1D(P81) 1E(P76)
#   1G(P82) 1I(P77) 1K(P87) 1L(P80)
#
# 4 cruces entre segundos (fijos):
#   2A vs 2B  (P73)
#   2E vs 2I  (P78)
#   2K vs 2L  (P83)
#   2D vs 2G  (P88)
# ─────────────────────────────────────────────

# Cruces 100% fijos — no dependen de terceros
CRUCES_FIJOS = {
    73: ("2A", "2B"),  # Segundo A vs Segundo B
    74: ("1C", "2F"),  # Líder C vs Segundo F
    75: ("1F", "2C"),  # Líder F vs Segundo C
    78: ("2E", "2I"),  # Segundo E vs Segundo I
    83: ("2K", "2L"),  # Segundo K vs Segundo L
    84: ("1H", "2J"),  # Líder H vs Segundo J
    86: ("1J", "2H"),  # Líder J vs Segundo H
    88: ("2D", "2G"),  # Segundo D vs Segundo G
}

# Orden oficial FIFA para leer matriz de 495 combinaciones
ORDEN_LIDERES_TERCEROS = ["1A", "1B", "1D", "1E", "1G", "1I", "1K", "1L"]

# Número de partido de cada líder que juega vs tercero
PARTIDO_POR_LIDER = {
    "1A": 79,
    "1B": 85,
    "1D": 81,
    "1E": 76,
    "1G": 82,
    "1I": 77,
    "1K": 87,
    "1L": 80,
}

# ─────────────────────────────────────────────
# FUNCIÓN: asignar terceros usando matriz 495
# ─────────────────────────────────────────────


def asignar_terceros_a_cruces(grupos_terceros_clasificados, ruta_matriz=None):
    """
    Asigna los 8 mejores terceros a los 8 líderes usando
    la matriz oficial de 495 combinaciones del Anexo C FIFA.

    Parámetros:
    -----------
    grupos_terceros_clasificados : list de str
        8 letras de grupo de los terceros clasificados.
        Ejemplo: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I']

    ruta_matriz : Path o str, opcional
        Ruta al archivo matriz_mundial_495.json

    Retorna:
    --------
    dict {lider: codigo_tercero}
        Ejemplo: {'1A': '3C', '1B': '3F', ...}
    """
    if ruta_matriz is None:
        ruta_matriz = Path("..") / "data" / "processed" / "matriz_mundial_495.json"

    with open(ruta_matriz, "r") as f:
        matriz = json.load(f)

    # Clave: grupos ordenados alfabéticamente
    clave = "".join(sorted(grupos_terceros_clasificados))

    if clave not in matriz:
        # Fallback secuencial si la clave no existe
        grupos_ord = sorted(grupos_terceros_clasificados)
        return {
            lider: f"3{grupos_ord[i]}" for i, lider in enumerate(ORDEN_LIDERES_TERCEROS)
        }

    resultado = matriz[clave]  # ["3C", "3F", ...]
    return {lider: resultado[i] for i, lider in enumerate(ORDEN_LIDERES_TERCEROS)}


# ─────────────────────────────────────────────
# OCTAVOS DE FINAL
# Emparejamientos oficiales ganadores P73-P88
# ─────────────────────────────────────────────

OCTAVOS = [
    ("W74", "W77"),  # Partido 89
    ("W73", "W75"),  # Partido 90
    ("W76", "W78"),  # Partido 91
    ("W79", "W80"),  # Partido 92
    ("W83", "W84"),  # Partido 93
    ("W81", "W82"),  # Partido 94
    ("W86", "W88"),  # Partido 95
    ("W85", "W87"),  # Partido 96
]

# ─────────────────────────────────────────────
# FASES Y PARTIDOS
# ─────────────────────────────────────────────

FASES_ELIMINATORIAS = [
    "Dieciseisavos",
    "Octavos",
    "Cuartos",
    "Semifinales",
    "Tercer_lugar",
    "Final",
]

PARTIDOS_POR_FASE = {
    "Grupos": 72,
    "Dieciseisavos": 16,
    "Octavos": 8,
    "Cuartos": 4,
    "Semifinales": 2,
    "Tercer_lugar": 1,
    "Final": 1,
    "TOTAL": 104,
}

"""
Módulo: convocados.py
Fuente 8: Convocados oficiales Mundial 2026
Fuente: https://www.clarin.com/deportes/mundial-2026-listas-convocados-todas-las-selecciones_0_LOoLvGaypI.html
Nota: Script con reintento inteligente - actualiza por selección
"""

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL_CONVOCADOS = (
    "https://www.clarin.com/deportes/"
    "mundial-2026-listas-convocados-todas-las-selecciones_0_LOoLvGaypI.html"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept-Language": "es-MX,es;q=0.9",
}

# Grupos para mapear selecciones
GRUPOS = [
    "Grupo A",
    "Grupo B",
    "Grupo C",
    "Grupo D",
    "Grupo E",
    "Grupo F",
    "Grupo G",
    "Grupo H",
    "Grupo I",
    "Grupo J",
    "Grupo K",
    "Grupo L",
]


def parsear_lista_jugadores(texto: str) -> list:
    """Parsea una lista de jugadores desde texto crudo."""
    if not texto:
        return []
    # Separar por comas y limpiar
    jugadores = []
    for j in texto.split(","):
        j = j.strip()
        # Eliminar club entre paréntesis si se desea mantener solo nombre
        if j and len(j) > 2:
            jugadores.append(j)
    return jugadores


def fuente_8_convocados(raw_dir: Path):
    """
    Fuente 8: Convocados oficiales Mundial 2026 desde Clarín
    Estructura: Grupo → Selección → Arqueros/Defensores/Centrocampistas/Delanteros
    """
    dest_dir = raw_dir / "convocados"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "convocados_wc2026.json"

    # Cargar datos previos si existen
    convocados_previos = {}
    if dest.exists():
        with open(dest, encoding="utf-8") as f:
            convocados_previos = json.load(f)
        print(f"   📂 Datos previos: {len(convocados_previos)} selecciones")

    print(f"\n📥 Descargando convocados oficiales WC2026 desde Clarín...")

    try:
        r = requests.get(URL_CONVOCADOS, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            print(f"   ❌ Error {r.status_code}")
            return 0, 1

        soup = BeautifulSoup(r.text, "html.parser")

        # Encontrar h2 principal
        h2_principal = None
        for h2 in soup.find_all("h2"):
            if "convocados" in h2.get_text().lower():
                h2_principal = h2
                break

        if not h2_principal:
            print("   ❌ No se encontró sección de convocados")
            return 0, 1

        # Obtener todos los elementos después del h2
        elementos = h2_principal.find_all_next(["h3", "p", "ul", "li"])

        convocados = convocados_previos.copy()
        grupo_actual = None
        seleccion_actual = None
        nuevas = 0
        actualizadas = 0

        i = 0
        while i < len(elementos):
            elem = elementos[i]
            texto = elem.get_text(strip=True)

            if not texto:
                i += 1
                continue

            # Detectar grupo
            if elem.name == "h3" and texto in GRUPOS:
                grupo_actual = texto
                i += 1
                continue

            # Detectar selección
            if elem.name == "h3" and texto not in GRUPOS and grupo_actual:
                seleccion_actual = texto
                es_nueva = seleccion_actual not in convocados
                convocados[seleccion_actual] = {
                    "grupo": grupo_actual,
                    "arqueros": [],
                    "defensores": [],
                    "centrocampistas": [],
                    "delanteros": [],
                    "dt": "",
                    "tipo_lista": "",
                    "completa": False,
                    "fuente": "clarin",
                }
                if es_nueva:
                    nuevas += 1
                else:
                    actualizadas += 1
                i += 1
                continue

            # Detectar tipo de lista
            if elem.name == "p" and seleccion_actual:
                texto_lower = texto.lower()
                if "convocatoria final" in texto_lower:
                    convocados[seleccion_actual]["tipo_lista"] = "final"
                elif "pre-lista" in texto_lower or "prelista" in texto_lower:
                    convocados[seleccion_actual]["tipo_lista"] = "pre-lista"
                elif (
                    "anunciada próximamente" in texto_lower
                    or "anunciada" in texto_lower
                ):
                    convocados[seleccion_actual]["tipo_lista"] = "pendiente"
                i += 1
                continue

            # Detectar jugadores por posición en li
            if elem.name == "li" and seleccion_actual:
                texto_lower = texto.lower()

                if texto_lower.startswith("arqueros:"):
                    contenido = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["arqueros"] = parsear_lista_jugadores(
                        contenido
                    )

                elif texto_lower.startswith("defensores:"):
                    contenido = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["defensores"] = (
                        parsear_lista_jugadores(contenido)
                    )

                elif texto_lower.startswith(
                    "centrocampistas:"
                ) or texto_lower.startswith("mediocampistas:"):
                    contenido = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["centrocampistas"] = (
                        parsear_lista_jugadores(contenido)
                    )

                elif texto_lower.startswith("delanteros:"):
                    contenido = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["delanteros"] = (
                        parsear_lista_jugadores(contenido)
                    )

                elif texto_lower.startswith(
                    "director técnico:"
                ) or texto_lower.startswith("dt:"):
                    dt = texto.split(":", 1)[-1].strip()
                    convocados[seleccion_actual]["dt"] = dt

                i += 1
                continue

            i += 1

        # Marcar como completa si tiene jugadores en al menos 3 posiciones
        completas = 0
        pendientes = []

        for nombre, datos in convocados.items():
            tiene_datos = (
                sum(
                    [
                        len(datos.get("arqueros", [])) > 0,
                        len(datos.get("defensores", [])) > 0,
                        len(datos.get("centrocampistas", [])) > 0,
                        len(datos.get("delanteros", [])) > 0,
                    ]
                )
                >= 3
            )

            datos["completa"] = tiene_datos
            if tiene_datos:
                completas += 1
            else:
                pendientes.append(nombre)
                datos["fuente"] = "pendiente_usar_transfermarkt"

        with open(dest, "w", encoding="utf-8") as f:
            json.dump(convocados, f, ensure_ascii=False, indent=2)

        print(f"   ✅ Guardado: {len(convocados)} selecciones")
        print(
            f"   📊 Completas: {completas} | Nuevas: {nuevas} | Actualizadas: {actualizadas}"
        )

        if pendientes:
            print(f"   ⚠️  Sin lista aún ({len(pendientes)}) → usarán Transfermarkt:")
            for p in sorted(pendientes):
                print(f"      - {p}")

        return 1, 1

    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        import traceback

        traceback.print_exc()
        return 0, 1

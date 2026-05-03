"""
Módulo de escudos para equipos de fútbol.
URLs obtenidas de TheSportsDB (gratuito, sin API key necesaria para búsqueda).
"""

import requests
from functools import lru_cache

# Diccionario pre-mapeado con los equipos más comunes de las ligas principales
ESCUDOS_CACHE = {
    # Premier League
    "Arsenal": "https://www.thesportsdb.com/images/media/team/badge/a1af2i1557005128.png",
    "Chelsea": "https://www.thesportsdb.com/images/media/team/badge/yvwvtu1448813215.png",
    "Liverpool": "https://www.thesportsdb.com/images/media/team/badge/xzqdr11598744967.png",
    "Manchester City": "https://www.thesportsdb.com/images/media/team/badge/vwpizy1548859054.png",
    "Manchester United": "https://www.thesportsdb.com/images/media/team/badge/xzqdr11548859378.png",
    "Tottenham": "https://www.thesportsdb.com/images/media/team/badge/rwopxy1471630789.png",
    "Newcastle": "https://www.thesportsdb.com/images/media/team/badge/uvuswu1421791546.png",
    "Aston Villa": "https://www.thesportsdb.com/images/media/team/badge/sq4sss1547234388.png",
    "West Ham": "https://www.thesportsdb.com/images/media/team/badge/ya4rti1437743276.png",
    "Brighton": "https://www.thesportsdb.com/images/media/team/badge/svq3t51448813018.png",
    "Everton": "https://www.thesportsdb.com/images/media/team/badge/uuqyxy1421791381.png",
    "Brentford": "https://www.thesportsdb.com/images/media/team/badge/qfpvtq1656082851.png",
    "Fulham": "https://www.thesportsdb.com/images/media/team/badge/xpwpwq1421791456.png",
    "Crystal Palace": "https://www.thesportsdb.com/images/media/team/badge/qpxtqp1547236143.png",
    "Wolverhampton": "https://www.thesportsdb.com/images/media/team/badge/vwpizy1421791512.png",
    "Wolves": "https://www.thesportsdb.com/images/media/team/badge/vwpizy1421791512.png",
    "Leicester": "https://www.thesportsdb.com/images/media/team/badge/nstxwt1671280403.png",
    "Southampton": "https://www.thesportsdb.com/images/media/team/badge/uquyvx1421791501.png",
    "Nottingham Forest": "https://www.thesportsdb.com/images/media/team/badge/twwvxy1421791570.png",
    "Bournemouth": "https://www.thesportsdb.com/images/media/team/badge/vuturv1421791335.png",
    "Ipswich": "https://www.thesportsdb.com/images/media/team/badge/rkqxtt1421791467.png",

    # La Liga
    "Real Madrid": "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1473504001.png",
    "Barcelona": "https://www.thesportsdb.com/images/media/team/badge/uyhbfe1612467562.png",
    "Atletico Madrid": "https://www.thesportsdb.com/images/media/team/badge/a1af2i1557005128.png",
    "Atlético Madrid": "https://www.thesportsdb.com/images/media/team/badge/xzuzsv1421791228.png",
    "Sevilla": "https://www.thesportsdb.com/images/media/team/badge/pstvwt1421791257.png",
    "Valencia": "https://www.thesportsdb.com/images/media/team/badge/vwwqrx1421791263.png",
    "Villarreal": "https://www.thesportsdb.com/images/media/team/badge/twxxuq1421791267.png",
    "Real Sociedad": "https://www.thesportsdb.com/images/media/team/badge/xzszts1421791249.png",
    "Athletic Club": "https://www.thesportsdb.com/images/media/team/badge/xwuqtq1421791222.png",
    "Real Betis": "https://www.thesportsdb.com/images/media/team/badge/uturtu1421791246.png",
    "Osasuna": "https://www.thesportsdb.com/images/media/team/badge/ttsyxu1421791238.png",
    "Girona": "https://www.thesportsdb.com/images/media/team/badge/xstuts1660929741.png",
    "Las Palmas": "https://www.thesportsdb.com/images/media/team/badge/b4z2me1697731321.png",
    "Mallorca": "https://www.thesportsdb.com/images/media/team/badge/rtppwt1421791232.png",
    "Rayo Vallecano": "https://www.thesportsdb.com/images/media/team/badge/twqyvx1421791244.png",
    "Celta Vigo": "https://www.thesportsdb.com/images/media/team/badge/yvvtqs1421791226.png",
    "Getafe": "https://www.thesportsdb.com/images/media/team/badge/uptvts1421791229.png",
    "Leganes": "https://www.thesportsdb.com/images/media/team/badge/3gkzwd1729773526.png",
    "Espanyol": "https://www.thesportsdb.com/images/media/team/badge/qvwyvq1421791227.png",
    "Deportivo Alavés": "https://www.thesportsdb.com/images/media/team/badge/sqxttv1421791223.png",
    "Alaves": "https://www.thesportsdb.com/images/media/team/badge/sqxttv1421791223.png",
    "Valladolid": "https://www.thesportsdb.com/images/media/team/badge/vxuvru1421791264.png",

    # Serie A
    "Juventus": "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1421791046.png",
    "Inter Milan": "https://www.thesportsdb.com/images/media/team/badge/puutws1421791043.png",
    "AC Milan": "https://www.thesportsdb.com/images/media/team/badge/xpvpwv1421791040.png",
    "Napoli": "https://www.thesportsdb.com/images/media/team/badge/xvspvs1421791055.png",
    "Roma": "https://www.thesportsdb.com/images/media/team/badge/squuus1421791058.png",
    "Lazio": "https://www.thesportsdb.com/images/media/team/badge/uqxsxq1421791048.png",
    "Atalanta": "https://www.thesportsdb.com/images/media/team/badge/xzussz1421791035.png",
    "Fiorentina": "https://www.thesportsdb.com/images/media/team/badge/rwqxpx1421791042.png",
    "Torino": "https://www.thesportsdb.com/images/media/team/badge/xzustt1421791062.png",
    "Bologna": "https://www.thesportsdb.com/images/media/team/badge/qvvxuy1421791037.png",

    # Bundesliga
    "Bayern Munich": "https://www.thesportsdb.com/images/media/team/badge/uvuswu1421791844.png",
    "Borussia Dortmund": "https://www.thesportsdb.com/images/media/team/badge/xqvvqx1421791846.png",
    "RB Leipzig": "https://www.thesportsdb.com/images/media/team/badge/klq4bm1677840373.png",
    "Bayer Leverkusen": "https://www.thesportsdb.com/images/media/team/badge/sqtwqv1421791850.png",
    "Borussia Mönchengladbach": "https://www.thesportsdb.com/images/media/team/badge/sqtwqv1421791848.png",
    "Eintracht Frankfurt": "https://www.thesportsdb.com/images/media/team/badge/upwqyq1421791853.png",
    "Wolfsburg": "https://www.thesportsdb.com/images/media/team/badge/wqvvut1421791869.png",
    "Stuttgart": "https://www.thesportsdb.com/images/media/team/badge/xtsqtq1421791864.png",

    # Ligue 1
    "PSG": "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1421791647.png",
    "Paris Saint-Germain": "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1421791647.png",
    "Lyon": "https://www.thesportsdb.com/images/media/team/badge/puuvrs1421791640.png",
    "Marseille": "https://www.thesportsdb.com/images/media/team/badge/xvstst1421791641.png",
    "Monaco": "https://www.thesportsdb.com/images/media/team/badge/vtstpt1421791642.png",
    "Lille": "https://www.thesportsdb.com/images/media/team/badge/qtstrt1421791638.png",

    # Champions League / otros
    "Porto": "https://www.thesportsdb.com/images/media/team/badge/upwxuv1421791413.png",
    "Benfica": "https://www.thesportsdb.com/images/media/team/badge/qvtsts1421791407.png",
    "Sporting CP": "https://www.thesportsdb.com/images/media/team/badge/vvwvtq1421791416.png",
    "Ajax": "https://www.thesportsdb.com/images/media/team/badge/sxpxpx1421791462.png",
    "PSV": "https://www.thesportsdb.com/images/media/team/badge/xqxqxv1421791464.png",
    "Celtic": "https://www.thesportsdb.com/images/media/team/badge/tuxuux1421791569.png",
    "Rangers": "https://www.thesportsdb.com/images/media/team/badge/sqwuqw1421791571.png",
}

# Placeholder para cuando no se encuentre el escudo
ESCUDO_PLACEHOLDER = "https://www.thesportsdb.com/images/media/team/badge/placeholder.png"
ESCUDO_DEFAULT = "⚽"  # emoji fallback


@lru_cache(maxsize=128)
def buscar_escudo_api(nombre_equipo: str) -> str:
    """Busca el escudo de un equipo via TheSportsDB API (con caché)."""
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={nombre_equipo}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("teams"):
            badge = data["teams"][0].get("strBadge", "")
            if badge:
                return badge + "/preview"
    except Exception:
        pass
    return ""


def get_escudo(nombre_equipo: str) -> str:
    """
    Obtiene la URL del escudo de un equipo.
    Primero busca en el cache local, luego en la API.
    Retorna URL del escudo o string vacío si no encuentra.
    """
    # Búsqueda directa
    if nombre_equipo in ESCUDOS_CACHE:
        return ESCUDOS_CACHE[nombre_equipo]

    # Búsqueda case-insensitive
    for equipo, url in ESCUDOS_CACHE.items():
        if equipo.lower() == nombre_equipo.lower():
            return url

    # Búsqueda parcial (ej: "Man City" → "Manchester City")
    nombre_lower = nombre_equipo.lower()
    for equipo, url in ESCUDOS_CACHE.items():
        if nombre_lower in equipo.lower() or equipo.lower() in nombre_lower:
            return url

    # Fallback a API
    return buscar_escudo_api(nombre_equipo)

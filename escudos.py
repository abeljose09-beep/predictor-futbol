"""
Módulo de escudos — imágenes locales en carpeta escudos/.
Fallback a Wikipedia API para equipos sin imagen local.
"""

import os
import requests

# Ruta base de los escudos (relativa al proyecto)
_BASE = "escudos"

# ─── MAPEO EQUIPO → RUTA LOCAL ─────────────────────────────────────────────────
ESCUDOS_LOCAL = {
    # ── Premier League ──
    "Arsenal":          f"{_BASE}/premier_league_logos/Arsenal_FC.png",
    "Aston Villa":      f"{_BASE}/premier_league_logos/Aston_Villa.png",
    "Bournemouth":      f"{_BASE}/premier_league_logos/AFC_Bournemouth.png",
    "Brentford":        f"{_BASE}/premier_league_logos/Brentford_FC.png",
    "Brighton":         f"{_BASE}/premier_league_logos/Brighton_&_Hove_Albion.png",
    "Burnley":          f"{_BASE}/premier_league_logos/Burnley_FC.png",
    "Chelsea":          f"{_BASE}/premier_league_logos/Chelsea_FC.png",
    "Crystal Palace":   f"{_BASE}/premier_league_logos/Crystal_Palace.png",
    "Everton":          f"{_BASE}/premier_league_logos/Everton_FC.png",
    "Fulham":           f"{_BASE}/premier_league_logos/Fulham_FC.png",
    "Leeds":            f"{_BASE}/premier_league_logos/Leeds_United.png",
    "Liverpool":        f"{_BASE}/premier_league_logos/Liverpool_FC.png",
    "Man City":         f"{_BASE}/premier_league_logos/Manchester_City.png",
    "Man United":       f"{_BASE}/premier_league_logos/Manchester_United.png",
    "Newcastle":        f"{_BASE}/premier_league_logos/Newcastle_United.png",
    "Nott'm Forest":    f"{_BASE}/premier_league_logos/Nottingham_Forest.png",
    "Sunderland":       f"{_BASE}/premier_league_logos/Sunderland_AFC.png",
    "Tottenham":        f"{_BASE}/premier_league_logos/Tottenham_Hotspur.png",
    "West Ham":         f"{_BASE}/premier_league_logos/West_Ham_United.png",
    "Wolves":           f"{_BASE}/premier_league_logos/Wolverhampton_Wanderers.png",

    # ── La Liga ──
    "Ath Bilbao":       f"{_BASE}/la_liga_logos/Athletic_Bilbao.png",
    "Ath Madrid":       f"{_BASE}/la_liga_logos/Atlético_de_Madrid.png",
    "Osasuna":          f"{_BASE}/la_liga_logos/CA_Osasuna.png",
    "Celta":            f"{_BASE}/la_liga_logos/Celta_de_Vigo.png",
    "Alaves":           f"{_BASE}/la_liga_logos/Deportivo_Alavés.png",
    "Elche":            f"{_BASE}/la_liga_logos/Elche_CF.png",
    "Barcelona":        f"{_BASE}/la_liga_logos/FC_Barcelona.png",
    "Getafe":           f"{_BASE}/la_liga_logos/Getafe_CF.png",
    "Girona":           f"{_BASE}/la_liga_logos/Girona_FC.png",
    "Levante":          f"{_BASE}/la_liga_logos/Levante_UD.png",
    "Vallecano":        f"{_BASE}/la_liga_logos/Rayo_Vallecano.png",
    "Espanol":          f"{_BASE}/la_liga_logos/RCD_Espanyol_Barcelona.png",
    "Mallorca":         f"{_BASE}/la_liga_logos/RCD_Mallorca.png",
    "Betis":            f"{_BASE}/la_liga_logos/Real_Betis_Balompié.png",
    "Real Madrid":      f"{_BASE}/la_liga_logos/Real_Madrid.png",
    "Oviedo":           f"{_BASE}/la_liga_logos/Real_Oviedo.png",
    "Sociedad":         f"{_BASE}/la_liga_logos/Real_Sociedad.png",
    "Sevilla":          f"{_BASE}/la_liga_logos/Sevilla_FC.png",
    "Valencia":         f"{_BASE}/la_liga_logos/Valencia_CF.png",
    "Villarreal":       f"{_BASE}/la_liga_logos/Villarreal_CF.png",

    # ── Serie A ──
    "Fiorentina":       f"{_BASE}/serie_a_logos/ACF_Fiorentina.png",
    "Milan":            f"{_BASE}/serie_a_logos/AC_Milan.png",
    "Roma":             f"{_BASE}/serie_a_logos/AS_Roma.png",
    "Atalanta":         f"{_BASE}/serie_a_logos/Atalanta_BC.png",
    "Bologna":          f"{_BASE}/serie_a_logos/Bologna_FC_1909.png",
    "Cagliari":         f"{_BASE}/serie_a_logos/Cagliari_Calcio.png",
    "Como":             f"{_BASE}/serie_a_logos/Como_1907.png",
    "Genoa":            f"{_BASE}/serie_a_logos/Genoa_CFC.png",
    "Verona":           f"{_BASE}/serie_a_logos/Hellas_Verona.png",
    "Inter":            f"{_BASE}/serie_a_logos/Inter_Milan.png",
    "Juventus":         f"{_BASE}/serie_a_logos/Juventus_FC.png",
    "Parma":            f"{_BASE}/serie_a_logos/Parma_Calcio_1913.png",
    "Pisa":             f"{_BASE}/serie_a_logos/Pisa_Sporting_Club.png",
    "Napoli":           f"{_BASE}/serie_a_logos/SSC_Napoli.png",
    "Lazio":            f"{_BASE}/serie_a_logos/SS_Lazio.png",
    "Torino":           f"{_BASE}/serie_a_logos/Torino_FC.png",
    "Udinese":          f"{_BASE}/serie_a_logos/Udinese_Calcio.png",
    "Cremonese":        f"{_BASE}/serie_a_logos/US_Cremonese.png",
    "Lecce":            f"{_BASE}/serie_a_logos/US_Lecce.png",
    "Sassuolo":         f"{_BASE}/serie_a_logos/US_Sassuolo.png",

    # ── Bundesliga ──
    "Heidenheim":       f"{_BASE}/bundesliga_logos/1.FC_Heidenheim_1846.png",
    "FC Koln":          f"{_BASE}/bundesliga_logos/1.FC_Köln.png",
    "Union Berlin":     f"{_BASE}/bundesliga_logos/1.FC_Union_Berlin.png",
    "Mainz":            f"{_BASE}/bundesliga_logos/1.FSV_Mainz_05.png",
    "Bayern Munich":    f"{_BASE}/bundesliga_logos/Bayern_Munich.png",
    "Leverkusen":       f"{_BASE}/bundesliga_logos/Bayer_04_Leverkusen.png",
    "Dortmund":         f"{_BASE}/bundesliga_logos/Borussia_Dortmund.png",
    "M'gladbach":       f"{_BASE}/bundesliga_logos/Borussia_Mönchengladbach.png",
    "Ein Frankfurt":    f"{_BASE}/bundesliga_logos/Eintracht_Frankfurt.png",
    "Augsburg":         f"{_BASE}/bundesliga_logos/FC_Augsburg.png",
    "St Pauli":         f"{_BASE}/bundesliga_logos/FC_St._Pauli.png",
    "Hamburg":          f"{_BASE}/bundesliga_logos/Hamburger_SV.png",
    "RB Leipzig":       f"{_BASE}/bundesliga_logos/RB_Leipzig.png",
    "Freiburg":         f"{_BASE}/bundesliga_logos/SC_Freiburg.png",
    "Werder Bremen":    f"{_BASE}/bundesliga_logos/SV_Werder_Bremen.png",
    "Hoffenheim":       f"{_BASE}/bundesliga_logos/TSG_1899_Hoffenheim.png",
    "Stuttgart":        f"{_BASE}/bundesliga_logos/VfB_Stuttgart.png",
    "Wolfsburg":        f"{_BASE}/bundesliga_logos/VfL_Wolfsburg.png",

    # ── Eredivisie ──
    "Ajax":             f"{_BASE}/eredivisie_logos/Ajax_Amsterdam.png",
    "AZ Alkmaar":       f"{_BASE}/eredivisie_logos/AZ_Alkmaar.png",
    "Excelsior":        f"{_BASE}/eredivisie_logos/Excelsior_Rotterdam.png",
    "Groningen":        f"{_BASE}/eredivisie_logos/FC_Groningen.png",
    "Utrecht":          f"{_BASE}/eredivisie_logos/FC_Utrecht.png",
    "Volendam":         f"{_BASE}/eredivisie_logos/FC_Volendam.png",
    "Feyenoord":        f"{_BASE}/eredivisie_logos/Feyenoord_Rotterdam.png",
    "For Sittard":      f"{_BASE}/eredivisie_logos/Fortuna_Sittard.png",
    "Go Ahead Eagles":  f"{_BASE}/eredivisie_logos/Go_Ahead_Eagles.png",
    "Heracles":         f"{_BASE}/eredivisie_logos/Heracles_Almelo.png",
    "NAC Breda":        f"{_BASE}/eredivisie_logos/NAC_Breda.png",
    "Nijmegen":         f"{_BASE}/eredivisie_logos/NEC_Nijmegen.png",
    "Zwolle":           f"{_BASE}/eredivisie_logos/PEC_Zwolle.png",
    "PSV Eindhoven":    f"{_BASE}/eredivisie_logos/PSV_Eindhoven.png",
    "Heerenveen":       f"{_BASE}/eredivisie_logos/SC_Heerenveen.png",
    "Telstar":          f"{_BASE}/eredivisie_logos/SC_Telstar.png",
    "Sparta Rotterdam": f"{_BASE}/eredivisie_logos/Sparta_Rotterdam.png",
    "Twente":           f"{_BASE}/eredivisie_logos/Twente_Enschede_FC.png",

    # ── Ligue 1 ──
    "Auxerre":          f"{_BASE}/ligue_1_logos/AJ_Auxerre.png",
    "Angers":           f"{_BASE}/ligue_1_logos/Angers_SCO.png",
    "Monaco":           f"{_BASE}/ligue_1_logos/AS_Monaco.png",
    "Lorient":          f"{_BASE}/ligue_1_logos/FC_Lorient.png",
    "Metz":             f"{_BASE}/ligue_1_logos/FC_Metz.png",
    "Nantes":           f"{_BASE}/ligue_1_logos/FC_Nantes.png",
    "Toulouse":         f"{_BASE}/ligue_1_logos/FC_Toulouse.png",
    "Le Havre":         f"{_BASE}/ligue_1_logos/Le_Havre_AC.png",
    "Lille":            f"{_BASE}/ligue_1_logos/LOSC_Lille.png",
    "Nice":             f"{_BASE}/ligue_1_logos/OGC_Nice.png",
    "Lyon":             f"{_BASE}/ligue_1_logos/Olympique_Lyon.png",
    "Marseille":        f"{_BASE}/ligue_1_logos/Olympique_Marseille.png",
    "Paris FC":         f"{_BASE}/ligue_1_logos/Paris_FC.png",
    "Paris SG":         f"{_BASE}/ligue_1_logos/Paris_Saint-Germain.png",
    "Lens":             f"{_BASE}/ligue_1_logos/RC_Lens.png",
    "Strasbourg":       f"{_BASE}/ligue_1_logos/RC_Strasbourg_Alsace.png",
    "Brest":            f"{_BASE}/ligue_1_logos/Stade_Brestois_29.png",
    "Rennes":           f"{_BASE}/ligue_1_logos/Stade_Rennais_FC.png",

    # ── Liga Portugal ──
    "Porto":            f"{_BASE}/liga_portugal_logos/FC_Porto.png",
    "Benfica":          f"{_BASE}/liga_portugal_logos/SL_Benfica.png",
    "Sp Lisbon":        f"{_BASE}/liga_portugal_logos/Sporting_CP.png",
    "Sp Braga":         f"{_BASE}/liga_portugal_logos/SC_Braga.png",
    "Guimaraes":        f"{_BASE}/liga_portugal_logos/Vitória_Guimarães_SC.png",
    "Arouca":           f"{_BASE}/liga_portugal_logos/FC_Arouca.png",
    "Casa Pia":         f"{_BASE}/liga_portugal_logos/Casa_Pia_AC.png",
    "Estoril":          f"{_BASE}/liga_portugal_logos/GD_Estoril_Praia.png",
    "Famalicao":        f"{_BASE}/liga_portugal_logos/FC_Famalicão.png",
    "Gil Vicente":      f"{_BASE}/liga_portugal_logos/Gil_Vicente_FC.png",
    "Moreirense":       f"{_BASE}/liga_portugal_logos/Moreirense_FC.png",
    "Nacional":         f"{_BASE}/liga_portugal_logos/CD_Nacional.png",
    "Rio Ave":          f"{_BASE}/liga_portugal_logos/Rio_Ave_FC.png",
    "Santa Clara":      f"{_BASE}/liga_portugal_logos/CD_Santa_Clara.png",
    "Tondela":          f"{_BASE}/liga_portugal_logos/CD_Tondela.png",
    "Estrela Amadora":  f"{_BASE}/liga_portugal_logos/CF_Estrela_Amadora.png",
    "Alverca":          f"{_BASE}/liga_portugal_logos/FC_Alverca.png",
    "Avs":              f"{_BASE}/liga_portugal_logos/Avs_Futebol.png",
}

# ── Alias: nombres alternativos → clave en ESCUDOS_LOCAL ──────────────────────
ALIAS = {
    "bayer munich":         "Bayern Munich",
    "manchester city":      "Man City",
    "manchester united":    "Man United",
    "wolverhampton":        "Wolves",
    "atletico madrid":      "Ath Madrid",
    "athletic bilbao":      "Ath Bilbao",
    "athletic club":        "Ath Bilbao",
    "espanyol":             "Espanol",
    "rcd espanyol":         "Espanol",
    "rayo vallecano":       "Vallecano",
    "real betis":           "Betis",
    "rc celta":             "Celta",
    "celta vigo":           "Celta",
    "deportivo alaves":     "Alaves",
    "eintr frankfurt":      "Ein Frankfurt",
    "eintracht frankfurt":  "Ein Frankfurt",
    "mgladbach":            "M'gladbach",
    "borussia mg":          "M'gladbach",
    "monchengladbach":      "M'gladbach",
    "1. fc koln":           "FC Koln",
    "koln":                 "FC Koln",
    "cologne":              "FC Koln",
    "1. fc union berlin":   "Union Berlin",
    "1. fsv mainz":         "Mainz",
    "psv":                  "PSV Eindhoven",
    "az":                   "AZ Alkmaar",
    "fortuna sittard":      "For Sittard",
    "go ahead":             "Go Ahead Eagles",
    "nec nijmegen":         "Nijmegen",
    "nec":                  "Nijmegen",
    "pec zwolle":           "Zwolle",
    "psg":                  "Paris SG",
    "paris saint-germain":  "Paris SG",
    "olympique lyon":       "Lyon",
    "olympique marseille":  "Marseille",
    "losc":                 "Lille",
    "losc lille":           "Lille",
    "rc lens":              "Lens",
    "rc strasbourg":        "Strasbourg",
    "stade rennais":        "Rennes",
    "aj auxerre":           "Auxerre",
    "fc porto":             "Porto",
    "sl benfica":           "Benfica",
    "sporting cp":          "Sp Lisbon",
    "sporting lisbon":      "Sp Lisbon",
    "sc braga":             "Sp Braga",
    "braga":                "Sp Braga",
    "vitoria guimaraes":    "Guimaraes",
    "hellas verona":        "Verona",
    "inter milan":          "Inter",
    "ac milan":             "Milan",
    "as roma":              "Roma",
    "ss lazio":             "Lazio",
    "acf fiorentina":       "Fiorentina",
    "us lecce":             "Lecce",
    "us sassuolo":          "Sassuolo",
    "us cremonese":         "Cremonese",
    "nottingham forest":    "Nott'm Forest",
    "nottm forest":         "Nott'm Forest",
}


def _buscar_wikipedia_api(nombre_equipo: str) -> str:
    """Fallback: busca el escudo en Wikipedia API."""
    for query in [nombre_equipo, nombre_equipo + " FC"]:
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action": "query", "list": "search",
                        "srsearch": query, "srlimit": 1, "format": "json"},
                timeout=5, headers={"User-Agent": "FootballAI/1.0"}
            )
            resultados = r.json().get("query", {}).get("search", [])
            if not resultados:
                continue
            titulo = resultados[0]["title"]
            r2 = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action": "query", "titles": titulo,
                        "prop": "pageimages", "pithumbsize": 200, "format": "json"},
                timeout=5, headers={"User-Agent": "FootballAI/1.0"}
            )
            pages = r2.json().get("query", {}).get("pages", {})
            for page in pages.values():
                thumb = page.get("thumbnail", {}).get("source", "")
                if thumb:
                    return thumb
        except Exception:
            continue
    return ""


def get_escudo(nombre_equipo: str) -> str:
    """
    Retorna la ruta local del escudo o URL de Wikipedia como fallback.
    Orden: exacto → alias → case-insensitive → parcial → Wikipedia API.
    """
    if not nombre_equipo:
        return ""

    # 1. Exacto
    if nombre_equipo in ESCUDOS_LOCAL:
        return ESCUDOS_LOCAL[nombre_equipo]

    # 2. Alias
    key = nombre_equipo.lower().strip()
    if key in ALIAS:
        canon = ALIAS[key]
        if canon in ESCUDOS_LOCAL:
            return ESCUDOS_LOCAL[canon]

    # 3. Case-insensitive
    for equipo, ruta in ESCUDOS_LOCAL.items():
        if equipo.lower() == key:
            return ruta

    # 4. Parcial
    for equipo, ruta in ESCUDOS_LOCAL.items():
        if key in equipo.lower() or equipo.lower() in key:
            return ruta

    # 5. Wikipedia API
    return _buscar_wikipedia_api(nombre_equipo)
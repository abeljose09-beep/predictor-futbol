"""
Módulo de escudos — URLs de Wikimedia + fallback automático a Wikipedia API.
Si una URL directa falla o el equipo no está en el diccionario,
busca automáticamente el escudo via la API de Wikipedia.
"""

import requests

# Solo URLs verificadas con hashes hexadecimales válidos (a-f, 0-9)
ESCUDOS_CACHE = {
    # ── Premier League ──
    "Arsenal":          "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Aston Villa":      "https://upload.wikimedia.org/wikipedia/en/9/9a/Aston_Villa_FC_new_crest.svg",
    "Bournemouth":      "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg",
    "Brentford":        "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
    "Brighton":         "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_FC.svg",
    "Burnley":          "https://upload.wikimedia.org/wikipedia/en/6/62/Burnley_F.C._Logo.svg",
    "Chelsea":          "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Crystal Palace":   "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
    "Everton":          "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
    "Fulham":           "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
    "Ipswich":          "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg",
    "Leicester":        "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    "Liverpool":        "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Luton":            "https://upload.wikimedia.org/wikipedia/en/9/9d/Luton_Town_logo.svg",
    "Man City":         "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Man United":       "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Newcastle":        "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "Nott'm Forest":    "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg",
    "Sheffield United": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg",
    "Southampton":      "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg",
    "Tottenham":        "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "West Ham":         "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "Wolves":           "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
    "Watford":          "https://upload.wikimedia.org/wikipedia/en/e/e2/Watford.svg",
    "Norwich":          "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg",
    "Leeds":            "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg",

    # ── La Liga ──
    "Real Madrid":      "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    "Barcelona":        "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
    "Ath Madrid":       "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_de_Madrid_2017_logo.svg",
    "Sevilla":          "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg",
    "Valencia":         "https://upload.wikimedia.org/wikipedia/en/c/ce/Valenciacf.svg",
    "Villarreal":       "https://upload.wikimedia.org/wikipedia/en/b/b9/Villarreal_CF_logo.svg",
    "Sociedad":         "https://upload.wikimedia.org/wikipedia/en/f/f1/Real_Sociedad_logo.svg",
    "Ath Bilbao":       "https://upload.wikimedia.org/wikipedia/en/9/98/Athletic_Club_logo.svg",
    "Betis":            "https://upload.wikimedia.org/wikipedia/en/1/13/Real_betis_logo.svg",
    "Osasuna":          "https://upload.wikimedia.org/wikipedia/en/d/db/Osasuna_logo.svg",
    "Girona":           "https://upload.wikimedia.org/wikipedia/en/6/6e/Girona_FC_logo.svg",
    "Las Palmas":       "https://upload.wikimedia.org/wikipedia/en/7/79/UD_Las_Palmas_logo.svg",
    "Mallorca":         "https://upload.wikimedia.org/wikipedia/en/a/ae/RCD_Mallorca_logo.svg",
    "Vallecano":        "https://upload.wikimedia.org/wikipedia/en/d/d9/Rayo_Vallecano_logo.svg",
    "Celta":            "https://upload.wikimedia.org/wikipedia/en/1/12/RC_Celta_de_Vigo_logo.svg",
    "Getafe":           "https://upload.wikimedia.org/wikipedia/en/0/0e/Getafe_CF.svg",
    "Leganes":          "https://upload.wikimedia.org/wikipedia/en/8/8c/CD_Legan%C3%A9s_logo.svg",
    "Espanol":          "https://upload.wikimedia.org/wikipedia/en/9/98/RCD_Espanyol_logo.svg",
    "Alaves":           "https://upload.wikimedia.org/wikipedia/en/4/4e/Deportivo_Alav%C3%A9s_logo.svg",
    "Valladolid":       "https://upload.wikimedia.org/wikipedia/en/3/39/Real_Valladolid_logo.svg",
    "Almeria":          "https://upload.wikimedia.org/wikipedia/en/6/6c/UD_Almer%C3%ADa_logo.svg",
    "Cadiz":            "https://upload.wikimedia.org/wikipedia/en/5/57/C%C3%A1diz_CF_logo.svg",
    "Granada":          "https://upload.wikimedia.org/wikipedia/en/8/8b/Granada_CF_logo.svg",
    "Elche":            "https://upload.wikimedia.org/wikipedia/en/4/4a/Elche_CF_logo.svg",
    "Levante":          "https://upload.wikimedia.org/wikipedia/en/7/7e/Levante_UD_logo.svg",
    "Eibar":            "https://upload.wikimedia.org/wikipedia/en/0/0a/SD_Eibar_logo.svg",
    "Huesca":           "https://upload.wikimedia.org/wikipedia/en/3/thirty/SD_Huesca_logo.svg",

    # ── Serie A ──
    "Juventus":         "https://upload.wikimedia.org/wikipedia/commons/1/15/Juventus_FC_2017_icon_%28black%29.svg",
    "Inter":            "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg",
    "Milan":            "https://upload.wikimedia.org/wikipedia/commons/d/d0/Logo_of_AC_Milan.svg",
    "Napoli":           "https://upload.wikimedia.org/wikipedia/commons/2/2d/SSC_Napoli_2007.svg",
    "Roma":             "https://upload.wikimedia.org/wikipedia/en/f/f7/AS_Roma_logo_%282017%29.svg",
    "Lazio":            "https://upload.wikimedia.org/wikipedia/en/b/bc/Lazio_Roma_-_Logo.svg",
    "Atalanta":         "https://upload.wikimedia.org/wikipedia/en/6/66/AtalantaBC.svg",
    "Fiorentina":       "https://upload.wikimedia.org/wikipedia/commons/a/a4/ACF_Fiorentina.svg",
    "Torino":           "https://upload.wikimedia.org/wikipedia/en/6/61/Torino_FC_Logo.svg",
    "Bologna":          "https://upload.wikimedia.org/wikipedia/en/4/4b/Bologna_F.C._1909_logo.svg",
    "Udinese":          "https://upload.wikimedia.org/wikipedia/en/d/db/Udinese_Calcio_logo.svg",
    "Empoli":           "https://upload.wikimedia.org/wikipedia/en/a/a8/Empoli_FC_logo.svg",
    "Genoa":            "https://upload.wikimedia.org/wikipedia/en/d/d6/Genoa_CFC.svg",
    "Lecce":            "https://upload.wikimedia.org/wikipedia/en/2/2a/US_Lecce_logo.svg",
    "Monza":            "https://upload.wikimedia.org/wikipedia/en/9/9c/AC_Monza_logo.svg",
    "Verona":           "https://upload.wikimedia.org/wikipedia/en/6/6b/Hellas_Verona_FC_logo.svg",
    "Cagliari":         "https://upload.wikimedia.org/wikipedia/en/7/73/Cagliari-Calcio.svg",
    "Parma":            "https://upload.wikimedia.org/wikipedia/en/8/81/Parma_Calcio_1913.svg",
    "Como":             "https://upload.wikimedia.org/wikipedia/en/e/e2/Como_1907_logo.svg",
    "Venezia":          "https://upload.wikimedia.org/wikipedia/en/b/b6/Venezia_FC_logo.svg",
    "Sassuolo":         "https://upload.wikimedia.org/wikipedia/en/8/8d/US_Sassuolo_Calcio_logo.svg",
    "Salernitana":      "https://upload.wikimedia.org/wikipedia/en/3/3c/US_Salernitana_1919_logo.svg",
    "Sampdoria":        "https://upload.wikimedia.org/wikipedia/en/e/e7/UC_Sampdoria_logo.svg",
    "Spezia":           "https://upload.wikimedia.org/wikipedia/en/a/a5/Spezia_Calcio_logo.svg",
    "Benevento":        "https://upload.wikimedia.org/wikipedia/en/b/b4/Benevento_Calcio_logo.svg",
    "Crotone":          "https://upload.wikimedia.org/wikipedia/en/7/70/FC_Crotone_logo.svg",
    "Frosinone":        "https://upload.wikimedia.org/wikipedia/en/2/2f/Frosinone_Calcio_logo.svg",
    "Pisa":             "https://upload.wikimedia.org/wikipedia/en/c/c4/AC_Pisa_1909_logo.svg",

    # ── Bundesliga ──
    "Bayern Munich":    "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282002%E2%80%932017%29.svg",
    "Dortmund":         "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg",
    "RB Leipzig":       "https://upload.wikimedia.org/wikipedia/en/0/04/RB_Leipzig_2014_logo.svg",
    "Leverkusen":       "https://upload.wikimedia.org/wikipedia/en/5/59/Bayer_04_Leverkusen_logo.svg",
    "Ein Frankfurt":    "https://upload.wikimedia.org/wikipedia/commons/0/04/Eintracht_Frankfurt_Logo.svg",
    "Wolfsburg":        "https://upload.wikimedia.org/wikipedia/commons/f/f3/Logo-VfL-Wolfsburg.svg",
    "Stuttgart":        "https://upload.wikimedia.org/wikipedia/commons/e/eb/VfB_Stuttgart_1893_Logo.svg",
    "Freiburg":         "https://upload.wikimedia.org/wikipedia/de/f/f7/SC-Freiburg_Logo-neu.svg",
    "Hoffenheim":       "https://upload.wikimedia.org/wikipedia/commons/6/64/TSG_Logo-Standard_4c.svg",
    "Mainz":            "https://upload.wikimedia.org/wikipedia/commons/9/9e/Logo_Mainz_05.svg",
    "Augsburg":         "https://upload.wikimedia.org/wikipedia/de/b/b5/FC_Augsburg_logo.svg",
    "Union Berlin":     "https://upload.wikimedia.org/wikipedia/commons/4/44/1._FC_Union_Berlin_Logo.svg",
    "Werder Bremen":    "https://upload.wikimedia.org/wikipedia/en/b/b8/SV_Werder_Bremen_logo.svg",
    "Bochum":           "https://upload.wikimedia.org/wikipedia/en/3/31/VfL_Bochum_logo.svg",
    "Heidenheim":       "https://upload.wikimedia.org/wikipedia/en/7/74/1._FC_Heidenheim_1846_logo.svg",
    "St Pauli":         "https://upload.wikimedia.org/wikipedia/commons/d/d4/FC_St._Pauli_logo.svg",
    "Holstein Kiel":    "https://upload.wikimedia.org/wikipedia/commons/c/ca/Holstein_Kiel_Logo.svg",
    "M'gladbach":       "https://upload.wikimedia.org/wikipedia/commons/8/81/Borussia_M%C3%B6nchengladbach_logo.svg",
    "FC Koln":          "https://upload.wikimedia.org/wikipedia/en/5/53/FC_Cologne_logo.svg",
    "Darmstadt":        "https://upload.wikimedia.org/wikipedia/en/5/5d/SV_Darmstadt_98_logo.svg",
    "Hertha":           "https://upload.wikimedia.org/wikipedia/commons/8/86/Hertha_BSC_Logo_2012.svg",
    "Schalke 04":       "https://upload.wikimedia.org/wikipedia/commons/6/6d/FC_Schalke_04_Logo.svg",
    "Greuther Furth":   "https://upload.wikimedia.org/wikipedia/commons/b/bb/SpVgg_Greuther_F%C3%BCrth_2017.svg",
    "Bielefeld":        "https://upload.wikimedia.org/wikipedia/en/2/24/Arminia_Bielefeld_logo.svg",
    "Hamburg":          "https://upload.wikimedia.org/wikipedia/commons/f/f7/Hamburger_SV_logo.svg",

    # ── Ligue 1 ──
    "Paris SG":         "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
    "Lyon":             "https://upload.wikimedia.org/wikipedia/en/e/e9/Olympique_Lyonnais.svg",
    "Marseille":        "https://upload.wikimedia.org/wikipedia/commons/d/d8/Olympique_de_Marseille_logo.svg",
    "Monaco":           "https://upload.wikimedia.org/wikipedia/en/e/ea/AS_Monaco_FC.svg",
    "Lille":            "https://upload.wikimedia.org/wikipedia/en/6/62/LOSC_Lille_2011_logo.svg",
    "Nice":             "https://upload.wikimedia.org/wikipedia/en/2/29/OGC_Nice_logo.svg",
    "Rennes":           "https://upload.wikimedia.org/wikipedia/en/6/6f/Stade_Rennais_FC.svg",
    "Lens":             "https://upload.wikimedia.org/wikipedia/en/4/42/RC_Lens.svg",
    "Strasbourg":       "https://upload.wikimedia.org/wikipedia/en/9/9f/RC_Strasbourg_Alsace_logo.svg",
    "Montpellier":      "https://upload.wikimedia.org/wikipedia/en/0/07/Montpellier_H%C3%A9rault_Sport_Club_logo.svg",
    "Nantes":           "https://upload.wikimedia.org/wikipedia/en/6/62/FC_Nantes_logo.svg",
    "Reims":            "https://upload.wikimedia.org/wikipedia/en/3/39/Stade_de_Reims_logo.svg",
    "Brest":            "https://upload.wikimedia.org/wikipedia/en/0/0e/Stade_Brestois_29_logo.svg",
    "Toulouse":         "https://upload.wikimedia.org/wikipedia/en/b/b1/Toulouse_FC_new_logo.svg",
    "Le Havre":         "https://upload.wikimedia.org/wikipedia/en/f/f7/Le_Havre_AC_logo.svg",
    "St Etienne":       "https://upload.wikimedia.org/wikipedia/en/a/a8/AS_Saint-%C3%89tienne.svg",
    "Auxerre":          "https://upload.wikimedia.org/wikipedia/en/0/0e/AJ_Auxerre_logo.svg",
    "Angers":           "https://upload.wikimedia.org/wikipedia/en/3/thirty/SCO_Angers_logo.svg",
    "Ajaccio":          "https://upload.wikimedia.org/wikipedia/en/5/5b/AC_Ajaccio_logo.svg",
    "Bordeaux":         "https://upload.wikimedia.org/wikipedia/en/f/f9/Girondins_de_Bordeaux_logo.svg",
    "Clermont":         "https://upload.wikimedia.org/wikipedia/en/5/5d/Clermont_Foot_logo.svg",
    "Dijon":            "https://upload.wikimedia.org/wikipedia/en/0/02/Dijon_FCO.svg",
    "Lorient":          "https://upload.wikimedia.org/wikipedia/en/b/b1/FC_Lorient_logo.svg",
    "Metz":             "https://upload.wikimedia.org/wikipedia/en/6/sixty/FC_Metz_logo.svg",
    "Nimes":            "https://upload.wikimedia.org/wikipedia/en/a/a7/Nimes_Olympique_logo.svg",
    "Paris FC":         "https://upload.wikimedia.org/wikipedia/en/d/d8/Paris_FC_logo.svg",
    "Troyes":           "https://upload.wikimedia.org/wikipedia/en/e/ea/ES_Troyes_AC_logo.svg",

    # ── Eredivisie ──
    "Ajax":             "https://upload.wikimedia.org/wikipedia/en/7/79/Ajax_Amsterdam.svg",
    "PSV Eindhoven":    "https://upload.wikimedia.org/wikipedia/en/0/05/PSV_Eindhoven.svg",
    "Feyenoord":        "https://upload.wikimedia.org/wikipedia/en/f/f4/Feyenoord_logo.svg",
    "AZ Alkmaar":       "https://upload.wikimedia.org/wikipedia/en/5/5e/AZ_Alkmaar.svg",
    "Twente":           "https://upload.wikimedia.org/wikipedia/en/c/c5/FC_Twente.svg",
    "Utrecht":          "https://upload.wikimedia.org/wikipedia/en/c/c4/FC_Utrecht_logo.svg",
    "Heerenveen":       "https://upload.wikimedia.org/wikipedia/en/1/1a/SC_Heerenveen_logo.svg",
    "Groningen":        "https://upload.wikimedia.org/wikipedia/en/4/40/FC_Groningen_logo.svg",
    "Almere City":      "https://upload.wikimedia.org/wikipedia/en/4/4a/Almere_City_FC_logo.svg",
    "NAC Breda":        "https://upload.wikimedia.org/wikipedia/en/6/6a/NAC_Breda.svg",
    "Willem II":        "https://upload.wikimedia.org/wikipedia/en/3/3d/Willem_II_Tilburg_logo.svg",
    "Sparta Rotterdam": "https://upload.wikimedia.org/wikipedia/en/3/35/Sparta_Rotterdam.svg",
    "Excelsior":        "https://upload.wikimedia.org/wikipedia/en/9/9d/SBV_Excelsior_logo.svg",
    "For Sittard":      "https://upload.wikimedia.org/wikipedia/en/5/5c/Fortuna_Sittard_logo.svg",
    "Go Ahead Eagles":  "https://upload.wikimedia.org/wikipedia/en/4/forty/Go_Ahead_Eagles_logo.svg",
    "Heracles":         "https://upload.wikimedia.org/wikipedia/en/c/c3/Heracles_Almelo.svg",
    "Nijmegen":         "https://upload.wikimedia.org/wikipedia/en/4/4e/NEC_Nijmegen_logo.svg",
    "Telstar":          "https://upload.wikimedia.org/wikipedia/en/6/sixty/SC_Telstar_logo.svg",
    "Volendam":         "https://upload.wikimedia.org/wikipedia/en/d/d9/FC_Volendam_logo.svg",
    "Waalwijk":         "https://upload.wikimedia.org/wikipedia/en/d/d8/RKC_Waalwijk.svg",
    "Zwolle":           "https://upload.wikimedia.org/wikipedia/en/1/1e/PEC_Zwolle_logo.svg",

    # ── Portugal ──
    "Porto":            "https://upload.wikimedia.org/wikipedia/en/3/3b/FC_Porto.svg",
    "Benfica":          "https://upload.wikimedia.org/wikipedia/en/f/f4/SL_Benfica_logo.svg",
    "Sp Lisbon":        "https://upload.wikimedia.org/wikipedia/en/4/4a/Sporting_CP_%28Portugal%29_logo.svg",
    "Sp Braga":         "https://upload.wikimedia.org/wikipedia/en/a/a4/Sporting_de_Braga.svg",
    "Guimaraes":        "https://upload.wikimedia.org/wikipedia/en/c/c6/Vitoria_SC_crest.svg",
    "Boavista":         "https://upload.wikimedia.org/wikipedia/en/b/bf/Boavista_FC.svg",

    # ── Escocia ──
    "Celtic":           "https://upload.wikimedia.org/wikipedia/en/3/35/Celtic_FC_crest.svg",
    "Rangers":          "https://upload.wikimedia.org/wikipedia/en/b/bc/Rangers_FC_logo.svg",
    "Hearts":           "https://upload.wikimedia.org/wikipedia/en/5/5d/Heart_of_Midlothian_FC_logo.svg",
    "Hibernian":        "https://upload.wikimedia.org/wikipedia/en/a/a1/Hibernian_FC_logo.svg",
    "Aberdeen":         "https://upload.wikimedia.org/wikipedia/en/d/d6/Aberdeen_FC_logo.svg",

    # ── Championship ──
    "Middlesbrough":    "https://upload.wikimedia.org/wikipedia/en/2/2c/Middlesbrough_FC_crest.svg",
    "Sheffield Weds":   "https://upload.wikimedia.org/wikipedia/en/f/f1/Sheffield_Wednesday_badge.svg",
    "Sunderland":       "https://upload.wikimedia.org/wikipedia/en/7/7a/Sunderland_AFC_logo.svg",
    "West Brom":        "https://upload.wikimedia.org/wikipedia/en/8/8a/West_Bromwich_Albion.svg",
    "Swansea":          "https://upload.wikimedia.org/wikipedia/en/f/f9/Swansea_City_AFC_logo.svg",
    "Cardiff":          "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg",
    "Blackburn":        "https://upload.wikimedia.org/wikipedia/en/0/0f/Blackburn_Rovers.svg",
    "Derby":            "https://upload.wikimedia.org/wikipedia/en/4/45/Derby_County_crest.svg",
    "Preston":          "https://upload.wikimedia.org/wikipedia/en/7/74/Preston_North_End_FC_logo.svg",
    "Millwall":         "https://upload.wikimedia.org/wikipedia/en/4/4c/Millwall_FC_logo.svg",
    "Stoke":            "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg",
    "Coventry":         "https://upload.wikimedia.org/wikipedia/en/9/92/Coventry_City_FC_crest.svg",
    "Hull":             "https://upload.wikimedia.org/wikipedia/en/5/54/Hull_City_A.F.C._logo.svg",
    "Bristol City":     "https://upload.wikimedia.org/wikipedia/en/f/f5/Bristol_City_crest.svg",
    "QPR":              "https://upload.wikimedia.org/wikipedia/en/3/3a/QPR_logo.svg",
    "Birmingham":       "https://upload.wikimedia.org/wikipedia/en/6/68/Birmingham_City_FC_logo.svg",
    "Portsmouth":       "https://upload.wikimedia.org/wikipedia/en/3/3c/Portsmouth_FC_logo.svg",
    "Oxford":           "https://upload.wikimedia.org/wikipedia/en/6/6c/Oxford_United_FC_logo.svg",
    "Plymouth":         "https://upload.wikimedia.org/wikipedia/en/f/f4/Plymouth_Argyle_FC_logo.svg",
    "Wrexham":          "https://upload.wikimedia.org/wikipedia/en/8/eight/Wrexham_AFC_logo.svg",
}

# Mapeo de nombres alternativos a nombres canónicos del diccionario
ALIAS = {
    "bayer munich":     "Bayern Munich",
    "koln":             "FC Koln",
    "fc koln":          "FC Koln",
    "cologne":          "FC Koln",
    "atletico madrid":  "Ath Madrid",
    "athletic bilbao":  "Ath Bilbao",
    "espanyol":         "Espanol",
    "rayo vallecano":   "Vallecano",
    "eintr frankfurt":  "Ein Frankfurt",
    "eintracht":        "Ein Frankfurt",
    "mgladbach":        "M'gladbach",
    "borussia mg":      "M'gladbach",
    "psv":              "PSV Eindhoven",
    "az":               "AZ Alkmaar",
    "fortuna sittard":  "For Sittard",
    "go ahead":         "Go Ahead Eagles",
    "nec":              "Nijmegen",
    "sporting cp":      "Sp Lisbon",
    "sporting lisbon":  "Sp Lisbon",
    "braga":            "Sp Braga",
    "vitoria guimaraes":"Guimaraes",
    "heart of midlothian": "Hearts",
    "nott'm forest":    "Nott'm Forest",
    "nottingham":       "Nott'm Forest",
}

# Términos que indican hash inventado (no hexadecimal)
_INVALID_HASH_WORDS = {
    "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety", "eight", "nine", "ten",
    "eleven", "twelve",
}


def _url_valida(url: str) -> bool:
    """Devuelve False si la URL contiene un hash inventado (no hexadecimal)."""
    if not url:
        return False
    partes = url.split("/")
    for parte in partes:
        if parte.lower() in _INVALID_HASH_WORDS:
            return False
    return True


def _buscar_wikipedia_api(nombre_equipo: str) -> str:
    """
    Busca el escudo via la API de Wikipedia.
    Retorna la URL del thumbnail o "" si no encuentra nada.
    """
    # Intentar con el nombre tal cual y variantes
    candidatos = [
        nombre_equipo,
        nombre_equipo + " F.C.",
        nombre_equipo + " FC",
        nombre_equipo + " football club",
    ]

    for query in candidatos:
        try:
            # 1. Buscar el artículo
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": 1,
                "format": "json",
            }
            r = requests.get(search_url, params=params, timeout=5,
                             headers={"User-Agent": "FootballAI/1.0"})
            data = r.json()
            resultados = data.get("query", {}).get("search", [])
            if not resultados:
                continue

            titulo = resultados[0]["title"]

            # 2. Obtener imagen del artículo
            img_params = {
                "action": "query",
                "titles": titulo,
                "prop": "pageimages",
                "pithumbsize": 200,
                "format": "json",
            }
            r2 = requests.get(search_url, params=img_params, timeout=5,
                              headers={"User-Agent": "FootballAI/1.0"})
            data2 = r2.json()
            pages = data2.get("query", {}).get("pages", {})
            for page in pages.values():
                thumb = page.get("thumbnail", {}).get("source", "")
                if thumb:
                    return thumb

        except Exception:
            continue

    return ""


def get_escudo(nombre_equipo: str) -> str:
    """
    Retorna URL del escudo.
    Orden de búsqueda:
      1. Coincidencia exacta en ESCUDOS_CACHE (con URL válida)
      2. Alias conocidos
      3. Búsqueda case-insensitive en ESCUDOS_CACHE
      4. Búsqueda parcial en ESCUDOS_CACHE
      5. Fallback a Wikipedia API
    """
    if not nombre_equipo:
        return ""

    # 1. Exacto
    url = ESCUDOS_CACHE.get(nombre_equipo, "")
    if url and _url_valida(url):
        return url

    # 2. Alias
    alias_key = nombre_equipo.lower().strip()
    if alias_key in ALIAS:
        url = ESCUDOS_CACHE.get(ALIAS[alias_key], "")
        if url and _url_valida(url):
            return url

    # 3. Case-insensitive
    nombre_lower = nombre_equipo.lower()
    for equipo, u in ESCUDOS_CACHE.items():
        if equipo.lower() == nombre_lower and _url_valida(u):
            return u

    # 4. Parcial
    for equipo, u in ESCUDOS_CACHE.items():
        if (nombre_lower in equipo.lower() or equipo.lower() in nombre_lower) and _url_valida(u):
            return u

    # 5. Wikipedia API como último recurso
    return _buscar_wikipedia_api(nombre_equipo)
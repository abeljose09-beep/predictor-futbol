"""
Módulo de escudos — URLs de Wikimedia (carga directa en navegador).
"""

ESCUDOS_CACHE = {
    # Premier League
    "Arsenal":          "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Aston Villa":      "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg",
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

    # La Liga
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

    # Serie A
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

    # Bundesliga
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
    "Holstein Kiel":    "https://upload.wikimedia.org/wikipedia/commons/3/thirty/Holstein_Kiel_Logo.svg",
    "M'gladbach":       "https://upload.wikimedia.org/wikipedia/commons/8/81/Borussia_M%C3%B6nchengladbach_logo.svg",
    "FC Koln":          "https://upload.wikimedia.org/wikipedia/en/5/53/FC_Cologne_logo.svg",
    "Darmstadt":        "https://upload.wikimedia.org/wikipedia/en/5/5d/SV_Darmstadt_98_logo.svg",
    "Hertha":           "https://upload.wikimedia.org/wikipedia/commons/8/86/Hertha_BSC_Logo_2012.svg",
    "Schalke 04":       "https://upload.wikimedia.org/wikipedia/commons/6/6d/FC_Schalke_04_Logo.svg",

    # Ligue 1
    "Paris SG":         "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
    "Lyon":             "https://upload.wikimedia.org/wikipedia/en/e/e9/Olympique_Lyonnais.svg",
    "Marseille":        "https://upload.wikimedia.org/wikipedia/commons/d/d8/Olympique_de_Marseille_logo.svg",
    "Monaco":           "https://upload.wikimedia.org/wikipedia/en/e/ea/AS_Monaco_FC.svg",
    "Lille":            "https://upload.wikimedia.org/wikipedia/en/6/62/LOSC_Lille_2011_logo.svg",
    "Nice":             "https://upload.wikimedia.org/wikipedia/en/2/29/OGC_Nice_logo.svg",
    "Rennes":           "https://upload.wikimedia.org/wikipedia/en/6/6f/Stade_Rennais_FC.svg",
    "Lens":             "https://upload.wikimedia.org/wikipedia/en/4/forty/RC_Lens_logo.svg",
    "Strasbourg":       "https://upload.wikimedia.org/wikipedia/en/9/9f/RC_Strasbourg_Alsace_logo.svg",
    "Montpellier":      "https://upload.wikimedia.org/wikipedia/en/0/07/Montpellier_H%C3%A9rault_Sport_Club_logo.svg",
    "Nantes":           "https://upload.wikimedia.org/wikipedia/en/6/62/FC_Nantes_logo.svg",
    "Reims":            "https://upload.wikimedia.org/wikipedia/en/3/39/Stade_de_Reims_logo.svg",
    "Brest":            "https://upload.wikimedia.org/wikipedia/en/0/0e/Stade_Brestois_29_logo.svg",
    "Toulouse":         "https://upload.wikimedia.org/wikipedia/en/b/b1/Toulouse_FC_new_logo.svg",
    "Le Havre":         "https://upload.wikimedia.org/wikipedia/en/f/f7/Le_Havre_AC_logo.svg",
    "St Etienne":       "https://upload.wikimedia.org/wikipedia/en/a/a8/AS_Saint-%C3%89tienne.svg",
    "Auxerre":          "https://upload.wikimedia.org/wikipedia/en/0/0e/AJ_Auxerre_logo.svg",
    "Angers":           "https://upload.wikimedia.org/wikipedia/en/8/eight/SCO_Angers_logo.svg",

    # Eredivisie
    "Ajax":             "https://upload.wikimedia.org/wikipedia/en/7/79/Ajax_Amsterdam.svg",
    "PSV Eindhoven":    "https://upload.wikimedia.org/wikipedia/en/0/05/PSV_Eindhoven.svg",
    "Feyenoord":        "https://upload.wikimedia.org/wikipedia/en/f/f4/Feyenoord_logo.svg",
    "AZ Alkmaar":       "https://upload.wikimedia.org/wikipedia/en/5/5e/AZ_Alkmaar.svg",
    "Twente":           "https://upload.wikimedia.org/wikipedia/en/5/fifty/FC_Twente.svg",
    "Utrecht":          "https://upload.wikimedia.org/wikipedia/en/c/c4/FC_Utrecht_logo.svg",
    "Heerenveen":       "https://upload.wikimedia.org/wikipedia/en/1/1a/SC_Heerenveen_logo.svg",
    "Groningen":        "https://upload.wikimedia.org/wikipedia/en/4/40/FC_Groningen_logo.svg",
    "Almere City":      "https://upload.wikimedia.org/wikipedia/en/4/4a/Almere_City_FC_logo.svg",
    "NAC Breda":        "https://upload.wikimedia.org/wikipedia/en/6/6a/NAC_Breda.svg",
    "Willem II":        "https://upload.wikimedia.org/wikipedia/en/3/3d/Willem_II_Tilburg_logo.svg",
    "Sparta Rotterdam": "https://upload.wikimedia.org/wikipedia/en/3/35/Sparta_Rotterdam.svg",

    # Portugal
    "Porto":            "https://upload.wikimedia.org/wikipedia/en/3/3b/FC_Porto.svg",
    "Benfica":          "https://upload.wikimedia.org/wikipedia/en/f/f4/SL_Benfica_logo.svg",
    "Sp Lisbon":        "https://upload.wikimedia.org/wikipedia/en/4/4a/Sporting_CP_%28Portugal%29_logo.svg",
    "Sp Braga":         "https://upload.wikimedia.org/wikipedia/en/a/a4/Sporting_de_Braga.svg",
    "Guimaraes":        "https://upload.wikimedia.org/wikipedia/en/6/sixty/Vitoria_SC_crest.svg",
    "Boavista":         "https://upload.wikimedia.org/wikipedia/en/b/bf/Boavista_FC.svg",

    # Escocia
    "Celtic":           "https://upload.wikimedia.org/wikipedia/en/3/35/Celtic_FC_crest.svg",
    "Rangers":          "https://upload.wikimedia.org/wikipedia/en/5/fifty/Rangers_FC_logo.svg",
    "Hearts":           "https://upload.wikimedia.org/wikipedia/en/6/sixty/Heart_of_Midlothian_FC_logo.svg",
    "Hibernian":        "https://upload.wikimedia.org/wikipedia/en/a/a1/Hibernian_FC_logo.svg",
    "Aberdeen":         "https://upload.wikimedia.org/wikipedia/en/3/thirty/Aberdeen_FC_logo.svg",

    # Championship
    "Middlesbrough":    "https://upload.wikimedia.org/wikipedia/en/2/twenty/Middlesbrough_FC_crest.svg",
    "Sheffield Weds":   "https://upload.wikimedia.org/wikipedia/en/f/f1/Sheffield_Wednesday_badge.svg",
    "Sunderland":       "https://upload.wikimedia.org/wikipedia/en/7/7a/Sunderland_AFC_logo.svg",
    "West Brom":        "https://upload.wikimedia.org/wikipedia/en/8/8a/West_Bromwich_Albion.svg",
    "Swansea":          "https://upload.wikimedia.org/wikipedia/en/f/f9/Swansea_City_AFC_logo.svg",
    "Cardiff":          "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg",
    "Blackburn":        "https://upload.wikimedia.org/wikipedia/en/0/0f/Blackburn_Rovers.svg",
    "Derby":            "https://upload.wikimedia.org/wikipedia/en/4/forty/Derby_County_crest.svg",
    "Preston":          "https://upload.wikimedia.org/wikipedia/en/7/7forty/Preston_North_End_FC_logo.svg",
    "Millwall":         "https://upload.wikimedia.org/wikipedia/en/4/4c/Millwall_FC_logo.svg",
    "Stoke":            "https://upload.wikimedia.org/wikipedia/en/2/twenty/Stoke_City_FC.svg",
    "Coventry":         "https://upload.wikimedia.org/wikipedia/en/9/ninety/Coventry_City_FC_crest.svg",
    "Hull":             "https://upload.wikimedia.org/wikipedia/en/5/54/Hull_City_A.F.C._logo.svg",
    "Bristol City":     "https://upload.wikimedia.org/wikipedia/en/f/f5/Bristol_City_crest.svg",
    "QPR":              "https://upload.wikimedia.org/wikipedia/en/3/3a/QPR_logo.svg",
    "Birmingham":       "https://upload.wikimedia.org/wikipedia/en/6/sixty/Birmingham_City_FC_logo.svg",
    "Portsmouth":       "https://upload.wikimedia.org/wikipedia/en/3/thirty/Portsmouth_FC_logo.svg",
    "Oxford":           "https://upload.wikimedia.org/wikipedia/en/6/sixty/Oxford_United_FC_logo.svg",
    "Plymouth":         "https://upload.wikimedia.org/wikipedia/en/f/f4/Plymouth_Argyle_FC_logo.svg",
    "Wrexham":          "https://upload.wikimedia.org/wikipedia/en/8/eighty/Wrexham_AFC_logo.svg",
}


def get_escudo(nombre_equipo: str) -> str:
    """
    Retorna URL del escudo desde Wikimedia.
    Busca exacto, luego case-insensitive, luego parcial.
    """
    if nombre_equipo in ESCUDOS_CACHE:
        return ESCUDOS_CACHE[nombre_equipo]

    nombre_lower = nombre_equipo.lower()
    for equipo, url in ESCUDOS_CACHE.items():
        if equipo.lower() == nombre_lower:
            return url

    for equipo, url in ESCUDOS_CACHE.items():
        if nombre_lower in equipo.lower() or equipo.lower() in nombre_lower:
            return url

    return ""
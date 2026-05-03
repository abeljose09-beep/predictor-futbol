# ══════════════════════════════════════════════════════
# Mapa de equipos → liga donde juegan
# ══════════════════════════════════════════════════════

EQUIPOS_LIGA = {
    # ── Premier League ─────────────────────────────────
    'Arsenal':              'premier',
    'Chelsea':              'premier',
    'Manchester United':    'premier',
    'Manchester City':      'premier',
    'Liverpool':            'premier',
    'Tottenham':            'premier',
    'Newcastle':            'premier',
    'Aston Villa':          'premier',
    'West Ham':             'premier',
    'Brighton':             'premier',
    'Everton':              'premier',
    'Fulham':               'premier',
    'Brentford':            'premier',
    'Crystal Palace':       'premier',
    'Wolves':               'premier',
    'Nottm Forest':         'premier',
    'Bournemouth':          'premier',
    'Leicester':            'premier',
    'Ipswich':              'premier',
    'Southampton':          'premier',

    # ── La Liga ────────────────────────────────────────
    'Real Madrid':          'laliga',
    'Barcelona':            'laliga',
    'Atletico Madrid':      'laliga',
    'Sevilla':              'laliga',
    'Real Sociedad':        'laliga',
    'Villarreal':           'laliga',
    'Athletic Club':        'laliga',
    'Valencia':             'laliga',
    'Betis':                'laliga',
    'Osasuna':              'laliga',
    'Celta':                'laliga',
    'Getafe':               'laliga',
    'Girona':               'laliga',
    'Mallorca':             'laliga',
    'Las Palmas':           'laliga',
    'Alaves':               'laliga',
    'Leganes':              'laliga',
    'Espanol':              'laliga',
    'Valladolid':           'laliga',
    'Rayo Vallecano':       'laliga',

    # ── Serie A ────────────────────────────────────────
    'Juventus':             'seriea',
    'Inter':                'seriea',
    'AC Milan':             'seriea',
    'Napoli':               'seriea',
    'Roma':                 'seriea',
    'Lazio':                'seriea',
    'Atalanta':             'seriea',
    'Fiorentina':           'seriea',
    'Bologna':              'seriea',
    'Torino':               'seriea',
    'Udinese':              'seriea',
    'Sampdoria':            'seriea',
    'Sassuolo':             'seriea',
    'Empoli':               'seriea',
    'Lecce':                'seriea',
    'Monza':                'seriea',
    'Cagliari':             'seriea',
    'Frosinone':            'seriea',
    'Hellas Verona':        'seriea',
    'Parma':                'seriea',

    # ── Bundesliga ─────────────────────────────────────
    'Bayern Munich':        'bundesliga',
    'Borussia Dortmund':    'bundesliga',
    'RB Leipzig':           'bundesliga',
    'Bayer Leverkusen':     'bundesliga',
    'Eintracht Frankfurt':  'bundesliga',
    'Wolfsburg':            'bundesliga',
    'Borussia Mgladbach':   'bundesliga',
    'Freiburg':             'bundesliga',
    'Hoffenheim':           'bundesliga',
    'Werder Bremen':        'bundesliga',
    'Stuttgart':            'bundesliga',
    'Augsburg':             'bundesliga',
    'Mainz':                'bundesliga',
    'Union Berlin':         'bundesliga',
    'Heidenheim':           'bundesliga',
    'Holstein Kiel':        'bundesliga',
    'St Pauli':             'bundesliga',
    'Bochum':               'bundesliga',

    # ── Ligue 1 ────────────────────────────────────────
    'Paris SG':             'ligue1',
    'Marseille':            'ligue1',
    'Lyon':                 'ligue1',
    'Monaco':               'ligue1',
    'Lille':                'ligue1',
    'Nice':                 'ligue1',
    'Rennes':               'ligue1',
    'Lens':                 'ligue1',
    'Strasbourg':           'ligue1',
    'Montpellier':          'ligue1',
    'Nantes':               'ligue1',
    'Toulouse':             'ligue1',
    'Reims':                'ligue1',
    'Brest':                'ligue1',
    'Le Havre':             'ligue1',
    'Auxerre':              'ligue1',
    'Angers':               'ligue1',
    'Saint-Etienne':        'ligue1',

    # ── Eredivisie ─────────────────────────────────────
    'Ajax':                 'eredivisie',
    'PSV Eindhoven':        'eredivisie',
    'Feyenoord':            'eredivisie',
    'AZ Alkmaar':           'eredivisie',
    'Utrecht':              'eredivisie',
    'Twente':               'eredivisie',
    'Vitesse':              'eredivisie',
    'Groningen':            'eredivisie',

    # ── Primeira Liga ──────────────────────────────────
    'Porto':                'portugal',
    'Benfica':              'portugal',
    'Sporting CP':          'portugal',
    'Braga':                'portugal',
    'Vitoria SC':           'portugal',
    'Guimaraes':            'portugal',

    # ── Mundial ────────────────────────────────────────
    'Argentina':            'mundial',
    'France':               'mundial',
    'Brazil':               'mundial',
    'England':              'mundial',
    'Spain':                'mundial',
    'Germany':              'mundial',
    'Portugal':             'mundial',
    'Netherlands':          'mundial',
    'Belgium':              'mundial',
    'Croatia':              'mundial',
    'Morocco':              'mundial',
    'Uruguay':              'mundial',
    'Colombia':             'mundial',
    'Ecuador':              'mundial',
    'Mexico':               'mundial',
    'USA':                  'mundial',
    'Japan':                'mundial',
    'South Korea':          'mundial',
    'Senegal':              'mundial',
    'Ghana':                'mundial',
    'Cameroon':             'mundial',
    'Qatar':                'mundial',
    'Saudi Arabia':         'mundial',
    'Australia':            'mundial',
    'Poland':               'mundial',
    'Serbia':               'mundial',
    'Switzerland':          'mundial',
    'Denmark':              'mundial',
    'Tunisia':              'mundial',
    'Costa Rica':           'mundial',
    'Wales':                'mundial',
    'Iran':                 'mundial',
    'Canada':               'mundial',
}

def obtener_liga(equipo):
    """Retorna la liga de un equipo o None si no se encuentra"""
    return EQUIPOS_LIGA.get(equipo, None)

def buscar_equipo(nombre_parcial):
    """Busca equipos por nombre parcial (para autocompletado)"""
    nombre_parcial = nombre_parcial.lower()
    return [e for e in EQUIPOS_LIGA.keys() 
            if nombre_parcial in e.lower()]

def equipos_por_liga(liga):
    """Retorna todos los equipos de una liga"""
    prefijo = liga.rstrip('_0123456789')
    return [e for e, l in EQUIPOS_LIGA.items() 
            if l.startswith(prefijo)]

if __name__ == '__main__':
    # Prueba
    print(f"Arsenal → {obtener_liga('Arsenal')}")
    print(f"Real Madrid → {obtener_liga('Real Madrid')}")
    print(f"Bayern Munich → {obtener_liga('Bayern Munich')}")
    print(f"\nEquipos Premier: {equipos_por_liga('premier')[:5]}")
    print(f"\nBúsqueda 'man': {buscar_equipo('man')}")
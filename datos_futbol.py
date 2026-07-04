import pandas as pd
import requests
import os

LIGAS = {
    # ── Premier League ─────────────────────────────────────────────
    'premier_25':    'https://www.football-data.co.uk/mmz4281/2526/E0.csv',
    'premier_24':    'https://www.football-data.co.uk/mmz4281/2425/E0.csv',
    'premier_23':    'https://www.football-data.co.uk/mmz4281/2324/E0.csv',
    'premier_22':    'https://www.football-data.co.uk/mmz4281/2223/E0.csv',
    'premier_21':    'https://www.football-data.co.uk/mmz4281/2122/E0.csv',
    'premier_20':    'https://www.football-data.co.uk/mmz4281/2021/E0.csv',

    # ── La Liga ────────────────────────────────────────────────────
    'laliga_25':     'https://www.football-data.co.uk/mmz4281/2526/SP1.csv',
    'laliga_24':     'https://www.football-data.co.uk/mmz4281/2425/SP1.csv',
    'laliga_23':     'https://www.football-data.co.uk/mmz4281/2324/SP1.csv',
    'laliga_22':     'https://www.football-data.co.uk/mmz4281/2223/SP1.csv',
    'laliga_21':     'https://www.football-data.co.uk/mmz4281/2122/SP1.csv',
    'laliga_20':     'https://www.football-data.co.uk/mmz4281/2021/SP1.csv',

    # ── Serie A ────────────────────────────────────────────────────
    'seriea_25':     'https://www.football-data.co.uk/mmz4281/2526/I1.csv',
    'seriea_24':     'https://www.football-data.co.uk/mmz4281/2425/I1.csv',
    'seriea_23':     'https://www.football-data.co.uk/mmz4281/2324/I1.csv',
    'seriea_22':     'https://www.football-data.co.uk/mmz4281/2223/I1.csv',
    'seriea_21':     'https://www.football-data.co.uk/mmz4281/2122/I1.csv',
    'seriea_20':     'https://www.football-data.co.uk/mmz4281/2021/I1.csv',

    # ── Bundesliga ─────────────────────────────────────────────────
    'bundesliga_25': 'https://www.football-data.co.uk/mmz4281/2526/D1.csv',
    'bundesliga_24': 'https://www.football-data.co.uk/mmz4281/2425/D1.csv',
    'bundesliga_23': 'https://www.football-data.co.uk/mmz4281/2324/D1.csv',
    'bundesliga_22': 'https://www.football-data.co.uk/mmz4281/2223/D1.csv',
    'bundesliga_21': 'https://www.football-data.co.uk/mmz4281/2122/D1.csv',
    'bundesliga_20': 'https://www.football-data.co.uk/mmz4281/2021/D1.csv',

    # ── Ligue 1 ────────────────────────────────────────────────────
    'ligue1_25':     'https://www.football-data.co.uk/mmz4281/2526/F1.csv',
    'ligue1_24':     'https://www.football-data.co.uk/mmz4281/2425/F1.csv',
    'ligue1_23':     'https://www.football-data.co.uk/mmz4281/2324/F1.csv',
    'ligue1_22':     'https://www.football-data.co.uk/mmz4281/2223/F1.csv',
    'ligue1_21':     'https://www.football-data.co.uk/mmz4281/2122/F1.csv',
    'ligue1_20':     'https://www.football-data.co.uk/mmz4281/2021/F1.csv',

    # ── Eredivisie (Holanda) ───────────────────────────────────────
    'eredivisie_25': 'https://www.football-data.co.uk/mmz4281/2526/N1.csv',
    'eredivisie_24': 'https://www.football-data.co.uk/mmz4281/2425/N1.csv',
    'eredivisie_23': 'https://www.football-data.co.uk/mmz4281/2324/N1.csv',

    # ── Primeira Liga (Portugal) ───────────────────────────────────
    'portugal_25':   'https://www.football-data.co.uk/mmz4281/2526/P1.csv',
    'portugal_24':   'https://www.football-data.co.uk/mmz4281/2425/P1.csv',
    'portugal_23':   'https://www.football-data.co.uk/mmz4281/2324/P1.csv',

    # ── Liga Escocesa ──────────────────────────────────────────────
    'escocia_25':    'https://www.football-data.co.uk/mmz4281/2526/SC0.csv',
    'escocia_24':    'https://www.football-data.co.uk/mmz4281/2425/SC0.csv',

    # ── Championship (Segunda Inglaterra) ─────────────────────────
    'championship_25': 'https://www.football-data.co.uk/mmz4281/2526/E1.csv',
    'championship_24': 'https://www.football-data.co.uk/mmz4281/2425/E1.csv',
}

# ── Champions, Europa, Mundial (URLs corregidas) ───────────────────────────
LIGAS_API = {
    # Mundial — repo worldcup.json (URLs verificadas ✅)
    'mundial_26': 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json',
    'mundial_22': 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2022/worldcup.json',
    'mundial_18': 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2018/worldcup.json',
    'mundial_14': 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2014/worldcup.json',

    # Champions League — via openfootball.github.io (JSON auto-generado)
    'champions_24': 'https://openfootball.github.io/champions-league/2023-24/cl.json',
    'champions_23': 'https://openfootball.github.io/champions-league/2022-23/cl.json',
    'champions_22': 'https://openfootball.github.io/champions-league/2021-22/cl.json',
    'champions_21': 'https://openfootball.github.io/champions-league/2020-21/cl.json',

    # Europa League
    'europa_24': 'https://openfootball.github.io/champions-league/2023-24/el.json',
    'europa_23': 'https://openfootball.github.io/champions-league/2022-23/el.json',
}
def descargar_liga(nombre, url):
    """Descarga ligas en formato CSV (football-data.co.uk)"""
    try:
        df = pd.read_csv(url)
        if len(df) == 0:
            print(f"  ⚠️  {nombre}: temporada aún sin partidos")
            return None
        df['Liga'] = nombre
        print(f"  ✅ {nombre}: {len(df)} partidos descargados")
        return df
    except Exception as e:
        print(f"  ❌ {nombre}: {e}")
        return None

def descargar_liga_json(nombre, url):
    """Descarga ligas en formato JSON (Mundial, Champions, etc.)"""
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        partidos = []
 
        # El repo worldcup.json usa 'matches' directo (sin 'rounds')
        # El repo football.json usa 'matches' también
        matches = data.get('matches', [])
 
        for match in matches:
            score = match.get('score', {})
 
            # Formato nuevo: score = {"ft": [2, 1]}
            if isinstance(score, dict):
                ft = score.get('ft', [])
                if not ft or len(ft) < 2:
                    continue
                hg, ag = int(ft[0]), int(ft[1])
 
            # Formato viejo: score = "2-1"
            elif isinstance(score, str) and '-' in score:
                partes = score.replace(' ', '').split('-')
                hg, ag = int(partes[0]), int(partes[1])
            else:
                continue
 
            if hg > ag:   res = 'H'
            elif hg < ag: res = 'A'
            else:         res = 'D'
 
            partidos.append({
                'Date':     match.get('date', ''),
                'HomeTeam': match.get('team1', ''),
                'AwayTeam': match.get('team2', ''),
                'FTHG': hg, 'FTAG': ag, 'FTR': res,
                'HTHG': 0,  'HTAG': 0,  'HTR': res,
                'HS': 0, 'AS': 0, 'HST': 0, 'AST': 0,
                'HC': 0, 'AC': 0, 'HY': 0, 'AY': 0,
                'HR': 0, 'AR': 0, 'Liga': nombre
            })
 
        if partidos:
            print(f"  ✅ {nombre}: {len(partidos)} partidos descargados")
            return pd.DataFrame(partidos)
        else:
            print(f"  ⚠️  {nombre}: sin resultados disponibles aún")
            return None
 
    except Exception as e:
        print(f"  ❌ {nombre}: {e}")
        return None

def descargar_todo():
    print("📥 Descargando ligas locales...\n")
    dfs = []

    # ── Ligas CSV ──────────────────────────────────────────────────
    for nombre, url in LIGAS.items():
        df = descargar_liga(nombre, url)
        if df is not None:
            dfs.append(df)

    # ── Competiciones internacionales JSON ─────────────────────────
    print("\n🌍 Descargando competiciones internacionales...")
    for nombre, url in LIGAS_API.items():
        df = descargar_liga_json(nombre, url)
        if df is not None:
            dfs.append(df)

    if not dfs:
        print("❌ No se pudo descargar ninguna liga")
        return None

    # ── Unir y limpiar todo ────────────────────────────────────────
    columnas_base = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR',
                     'HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST', 'AST',
                     'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'Liga']

    dfs_limpios = []
    for df in dfs:
        cols_disponibles = [c for c in columnas_base if c in df.columns]
        dfs_limpios.append(df[cols_disponibles])

    datos = pd.concat(dfs_limpios, ignore_index=True)
    datos.dropna(subset=['FTHG', 'FTAG', 'FTR'], inplace=True)
    datos['Date'] = pd.to_datetime(datos['Date'], dayfirst=True, errors='coerce')
    datos.dropna(subset=['Date'], inplace=True)
    datos.sort_values('Date', inplace=True)
    datos.reset_index(drop=True, inplace=True)

    os.makedirs('datos', exist_ok=True)
    datos.to_csv('datos/partidos.csv', index=False)

    print(f"\n{'='*50}")
    print(f"✅ TOTAL: {len(datos)} partidos guardados")
    print(f"📅 Desde: {datos['Date'].min().date()} hasta {datos['Date'].max().date()}")
    print(f"🏟️  Equipos únicos: {datos['HomeTeam'].nunique()}")
    print(f"🏆 Ligas incluidas: {datos['Liga'].nunique()}")
    print(f"{'='*50}")

    # Resumen por liga
    print("\n📊 Partidos por liga:")
    resumen = datos.groupby('Liga').size().sort_values(ascending=False)
    for liga, total in resumen.items():
        print(f"  {liga}: {total}")

    return datos

if __name__ == '__main__':
    datos = descargar_todo()
    if datos is not None:
        print(f"\nEjemplo de datos más recientes:")
        print(datos[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','Liga']].tail(5))
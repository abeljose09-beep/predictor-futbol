import pandas as pd
import numpy as np
import json, sys
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from equipos import obtener_liga

# ══════════════════════════════════════════════════════
# INDICADORES CLAVE para predecir fútbol:
# - Forma reciente (últimos 5 partidos)
# - Goles marcados y recibidos promedio
# - Puntos acumulados en la temporada
# - Rendimiento de local vs visitante
# - Diferencia de goles histórica entre equipos
# ══════════════════════════════════════════════════════

def calcular_forma(df, equipo, fecha, n=5):
    """Calcula estadísticas de los últimos N partidos de un equipo"""
    partidos_local  = df[(df['HomeTeam'] == equipo) & (df['Date'] < fecha)]
    partidos_visita = df[(df['AwayTeam'] == equipo) & (df['Date'] < fecha)]

    historial = []

    for _, p in partidos_local.iterrows():
        gf  = p['FTHG']; gc = p['FTAG']
        pts = 3 if p['FTR'] == 'H' else (1 if p['FTR'] == 'D' else 0)
        historial.append({'fecha': p['Date'], 'gf': gf, 'gc': gc, 'pts': pts,
                          'tiros': p.get('HS', 0), 'tiros_contra': p.get('AS', 0)})

    for _, p in partidos_visita.iterrows():
        gf  = p['FTAG']; gc = p['FTHG']
        pts = 3 if p['FTR'] == 'A' else (1 if p['FTR'] == 'D' else 0)
        historial.append({'fecha': p['Date'], 'gf': gf, 'gc': gc, 'pts': pts,
                          'tiros': p.get('AS', 0), 'tiros_contra': p.get('HS', 0)})

    historial = sorted(historial, key=lambda x: x['fecha'])[-n:]

    if len(historial) < 2:
        return {'gf_prom': 1.2, 'gc_prom': 1.2, 'pts_prom': 1.0,
                'tiros_prom': 12, 'forma_reciente': 1.0}

    return {
        'gf_prom':        np.mean([h['gf']  for h in historial]),
        'gc_prom':        np.mean([h['gc']  for h in historial]),
        'pts_prom':       np.mean([h['pts'] for h in historial]),
        'tiros_prom':     np.mean([h['tiros'] for h in historial]),
        'forma_reciente': np.mean([h['pts'] for h in historial[-3:]])
    }


def construir_features(df):
    print("⚙️  Calculando indicadores de cada partido...")
    filas = []

    for idx, partido in df.iterrows():
        if idx % 200 == 0:
            print(f"  Procesando partido {idx}/{len(df)}...")

        local  = partido['HomeTeam']
        visita = partido['AwayTeam']
        fecha  = partido['Date']

        forma_l = calcular_forma(df, local,  fecha, n=5)
        forma_v = calcular_forma(df, visita, fecha, n=5)

        # Historial directo entre los dos equipos
        enfrentamientos = df[
            (
                ((df['HomeTeam'] == local)  & (df['AwayTeam'] == visita)) |
                ((df['HomeTeam'] == visita) & (df['AwayTeam'] == local))
            ) & (df['Date'] < fecha)
        ].tail(5)

        h2h_goles      = enfrentamientos['FTHG'].sum() + enfrentamientos['FTAG'].sum()
        h2h_goles_prom = h2h_goles / max(len(enfrentamientos), 1)

        fila = {
            # Forma local
            'local_gf':       forma_l['gf_prom'],
            'local_gc':       forma_l['gc_prom'],
            'local_pts':      forma_l['pts_prom'],
            'local_tiros':    forma_l['tiros_prom'],
            'local_forma':    forma_l['forma_reciente'],

            # Forma visitante
            'visita_gf':      forma_v['gf_prom'],
            'visita_gc':      forma_v['gc_prom'],
            'visita_pts':     forma_v['pts_prom'],
            'visita_tiros':   forma_v['tiros_prom'],
            'visita_forma':   forma_v['forma_reciente'],

            # Diferencias
            'diff_pts':       forma_l['pts_prom']      - forma_v['pts_prom'],
            'diff_gf':        forma_l['gf_prom']       - forma_v['gf_prom'],
            'diff_gc':        forma_l['gc_prom']       - forma_v['gc_prom'],
            'diff_forma':     forma_l['forma_reciente'] - forma_v['forma_reciente'],

            # Head to head
            'h2h_goles_prom': h2h_goles_prom,
            'h2h_partidos':   len(enfrentamientos),

            # Targets
            'resultado':   partido['FTR'],
            'total_goles': partido['FTHG'] + partido['FTAG'],
            'mas_2_5':     int((partido['FTHG'] + partido['FTAG']) > 2.5),
        }
        filas.append(fila)

    return pd.DataFrame(filas)


def entrenar_modelos(local, visita):
    df = pd.read_csv('datos/partidos.csv', parse_dates=['Date'])

    # Detectar liga automáticamente según los equipos
    liga_local  = obtener_liga(local)
    liga_visita = obtener_liga(visita)

    if liga_local and liga_visita and liga_local == liga_visita:
        prefijo = liga_local.rstrip('_0123456789')
        df = df[df['Liga'].str.startswith(prefijo)]
        print(f"  🏆 Liga detectada: {prefijo} ({len(df)} partidos)")
    elif liga_local and liga_visita:
        prefijo_l = liga_local.rstrip('_0123456789')
        prefijo_v = liga_visita.rstrip('_0123456789')
        df = df[
            df['Liga'].str.startswith(prefijo_l) |
            df['Liga'].str.startswith(prefijo_v)
        ]
        print(f"  🌍 Partido internacional: {prefijo_l} + {prefijo_v} ({len(df)} partidos)")
    else:
        equipo_desc = local if not liga_local else visita
        print(f"  ⚠️  '{equipo_desc}' no encontrado en el mapa — usando todos los datos")

    print(f"📊 Partidos a procesar: {len(df)}")

    features_df = construir_features(df)
    features_df.dropna(inplace=True)

    cols_X = [
        'local_gf',  'local_gc',  'local_pts',  'local_tiros',  'local_forma',
        'visita_gf', 'visita_gc', 'visita_pts', 'visita_tiros', 'visita_forma',
        'diff_pts',  'diff_gf',   'diff_gc',    'diff_forma',
        'h2h_goles_prom', 'h2h_partidos'
    ]

    X = features_df[cols_X]
    modelos = {}

    # ── Modelo 1: Resultado (H/D/A) ───────────────────────────────────────
    y_res = features_df['resultado']
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_res, test_size=0.2, shuffle=False)
    m1 = RandomForestClassifier(n_estimators=300, max_depth=6,
                                 class_weight='balanced', random_state=42)
    m1.fit(X_tr, y_tr)
    acc1 = accuracy_score(y_te, m1.predict(X_te))
    print(f"\n✅ Modelo Resultado    — Accuracy: {acc1:.2%}")
    modelos['resultado'] = m1

    # ── Modelo 2: Más/menos 2.5 goles ────────────────────────────────────
    y_gol = features_df['mas_2_5']
    X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X, y_gol, test_size=0.2, shuffle=False)
    m2 = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=42)
    m2.fit(X_tr2, y_tr2)
    acc2 = accuracy_score(y_te2, m2.predict(X_te2))
    print(f"✅ Modelo Goles +2.5   — Accuracy: {acc2:.2%}")
    modelos['goles'] = m2

    # ── Modelo 3: Solo victoria (sin empate) ──────────────────────────────
    features_sin_empate = features_df[features_df['resultado'] != 'D'].copy()
    X3 = features_sin_empate[cols_X]
    y3 = (features_sin_empate['resultado'] == 'H').astype(int)
    X_tr3, X_te3, y_tr3, y_te3 = train_test_split(X3, y3, test_size=0.2, shuffle=False)
    m3 = RandomForestClassifier(n_estimators=300, max_depth=5, random_state=42)
    m3.fit(X_tr3, y_tr3)
    acc3 = accuracy_score(y_te3, m3.predict(X_te3))
    print(f"✅ Modelo Ganador      — Accuracy: {acc3:.2%}")
    modelos['ganador'] = m3

    return modelos, cols_X, df   # ← return que faltaba


def predecir_partido(modelos, cols_X, df, local, visita):
    from datetime import datetime
    fecha = pd.Timestamp(datetime.now())

    forma_l = calcular_forma(df, local,  fecha, n=5)
    forma_v = calcular_forma(df, visita, fecha, n=5)

    enfrentamientos = df[
        ((df['HomeTeam'] == local)  & (df['AwayTeam'] == visita)) |
        ((df['HomeTeam'] == visita) & (df['AwayTeam'] == local))
    ].tail(5)

    h2h_goles_prom = (
        enfrentamientos['FTHG'].sum() + enfrentamientos['FTAG'].sum()
    ) / max(len(enfrentamientos), 1)

    X_pred = pd.DataFrame([{
        'local_gf':       forma_l['gf_prom'],
        'local_gc':       forma_l['gc_prom'],
        'local_pts':      forma_l['pts_prom'],
        'local_tiros':    forma_l['tiros_prom'],
        'local_forma':    forma_l['forma_reciente'],
        'visita_gf':      forma_v['gf_prom'],
        'visita_gc':      forma_v['gc_prom'],
        'visita_pts':     forma_v['pts_prom'],
        'visita_tiros':   forma_v['tiros_prom'],
        'visita_forma':   forma_v['forma_reciente'],
        'diff_pts':       forma_l['pts_prom']       - forma_v['pts_prom'],
        'diff_gf':        forma_l['gf_prom']        - forma_v['gf_prom'],
        'diff_gc':        forma_l['gc_prom']        - forma_v['gc_prom'],
        'diff_forma':     forma_l['forma_reciente'] - forma_v['forma_reciente'],
        'h2h_goles_prom': h2h_goles_prom,
        'h2h_partidos':   len(enfrentamientos),
    }])

    prob_res = modelos['resultado'].predict_proba(X_pred)[0]
    clases   = modelos['resultado'].classes_
    prob_gol = modelos['goles'].predict_proba(X_pred)[0]
    prob_gan = modelos['ganador'].predict_proba(X_pred)[0]

    resultado = {
        'local':            local,
        'visita':           visita,
        'prob_local':       round(float(prob_res[list(clases).index('H')]), 3),
        'prob_empate':      round(float(prob_res[list(clases).index('D')]), 3),
        'prob_visita':      round(float(prob_res[list(clases).index('A')]), 3),
        'prob_mas_2_5':     round(float(prob_gol[1]), 3),
        'prob_menos_2_5':   round(float(prob_gol[0]), 3),
        'prob_gana_local':  round(float(prob_gan[1]), 3),
        'prob_gana_visita': round(float(prob_gan[0]), 3),
        'forma_local':      round(forma_l['pts_prom'], 2),
        'forma_visita':     round(forma_v['pts_prom'], 2),
        'h2h_partidos':     len(enfrentamientos),
        'h2h_goles_prom':   round(h2h_goles_prom, 2),
    }
    return resultado


if __name__ == '__main__':
    args   = sys.argv[1:]
    local  = args[0] if len(args) > 0 else 'Arsenal'
    visita = args[1] if len(args) > 1 else 'Chelsea'

    modelos, cols_X, df = entrenar_modelos(local, visita)
    pred = predecir_partido(modelos, cols_X, df, local, visita)

    print("\n" + "═" * 45)
    print(f"⚽  {pred['local']}  vs  {pred['visita']}")
    print("═" * 45)
    print(f"🏠 Victoria local  : {pred['prob_local']*100:.1f}%")
    print(f"🤝 Empate          : {pred['prob_empate']*100:.1f}%")
    print(f"✈️  Victoria visita : {pred['prob_visita']*100:.1f}%")
    print(f"⚽ Más de 2.5 goles: {pred['prob_mas_2_5']*100:.1f}%")
    print(f"🔒 Menos de 2.5   : {pred['prob_menos_2_5']*100:.1f}%")
    print(f"🏆 Ganador directo : {'Local' if pred['prob_gana_local'] > 0.5 else 'Visita'} ({max(pred['prob_gana_local'], pred['prob_gana_visita'])*100:.1f}%)")
    print(f"\n📊 Forma local : {pred['forma_local']} pts/partido")
    print(f"📊 Forma visita: {pred['forma_visita']} pts/partido")
    print(f"🔁 H2H: {pred['h2h_partidos']} enfrentamientos | {pred['h2h_goles_prom']} goles/partido")
    print("═" * 45)
    print(json.dumps(pred))
import streamlit as st
import pandas as pd
import numpy as np
import sys, os

# ── Asegura que Python encuentre los módulos del proyecto ──────────────────
sys.path.insert(0, os.path.dirname(__file__))

from modelo_futbol import entrenar_modelos, predecir_partido, calcular_forma
from equipos import EQUIPOS_LIGA, equipos_por_liga

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚽ Predictor de Fútbol IA",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Forzar sidebar siempre visible y ocultar el botón de colapso
st.markdown("""
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 320px !important; }
    section[data-testid="stSidebar"] > div { width: 320px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }

    .prob-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid #2e3450;
        margin: 8px 0;
    }
    .prob-card h1 { font-size: 2.8rem; margin: 0; }
    .prob-card p  { color: #8892b0; margin: 4px 0 0 0; font-size: 0.9rem; }

    .bar-container {
        background: #1e2130;
        border-radius: 50px;
        height: 22px;
        overflow: hidden;
        margin: 6px 0;
    }
    .bar-fill {
        height: 100%;
        border-radius: 50px;
        display: flex;
        align-items: center;
        padding-left: 10px;
        font-size: 0.75rem;
        font-weight: bold;
        color: white;
    }

    .match-header {
        background: linear-gradient(135deg, #1a1f35, #0e1117);
        border: 1px solid #2e3450;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 24px;
    }
    .match-header h1 { font-size: 2rem; margin: 0; letter-spacing: 2px; }
    .match-header p  { color: #8892b0; margin: 6px 0 0 0; }

    .h2h-row {
        background: #1e2130;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #2e3450;
    }
    .h2h-win-home  { border-left-color: #00d4aa; }
    .h2h-win-away  { border-left-color: #ff6b6b; }
    .h2h-draw      { border-left-color: #ffa500; }

    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-win  { background: #00d4aa22; color: #00d4aa; border: 1px solid #00d4aa44; }
    .badge-draw { background: #ffa50022; color: #ffa500; border: 1px solid #ffa50044; }
    .badge-loss { background: #ff6b6b22; color: #ff6b6b; border: 1px solid #ff6b6b44; }

    .forma-dot {
        display: inline-block;
        width: 28px; height: 28px;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-size: 0.7rem;
        font-weight: bold;
        margin: 2px;
    }
    .forma-W { background: #00d4aa; color: #000; }
    .forma-D { background: #ffa500; color: #000; }
    .forma-L { background: #ff6b6b; color: #fff; }

    .section-title {
        color: #64ffda;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 24px 0 12px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #2e3450;
    }

    #MainMenu {visibility: hidden;}
    footer    {visibility: hidden;}
    header    {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

def barra_html(pct, color, etiqueta):
    pct_r = round(pct * 100, 1)
    return f"""
    <div style="margin:6px 0">
      <div style="display:flex; justify-content:space-between; margin-bottom:3px">
        <span style="color:#ccd6f6; font-size:0.85rem">{etiqueta}</span>
        <span style="color:#64ffda; font-weight:bold">{pct_r}%</span>
      </div>
      <div class="bar-container">
        <div class="bar-fill" style="width:{pct_r}%; background:{color};">&nbsp;</div>
      </div>
    </div>"""


def forma_html(df, equipo, n=6):
    from datetime import datetime
    fecha = pd.Timestamp(datetime.now())

    partidos_l = df[(df['HomeTeam'] == equipo) & (df['Date'] < fecha)]
    partidos_v = df[(df['AwayTeam'] == equipo) & (df['Date'] < fecha)]

    historial = []
    for _, p in partidos_l.iterrows():
        res = 'W' if p['FTR'] == 'H' else ('D' if p['FTR'] == 'D' else 'L')
        historial.append((p['Date'], res, p['AwayTeam'], p['FTHG'], p['FTAG']))
    for _, p in partidos_v.iterrows():
        res = 'W' if p['FTR'] == 'A' else ('D' if p['FTR'] == 'D' else 'L')
        historial.append((p['Date'], res, p['HomeTeam'], p['FTAG'], p['FTHG']))

    historial = sorted(historial, key=lambda x: x[0])[-n:]

    dots = ""
    for _, res, rival, gf, gc in historial:
        dots += f'<span class="forma-dot forma-{res}" title="{res} vs {rival} ({gf}-{gc})">{res}</span>'
    return dots


def obtener_h2h(df, local, visita, n=8):
    mask = (
        ((df['HomeTeam'] == local)  & (df['AwayTeam'] == visita)) |
        ((df['HomeTeam'] == visita) & (df['AwayTeam'] == local))
    )
    return df[mask].sort_values('Date', ascending=False).head(n)


def stats_equipo(df, equipo):
    from datetime import datetime
    fecha = pd.Timestamp(datetime.now())

    pl = df[(df['HomeTeam'] == equipo) & (df['Date'] < fecha)]
    pv = df[(df['AwayTeam'] == equipo) & (df['Date'] < fecha)]

    gf    = pl['FTHG'].sum() + pv['FTAG'].sum()
    gc    = pl['FTAG'].sum() + pv['FTHG'].sum()
    total = len(pl) + len(pv)
    wins  = len(pl[pl['FTR'] == 'H']) + len(pv[pv['FTR'] == 'A'])
    draws = len(pl[pl['FTR'] == 'D']) + len(pv[pv['FTR'] == 'D'])
    loss  = total - wins - draws

    return {
        'PJ': total, 'G': wins, 'E': draws, 'P': loss,
        'GF': int(gf), 'GC': int(gc),
        'GF/PJ': round(gf / max(total, 1), 2),
        'GC/PJ': round(gc / max(total, 1), 2),
        '%Win':  round(wins / max(total, 1) * 100, 1),
    }


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚽ Predictor IA")
    st.markdown("---")

    LIGAS_DISPLAY = {
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": "premier",
        "🇪🇸 La Liga":           "laliga",
        "🇮🇹 Serie A":           "seriea",
        "🇩🇪 Bundesliga":        "bundesliga",
        "🇫🇷 Ligue 1":           "ligue1",
        "🇳🇱 Eredivisie":        "eredivisie",
        "🇵🇹 Primeira Liga":     "portugal",
        "🌍 Mundial":            "mundial",
    }

    liga_label = st.selectbox("🏆 Liga", list(LIGAS_DISPLAY.keys()))
    liga_key   = LIGAS_DISPLAY[liga_label]

    equipos_liga = sorted(equipos_por_liga(liga_key))

    if len(equipos_liga) < 2:
        st.warning("No hay equipos registrados para esta liga.")
        st.stop()

    equipo_local  = st.selectbox("🏠 Equipo Local",     equipos_liga, index=0)
    equipo_visita = st.selectbox("✈️  Equipo Visitante", equipos_liga, index=1)

    st.markdown("---")
    predecir_btn = st.button("🔮 Predecir Partido", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("Modelo: Random Forest + Gradient Boosting")
    st.caption("Datos: football-data.co.uk")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("# ⚽ Predictor de Fútbol con IA")
st.markdown("Selecciona dos equipos en la barra lateral y presiona **Predecir Partido**.")

if equipo_local == equipo_visita:
    st.warning("⚠️ Selecciona dos equipos diferentes.")
    st.stop()

if predecir_btn:

    with st.spinner(f"⚙️ Entrenando modelo para {liga_label}..."):
        try:
            modelos, cols_X, df = entrenar_modelos(equipo_local, equipo_visita)
            pred = predecir_partido(modelos, cols_X, df, equipo_local, equipo_visita)
        except Exception as e:
            st.error(f"❌ Error al predecir: {e}")
            st.stop()

    # ── Encabezado ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="match-header">
        <h1>🏠 {equipo_local} &nbsp;vs&nbsp; {equipo_visita} ✈️</h1>
        <p>{liga_label} &nbsp;·&nbsp; Predicción con Inteligencia Artificial</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Probabilidades principales ────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Probabilidades del Resultado</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    max_prob = max(pred['prob_local'], pred['prob_empate'], pred['prob_visita'])

    with c1:
        col = "#00d4aa" if pred['prob_local'] == max_prob else "#4a5568"
        st.markdown(f"""
        <div class="prob-card" style="border-color:{col}44">
            <h1 style="color:{col}">{pred['prob_local']*100:.1f}%</h1>
            <p>🏠 Victoria {equipo_local}</p>
        </div>""", unsafe_allow_html=True)

    with c2:
        col = "#ffa500" if pred['prob_empate'] == max_prob else "#4a5568"
        st.markdown(f"""
        <div class="prob-card" style="border-color:{col}44">
            <h1 style="color:{col}">{pred['prob_empate']*100:.1f}%</h1>
            <p>🤝 Empate</p>
        </div>""", unsafe_allow_html=True)

    with c3:
        col = "#ff6b6b" if pred['prob_visita'] == max_prob else "#4a5568"
        st.markdown(f"""
        <div class="prob-card" style="border-color:{col}44">
            <h1 style="color:{col}">{pred['prob_visita']*100:.1f}%</h1>
            <p>✈️ Victoria {equipo_visita}</p>
        </div>""", unsafe_allow_html=True)

    # ── Barras ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📈 Desglose Visual</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Resultado del partido**")
        st.markdown(barra_html(pred['prob_local'],  "#00d4aa", f"🏠 {equipo_local}"),   unsafe_allow_html=True)
        st.markdown(barra_html(pred['prob_empate'], "#ffa500", "🤝 Empate"),              unsafe_allow_html=True)
        st.markdown(barra_html(pred['prob_visita'], "#ff6b6b", f"✈️ {equipo_visita}"),  unsafe_allow_html=True)

    with col_b:
        st.markdown("**Línea de goles**")
        st.markdown(barra_html(pred['prob_mas_2_5'],   "#a78bfa", "⚽ Más de 2.5 goles"),   unsafe_allow_html=True)
        st.markdown(barra_html(pred['prob_menos_2_5'], "#64748b", "🔒 Menos de 2.5 goles"), unsafe_allow_html=True)
        st.markdown("**Ganador directo** (sin empate)")
        st.markdown(barra_html(pred['prob_gana_local'],  "#00d4aa", f"🏠 {equipo_local}"),  unsafe_allow_html=True)
        st.markdown(barra_html(pred['prob_gana_visita'], "#ff6b6b", f"✈️ {equipo_visita}"), unsafe_allow_html=True)

    # ── Forma reciente ────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔥 Forma Reciente (últimos 6 partidos)</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        st.markdown(f"**{equipo_local}**")
        dots_l = forma_html(df, equipo_local, n=6)
        st.markdown(dots_l if dots_l else "_Sin datos suficientes_", unsafe_allow_html=True)
    with f2:
        st.markdown(f"**{equipo_visita}**")
        dots_v = forma_html(df, equipo_visita, n=6)
        st.markdown(dots_v if dots_v else "_Sin datos suficientes_", unsafe_allow_html=True)

    # ── Estadísticas ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 Estadísticas en la Liga</div>', unsafe_allow_html=True)

    stats_l = stats_equipo(df, equipo_local)
    stats_v = stats_equipo(df, equipo_visita)

    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"**{equipo_local}**")
        a1, a2, a3 = st.columns(3)
        a1.metric("PJ",      stats_l['PJ'])
        a2.metric("Victorias", stats_l['G'])
        a3.metric("% Win",   f"{stats_l['%Win']}%")
        a1.metric("GF",      stats_l['GF'])
        a2.metric("GC",      stats_l['GC'])
        a3.metric("GF/PJ",   stats_l['GF/PJ'])

    with s2:
        st.markdown(f"**{equipo_visita}**")
        b1, b2, b3 = st.columns(3)
        b1.metric("PJ",      stats_v['PJ'])
        b2.metric("Victorias", stats_v['G'])
        b3.metric("% Win",   f"{stats_v['%Win']}%")
        b1.metric("GF",      stats_v['GF'])
        b2.metric("GC",      stats_v['GC'])
        b3.metric("GF/PJ",   stats_v['GF/PJ'])

    # ── Historial H2H ─────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔁 Historial de Enfrentamientos Directos</div>', unsafe_allow_html=True)

    h2h = obtener_h2h(df, equipo_local, equipo_visita, n=8)

    if h2h.empty:
        st.info("No hay enfrentamientos directos registrados entre estos equipos en los datos disponibles.")
    else:
        wins_l = len(h2h[(h2h['HomeTeam'] == equipo_local)  & (h2h['FTR'] == 'H')]) + \
                 len(h2h[(h2h['AwayTeam'] == equipo_local)  & (h2h['FTR'] == 'A')])
        wins_v = len(h2h[(h2h['HomeTeam'] == equipo_visita) & (h2h['FTR'] == 'H')]) + \
                 len(h2h[(h2h['AwayTeam'] == equipo_visita) & (h2h['FTR'] == 'A')])
        draws  = len(h2h[h2h['FTR'] == 'D'])
        avg_g  = (h2h['FTHG'].sum() + h2h['FTAG'].sum()) / max(len(h2h), 1)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric(f"🏠 {equipo_local[:12]}", wins_l)
        r2.metric("🤝 Empates", draws)
        r3.metric(f"✈️ {equipo_visita[:12]}", wins_v)
        r4.metric("⚽ Goles/partido", f"{avg_g:.1f}")

        st.markdown("---")

        for _, p in h2h.iterrows():
            fecha_str = p['Date'].strftime('%d %b %Y') if pd.notnull(p['Date']) else "?"
            home, away = p['HomeTeam'], p['AwayTeam']
            hg, ag     = int(p['FTHG']), int(p['FTAG'])
            ftr        = p['FTR']

            if ftr == 'H':
                css = "h2h-win-home" if home == equipo_local else "h2h-win-away"
                badge = f'<span class="badge badge-win">🏆 {home}</span>'
            elif ftr == 'A':
                css = "h2h-win-home" if away == equipo_local else "h2h-win-away"
                badge = f'<span class="badge badge-win">🏆 {away}</span>'
            else:
                css = "h2h-draw"
                badge = '<span class="badge badge-draw">🤝 Empate</span>'

            liga_p = p.get('Liga', '')
            st.markdown(f"""
            <div class="h2h-row {css}">
                <span style="color:#8892b0;font-size:0.8rem;min-width:90px">{fecha_str}</span>
                <span style="flex:1;text-align:right;color:#ccd6f6">{home}</span>
                <span style="margin:0 16px;font-size:1.2rem;font-weight:bold;color:#64ffda">{hg} — {ag}</span>
                <span style="flex:1;color:#ccd6f6">{away}</span>
                <span style="min-width:140px;text-align:right">{badge}</span>
                <span style="color:#4a5568;font-size:0.75rem;min-width:80px;text-align:right">{liga_p}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Veredicto final ───────────────────────────────────────────────────
    st.markdown('<div class="section-title">🤖 Veredicto de la IA</div>', unsafe_allow_html=True)

    if pred['prob_local'] == max_prob:
        veredicto = f"🏠 **{equipo_local}** tiene la mayor probabilidad de ganar ({pred['prob_local']*100:.1f}%)"
        color_v   = "#00d4aa"
    elif pred['prob_visita'] == max_prob:
        veredicto = f"✈️ **{equipo_visita}** tiene la mayor probabilidad de ganar ({pred['prob_visita']*100:.1f}%)"
        color_v   = "#ff6b6b"
    else:
        veredicto = f"🤝 El **empate** es el resultado más probable ({pred['prob_empate']*100:.1f}%)"
        color_v   = "#ffa500"

    goles_pred = "⚽ Se esperan **más de 2.5 goles**" if pred['prob_mas_2_5'] > 0.5 \
                 else "🔒 Se esperan **menos de 2.5 goles**"

    st.markdown(f"""
    <div class="prob-card" style="border-color:{color_v}55;text-align:left;padding:20px 28px">
        <p style="font-size:1.1rem;color:#ccd6f6;margin:0">🔮 {veredicto}</p>
        <p style="font-size:0.95rem;color:#8892b0;margin:10px 0 0 0">{goles_pred}</p>
        <p style="font-size:0.85rem;color:#4a5568;margin:8px 0 0 0">
            ⚠️ Predicción basada en datos históricos. No es garantía de resultado.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#8892b0">
        <div style="font-size:5rem">⚽</div>
        <h2 style="color:#ccd6f6">Selecciona un partido en la barra lateral</h2>
        <p>Elige la liga, los dos equipos y presiona <strong>Predecir Partido</strong></p>
        <br>
        <p>El modelo analiza:</p>
        <p>📊 Forma de los últimos 5 partidos &nbsp;·&nbsp; ⚽ Promedio de goles &nbsp;·&nbsp; 🔁 Historial directo</p>
        <p>🏠 Rendimiento local vs visitante &nbsp;·&nbsp; 📈 Diferencia de puntos</p>
    </div>
    """, unsafe_allow_html=True)

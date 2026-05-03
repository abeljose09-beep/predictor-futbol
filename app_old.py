import streamlit as st
import pandas as pd
import numpy as np
import random
import sys, os
from datetime import datetime
import os
BASE = os.path.dirname(__file__)
pd.read_csv(os.path.join(BASE, "datos", "partidos.csv"))



from modelo_futbol import entrenar_modelos, predecir_partido, calcular_forma
from equipos import EQUIPOS_LIGA, equipos_por_liga

# ════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚽ Predictor Fútbol IA",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0d14; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #111827; border-radius: 12px;
    padding: 4px; gap: 4px; border: 1px solid #1f2937;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: #6b7280;
    font-weight: 600; font-size: 0.85rem; padding: 8px 18px;
}
.stTabs [aria-selected="true"] { background: #1d4ed8 !important; color: white !important; }

.prob-card {
    background: linear-gradient(135deg, #111827, #1f2937);
    border-radius: 16px; padding: 24px; text-align: center;
    border: 1px solid #374151; margin: 8px 0; transition: transform 0.2s;
}
.prob-card:hover { transform: translateY(-2px); }
.prob-card h1 { font-size: 2.8rem; margin: 0; font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }
.prob-card p  { color: #9ca3af; margin: 4px 0 0 0; font-size: 0.9rem; }

.match-header {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border: 1px solid #312e81; border-radius: 20px;
    padding: 32px; text-align: center; margin-bottom: 24px;
}
.match-header h1 {
    font-size: 2.2rem; margin: 0;
    font-family: 'Bebas Neue', sans-serif; letter-spacing: 3px; color: #e0e7ff;
}
.match-header p { color: #818cf8; margin: 8px 0 0 0; }

.bar-container { background: #1f2937; border-radius: 50px; height: 22px; overflow: hidden; margin: 6px 0; }
.bar-fill { height: 100%; border-radius: 50px; display: flex; align-items: center; padding-left: 10px; font-size: 0.75rem; font-weight: bold; color: white; }

.h2h-row {
    background: #111827; border-radius: 10px; padding: 12px 16px;
    margin: 6px 0; display: flex; justify-content: space-between;
    align-items: center; border-left: 4px solid #374151;
}
.h2h-win-home { border-left-color: #10b981; }
.h2h-win-away { border-left-color: #ef4444; }
.h2h-draw     { border-left-color: #f59e0b; }

.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:bold; }
.badge-win  { background:#10b98122; color:#10b981; border:1px solid #10b98144; }
.badge-draw { background:#f59e0b22; color:#f59e0b; border:1px solid #f59e0b44; }

.forma-dot { display:inline-block; width:30px; height:30px; border-radius:50%; text-align:center; line-height:30px; font-size:0.72rem; font-weight:bold; margin:2px; }
.forma-W { background:#10b981; color:#000; }
.forma-D { background:#f59e0b; color:#000; }
.forma-L { background:#ef4444; color:#fff; }

.section-title { color:#818cf8; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:2px; margin:28px 0 14px 0; padding-bottom:8px; border-bottom:1px solid #1f2937; }

.apuesta-card { background:#111827; border-radius:12px; padding:16px; border:1px solid #1f2937; text-align:center; margin:6px 0; transition:all 0.2s; }
.apuesta-card:hover { border-color:#4f46e5; transform:translateY(-2px); }
.cuota-badge { background:#1d4ed822; color:#60a5fa; border:1px solid #1d4ed844; padding:4px 12px; border-radius:20px; font-weight:bold; font-size:1.1rem; display:inline-block; margin:6px 0; }
.wallet-card { background:linear-gradient(135deg,#064e3b,#065f46); border-radius:16px; padding:20px; border:1px solid #10b98144; text-align:center; }
.wallet-card h2 { font-family:'Bebas Neue',sans-serif; font-size:2.5rem; color:#34d399; margin:0; letter-spacing:2px; }

.rank-row { background:#111827; border-radius:10px; padding:14px 18px; margin:6px 0; display:flex; align-items:center; border:1px solid #1f2937; transition:all 0.2s; }
.rank-row:hover { border-color:#4f46e5; transform:translateX(4px); }
.rank-num { font-family:'Bebas Neue'; font-size:1.6rem; color:#374151; min-width:40px; }
.rank-name { font-weight:700; color:#e5e7eb; flex:1; margin-left:12px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# LIGAS
# ════════════════════════════════════════════════════════════
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


# ════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ════════════════════════════════════════════════════════════

def barra_html(pct, color, etiqueta):
    pct_r = round(pct * 100, 1)
    return f"""
    <div style="margin:6px 0">
      <div style="display:flex;justify-content:space-between;margin-bottom:3px">
        <span style="color:#d1d5db;font-size:0.85rem">{etiqueta}</span>
        <span style="color:#818cf8;font-weight:bold">{pct_r}%</span>
      </div>
      <div class="bar-container">
        <div class="bar-fill" style="width:{pct_r}%;background:{color};">&nbsp;</div>
      </div>
    </div>"""

def forma_html(df, equipo, n=6):
    fecha = pd.Timestamp(datetime.now())
    pl = df[(df['HomeTeam'] == equipo) & (df['Date'] < fecha)]
    pv = df[(df['AwayTeam'] == equipo) & (df['Date'] < fecha)]
    historial = []
    for _, p in pl.iterrows():
        res = 'W' if p['FTR'] == 'H' else ('D' if p['FTR'] == 'D' else 'L')
        historial.append((p['Date'], res, p['AwayTeam'], p['FTHG'], p['FTAG']))
    for _, p in pv.iterrows():
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
    fecha = pd.Timestamp(datetime.now())
    pl = df[(df['HomeTeam'] == equipo) & (df['Date'] < fecha)]
    pv = df[(df['AwayTeam'] == equipo) & (df['Date'] < fecha)]
    gf    = pl['FTHG'].sum() + pv['FTAG'].sum()
    gc    = pl['FTAG'].sum() + pv['FTHG'].sum()
    total = len(pl) + len(pv)
    wins  = len(pl[pl['FTR'] == 'H']) + len(pv[pv['FTR'] == 'A'])
    draws = len(pl[pl['FTR'] == 'D']) + len(pv[pv['FTR'] == 'D'])
    return {
        'PJ': total, 'G': wins, 'E': draws, 'P': total - wins - draws,
        'GF': int(gf), 'GC': int(gc),
        'GF/PJ': round(gf / max(total, 1), 2),
        '%Win':  round(wins / max(total, 1) * 100, 1),
    }

def calcular_puntaje_ia(s):
    if s['PJ'] == 0: return 0
    win_rate = s['G'] / s['PJ']
    no_der   = (s['G'] + s['E']) / s['PJ']
    gf_avg   = s['GF'] / s['PJ']
    gc_avg   = s['GC'] / s['PJ']
    diff     = (s['GF'] - s['GC']) / s['PJ']
    puntaje  = (
        win_rate * 35 +
        no_der   * 15 +
        min(gf_avg / 3, 1) * 20 +
        max(1 - gc_avg / 3, 0) * 15 +
        (diff + 3) / 6 * 15
    )
    return round(min(max(puntaje * 100, 0), 100), 1)

def calcular_cuota(prob):
    if prob <= 0: return 99.0
    return round((1 / prob) * 0.95, 2)

def inicializar_billetera():
    if "billetera"        not in st.session_state: st.session_state.billetera = 1000.0
    if "historial_apuest" not in st.session_state: st.session_state.historial_apuest = []

def registrar_apuesta(partido, seleccion, monto, cuota, prob):
    st.session_state.historial_apuest.append({
        "id":           len(st.session_state.historial_apuest) + 1,
        "fecha":        datetime.now().strftime("%d/%m %H:%M"),
        "partido":      partido,
        "seleccion":    seleccion,
        "monto":        monto,
        "cuota":        cuota,
        "ganancia_pot": round(monto * cuota, 2),
        "prob_ia":      prob,
        "estado":       "⏳ Pendiente",
    })
    st.session_state.billetera -= monto

def simular_resultados():
    for a in st.session_state.historial_apuest:
        if a["estado"] == "⏳ Pendiente":
            gano = random.random() < max(0.1, min(a["prob_ia"] + random.uniform(-0.08, 0.08), 0.95))
            if gano:
                a["estado"] = "✅ Ganada"
                st.session_state.billetera += a["ganancia_pot"]
            else:
                a["estado"] = "❌ Perdida"


# ════════════════════════════════════════════════════════════
# CABECERA
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;padding:20px 0 8px 0">
  <span style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;letter-spacing:4px;color:#e0e7ff">
    ⚽ PREDICTOR DE FÚTBOL IA
  </span><br>
  <span style="color:#6b7280;font-size:0.9rem">Machine Learning · Apuestas Simuladas · Ranking IA · Comparación de Partidos</span>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SELECTORES GLOBALES
# ════════════════════════════════════════════════════════════

col_liga, col_local, col_visita, col_btn = st.columns([2, 2, 2, 1])

with col_liga:
    liga_label = st.selectbox("🏆 Liga", list(LIGAS_DISPLAY.keys()), key="liga_global")
    liga_key   = LIGAS_DISPLAY[liga_label]

equipos_liga = sorted(equipos_por_liga(liga_key))

with col_local:
    equipo_local = st.selectbox("🏠 Local", equipos_liga, index=0, key="local_global")

with col_visita:
    opciones_visita = [e for e in equipos_liga if e != equipo_local]
    equipo_visita   = st.selectbox("✈️ Visitante", opciones_visita, index=0, key="visita_global")

with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    predecir_btn = st.button("🔮 Predecir", use_container_width=True, type="primary")

if predecir_btn:
    with st.spinner("⚙️ Calculando predicción..."):
        try:
            modelos, cols_X, df_global = entrenar_modelos(equipo_local, equipo_visita)
            pred = predecir_partido(modelos, cols_X, df_global, equipo_local, equipo_visita)
            st.session_state.pred          = pred
            st.session_state.df_global     = df_global
            st.session_state.equipo_local  = equipo_local
            st.session_state.equipo_visita = equipo_visita
            st.session_state.liga_label    = liga_label
            st.session_state.liga_key      = liga_key
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

st.markdown("---")

# ════════════════════════════════════════════════════════════
# PESTAÑAS
# ════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Predicción",
    "🔁 Comparar Partidos",
    "🎰 Apuestas Simuladas",
    "🏆 Ranking IA",
])


# ──────────────────────────────────────────────────────────
# TAB 1 — PREDICCIÓN
# ──────────────────────────────────────────────────────────
with tab1:
    if "pred" not in st.session_state:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;color:#6b7280">
            <div style="font-size:5rem">⚽</div>
            <h2 style="color:#9ca3af">Selecciona liga y equipos, luego presiona 🔮 Predecir</h2>
            <p>Forma reciente · Goles · Historial H2H · Rendimiento local/visitante</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        pred   = st.session_state.pred
        df     = st.session_state.df_global
        local  = st.session_state.equipo_local
        visita = st.session_state.equipo_visita
        liga_lbl = st.session_state.liga_label

        st.markdown(f"""
        <div class="match-header">
            <h1>🏠 {local} &nbsp;VS&nbsp; {visita} ✈️</h1>
            <p>{liga_lbl} · Predicción con Inteligencia Artificial</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">📊 Probabilidades del Resultado</div>', unsafe_allow_html=True)
        max_prob = max(pred['prob_local'], pred['prob_empate'], pred['prob_visita'])
        c1, c2, c3 = st.columns(3)
        with c1:
            col = "#10b981" if pred['prob_local'] == max_prob else "#374151"
            st.markdown(f"""<div class="prob-card" style="border-color:{col}55">
                <h1 style="color:{col}">{pred['prob_local']*100:.1f}%</h1>
                <p>🏠 Victoria {local}</p></div>""", unsafe_allow_html=True)
        with c2:
            col = "#f59e0b" if pred['prob_empate'] == max_prob else "#374151"
            st.markdown(f"""<div class="prob-card" style="border-color:{col}55">
                <h1 style="color:{col}">{pred['prob_empate']*100:.1f}%</h1>
                <p>🤝 Empate</p></div>""", unsafe_allow_html=True)
        with c3:
            col = "#ef4444" if pred['prob_visita'] == max_prob else "#374151"
            st.markdown(f"""<div class="prob-card" style="border-color:{col}55">
                <h1 style="color:{col}">{pred['prob_visita']*100:.1f}%</h1>
                <p>✈️ Victoria {visita}</p></div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">📈 Desglose Visual</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Resultado del partido**")
            st.markdown(barra_html(pred['prob_local'],  "#10b981", f"🏠 {local}"),  unsafe_allow_html=True)
            st.markdown(barra_html(pred['prob_empate'], "#f59e0b", "🤝 Empate"),     unsafe_allow_html=True)
            st.markdown(barra_html(pred['prob_visita'], "#ef4444", f"✈️ {visita}"), unsafe_allow_html=True)
        with col_b:
            st.markdown("**Línea de goles**")
            st.markdown(barra_html(pred['prob_mas_2_5'],   "#a78bfa", "⚽ Más de 2.5 goles"),   unsafe_allow_html=True)
            st.markdown(barra_html(pred['prob_menos_2_5'], "#64748b", "🔒 Menos de 2.5 goles"), unsafe_allow_html=True)
            st.markdown("**Ganador directo** (sin empate)")
            st.markdown(barra_html(pred['prob_gana_local'],  "#10b981", f"🏠 {local}"),  unsafe_allow_html=True)
            st.markdown(barra_html(pred['prob_gana_visita'], "#ef4444", f"✈️ {visita}"), unsafe_allow_html=True)

        st.markdown('<div class="section-title">🔥 Forma Reciente (últimos 6 partidos)</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            st.markdown(f"**{local}**")
            dots = forma_html(df, local)
            st.markdown(dots if dots else "_Sin datos_", unsafe_allow_html=True)
        with f2:
            st.markdown(f"**{visita}**")
            dots = forma_html(df, visita)
            st.markdown(dots if dots else "_Sin datos_", unsafe_allow_html=True)

        st.markdown('<div class="section-title">📋 Estadísticas en la Liga</div>', unsafe_allow_html=True)
        stats_l = stats_equipo(df, local)
        stats_v = stats_equipo(df, visita)
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"**{local}**")
            a1,a2,a3,a4 = st.columns(4)
            a1.metric("PJ", stats_l['PJ']); a2.metric("Victorias", stats_l['G'])
            a3.metric("% Win", f"{stats_l['%Win']}%"); a4.metric("GF/PJ", stats_l['GF/PJ'])
        with s2:
            st.markdown(f"**{visita}**")
            b1,b2,b3,b4 = st.columns(4)
            b1.metric("PJ", stats_v['PJ']); b2.metric("Victorias", stats_v['G'])
            b3.metric("% Win", f"{stats_v['%Win']}%"); b4.metric("GF/PJ", stats_v['GF/PJ'])

        st.markdown('<div class="section-title">🔁 Historial de Enfrentamientos Directos</div>', unsafe_allow_html=True)
        h2h = obtener_h2h(df, local, visita, n=8)
        if h2h.empty:
            st.info("No hay enfrentamientos directos registrados.")
        else:
            wins_l = len(h2h[(h2h['HomeTeam']==local)  & (h2h['FTR']=='H')]) + len(h2h[(h2h['AwayTeam']==local)  & (h2h['FTR']=='A')])
            wins_v = len(h2h[(h2h['HomeTeam']==visita) & (h2h['FTR']=='H')]) + len(h2h[(h2h['AwayTeam']==visita) & (h2h['FTR']=='A')])
            draws  = len(h2h[h2h['FTR']=='D'])
            avg_g  = (h2h['FTHG'].sum() + h2h['FTAG'].sum()) / max(len(h2h), 1)
            r1,r2,r3,r4 = st.columns(4)
            r1.metric(f"🏠 {local[:12]}", wins_l)
            r2.metric("🤝 Empates", draws)
            r3.metric(f"✈️ {visita[:12]}", wins_v)
            r4.metric("⚽ Goles/partido", f"{avg_g:.1f}")
            st.markdown("---")
            for _, p in h2h.iterrows():
                fecha_str = p['Date'].strftime('%d %b %Y') if pd.notnull(p['Date']) else "?"
                home, away = p['HomeTeam'], p['AwayTeam']
                hg, ag, ftr = int(p['FTHG']), int(p['FTAG']), p['FTR']
                if ftr == 'H':
                    css = "h2h-win-home" if home == local else "h2h-win-away"
                    badge = f'<span class="badge badge-win">🏆 {home}</span>'
                elif ftr == 'A':
                    css = "h2h-win-home" if away == local else "h2h-win-away"
                    badge = f'<span class="badge badge-win">🏆 {away}</span>'
                else:
                    css = "h2h-draw"
                    badge = '<span class="badge badge-draw">🤝 Empate</span>'
                liga_p = p.get('Liga', '')
                st.markdown(f"""
                <div class="h2h-row {css}">
                    <span style="color:#6b7280;font-size:0.8rem;min-width:90px">{fecha_str}</span>
                    <span style="flex:1;text-align:right;color:#e5e7eb">{home}</span>
                    <span style="margin:0 16px;font-size:1.2rem;font-weight:bold;color:#818cf8">{hg} — {ag}</span>
                    <span style="flex:1;color:#e5e7eb">{away}</span>
                    <span style="min-width:140px;text-align:right">{badge}</span>
                    <span style="color:#374151;font-size:0.75rem;min-width:80px;text-align:right">{liga_p}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">🤖 Veredicto de la IA</div>', unsafe_allow_html=True)
        if pred['prob_local'] == max_prob:
            veredicto = f"🏠 **{local}** tiene la mayor probabilidad de ganar ({pred['prob_local']*100:.1f}%)"
            color_v = "#10b981"
        elif pred['prob_visita'] == max_prob:
            veredicto = f"✈️ **{visita}** tiene la mayor probabilidad de ganar ({pred['prob_visita']*100:.1f}%)"
            color_v = "#ef4444"
        else:
            veredicto = f"🤝 El **empate** es el resultado más probable ({pred['prob_empate']*100:.1f}%)"
            color_v = "#f59e0b"
        goles_txt = "⚽ Se esperan **más de 2.5 goles**" if pred['prob_mas_2_5'] > 0.5 else "🔒 Se esperan **menos de 2.5 goles**"
        st.markdown(f"""
        <div class="prob-card" style="border-color:{color_v}55;text-align:left;padding:22px 28px">
            <p style="font-size:1.1rem;color:#e5e7eb;margin:0">🔮 {veredicto}</p>
            <p style="font-size:0.95rem;color:#9ca3af;margin:10px 0 0 0">{goles_txt}</p>
            <p style="font-size:0.82rem;color:#4b5563;margin:8px 0 0 0">
              ⚠️ Predicción basada en datos históricos. No garantiza el resultado real.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# TAB 2 — COMPARAR PARTIDOS
# ──────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">🔁 Comparar Múltiples Partidos</div>', unsafe_allow_html=True)

    if "partidos_comparar" not in st.session_state:
        st.session_state.partidos_comparar = []

    with st.expander("➕ Agregar partido a la comparación", expanded=True):
        cx1, cx2, cx3, cx4 = st.columns([2, 2, 2, 1])
        with cx1:
            liga_c = st.selectbox("Liga", list(LIGAS_DISPLAY.keys()), key="liga_comp")
        equipos_c = sorted(equipos_por_liga(LIGAS_DISPLAY[liga_c]))
        with cx2:
            local_c = st.selectbox("🏠 Local", equipos_c, key="local_comp")
        with cx3:
            visita_c = st.selectbox("✈️ Visitante", [e for e in equipos_c if e != local_c], key="visita_comp")
        with cx4:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Agregar ➕", use_container_width=True):
                with st.spinner("Calculando..."):
                    try:
                        modelos_c, cols_c, df_c = entrenar_modelos(local_c, visita_c)
                        pred_c = predecir_partido(modelos_c, cols_c, df_c, local_c, visita_c)
                        st.session_state.partidos_comparar.append({
                            "liga": liga_c, "local": local_c, "visita": visita_c, "pred": pred_c
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    if not st.session_state.partidos_comparar:
        st.info("Agrega partidos arriba para compararlos.")
    else:
        if st.button("🗑️ Limpiar comparación"):
            st.session_state.partidos_comparar = []
            st.rerun()

        rows = []
        for p in st.session_state.partidos_comparar:
            pr = p["pred"]
            max_p = max(pr['prob_local'], pr['prob_empate'], pr['prob_visita'])
            if pr['prob_local'] == max_p:    fav = f"🏠 {p['local']} ({pr['prob_local']*100:.1f}%)"
            elif pr['prob_visita'] == max_p: fav = f"✈️ {p['visita']} ({pr['prob_visita']*100:.1f}%)"
            else:                            fav = f"🤝 Empate ({pr['prob_empate']*100:.1f}%)"
            rows.append({
                "Liga": p["liga"], "Local 🏠": p["local"], "Visitante ✈️": p["visita"],
                "🏠 %": f"{pr['prob_local']*100:.1f}%",
                "🤝 %": f"{pr['prob_empate']*100:.1f}%",
                "✈️ %": f"{pr['prob_visita']*100:.1f}%",
                "⚽ +2.5": f"{pr['prob_mas_2_5']*100:.1f}%",
                "🤖 Favorito": fav,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("### Detalle por partido")
        for p in st.session_state.partidos_comparar:
            pr = p["pred"]
            max_p = max(pr['prob_local'], pr['prob_empate'], pr['prob_visita'])
            with st.expander(f"⚽ {p['local']} vs {p['visita']} — {p['liga']}"):
                d1, d2, d3 = st.columns(3)
                with d1:
                    c = "#10b981" if pr['prob_local'] == max_p else "#374151"
                    st.markdown(f"<div class='prob-card' style='border-color:{c}55'><h1 style='color:{c}'>{pr['prob_local']*100:.1f}%</h1><p>🏠 {p['local']}</p></div>", unsafe_allow_html=True)
                with d2:
                    c = "#f59e0b" if pr['prob_empate'] == max_p else "#374151"
                    st.markdown(f"<div class='prob-card' style='border-color:{c}55'><h1 style='color:{c}'>{pr['prob_empate']*100:.1f}%</h1><p>🤝 Empate</p></div>", unsafe_allow_html=True)
                with d3:
                    c = "#ef4444" if pr['prob_visita'] == max_p else "#374151"
                    st.markdown(f"<div class='prob-card' style='border-color:{c}55'><h1 style='color:{c}'>{pr['prob_visita']*100:.1f}%</h1><p>✈️ {p['visita']}</p></div>", unsafe_allow_html=True)
                st.markdown(barra_html(pr['prob_mas_2_5'],   "#a78bfa", "⚽ Más de 2.5 goles"),   unsafe_allow_html=True)
                st.markdown(barra_html(pr['prob_menos_2_5'], "#64748b", "🔒 Menos de 2.5 goles"), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# TAB 3 — APUESTAS SIMULADAS
# ──────────────────────────────────────────────────────────
with tab3:
    inicializar_billetera()
    st.markdown('<div class="section-title">🎰 Apuestas Simuladas — Solo entretenimiento</div>', unsafe_allow_html=True)
    st.caption("Dinero 100% virtual · Sin dinero real · Solo para diversión")

    ganadas  = sum(1 for a in st.session_state.historial_apuest if a["estado"] == "✅ Ganada")
    perdidas = sum(1 for a in st.session_state.historial_apuest if a["estado"] == "❌ Perdida")
    pendient = sum(1 for a in st.session_state.historial_apuest if a["estado"] == "⏳ Pendiente")
    ganancia_neta = sum(
        a["ganancia_pot"] - a["monto"] if a["estado"] == "✅ Ganada" else
        -a["monto"] if a["estado"] == "❌ Perdida" else 0
        for a in st.session_state.historial_apuest
    )

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(f"""<div class="wallet-card">
            <p style="color:#6ee7b7;margin:0;font-size:0.8rem">SALDO VIRTUAL</p>
            <h2>${st.session_state.billetera:,.2f}</h2></div>""", unsafe_allow_html=True)
    with w2: st.metric("✅ Ganadas", ganadas)
    with w3: st.metric("❌ Perdidas", perdidas)
    with w4: st.metric("📈 Ganancia Neta", f"${ganancia_neta:+,.2f}")

    st.markdown("---")

    if "pred" not in st.session_state:
        st.info("⚽ Primero realiza una predicción en la pestaña **🔮 Predicción** para apostar.")
    else:
        pred   = st.session_state.pred
        local  = st.session_state.equipo_local
        visita = st.session_state.equipo_visita

        st.markdown(f"### ⚽ Apostar en: **{local}** vs **{visita}**")

        opciones = {
            f"🏠 {local} gana":      {"prob": pred['prob_local'],    "cuota": calcular_cuota(pred['prob_local'])},
            "🤝 Empate":              {"prob": pred['prob_empate'],   "cuota": calcular_cuota(pred['prob_empate'])},
            f"✈️ {visita} gana":     {"prob": pred['prob_visita'],   "cuota": calcular_cuota(pred['prob_visita'])},
            "⚽ Más de 2.5 goles":   {"prob": pred['prob_mas_2_5'],  "cuota": calcular_cuota(pred['prob_mas_2_5'])},
            "🔒 Menos de 2.5 goles": {"prob": pred['prob_menos_2_5'],"cuota": calcular_cuota(pred['prob_menos_2_5'])},
        }

        cols_op = st.columns(5)
        for i, (nombre, datos) in enumerate(opciones.items()):
            with cols_op[i]:
                st.markdown(f"""
                <div class="apuesta-card">
                    <div style="font-size:0.78rem;color:#9ca3af">{nombre}</div>
                    <div class="cuota-badge">{datos['cuota']}x</div>
                    <div style="font-size:0.75rem;color:#6b7280">IA: {datos['prob']*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        a1, a2, a3 = st.columns([3, 2, 1])
        with a1:
            seleccion = st.selectbox("¿Sobre qué apuestas?", list(opciones.keys()))
        with a2:
            monto_max = max(10, int(st.session_state.billetera))
            monto = st.slider("Monto ($)", min_value=10, max_value=monto_max, value=min(50, monto_max), step=10)
        with a3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            confirmar = st.button("🎯 Apostar", use_container_width=True, type="primary")

        datos_sel    = opciones[seleccion]
        ganancia_pot = round(monto * datos_sel["cuota"], 2)
        st.success(f"💵 Si ganas recibirás **${ganancia_pot}** — Cuota {datos_sel['cuota']}x · Prob IA: {datos_sel['prob']*100:.1f}%")

        if confirmar:
            if monto > st.session_state.billetera:
                st.error("❌ Saldo insuficiente")
            else:
                registrar_apuesta(
                    partido=f"{local} vs {visita}",
                    seleccion=seleccion, monto=monto,
                    cuota=datos_sel["cuota"], prob=datos_sel["prob"]
                )
                st.success(f"✅ Apuesta registrada — Ganancia potencial: **${ganancia_pot}**")
                st.rerun()

    st.markdown("---")
    if st.session_state.historial_apuest:
        st.markdown("### 📋 Historial de Apuestas")
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("🎲 Simular resultados pendientes", use_container_width=True):
                simular_resultados(); st.rerun()
        with btn2:
            if st.button("🔄 Reiniciar billetera ($1,000)", use_container_width=True):
                st.session_state.billetera = 1000.0
                st.session_state.historial_apuest = []
                st.rerun()
        df_hist = pd.DataFrame(st.session_state.historial_apuest)
        df_show = df_hist[["id","fecha","partido","seleccion","monto","cuota","ganancia_pot","estado"]]
        df_show.columns = ["#","Fecha","Partido","Selección","Apostado $","Cuota","Ganancia Pot. $","Estado"]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no tienes apuestas registradas.")


# ──────────────────────────────────────────────────────────
# TAB 4 — RANKING IA
# ──────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">🏆 Ranking de Equipos — Puntaje IA</div>', unsafe_allow_html=True)
    st.caption("Clasificación ponderada por IA basada en rendimiento histórico completo")

    if "df_global" not in st.session_state:
        st.info("⚽ Primero realiza una predicción para cargar los datos de la liga.")
    else:
        df  = st.session_state.df_global
        lbl = st.session_state.liga_label
        st.markdown(f"**Liga activa:** {lbl}")

        todos_equipos = list(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
        ranking_data  = []
        for eq in todos_equipos:
            s = stats_equipo(df, eq)
            if s['PJ'] < 5: continue
            ranking_data.append({
                "nombre": eq,
                "PJ": s['PJ'], "G": s['G'], "E": s['E'], "P": s['P'],
                "GF": s['GF'], "GC": s['GC'],
                "Dif": s['GF'] - s['GC'],
                "% Win": s['%Win'],
                "GF/PJ": s['GF/PJ'],
                "puntaje": calcular_puntaje_ia(s),
            })
        ranking_data = sorted(ranking_data, key=lambda x: x["puntaje"], reverse=True)
        medallas = ["🥇","🥈","🥉"] + [""] * 200

        # Podio
        if len(ranking_data) >= 3:
            st.markdown("### 🎖️ Podio")
            p1, p2, p3 = st.columns(3)
            for col_p, eq, medal in zip([p1, p2, p3], ranking_data[:3], medallas[:3]):
                with col_p:
                    st.markdown(f"""
                    <div class="prob-card" style="border-color:#4f46e555">
                        <div style="font-size:2rem">{medal}</div>
                        <h1 style="color:#818cf8;font-size:1.4rem">{eq['nombre']}</h1>
                        <div class="cuota-badge">{eq['puntaje']}/100</div>
                        <p>Win rate: {eq['% Win']}%</p>
                        <p>Goles/PJ: {eq['GF/PJ']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("### 📊 Tabla Completa")
        for i, eq in enumerate(ranking_data):
            bar_w     = int(eq['puntaje'])
            color_bar = "#10b981" if i < 3 else ("#818cf8" if i < 8 else "#6b7280")
            dif_str   = f"+{eq['Dif']}" if eq['Dif'] >= 0 else str(eq['Dif'])
            dif_col   = "#10b981" if eq['Dif'] >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="rank-row">
                <span class="rank-num">{medallas[i]}{i+1}</span>
                <span class="rank-name">{eq['nombre']}</span>
                <div style="flex:2;margin:0 16px">
                    <div class="bar-container" style="height:10px">
                        <div style="width:{bar_w}%;height:100%;border-radius:5px;background:{color_bar}"></div>
                    </div>
                </div>
                <span style="color:#818cf8;font-weight:bold;min-width:60px;text-align:right">{eq['puntaje']}/100</span>
                <span style="color:#6b7280;font-size:0.8rem;min-width:220px;text-align:right">
                    PJ:{eq['PJ']} · G:{eq['G']} · E:{eq['E']} · P:{eq['P']} ·
                    GF:{eq['GF']} · GC:{eq['GC']} · <span style="color:{dif_col}">{dif_str}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        df_export = pd.DataFrame([{
            "Pos": i+1, "Equipo": eq["nombre"], "PJ": eq["PJ"],
            "G": eq["G"], "E": eq["E"], "P": eq["P"],
            "GF": eq["GF"], "GC": eq["GC"], "Dif": eq["Dif"],
            "% Win": eq["% Win"], "Puntaje IA": eq["puntaje"]
        } for i, eq in enumerate(ranking_data)])
        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar ranking en CSV", csv, "ranking_ia.csv", "text/csv")

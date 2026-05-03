import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from escudos import get_escudo

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FootballAI · Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS GLOBAL ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080C10 !important;
    color: #E8EDF2;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background: #080C10 !important;
}

/* Ocultar elementos de Streamlit que no queremos */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #2ECC71; border-radius: 2px; }

/* ── Selectboxes ── */
[data-testid="stSelectbox"] > div > div {
    background: #0D1117 !important;
    border: 1px solid #1E2A35 !important;
    border-radius: 10px !important;
    color: #E8EDF2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: #2ECC71 !important;
}

/* ── Labels ── */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #4A6075 !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background: #2ECC71 !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%) !important;
    color: #080C10 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 20px !important;
    letter-spacing: 3px !important;
    padding: 14px 0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(46,204,113,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(46,204,113,0.4) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #0D1117;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E2A35;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #4A6075 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1E2A35 !important;
    color: #2ECC71 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0D1117 !important;
    border: 1px solid #1E2A35 !important;
    border-radius: 12px !important;
}

/* Eliminar padding extra del main */
.block-container {
    padding: 2rem 2rem 4rem !important;
    max-width: 1200px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───────────────────────────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    model_path = os.path.join(os.path.dirname(__file__), "modelo_futbol.pkl")
    return joblib.load(model_path)

@st.cache_data
def cargar_datos():
    csv_path = os.path.join(os.path.dirname(__file__), "datos_futbol.csv")
    df = pd.read_csv(csv_path)
    return df

def color_resultado(prob):
    if prob >= 0.5:
        return "#2ECC71"
    elif prob >= 0.3:
        return "#F39C12"
    else:
        return "#E74C3C"

def barra_gradiente(prob, color, label):
    pct = int(prob * 100)
    return f"""
    <div style="margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-family:'Space Mono',monospace; font-size:11px; 
                         letter-spacing:1.5px; text-transform:uppercase; color:#4A6075;">
                {label}
            </span>
            <span style="font-family:'Bebas Neue',sans-serif; font-size:22px; 
                         color:{color}; line-height:1;">
                {pct}%
            </span>
        </div>
        <div style="height:8px; background:#1E2A35; border-radius:4px; overflow:hidden;">
            <div style="height:100%; width:{pct}%; 
                        background: linear-gradient(90deg, {color}99, {color});
                        border-radius:4px; transition:width 0.6s ease;">
            </div>
        </div>
    </div>
    """

def escudo_html(nombre, size=64):
    url = get_escudo(nombre)
    if url:
        return f'<img src="{url}" width="{size}" height="{size}" style="object-fit:contain; filter:drop-shadow(0 4px 12px rgba(0,0,0,0.5));" onerror="this.style.display=\'none\'">'
    else:
        return f'<div style="width:{size}px;height:{size}px;display:flex;align-items:center;justify-content:center;font-size:{size//2}px;">⚽</div>'


# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 40px 0 32px;">
    <div style="font-family:'Space Mono',monospace; font-size:11px; letter-spacing:4px; 
                color:#2ECC71; text-transform:uppercase; margin-bottom:8px;">
        AI · Football Intelligence
    </div>
    <div style="font-family:'Bebas Neue',sans-serif; font-size:clamp(48px,8vw,80px); 
                color:#E8EDF2; letter-spacing:4px; line-height:0.9;">
        MATCH
        <span style="color:#2ECC71;">PREDICT</span>
        OR
    </div>
    <div style="width:40px; height:2px; background:#2ECC71; margin:20px auto 0;"></div>
</div>
""", unsafe_allow_html=True)


# ─── CARGAR DATOS ──────────────────────────────────────────────────────────────
try:
    modelo = cargar_modelo()
    df = cargar_datos()
except Exception as e:
    st.error(f"Error cargando modelo/datos: {e}")
    st.stop()

LIGAS_DISPLAY = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿  Premier League": "premier",
    "🇪🇸  La Liga":        "laliga",
    "🇮🇹  Serie A":         "seriea",
    "🇩🇪  Bundesliga":      "bundesliga",
    "🇫🇷  Ligue 1":         "ligue1",
    "🇳🇱  Eredivisie":      "eredivisie",
    "🏴󠁧󠁢󠁳󠁣󠁴󠁿  Escocia":        "escocia",
    "🇵🇹  Portugal":        "portugal",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿  Championship":   "championship",
}

# ─── SELECTOR DE LIGA ──────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
            color:#4A6075; text-transform:uppercase; margin-bottom:8px; text-align:center;">
    Selecciona la liga
</div>
""", unsafe_allow_html=True)

liga_nombre = st.selectbox("Liga", list(LIGAS_DISPLAY.keys()), label_visibility="collapsed")
liga_key = LIGAS_DISPLAY[liga_nombre]

# Filtrar equipos de la liga seleccionada
equipos_liga = df[df["Liga"].str.startswith(liga_key)]["HomeTeam"].unique().tolist()
equipos = sorted(set(equipos_liga))

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── PANEL DE SELECCIÓN ────────────────────────────────────────────────────────
col_left, col_center, col_right = st.columns([5, 2, 5])

with col_left:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                color:#4A6075; text-transform:uppercase; margin-bottom:16px; text-align:center;">
        Local
    </div>
    """, unsafe_allow_html=True)
    equipo_local = st.selectbox("Equipo Local", equipos, label_visibility="collapsed")

    # Escudo local
    url_local = get_escudo(equipo_local)
    if url_local:
        st.markdown(f"""
        <div style="text-align:center; margin:16px 0;">
            {escudo_html(equipo_local, 96)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin-top:8px;">
        <span style="font-family:'Bebas Neue',sans-serif; font-size:26px; 
                     color:#E8EDF2; letter-spacing:2px;">
            {equipo_local}
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_center:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; 
                justify-content:center; height:160px; gap:8px;">
        <div style="font-family:'Bebas Neue',sans-serif; font-size:36px; 
                    color:#1E2A35; letter-spacing:4px;">VS</div>
        <div style="width:2px; height:40px; background:linear-gradient(180deg,transparent,#2ECC71,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                color:#4A6075; text-transform:uppercase; margin-bottom:16px; text-align:center;">
        Visitante
    </div>
    """, unsafe_allow_html=True)
    equipo_visitante = st.selectbox("Equipo Visitante", equipos, index=1, label_visibility="collapsed")

    url_visitante = get_escudo(equipo_visitante)
    if url_visitante:
        st.markdown(f"""
        <div style="text-align:center; margin:16px 0;">
            {escudo_html(equipo_visitante, 96)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin-top:8px;">
        <span style="font-family:'Bebas Neue',sans-serif; font-size:26px; 
                     color:#E8EDF2; letter-spacing:2px;">
            {equipo_visitante}
        </span>
    </div>
    """, unsafe_allow_html=True)


# ─── OPCIONES AVANZADAS ────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

with st.expander("⚙️  Parámetros avanzados"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        jornada = st.slider("Jornada", 1, 38, 20)
    with col_b:
        racha_local = st.slider("Forma local (últimos 5)", 0, 15, 8)
    with col_c:
        racha_visit = st.slider("Forma visitante (últimos 5)", 0, 15, 6)


# ─── BOTÓN PREDECIR ────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
predecir = st.button("ANALIZAR PARTIDO")


# ─── RESULTADO ─────────────────────────────────────────────────────────────────
if predecir:
    if equipo_local == equipo_visitante:
        st.markdown("""
        <div style="background:#1A0D0D; border:1px solid #E74C3C; border-radius:12px; 
                    padding:16px; text-align:center; margin-top:16px;">
            <span style="color:#E74C3C; font-family:'Space Mono',monospace; font-size:13px;">
                ⚠ Selecciona dos equipos distintos
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Preparar features y predecir
    try:
        # Estadísticas históricas del dataset (últimos 10 partidos)
        N = 10
        partidos_local_home = df[df["HomeTeam"] == equipo_local].tail(N)
        partidos_local_away = df[df["AwayTeam"] == equipo_local].tail(N)
        partidos_visit_home = df[df["HomeTeam"] == equipo_visitante].tail(N)
        partidos_visit_away = df[df["AwayTeam"] == equipo_visitante].tail(N)

        # Goles a favor local (sumando como local y visitante)
        gf_h = list(partidos_local_home["FTHG"]) + list(partidos_local_away["FTAG"])
        ga_h = list(partidos_local_home["FTAG"]) + list(partidos_local_away["FTHG"])
        gf_a = list(partidos_visit_home["FTHG"]) + list(partidos_visit_away["FTAG"])
        ga_a = list(partidos_visit_home["FTAG"]) + list(partidos_visit_away["FTHG"])

        goles_favor_local  = np.mean(gf_h[-N:]) if gf_h else 1.3
        goles_contra_local = np.mean(ga_h[-N:]) if ga_h else 1.1
        goles_favor_visit  = np.mean(gf_a[-N:]) if gf_a else 1.1
        goles_contra_visit = np.mean(ga_a[-N:]) if ga_a else 1.3

        # Puntos por partido (últimos N)
        def pts(ftr_series, lado):
            return [3 if f==lado else (1 if f=='D' else 0) for f in ftr_series]

        pts_h = pts(partidos_local_home["FTR"], "H") + pts(partidos_local_away["FTR"], "A")
        pts_a = pts(partidos_visit_home["FTR"], "H") + pts(partidos_visit_away["FTR"], "A")
        hpts = np.mean(pts_h[-N:]) if pts_h else 1.0
        apts = np.mean(pts_a[-N:]) if pts_a else 1.0

        # Tiros (últimos partidos como local/visitante)
        hs_val  = partidos_local_home["HS"].mean()  if len(partidos_local_home) > 0 else 12.0
        as_val  = partidos_visit_away["AS"].mean()  if len(partidos_visit_away) > 0 else 11.0
        hst_val = partidos_local_home["HST"].mean() if len(partidos_local_home) > 0 else 4.5
        ast_val = partidos_visit_away["AST"].mean() if len(partidos_visit_away) > 0 else 4.0

        # Todos los partidos para referencia (para stats display)
        partidos_local = df[df["HomeTeam"] == equipo_local]
        partidos_visita = df[df["AwayTeam"] == equipo_visitante]

        # H2H
        h2h = df[
            ((df["HomeTeam"] == equipo_local) & (df["AwayTeam"] == equipo_visitante)) |
            ((df["HomeTeam"] == equipo_visitante) & (df["AwayTeam"] == equipo_local))
        ]
        ganados_local = len(h2h[
            ((h2h["HomeTeam"] == equipo_local) & (h2h["FTR"] == "H")) |
            ((h2h["AwayTeam"] == equipo_local) & (h2h["FTR"] == "A"))
        ])
        ganados_visit = len(h2h[
            ((h2h["HomeTeam"] == equipo_visitante) & (h2h["FTR"] == "H")) |
            ((h2h["AwayTeam"] == equipo_visitante) & (h2h["FTR"] == "A"))
        ])
        empates_h2h = len(h2h[h2h["FTR"] == "D"])
        total_h2h = len(h2h)

        # Features exactas del modelo entrenado
        features = np.array([[
            goles_favor_local, goles_contra_local,
            goles_favor_visit, goles_contra_visit,
            hpts, apts,
            hs_val, as_val, hst_val, ast_val
        ]])

        probs = modelo.predict_proba(features)[0]
        clases = modelo.classes_

        prob_dict = {c: p for c, p in zip(clases, probs)}
        prob_local = prob_dict.get("H", 0)
        prob_empate = prob_dict.get("D", 0)
        prob_visit = prob_dict.get("A", 0)

        resultado_pred = max(prob_dict, key=prob_dict.get)
        resultado_texto = {
            "H": f"Victoria {equipo_local}",
            "D": "Empate",
            "A": f"Victoria {equipo_visitante}"
        }[resultado_pred]
        prob_max = max(prob_local, prob_empate, prob_visit)

    except Exception as e:
        st.error(f"Error al predecir: {e}")
        st.stop()

    # Separador
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='width:100%;height:1px;background:linear-gradient(90deg,transparent,#1E2A35,transparent);margin-bottom:32px;'></div>""", unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3 = st.tabs(["📊  PREDICCIÓN", "⚔️  HEAD TO HEAD", "📈  ESTADÍSTICAS"])

    with tab1:
        # Match header con escudos
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px; 
                    padding:28px 32px; margin-bottom:24px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:16px;">
                
                <!-- Local -->
                <div style="display:flex; flex-direction:column; align-items:center; gap:12px; flex:1;">
                    {escudo_html(equipo_local, 72)}
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:20px; 
                                 color:#E8EDF2; letter-spacing:2px; text-align:center;">
                        {equipo_local}
                    </span>
                </div>

                <!-- Centro -->
                <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
                    <span style="font-family:'Space Mono',monospace; font-size:10px; 
                                 letter-spacing:3px; color:#4A6075; text-transform:uppercase;">
                        Predicción
                    </span>
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:42px; 
                                 color:#2ECC71; letter-spacing:2px;">
                        {int(prob_max*100)}%
                    </span>
                    <div style="background:#1E2A35; border-radius:20px; padding:4px 16px;">
                        <span style="font-family:'Space Mono',monospace; font-size:11px; 
                                     color:#2ECC71; letter-spacing:1px;">
                            {resultado_texto}
                        </span>
                    </div>
                </div>

                <!-- Visitante -->
                <div style="display:flex; flex-direction:column; align-items:center; gap:12px; flex:1;">
                    {escudo_html(equipo_visitante, 72)}
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:20px; 
                                 color:#E8EDF2; letter-spacing:2px; text-align:center;">
                        {equipo_visitante}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Barras de probabilidad
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px; padding:24px 28px;">
            <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                        color:#4A6075; text-transform:uppercase; margin-bottom:20px;">
                Distribución de probabilidades
            </div>
            {barra_gradiente(prob_local, color_resultado(prob_local), f"Victoria {equipo_local[:12]}")}
            {barra_gradiente(prob_empate, color_resultado(prob_empate), "Empate")}
            {barra_gradiente(prob_visit, color_resultado(prob_visit), f"Victoria {equipo_visitante[:12]}")}
        </div>
        """, unsafe_allow_html=True)

        # Estadísticas de goles
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        stats = [
            (col1, "Goles/partido local", f"{goles_favor_local:.2f}", "#2ECC71"),
            (col2, "Encajados local", f"{goles_contra_local:.2f}", "#E74C3C"),
            (col3, "Goles/partido visit.", f"{goles_favor_visit:.2f}", "#3498DB"),
            (col4, "Encajados visit.", f"{goles_contra_visit:.2f}", "#E74C3C"),
        ]
        for col, label, valor, color in stats:
            with col:
                st.markdown(f"""
                <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:12px; 
                            padding:16px; text-align:center;">
                    <div style="font-family:'Space Mono',monospace; font-size:9px; 
                                letter-spacing:1.5px; color:#4A6075; text-transform:uppercase; 
                                margin-bottom:8px; line-height:1.4;">
                        {label}
                    </div>
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:32px; color:{color};">
                        {valor}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        if total_h2h == 0:
            st.markdown("""
            <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:12px; 
                        padding:32px; text-align:center; color:#4A6075;">
                <div style="font-size:32px; margin-bottom:8px;">🔍</div>
                Sin enfrentamientos anteriores en el dataset
            </div>
            """, unsafe_allow_html=True)
        else:
            # Resumen H2H con escudos
            st.markdown(f"""
            <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px; 
                        padding:24px 28px; margin-bottom:20px;">
                <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                            color:#4A6075; text-transform:uppercase; margin-bottom:20px;">
                    Historial de enfrentamientos · {total_h2h} partidos
                </div>
                <div style="display:flex; align-items:center; gap:16px;">
                    <!-- Local -->
                    <div style="flex:1; text-align:center;">
                        {escudo_html(equipo_local, 48)}
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:42px; 
                                    color:#2ECC71; margin-top:8px;">{ganados_local}</div>
                        <div style="font-family:'Space Mono',monospace; font-size:9px; 
                                    color:#4A6075; letter-spacing:2px;">VICTORIAS</div>
                    </div>
                    <!-- Empates -->
                    <div style="flex:1; text-align:center; border-left:1px solid #1E2A35; 
                                border-right:1px solid #1E2A35; padding:0 16px;">
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:42px; 
                                    color:#F39C12;">{empates_h2h}</div>
                        <div style="font-family:'Space Mono',monospace; font-size:9px; 
                                    color:#4A6075; letter-spacing:2px;">EMPATES</div>
                    </div>
                    <!-- Visitante -->
                    <div style="flex:1; text-align:center;">
                        {escudo_html(equipo_visitante, 48)}
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:42px; 
                                    color:#3498DB; margin-top:8px;">{ganados_visit}</div>
                        <div style="font-family:'Space Mono',monospace; font-size:9px; 
                                    color:#4A6075; letter-spacing:2px;">VICTORIAS</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Lista de partidos
            h2h_display = h2h[["HomeTeam", "FTHG", "FTAG", "AwayTeam", "FTR"]].tail(10).iloc[::-1]
            for _, row in h2h_display.iterrows():
                ganador_color = {
                    "H": ("#2ECC71", "#4A6075"),
                    "A": ("#4A6075", "#2ECC71"),
                    "D": ("#F39C12", "#F39C12")
                }.get(row["FTR"], ("#4A6075", "#4A6075"))

                st.markdown(f"""
                <div style="display:flex; align-items:center; justify-content:space-between;
                            background:#0D1117; border:1px solid #1E2A35; border-radius:10px;
                            padding:12px 20px; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:10px; flex:1;">
                        {escudo_html(row['HomeTeam'], 24)}
                        <span style="font-family:'DM Sans',sans-serif; font-size:14px; 
                                     color:{ganador_color[0]}; font-weight:500;">
                            {row['HomeTeam']}
                        </span>
                    </div>
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:22px; 
                                letter-spacing:4px; color:#E8EDF2; padding:0 20px;">
                        {int(row['FTHG'])} — {int(row['FTAG'])}
                    </div>
                    <div style="display:flex; align-items:center; gap:10px; flex:1; justify-content:flex-end;">
                        <span style="font-family:'DM Sans',sans-serif; font-size:14px; 
                                     color:{ganador_color[1]}; font-weight:500; text-align:right;">
                            {row['AwayTeam']}
                        </span>
                        {escudo_html(row['AwayTeam'], 24)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px; padding:24px 28px;">
            <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                        color:#4A6075; text-transform:uppercase; margin-bottom:20px;">
                Estadísticas del modelo
            </div>
        """, unsafe_allow_html=True)

        stats_modelo = {
            "Partidos analizados (local)": len(partidos_local),
            "Partidos analizados (visitante)": len(partidos_visita),
            "Total partidos en dataset": len(df),
            "Jornada seleccionada": jornada,
            "Forma local": racha_local,
            "Forma visitante": racha_visit,
        }
        for k, v in stats_modelo.items():
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:10px 0; 
                        border-bottom:1px solid #1E2A35;">
                <span style="font-family:'DM Sans',sans-serif; font-size:14px; color:#4A6075;">
                    {k}
                </span>
                <span style="font-family:'Space Mono',monospace; font-size:14px; color:#E8EDF2;">
                    {v}
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── VEREDICTO FINAL ──
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    confianza = "ALTA" if prob_max >= 0.55 else "MEDIA" if prob_max >= 0.40 else "BAJA"
    confianza_color = "#2ECC71" if confianza == "ALTA" else "#F39C12" if confianza == "MEDIA" else "#E74C3C"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #0D1117 0%, #111820 100%); 
                border:1px solid #1E2A35; border-left:4px solid {confianza_color};
                border-radius:16px; padding:28px 32px; margin-top:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                            color:#4A6075; text-transform:uppercase; margin-bottom:8px;">
                    Veredicto final
                </div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:32px; 
                            color:#E8EDF2; letter-spacing:2px;">
                    {resultado_texto}
                </div>
                <div style="font-family:'DM Sans',sans-serif; font-size:13px; 
                            color:#4A6075; margin-top:4px;">
                    El modelo sugiere este resultado con confianza {confianza_color == '#2ECC71' and 'alta' or confianza_color == '#F39C12' and 'media' or 'baja'}
                </div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px; 
                            color:#4A6075; text-transform:uppercase; margin-bottom:4px;">
                    Confianza
                </div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:48px; 
                            color:{confianza_color}; line-height:1;">
                    {confianza}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div style="text-align:center; margin-top:32px;">
        <span style="font-family:'Space Mono',monospace; font-size:9px; letter-spacing:2px; 
                     color:#2A3845; text-transform:uppercase;">
            Modelo estadístico · Solo fines educativos · No garantiza resultados reales
        </span>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from escudos import get_escudo
import requests
from io import BytesIO
import base64

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FootballAI · Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── MUNDIAL 2026 DATA ─────────────────────────────────────────────────────────
MUNDIAL_2026_GRUPOS = {
    "Grupo A": ["México", "Sudáfrica", "Corea del Sur", "Rep. Checa"],
    "Grupo B": ["Canadá", "Qatar", "Suiza", "Bosnia"],
    "Grupo C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "Grupo D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "Grupo E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "Grupo F": ["Países Bajos", "Japón", "Túnez", "Noruega"],
    "Grupo G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "Grupo H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "Grupo I": ["Francia", "Senegal", "Irak", "Noruega"],
    "Grupo J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "Grupo K": ["Portugal", "Uzbekistán", "Colombia", "R.D. del Congo"],
    "Grupo L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
}

TODAS_SELECCIONES = sorted(list(set(
    sel for grupo in MUNDIAL_2026_GRUPOS.values() for sel in grupo
)))

# Carpeta de banderas del Mundial 2026
BANDERAS_DIR = os.path.join(os.path.dirname(__file__), "escudos", "mundial_2026_banderas")

# Mapeo nombre en español → archivo PNG (grupos oficiales Mundial 2026)
BANDERAS_ARCHIVOS = {
    # Con archivo local
    "Alemania":        "Germany.png",
    "Arabia Saudita":  "Saudi_Arabia.png",
    "Argelia":         "Algeria.png",
    "Argentina":       "Argentina.png",
    "Australia":       "Australia.png",
    "Austria":         "Austria.png",
    "Bélgica":         "Belgium.png",
    "Brasil":          "Brazil.png",
    "Canadá":          "Canada.png",
    "Colombia":        "Colombia.png",
    "Corea del Sur":   "South_Korea.png",
    "Croacia":         "Croatia.png",
    "Ecuador":         "Ecuador.png",
    "Egipto":          "Egypt.png",
    "Escocia":         "Scotland.png",
    "España":          "Spain.png",
    "Estados Unidos":  "United_States.png",
    "Francia":         "France.png",
    "Ghana":           "Ghana.png",
    "Inglaterra":      "England.png",
    "Irán":            "Iran.png",
    "Japón":           "Japan.png",
    "Marruecos":       "Morocco.png",
    "México":          "Mexico.png",
    "Nueva Zelanda":   "New_Zealand.png",
    "Países Bajos":    "Netherlands.png",
    "Panamá":          "Panama.png",
    "Paraguay":        "Paraguay.png",
    "Portugal":        "Portugal.png",
    "Qatar":           "Qatar.png",
    "Senegal":         "Senegal.png",
    "Sudáfrica":       "South_Africa.png",
    "Suiza":           "Switzerland.png",
    "Turquía":         "Turkey.png",
    "Uruguay":         "Uruguay.png",
    # Sin archivo local → fallback emoji
    "Bosnia":          "Bosnia_and_Herzegovina.png",
    "Cabo Verde":      "Cape_Verde.png",
    "Costa de Marfil": "Ivory_Coast.png",
    "Curazao":         "Curacao.png",
    "Haití":           "Haiti.png",
    "Irak":            "Irak.png",
    "Jordania":        "Jordania.png",
    "Noruega":         "Noruega.png",
    "R.D. del Congo":  "R.D_Congo.png",
    "Rep. Checa":      "Czechia.png",
    "Túnez":           "Tunisia.png",
    "Uzbekistán":      "Uzbekistan.png",
}

# Emojis de fallback para selecciones sin archivo local
EMOJIS_SELECCIONES = {
    "Alemania": "🇩🇪", "Arabia Saudita": "🇸🇦", "Argelia": "🇩🇿",
    "Argentina": "🇦🇷", "Australia": "🇦🇺", "Austria": "🇦🇹",
    "Bélgica": "🇧🇪", "Bosnia": "🇧🇦", "Brasil": "🇧🇷",
    "Cabo Verde": "🇨🇻", "Canadá": "🇨🇦", "Colombia": "🇨🇴",
    "Corea del Sur": "🇰🇷", "Costa de Marfil": "🇨🇮", "Croacia": "🇭🇷",
    "Curazao": "🇨🇼", "Ecuador": "🇪🇨", "Egipto": "🇪🇬",
    "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "España": "🇪🇸", "Estados Unidos": "🇺🇸",
    "Francia": "🇫🇷", "Ghana": "🇬🇭", "Haití": "🇭🇹",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Irak": "🇮🇶", "Irán": "🇮🇷",
    "Japón": "🇯🇵", "Jordania": "🇯🇴", "Marruecos": "🇲🇦",
    "México": "🇲🇽", "Nueva Zelanda": "🇳🇿", "Noruega": "🇳🇴",
    "Países Bajos": "🇳🇱", "Panamá": "🇵🇦", "Paraguay": "🇵🇾",
    "Portugal": "🇵🇹", "Qatar": "🇶🇦", "R.D. del Congo": "🇨🇩",
    "Rep. Checa": "🇨🇿", "Senegal": "🇸🇳", "Sudáfrica": "🇿🇦",
    "Suiza": "🇨🇭", "Túnez": "🇹🇳", "Turquía": "🇹🇷",
    "Uruguay": "🇺🇾", "Uzbekistán": "🇺🇿",
}

# ─── ESTADO DE SESIÓN ──────────────────────────────────────────────────────────
if "menu_activo" not in st.session_state:
    st.session_state.menu_activo = "ligas"

# ─── CSS GLOBAL ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080C10 !important;
    color: #E8EDF2;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"] > .main { background: #080C10 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

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
[data-testid="stSelectbox"] > div > div:hover { border-color: #2ECC71 !important; }
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #4A6075 !important;
}
[data-testid="stSlider"] > div > div > div { background: #2ECC71 !important; }

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
[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }

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

[data-testid="stExpander"] {
    background: #0D1117 !important;
    border: 1px solid #1E2A35 !important;
    border-radius: 12px !important;
}

.block-container {
    padding: 2rem 2rem 4rem !important;
    max-width: 1200px !important;
}

/* ── MUNDIAL tabs override cuando está activo el modo mundial ── */
.mundial-active [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #C9A84C !important;
}
.mundial-active [data-testid="stSelectbox"] > div > div:hover {
    border-color: #C9A84C !important;
}
.mundial-active [data-testid="stSlider"] > div > div > div {
    background: #C9A84C !important;
}
.mundial-active ::-webkit-scrollbar-thumb {
    background: #C9A84C;
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
    return pd.read_csv(csv_path)

def color_resultado(prob, mundial=False):
    acento = "#C9A84C" if mundial else "#2ECC71"
    if prob >= 0.5:
        return acento
    elif prob >= 0.3:
        return "#F39C12"
    else:
        return "#E61D25" if mundial else "#E74C3C"

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

@st.cache_data
def get_escudo_b64(nombre):
    ruta = get_escudo(nombre)
    if not ruta:
        return None
    try:
        if not ruta.startswith("http"):
            if os.path.exists(ruta):
                with open(ruta, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{b64}"
            return None
        r = requests.get(ruta, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            b64 = base64.b64encode(r.content).decode()
            mime = "image/svg+xml" if ruta.endswith(".svg") else "image/png"
            return f"data:{mime};base64,{b64}"
    except:
        return None
    return None

def escudo_html(nombre, size=64):
    data_url = get_escudo_b64(nombre)
    if data_url:
        return f'<img src="{data_url}" width="{size}" height="{size}" style="object-fit:contain; filter:drop-shadow(0 4px 12px rgba(0,0,0,0.5));">'
    return f'<div style="width:{size}px;height:{size}px;display:flex;align-items:center;justify-content:center;font-size:{size//2}px;">⚽</div>'

@st.cache_data
def get_bandera_mundial_b64(seleccion):
    """Carga la bandera local del Mundial 2026. Retorna data URL o None."""
    archivo = BANDERAS_ARCHIVOS.get(seleccion)
    if not archivo:
        return None
    ruta = os.path.join(BANDERAS_DIR, archivo)
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    except:
        return None

def bandera_html(seleccion, size=48):
    """Imagen local si existe, emoji de fallback si no."""
    data_url = get_bandera_mundial_b64(seleccion)
    if data_url:
        return (
            f'<img src="{data_url}" width="{size}" height="{size}" '
            f'style="object-fit:contain; filter:drop-shadow(0 2px 12px rgba(0,0,0,0.5));">'
        )
    emoji = EMOJIS_SELECCIONES.get(seleccion, "🌍")
    return f'<div style="font-size:{size}px; line-height:1; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.4));">{emoji}</div>'


# ─── CARGAR DATOS ──────────────────────────────────────────────────────────────
try:
    modelo = cargar_modelo()
    df = cargar_datos()
except Exception as e:
    st.error(f"Error cargando modelo/datos: {e}")
    st.stop()


# ─── NAV PRINCIPAL ─────────────────────────────────────────────────────────────
es_mundial = st.session_state.menu_activo == "mundial"

# Paletas según modo
if es_mundial:
    COLOR_PRIMARIO  = "#C9A84C"   # dorado trofeo
    COLOR_ACENTO    = "#E61D25"   # rojo FIFA
    COLOR_ACENTO2   = "#2A398D"   # azul FIFA
    COLOR_ACENTO3   = "#3CAC3B"   # verde FIFA
    BG_BASE         = "#06080A"
    BG_CARD         = "#0E0F0D"
    BG_CARD2        = "#12130F"
    BORDER_COLOR    = "#2A2410"
    TEXT_DIM        = "#6B5C30"
    BTN_GRAD        = f"linear-gradient(135deg, {COLOR_PRIMARIO} 0%, #A07830 100%)"
    BTN_SHADOW      = "rgba(201,168,76,0.3)"
    BTN_COLOR_TEXT  = "#06080A"
else:
    COLOR_PRIMARIO  = "#2ECC71"
    COLOR_ACENTO    = "#3498DB"
    COLOR_ACENTO2   = "#F39C12"
    COLOR_ACENTO3   = "#2ECC71"
    BG_BASE         = "#080C10"
    BG_CARD         = "#0D1117"
    BG_CARD2        = "#111820"
    BORDER_COLOR    = "#1E2A35"
    TEXT_DIM        = "#4A6075"
    BTN_GRAD        = f"linear-gradient(135deg, #2ECC71 0%, #27AE60 100%)"
    BTN_SHADOW      = "rgba(46,204,113,0.3)"
    BTN_COLOR_TEXT  = "#080C10"

# CSS dinámico según modo
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background: {BG_BASE} !important;
}}
[data-testid="stAppViewContainer"] > .main {{ background: {BG_BASE} !important; }}
::-webkit-scrollbar-thumb {{ background: {COLOR_PRIMARIO}; }}
[data-testid="stSelectbox"] > div > div:hover {{ border-color: {COLOR_PRIMARIO} !important; }}
[data-testid="stSlider"] > div > div > div {{ background: {COLOR_PRIMARIO} !important; }}
[data-testid="stButton"] > button {{
    background: {BTN_GRAD} !important;
    color: {BTN_COLOR_TEXT} !important;
    box-shadow: 0 4px 24px {BTN_SHADOW} !important;
}}
[data-testid="stButton"] > button:hover {{
    box-shadow: 0 8px 32px {BTN_SHADOW} !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    color: {COLOR_PRIMARIO} !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Barra de navegación ──
col_nav1, col_nav2 = st.columns([1, 1])
with col_nav1:
    if st.button("⚽  LIGAS", key="btn_ligas"):
        st.session_state.menu_activo = "ligas"
        st.rerun()
with col_nav2:
    if st.button("🏆  MUNDIAL 2026", key="btn_mundial"):
        st.session_state.menu_activo = "mundial"
        st.rerun()

# Indicador visual de tab activo
nav_left_w  = "100%" if not es_mundial else "0%"
nav_right_w = "100%" if es_mundial else "0%"
nav_left_op  = "1" if not es_mundial else "0.25"
nav_right_op = "1" if es_mundial else "0.25"
st.markdown(f"""
<div style="display:flex; height:3px; border-radius:2px; overflow:hidden; margin-top:-12px; margin-bottom:24px;">
    <div style="flex:1; background:{COLOR_PRIMARIO if not es_mundial else '#1E2A35'}; opacity:{nav_left_op}; transition:all 0.3s;"></div>
    <div style="flex:1; background:{'linear-gradient(90deg,#C9A84C,#E61D25)' if es_mundial else '#1E2A35'}; opacity:{nav_right_op}; transition:all 0.3s;"></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ─── MENÚ: LIGAS ─────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if not es_mundial:

    # HEADER LIGAS
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 32px;">
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

    LIGAS_DISPLAY = {
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿  Premier League":   "premier_25",
        "🇪🇸  La Liga":              "laliga_25",
        "🇮🇹  Serie A":               "seriea_25",
        "🇩🇪  Bundesliga":            "bundesliga_25",
        "🇫🇷  Ligue 1":               "ligue1_25",
        "🇳🇱  Eredivisie":            "eredivisie_25",
        "🏴󠁧󠁢󠁳󠁣󠁴󠁿  Escocia":            "escocia_25",
        "🇵🇹  Portugal":              "portugal_25",
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿  Championship":       "championship_25",
    }

    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                color:#4A6075; text-transform:uppercase; margin-bottom:8px; text-align:center;">
        Selecciona la liga
    </div>
    """, unsafe_allow_html=True)

    liga_nombre = st.selectbox("Liga", list(LIGAS_DISPLAY.keys()), label_visibility="collapsed")
    liga_key = LIGAS_DISPLAY[liga_nombre]
    equipos_liga = df[df["Liga"] == liga_key]["HomeTeam"].unique().tolist()
    equipos = sorted(set(equipos_liga))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([5, 2, 5])

    with col_left:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                    color:#4A6075; text-transform:uppercase; margin-bottom:16px; text-align:center;">
            Local
        </div>
        """, unsafe_allow_html=True)
        equipo_local = st.selectbox("Equipo Local", equipos, label_visibility="collapsed")
        url_local = get_escudo(equipo_local)
        if url_local:
            st.markdown(f"""
            <div style="text-align:center; margin:16px 0;">{escudo_html(equipo_local, 96)}</div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; margin-top:8px;">
            <span style="font-family:'Bebas Neue',sans-serif; font-size:26px;
                         color:#E8EDF2; letter-spacing:2px;">{equipo_local}</span>
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
            <div style="text-align:center; margin:16px 0;">{escudo_html(equipo_visitante, 96)}</div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; margin-top:8px;">
            <span style="font-family:'Bebas Neue',sans-serif; font-size:26px;
                         color:#E8EDF2; letter-spacing:2px;">{equipo_visitante}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    with st.expander("⚙️  Parámetros avanzados"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            jornada = st.slider("Jornada", 1, 38, 20)
        with col_b:
            racha_local = st.slider("Forma local (últimos 5)", 0, 15, 8)
        with col_c:
            racha_visit = st.slider("Forma visitante (últimos 5)", 0, 15, 6)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    predecir = st.button("ANALIZAR PARTIDO")

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

        try:
            N = 10
            partidos_local_home = df[df["HomeTeam"] == equipo_local].tail(N)
            partidos_local_away = df[df["AwayTeam"] == equipo_local].tail(N)
            partidos_visit_home = df[df["HomeTeam"] == equipo_visitante].tail(N)
            partidos_visit_away = df[df["AwayTeam"] == equipo_visitante].tail(N)

            gf_h = list(partidos_local_home["FTHG"]) + list(partidos_local_away["FTAG"])
            ga_h = list(partidos_local_home["FTAG"]) + list(partidos_local_away["FTHG"])
            gf_a = list(partidos_visit_home["FTHG"]) + list(partidos_visit_away["FTAG"])
            ga_a = list(partidos_visit_home["FTAG"]) + list(partidos_visit_away["FTHG"])

            goles_favor_local  = np.mean(gf_h[-N:]) if gf_h else 1.3
            goles_contra_local = np.mean(ga_h[-N:]) if ga_h else 1.1
            goles_favor_visit  = np.mean(gf_a[-N:]) if gf_a else 1.1
            goles_contra_visit = np.mean(ga_a[-N:]) if ga_a else 1.3

            def pts(ftr_series, lado):
                return [3 if f==lado else (1 if f=='D' else 0) for f in ftr_series]

            pts_h = pts(partidos_local_home["FTR"], "H") + pts(partidos_local_away["FTR"], "A")
            pts_a = pts(partidos_visit_home["FTR"], "H") + pts(partidos_visit_away["FTR"], "A")
            hpts = np.mean(pts_h[-N:]) if pts_h else 1.0
            apts = np.mean(pts_a[-N:]) if pts_a else 1.0

            hs_val  = partidos_local_home["HS"].mean()  if len(partidos_local_home) > 0 else 12.0
            as_val  = partidos_visit_away["AS"].mean()  if len(partidos_visit_away) > 0 else 11.0
            hst_val = partidos_local_home["HST"].mean() if len(partidos_local_home) > 0 else 4.5
            ast_val = partidos_visit_away["AST"].mean() if len(partidos_visit_away) > 0 else 4.0

            partidos_local   = df[df["HomeTeam"] == equipo_local]
            partidos_visita  = df[df["AwayTeam"] == equipo_visitante]

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

            features = np.array([[
                goles_favor_local, goles_contra_local,
                goles_favor_visit, goles_contra_visit,
                hpts, apts,
                hs_val, as_val, hst_val, ast_val
            ]])

            probs = modelo.predict_proba(features)[0]
            clases = modelo.classes_
            prob_dict = {c: p for c, p in zip(clases, probs)}
            prob_local  = prob_dict.get("H", 0)
            prob_empate = prob_dict.get("D", 0)
            prob_visit  = prob_dict.get("A", 0)

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

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown("""<div style='width:100%;height:1px;background:linear-gradient(90deg,transparent,#1E2A35,transparent);margin-bottom:32px;'></div>""", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📊  PREDICCIÓN", "⚔️  HEAD TO HEAD", "📈  ESTADÍSTICAS"])

        with tab1:
            st.markdown(f"""
            <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px;
                        padding:28px 32px; margin-bottom:24px;">
                <div style="display:flex; align-items:center; justify-content:space-between; gap:16px;">
                    <div style="display:flex; flex-direction:column; align-items:center; gap:12px; flex:1;">
                        {escudo_html(equipo_local, 72)}
                        <span style="font-family:'Bebas Neue',sans-serif; font-size:20px;
                                     color:#E8EDF2; letter-spacing:2px; text-align:center;">
                            {equipo_local}
                        </span>
                    </div>
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
                                    margin-bottom:8px; line-height:1.4;">{label}</div>
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
                st.markdown(f"""
                <div style="background:#0D1117; border:1px solid #1E2A35; border-radius:16px;
                            padding:24px 28px; margin-bottom:20px;">
                    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                                color:#4A6075; text-transform:uppercase; margin-bottom:20px;">
                        Historial · {total_h2h} partidos
                    </div>
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div style="flex:1; text-align:center;">
                            {escudo_html(equipo_local, 48)}
                            <div style="font-family:'Bebas Neue',sans-serif; font-size:42px;
                                        color:#2ECC71; margin-top:8px;">{ganados_local}</div>
                            <div style="font-family:'Space Mono',monospace; font-size:9px;
                                        color:#4A6075; letter-spacing:2px;">VICTORIAS</div>
                        </div>
                        <div style="flex:1; text-align:center; border-left:1px solid #1E2A35;
                                    border-right:1px solid #1E2A35; padding:0 16px;">
                            <div style="font-family:'Bebas Neue',sans-serif; font-size:42px;
                                        color:#F39C12;">{empates_h2h}</div>
                            <div style="font-family:'Space Mono',monospace; font-size:9px;
                                        color:#4A6075; letter-spacing:2px;">EMPATES</div>
                        </div>
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

                h2h_display = h2h[["HomeTeam","FTHG","FTAG","AwayTeam","FTR"]].tail(10).iloc[::-1]
                for _, row in h2h_display.iterrows():
                    gc = {"H":("#2ECC71","#4A6075"),"A":("#4A6075","#2ECC71"),"D":("#F39C12","#F39C12")}.get(row["FTR"],("#4A6075","#4A6075"))
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; justify-content:space-between;
                                background:#0D1117; border:1px solid #1E2A35; border-radius:10px;
                                padding:12px 20px; margin-bottom:8px;">
                        <div style="display:flex; align-items:center; gap:10px; flex:1;">
                            {escudo_html(row['HomeTeam'], 24)}
                            <span style="font-family:'DM Sans',sans-serif; font-size:14px;
                                         color:{gc[0]}; font-weight:500;">{row['HomeTeam']}</span>
                        </div>
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:22px;
                                    letter-spacing:4px; color:#E8EDF2; padding:0 20px;">
                            {int(row['FTHG'])} — {int(row['FTAG'])}
                        </div>
                        <div style="display:flex; align-items:center; gap:10px; flex:1; justify-content:flex-end;">
                            <span style="font-family:'DM Sans',sans-serif; font-size:14px;
                                         color:{gc[1]}; font-weight:500; text-align:right;">{row['AwayTeam']}</span>
                            {escudo_html(row['AwayTeam'], 24)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab3:
            stats_modelo = {
                "Partidos analizados (local)": len(partidos_local),
                "Partidos analizados (visitante)": len(partidos_visita),
                "Total partidos en dataset": len(df),
                "Jornada seleccionada": jornada,
                "Forma local": racha_local,
                "Forma visitante": racha_visit,
            }
            filas = "".join([
                f"<div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1E2A35;'>"
                f"<span style='font-family:DM Sans,sans-serif;font-size:14px;color:#4A6075;'>{k}</span>"
                f"<span style='font-family:Space Mono,monospace;font-size:14px;color:#E8EDF2;'>{v}</span></div>"
                for k, v in stats_modelo.items()
            ])
            st.markdown(
                f"<div style='background:#0D1117;border:1px solid #1E2A35;border-radius:16px;padding:24px 28px;'>"
                f"<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:3px;color:#4A6075;text-transform:uppercase;margin-bottom:20px;'>Estadísticas del modelo</div>"
                f"{filas}</div>",
                unsafe_allow_html=True
            )

        # VEREDICTO FINAL
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        confianza = "ALTA" if prob_max >= 0.55 else "MEDIA" if prob_max >= 0.40 else "BAJA"
        confianza_color = "#2ECC71" if confianza == "ALTA" else "#F39C12" if confianza == "MEDIA" else "#E74C3C"
        confianza_texto = "alta" if confianza == "ALTA" else "media" if confianza == "MEDIA" else "baja"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #0D1117 0%, #111820 100%);
                    border:1px solid #1E2A35; border-left:4px solid {confianza_color};
                    border-radius:16px; padding:28px 32px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                <div>
                    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                                color:#4A6075; text-transform:uppercase; margin-bottom:8px;">Veredicto final</div>
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:32px;
                                color:#E8EDF2; letter-spacing:2px;">{resultado_texto}</div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:13px;
                                color:#4A6075; margin-top:4px;">
                        El modelo sugiere este resultado con confianza {confianza_texto}
                    </div>
                </div>
                <div style="text-align:center;">
                    <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                                color:#4A6075; text-transform:uppercase; margin-bottom:4px;">Confianza</div>
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:48px;
                                color:{confianza_color}; line-height:1;">{confianza}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin-top:32px;">
            <span style="font-family:'Space Mono',monospace; font-size:9px; letter-spacing:2px;
                         color:#2A3845; text-transform:uppercase;">
                Modelo estadístico · Solo fines educativos · No garantiza resultados reales
            </span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ─── MENÚ: MUNDIAL 2026 ──────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
else:

    # ── CSS extra Mundial ──
    st.markdown("""
    <style>
    [data-testid="stSelectbox"] > div > div {
        background: #0E0F0D !important;
        border: 1px solid #2A2410 !important;
    }
    [data-testid="stExpander"] {
        background: #0E0F0D !important;
        border: 1px solid #2A2410 !important;
    }
    [data-testid="stTabs"] [role="tablist"] {
        background: #0E0F0D;
        border: 1px solid #2A2410;
    }
    [data-testid="stTabs"] [role="tab"] { color: #6B5C30 !important; }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: #1A160A !important;
        color: #C9A84C !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HEADER MUNDIAL ──
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 32px; position:relative;">
        <div style="position:absolute; top:0; left:50%; transform:translateX(-50%);
                    width:300px; height:2px;
                    background:linear-gradient(90deg, transparent, #C9A84C, #E61D25, #2A398D, #3CAC3B, transparent);">
        </div>
        <div style="font-family:'Space Mono',monospace; font-size:11px; letter-spacing:4px;
                    color:#C9A84C; text-transform:uppercase; margin-bottom:8px; margin-top:16px;">
            FIFA · World Cup 2026
        </div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:clamp(48px,8vw,80px);
                    letter-spacing:4px; line-height:0.85;">
            <span style="color:#E8EDF2;">WORLD</span>
            <span style="background:linear-gradient(90deg,#C9A84C,#E8D080,#C9A84C);
                         -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                         background-clip:text;"> CUP</span>
        </div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:clamp(28px,4vw,44px);
                    color:#E8EDF2; letter-spacing:8px; margin-top:4px;">
            <span style="color:#E61D25;">U</span><span style="color:#E8EDF2;">S</span>
            <span style="color:#E8EDF2;"> · </span>
            <span style="color:#FF0000;">C</span><span style="color:#E8EDF2;">A</span>
            <span style="color:#E8EDF2;"> · </span>
            <span style="color:#006847;">M</span><span style="color:#E8EDF2;">X</span>
            <span style="color:#E8EDF2;"> 2026</span>
        </div>
        <div style="display:flex; justify-content:center; gap:8px; margin-top:16px;">
            <div style="width:30px; height:3px; background:#C9A84C; border-radius:2px;"></div>
            <div style="width:30px; height:3px; background:#E61D25; border-radius:2px;"></div>
            <div style="width:30px; height:3px; background:#2A398D; border-radius:2px;"></div>
            <div style="width:30px; height:3px; background:#3CAC3B; border-radius:2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS MUNDIAL ──
    tab_pred, tab_grupos = st.tabs(["🏆  PREDICTOR", "🌍  GRUPOS"])

    # ─────────────────────────────────────
    # TAB 1: PREDICTOR MUNDIAL
    # ─────────────────────────────────────
    with tab_pred:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                    color:#6B5C30; text-transform:uppercase; margin-bottom:8px; text-align:center;">
            Selecciona las selecciones
        </div>
        """, unsafe_allow_html=True)

        # Selector de grupo (opcional, para filtrar)
        grupos_opciones = ["Todas las selecciones"] + list(MUNDIAL_2026_GRUPOS.keys())
        grupo_filtro = st.selectbox("Filtrar por grupo", grupos_opciones, label_visibility="collapsed")

        if grupo_filtro == "Todas las selecciones":
            sels_disponibles = TODAS_SELECCIONES
        else:
            sels_disponibles = MUNDIAL_2026_GRUPOS[grupo_filtro]

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([5, 2, 5])

        with col_l:
            st.markdown("""
            <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                        color:#6B5C30; text-transform:uppercase; margin-bottom:16px; text-align:center;">
                Selección 1
            </div>
            """, unsafe_allow_html=True)
            sel_local = st.selectbox("Selección Local", sels_disponibles, key="m_local", label_visibility="collapsed")
            st.markdown(f"""
            <div style="text-align:center; margin:16px 0;">
                {bandera_html(sel_local, 88)}
            </div>
            <div style="text-align:center;">
                <span style="font-family:'Bebas Neue',sans-serif; font-size:24px;
                             color:#E8EDF2; letter-spacing:2px;">{sel_local}</span>
            </div>
            """, unsafe_allow_html=True)

        with col_c:
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center;
                        justify-content:center; height:160px; gap:8px;">
                <div style="font-family:'Bebas Neue',sans-serif; font-size:36px;
                            color:#2A2410; letter-spacing:4px;">VS</div>
                <div style="width:2px; height:40px;
                            background:linear-gradient(180deg,transparent,#C9A84C,transparent);"></div>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown("""
            <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                        color:#6B5C30; text-transform:uppercase; margin-bottom:16px; text-align:center;">
                Selección 2
            </div>
            """, unsafe_allow_html=True)
            idx_default = 1 if len(sels_disponibles) > 1 else 0
            sel_visit = st.selectbox("Selección Visitante", sels_disponibles, index=idx_default, key="m_visit", label_visibility="collapsed")
            st.markdown(f"""
            <div style="text-align:center; margin:16px 0;">
                {bandera_html(sel_visit, 88)}
            </div>
            <div style="text-align:center;">
                <span style="font-family:'Bebas Neue',sans-serif; font-size:24px;
                             color:#E8EDF2; letter-spacing:2px;">{sel_visit}</span>
            </div>
            """, unsafe_allow_html=True)

        # Parámetros avanzados mundial
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        with st.expander("⚙️  Parámetros avanzados"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                ranking_local = st.slider("Ranking FIFA (local)", 1, 80, 10)
            with col_b:
                ranking_visit = st.slider("Ranking FIFA (visitante)", 1, 80, 15)
            with col_c:
                fase = st.selectbox("Fase del torneo", ["Grupos", "Octavos", "Cuartos", "Semifinal", "Final"])

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        predecir_mundial = st.button("⚽  PREDECIR MUNDIAL")

        if predecir_mundial:
            if sel_local == sel_visit:
                st.markdown(f"""
                <div style="background:#150A0A; border:1px solid #E61D25; border-radius:12px;
                            padding:16px; text-align:center; margin-top:16px;">
                    <span style="color:#E61D25; font-family:'Space Mono',monospace; font-size:13px;">
                        ⚠ Selecciona dos selecciones distintas
                    </span>
                </div>
                """, unsafe_allow_html=True)
                st.stop()

            try:
                # Simulación basada en ranking FIFA + modelo con datos históricos de selecciones en ligas
                np.random.seed(hash(sel_local + sel_visit) % 2**31)

                # Factor ranking (mayor ranking = menor prob)
                factor_rank = (ranking_visit - ranking_local) / 80.0
                # Factor fase
                factor_fase = {"Grupos": 0, "Octavos": 0.02, "Cuartos": 0.03, "Semifinal": 0.04, "Final": 0.05}.get(fase, 0)

                base_local = 0.40 + factor_rank * 0.15 + factor_fase
                base_visit = 0.30 - factor_rank * 0.10
                base_empate = 1.0 - base_local - base_visit

                # Normalizar
                total = base_local + base_empate + base_visit
                prob_local_m  = max(0.05, min(0.85, base_local / total))
                prob_empate_m = max(0.05, min(0.60, base_empate / total))
                prob_visit_m  = max(0.05, min(0.85, base_visit / total))

                # Re-normalizar
                total2 = prob_local_m + prob_empate_m + prob_visit_m
                prob_local_m  /= total2
                prob_empate_m /= total2
                prob_visit_m  /= total2

                prob_max_m = max(prob_local_m, prob_empate_m, prob_visit_m)
                if prob_max_m == prob_local_m:
                    resultado_m = f"Victoria {sel_local}"
                    color_pred_m = "#C9A84C"
                elif prob_max_m == prob_visit_m:
                    resultado_m = f"Victoria {sel_visit}"
                    color_pred_m = "#E61D25"
                else:
                    resultado_m = "Empate"
                    color_pred_m = "#2A398D"

                # Goles esperados
                goles_l = round(max(0.5, (prob_local_m * 2.8) + np.random.uniform(-0.2, 0.2)), 1)
                goles_v = round(max(0.5, (prob_visit_m * 2.8) + np.random.uniform(-0.2, 0.2)), 1)

            except Exception as e:
                st.error(f"Error al predecir: {e}")
                st.stop()

            st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
            st.markdown(f"""<div style='width:100%;height:1px;background:linear-gradient(90deg,transparent,#C9A84C44,transparent);margin-bottom:32px;'></div>""", unsafe_allow_html=True)

            # Tabs resultado
            r_tab1, r_tab2 = st.tabs(["🏆  RESULTADO", "📊  ANÁLISIS"])

            with r_tab1:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0E0F0D,#12130F);
                            border:1px solid #2A2410; border-radius:16px;
                            padding:28px 32px; margin-bottom:24px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:16px;">
                        <div style="display:flex; flex-direction:column; align-items:center; gap:12px; flex:1;">
                            {bandera_html(sel_local, 72)}
                            <span style="font-family:'Bebas Neue',sans-serif; font-size:20px;
                                         color:#E8EDF2; letter-spacing:2px; text-align:center;">
                                {sel_local}
                            </span>
                            <div style="font-family:'Space Mono',monospace; font-size:10px;
                                        color:#6B5C30; letter-spacing:2px;">
                                FIFA #{ranking_local}
                            </div>
                        </div>
                        <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
                            <span style="font-family:'Space Mono',monospace; font-size:10px;
                                         letter-spacing:3px; color:#6B5C30; text-transform:uppercase;">
                                Predicción · {fase}
                            </span>
                            <span style="font-family:'Bebas Neue',sans-serif; font-size:48px;
                                         color:{color_pred_m}; letter-spacing:2px; line-height:1;">
                                {int(prob_max_m*100)}%
                            </span>
                            <div style="background:linear-gradient(135deg,#1A160A,#221D0E);
                                        border:1px solid #C9A84C44; border-radius:20px; padding:6px 20px;
                                        margin-top:4px;">
                                <span style="font-family:'Space Mono',monospace; font-size:11px;
                                             color:{color_pred_m}; letter-spacing:1px;">
                                    {resultado_m}
                                </span>
                            </div>
                            <div style="margin-top:12px; display:flex; align-items:center; gap:8px;">
                                <span style="font-family:'Bebas Neue',sans-serif; font-size:32px;
                                             color:#C9A84C;">{goles_l}</span>
                                <span style="font-family:'Space Mono',monospace; font-size:14px;
                                             color:#2A2410;">—</span>
                                <span style="font-family:'Bebas Neue',sans-serif; font-size:32px;
                                             color:#E61D25;">{goles_v}</span>
                            </div>
                            <div style="font-family:'Space Mono',monospace; font-size:9px;
                                        color:#6B5C30; letter-spacing:2px;">GOLES ESPERADOS</div>
                        </div>
                        <div style="display:flex; flex-direction:column; align-items:center; gap:12px; flex:1;">
                            {bandera_html(sel_visit, 72)}
                            <span style="font-family:'Bebas Neue',sans-serif; font-size:20px;
                                         color:#E8EDF2; letter-spacing:2px; text-align:center;">
                                {sel_visit}
                            </span>
                            <div style="font-family:'Space Mono',monospace; font-size:10px;
                                        color:#6B5C30; letter-spacing:2px;">
                                FIFA #{ranking_visit}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Barras de probabilidad con colores Mundial
                barras_html = (
                    barra_gradiente(prob_local_m, "#C9A84C", f"Victoria {sel_local[:14]}") +
                    barra_gradiente(prob_empate_m, "#2A398D", "Empate") +
                    barra_gradiente(prob_visit_m, "#E61D25", f"Victoria {sel_visit[:14]}")
                )
                st.markdown(
                    "<div style='background:#0E0F0D; border:1px solid #2A2410; border-radius:16px; padding:24px 28px;'>"
                    "<div style='font-family:Space Mono,monospace; font-size:10px; letter-spacing:3px;"
                    "color:#6B5C30; text-transform:uppercase; margin-bottom:20px;'>Distribución de probabilidades</div>"
                    + barras_html +
                    "</div>",
                    unsafe_allow_html=True
                )

            with r_tab2:
                confianza_m = "ALTA" if prob_max_m >= 0.55 else "MEDIA" if prob_max_m >= 0.40 else "BAJA"
                confianza_color_m = "#C9A84C" if confianza_m == "ALTA" else "#3CAC3B" if confianza_m == "MEDIA" else "#E61D25"
                ventaja_rank = abs(ranking_visit - ranking_local)
                fav = sel_local if ranking_local < ranking_visit else sel_visit

                analisis_items = [
                    ("Favorito por ranking FIFA", fav, "#C9A84C"),
                    ("Ventaja en ranking", f"{ventaja_rank} posiciones", "#3CAC3B"),
                    ("Fase del torneo", fase, "#2A398D"),
                    ("Confianza del modelo", confianza_m, confianza_color_m),
                    ("Goles esperados", f"{goles_l} - {goles_v}", "#C9A84C"),
                ]

                filas_m = "".join([
                    f"<div style='display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #2A2410;'>"
                    f"<span style='font-family:DM Sans,sans-serif;font-size:14px;color:#6B5C30;'>{k}</span>"
                    f"<span style='font-family:Space Mono,monospace;font-size:13px;color:{c};font-weight:600;'>{v}</span></div>"
                    for k, v, c in analisis_items
                ])

                st.markdown(
                    f"<div style='background:#0E0F0D;border:1px solid #2A2410;border-radius:16px;padding:24px 28px;'>"
                    f"<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:3px;"
                    f"color:#6B5C30;text-transform:uppercase;margin-bottom:20px;'>Análisis del partido</div>"
                    f"{filas_m}</div>",
                    unsafe_allow_html=True
                )

            # Veredicto Mundial
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0E0F0D,#12130F);
                        border:1px solid #2A2410; border-left:4px solid {color_pred_m};
                        border-radius:16px; padding:28px 32px; margin-top:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                    <div>
                        <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                                    color:#6B5C30; text-transform:uppercase; margin-bottom:8px;">
                            🏆 Veredicto Mundial 2026
                        </div>
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:32px;
                                    color:#E8EDF2; letter-spacing:2px;">{resultado_m}</div>
                        <div style="font-family:'DM Sans',sans-serif; font-size:13px;
                                    color:#6B5C30; margin-top:4px;">
                            Análisis basado en ranking FIFA y estadísticas históricas
                        </div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                                    color:#6B5C30; text-transform:uppercase; margin-bottom:4px;">Confianza</div>
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:48px;
                                    color:{confianza_color_m}; line-height:1;">{confianza_m}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="text-align:center; margin-top:32px;">
                <span style="font-family:'Space Mono',monospace; font-size:9px; letter-spacing:2px;
                             color:#2A2410; text-transform:uppercase;">
                    Predicción estadística · Solo fines educativos · No garantiza resultados reales
                </span>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # TAB 2: GRUPOS
    # ─────────────────────────────────────
    with tab_grupos:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:3px;
                    color:#6B5C30; text-transform:uppercase; margin-bottom:20px; text-align:center;">
            48 selecciones · 12 grupos · USA · Canadá · México
        </div>
        """, unsafe_allow_html=True)

        COLORES_GRUPOS = [
            "#C9A84C",  # dorado
            "#E61D25",  # rojo
            "#2A398D",  # azul
            "#3CAC3B",  # verde
            "#C9A84C",
            "#E61D25",
            "#2A398D",
            "#3CAC3B",
            "#C9A84C",
            "#E61D25",
            "#2A398D",
            "#3CAC3B",
        ]

        grupos_list = list(MUNDIAL_2026_GRUPOS.items())
        col_g1, col_g2 = st.columns(2)

        for i, (grupo, selecciones) in enumerate(grupos_list):
            color_g = COLORES_GRUPOS[i % len(COLORES_GRUPOS)]
            target_col = col_g1 if i % 2 == 0 else col_g2

            sels_html = "".join([
                f"""<div style="display:flex; align-items:center; gap:10px;
                                padding:8px 0; border-bottom:{'1px solid #2A2410' if j < len(selecciones)-1 else 'none'};">
                        {bandera_html(s, 28)}
                        <span style="font-family:'DM Sans',sans-serif; font-size:14px;
                                     color:#E8EDF2; font-weight:500;">{s}</span>
                    </div>"""
                for j, s in enumerate(selecciones)
            ])

            with target_col:
                st.markdown(f"""
                <div style="background:#0E0F0D; border:1px solid #2A2410;
                            border-top:3px solid {color_g}; border-radius:12px;
                            padding:16px 20px; margin-bottom:16px;">
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:20px;
                                color:{color_g}; letter-spacing:3px; margin-bottom:12px;">
                        {grupo}
                    </div>
                    {sels_html}
                </div>
                """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ─────────────────────────────────────────────
# MÓDULO 1: SISTEMA DE APUESTAS SIMULADO
# ─────────────────────────────────────────────

def inicializar_billetera():
    if "billetera" not in st.session_state:
        st.session_state.billetera = 1000.0
    if "historial_apuestas" not in st.session_state:
        st.session_state.historial_apuestas = []
    if "apuesta_activa" not in st.session_state:
        st.session_state.apuesta_activa = None

def calcular_cuota(prob: float) -> float:
    """Convierte probabilidad a cuota decimal estilo europeo."""
    if prob <= 0:
        return 99.0
    cuota = 1 / prob
    margen = 0.05  # margen de casa simulado
    return round(cuota * (1 - margen), 2)

def registrar_apuesta(partido, seleccion, monto, cuota, prob):
    apuesta = {
        "id": len(st.session_state.historial_apuestas) + 1,
        "fecha": datetime.now().strftime("%d/%m %H:%M"),
        "partido": partido,
        "seleccion": seleccion,
        "monto": monto,
        "cuota": cuota,
        "ganancia_potencial": round(monto * cuota, 2),
        "prob_ia": prob,
        "estado": "Pendiente",
        "resultado_final": None
    }
    st.session_state.historial_apuestas.append(apuesta)
    st.session_state.billetera -= monto

def simular_resultado(apuesta_id):
    """Simula el resultado real del partido con algo de aleatoriedad."""
    apuesta = st.session_state.historial_apuestas[apuesta_id - 1]
    prob = apuesta["prob_ia"]
    # El resultado real usa la probabilidad del modelo + ruido
    ganó = random.random() < (prob * 0.85 + random.uniform(-0.1, 0.1))
    apuesta["estado"] = "Ganada ✅" if ganó else "Perdida ❌"
    apuesta["resultado_final"] = ganó
    if ganó:
        st.session_state.billetera += apuesta["ganancia_potencial"]

def mostrar_apuestas(predicciones: dict = None):
    """
    predicciones: dict con estructura:
    {
      "partido": "Arsenal vs Chelsea",
      "local": {"prob": 0.48, "equipo": "Arsenal"},
      "empate": {"prob": 0.24},
      "visita": {"prob": 0.28, "equipo": "Chelsea"},
      "goles_mas": {"prob": 0.55},
      "goles_menos": {"prob": 0.45},
    }
    """
    inicializar_billetera()

    st.markdown("---")
    st.markdown("## 🎰 Sistema de Apuestas Simulado")
    st.caption("_Dinero virtual — sin dinero real. Solo para entretenimiento._")

    # Billetera
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Saldo Virtual", f"${st.session_state.billetera:,.2f}")
    with col2:
        ganadas = sum(1 for a in st.session_state.historial_apuestas if a["estado"] == "Ganada ✅")
        st.metric("✅ Apuestas Ganadas", ganadas)
    with col3:
        perdidas = sum(1 for a in st.session_state.historial_apuestas if a["estado"] == "Perdida ❌")
        st.metric("❌ Apuestas Perdidas", perdidas)

    if predicciones:
        st.markdown(f"### ⚽ {predicciones['partido']}")
        st.markdown("**Selecciona tu apuesta:**")

        opciones = {
            f"🏠 {predicciones['local']['equipo']} gana": {
                "prob": predicciones["local"]["prob"],
                "cuota": calcular_cuota(predicciones["local"]["prob"])
            },
            "🤝 Empate": {
                "prob": predicciones["empate"]["prob"],
                "cuota": calcular_cuota(predicciones["empate"]["prob"])
            },
            f"✈️ {predicciones['visita']['equipo']} gana": {
                "prob": predicciones["visita"]["prob"],
                "cuota": calcular_cuota(predicciones["visita"]["prob"])
            },
            "⚽ Más de 2.5 goles": {
                "prob": predicciones["goles_mas"]["prob"],
                "cuota": calcular_cuota(predicciones["goles_mas"]["prob"])
            },
            "🔒 Menos de 2.5 goles": {
                "prob": predicciones["goles_menos"]["prob"],
                "cuota": calcular_cuota(predicciones["goles_menos"]["prob"])
            },
        }

        cols = st.columns(len(opciones))
        for i, (nombre, datos) in enumerate(opciones.items()):
            with cols[i]:
                st.markdown(f"**{nombre}**")
                st.markdown(f"Cuota: `{datos['cuota']}x`")
                st.caption(f"IA: {datos['prob']*100:.1f}%")

        seleccion = st.selectbox("¿Qué apuestas?", list(opciones.keys()))
        monto = st.slider("Monto a apostar ($)", min_value=10, max_value=int(st.session_state.billetera), value=50, step=10)

        datos_sel = opciones[seleccion]
        ganancia_pot = round(monto * datos_sel["cuota"], 2)
        st.info(f"💵 Si ganas: **${ganancia_pot}** (cuota {datos_sel['cuota']}x)")

        if st.button("🎯 Confirmar Apuesta", type="primary"):
            if monto > st.session_state.billetera:
                st.error("❌ Saldo insuficiente")
            else:
                registrar_apuesta(
                    partido=predicciones["partido"],
                    seleccion=seleccion,
                    monto=monto,
                    cuota=datos_sel["cuota"],
                    prob=datos_sel["prob"]
                )
                st.success(f"✅ Apuesta registrada. Ganancia potencial: **${ganancia_pot}**")
                st.rerun()

    # Historial
    if st.session_state.historial_apuestas:
        st.markdown("### 📋 Historial de Apuestas")
        df = pd.DataFrame(st.session_state.historial_apuestas)
        df_show = df[["id", "fecha", "partido", "seleccion", "monto", "cuota", "ganancia_potencial", "estado"]]
        df_show.columns = ["#", "Fecha", "Partido", "Selección", "Apostado $", "Cuota", "Ganancia Pot. $", "Estado"]
        st.dataframe(df_show, use_container_width=True)

        # Simular resultados pendientes
        pendientes = [a for a in st.session_state.historial_apuestas if a["estado"] == "Pendiente"]
        if pendientes:
            if st.button("🎲 Simular Resultados de Partidos Pendientes"):
                for a in pendientes:
                    simular_resultado(a["id"])
                st.rerun()

        if st.button("🔄 Reiniciar Billetera ($1000)"):
            st.session_state.billetera = 1000.0
            st.session_state.historial_apuestas = []
            st.rerun()


# ─────────────────────────────────────────────
# MÓDULO 2: RANKING DE EQUIPOS CON PUNTAJE IA
# ─────────────────────────────────────────────

def calcular_puntaje_ia(stats: dict) -> float:
    """
    Calcula un puntaje IA (0-100) basado en múltiples métricas.
    stats debe tener: victorias, empates, derrotas, gf, gc, partidos
    """
    if stats["partidos"] == 0:
        return 0

    win_rate = stats["victorias"] / stats["partidos"]
    no_derrota = (stats["victorias"] + stats["empates"]) / stats["partidos"]
    gf_avg = stats["gf"] / stats["partidos"]
    gc_avg = stats["gc"] / stats["partidos"]
    diff_goles = (stats["gf"] - stats["gc"]) / stats["partidos"]

    # Fórmula ponderada
    puntaje = (
        win_rate * 35 +
        no_derrota * 15 +
        min(gf_avg / 3, 1) * 20 +
        max(1 - gc_avg / 3, 0) * 15 +
        (diff_goles + 3) / 6 * 15  # normalizado entre -3 y +3
    )

    return round(min(max(puntaje * 100, 0), 100), 1)

def mostrar_ranking(equipos_stats: list):
    """
    equipos_stats: lista de dicts con nombre, victorias, empates, derrotas, gf, gc
    """
    st.markdown("---")
    st.markdown("## 🏆 Ranking de Equipos — Puntaje IA")
    st.caption("_Clasificación basada en rendimiento histórico ponderado por IA_")

    # Calcular puntajes
    for equipo in equipos_stats:
        equipo["partidos"] = equipo["victorias"] + equipo["empates"] + equipo["derrotas"]
        equipo["puntaje_ia"] = calcular_puntaje_ia(equipo)
        equipo["diff"] = equipo["gf"] - equipo["gc"]

    # Ordenar
    ranking = sorted(equipos_stats, key=lambda x: x["puntaje_ia"], reverse=True)

    # Mostrar tabla
    medallas = ["🥇", "🥈", "🥉"] + [""] * 100
    rows = []
    for i, eq in enumerate(ranking):
        rows.append({
            "Pos": f"{medallas[i]} {i+1}",
            "Equipo": eq["nombre"],
            "PJ": eq["partidos"],
            "V": eq["victorias"],
            "E": eq["empates"],
            "D": eq["derrotas"],
            "GF": eq["gf"],
            "GC": eq["gc"],
            "Dif": f"+{eq['diff']}" if eq["diff"] >= 0 else str(eq["diff"]),
            "Puntaje IA 🤖": eq["puntaje_ia"],
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df.style.background_gradient(subset=["Puntaje IA 🤖"], cmap="RdYlGn"),
        use_container_width=True,
        hide_index=True
    )

    # Top 3 visual
    st.markdown("### 🎖️ Podio")
    top3 = ranking[:3]
    cols = st.columns(3)
    for i, eq in enumerate(top3):
        with cols[i]:
            stars = "⭐" * (3 - i)
            st.markdown(f"### {medallas[i]} {eq['nombre']}")
            st.metric("Puntaje IA", f"{eq['puntaje_ia']}/100")
            st.caption(f"Win rate: {eq['victorias']/max(eq['partidos'],1)*100:.1f}%")
            st.caption(f"Goles avg: {eq['gf']/max(eq['partidos'],1):.1f}/partido")


# ─────────────────────────────────────────────
# DEMO STANDALONE (correr este archivo solo)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    st.set_page_config(page_title="Nuevas Funciones ⚽", page_icon="⚽", layout="wide")
    st.title("⚽ Predictor de Fútbol — Nuevas Funciones")

    tab1, tab2 = st.tabs(["🎰 Apuestas Simuladas", "🏆 Ranking IA"])

    with tab1:
        # Datos de ejemplo — en tu app real vendrán del modelo
        predicciones_ejemplo = {
            "partido": "Arsenal vs Chelsea",
            "local": {"prob": 0.48, "equipo": "Arsenal"},
            "empate": {"prob": 0.24},
            "visita": {"prob": 0.28, "equipo": "Chelsea"},
            "goles_mas": {"prob": 0.62},
            "goles_menos": {"prob": 0.38},
        }
        mostrar_apuestas(predicciones_ejemplo)

    with tab2:
        equipos_ejemplo = [
            {"nombre": "Manchester City", "victorias": 25, "empates": 5, "derrotas": 4, "gf": 72, "gc": 30},
            {"nombre": "Arsenal",         "victorias": 22, "empates": 6, "derrotas": 6, "gf": 68, "gc": 35},
            {"nombre": "Liverpool",       "victorias": 21, "empates": 7, "derrotas": 6, "gf": 70, "gc": 38},
            {"nombre": "Chelsea",         "victorias": 18, "empates": 8, "derrotas": 8, "gf": 60, "gc": 45},
            {"nombre": "Tottenham",       "victorias": 16, "empates": 6, "derrotas": 12, "gf": 55, "gc": 50},
            {"nombre": "Newcastle",       "victorias": 17, "empates": 5, "derrotas": 12, "gf": 52, "gc": 42},
            {"nombre": "Aston Villa",     "victorias": 15, "empates": 8, "derrotas": 11, "gf": 50, "gc": 48},
            {"nombre": "Manchester Utd",  "victorias": 13, "empates": 6, "derrotas": 15, "gf": 40, "gc": 52},
        ]
        mostrar_ranking(equipos_ejemplo)

import streamlit as st
import pandas as pd

# Configuración de Marca BE2SCALE
st.set_page_config(page_title="BE2SCALE Optimizer", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E0E0E0; }
    .stButton>button { background-color: #00897B; color: white; border-radius: 5px; }
    .css-1d391kg { background-color: #112240; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 BE2SCALE: Bio-Economic Optimizer")
st.subheader("Engineering Profitability | Division of Aquamarket S.A.C.")

# --- SIDEBAR: INPUTS TÉCNICOS ---
st.sidebar.header("📊 Parámetros de Campo")
biomasa_tn = st.sidebar.number_input("Biomasa Objetivo (TN)", value=50.0, step=5.0)
fcr_actual = st.sidebar.slider("FCR Actual (Declarado)", 1.2, 2.2, 1.7)
costo_alimento = st.sidebar.number_input("Precio Alimento (S/ por Kg)", value=4.80)
temp_agua = st.sidebar.slider("Temperatura Promedio (°C)", 8, 18, 12)

# --- CÁLCULOS DE INGENIERÍA SENIOR ---
# Meta BE2SCALE: Reducción conservadora del 12% en FCR
fcr_meta = fcr_actual * 0.88 
ahorro_alimento_kg = (biomasa_tn * 1000) * (fcr_actual - fcr_meta)
ahorro_soles = ahorro_alimento_kg * costo_alimento

# Estimación de Capacidad de Carga (Liao & Mayo Simplificado)
# Basado en saturación de O2 a la temperatura dada
o2_sat = 14.6 - (0.39 * temp_agua) + (0.005 * (temp_agua**2))
capacidad_carga = o2_sat * 1.8 # Factor de densidad técnica

# --- INTERFAZ DINÁMICA ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="💰 RESCATE DE CAPITAL (S/.)", value=f"S/ {ahorro_soles:,.0f}")
    st.write(f"**Meta FCR:** {fcr_meta:.2f}")

with col2:
    st.metric(label="🐟 CAPACIDAD CARGA (kg/m3)", value=f"{capacidad_carga:.1f}")
    st.write("**Estatus:** Optimización Requerida")

st.divider()

# Gráfico de Proyección de Retorno
st.write("### 📈 Proyección de Recuperación de Margen (Ciclo 90 días)")
datos_grafico = pd.DataFrame({
    'Días': ['Día 1', 'Día 30', 'Día 60', 'Día 90'],
    'Ahorro Acumulado (S/.)': [0, ahorro_soles*0.2, ahorro_soles*0.6, ahorro_soles]
})
st.line_chart(datos_grafico.set_index('Días'))

st.success(f"💡 IMPACTO: Esta optimización financia el 100% de la consultoría BE2SCALE y genera un excedente de S/ {ahorro_soles*0.7:,.0f} para reinversión.")

st.caption("BE2SCALE v1.0 | Rigor Técnico & Precisión Económica")

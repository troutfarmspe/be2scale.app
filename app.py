import streamlit as st
import pandas as pd

# 1. Configuración Profesional
st.set_page_config(page_title="BE2SCALE | Optimizer", layout="centered", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #FFFFFF; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #00897B; }
    .stNumberInput div div input { color: #00897B !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado Limpio (Sin error de icono)
st.title("📊 BE2SCALE")
st.markdown("### **Bio-Economic Optimizer v1.1**")
st.write("---")

# 3. Panel de Control (Ajustado a Números Redondos)
st.sidebar.header("⚙️ PARÁMETROS TÉCNICOS")

# Configurado como Entero (int) para evitar el ".0"
tm_objetivo = st.sidebar.number_input("Biomasa Objetivo (TM)", value=20, step=1, format="%d")
kg_equivalentes = tm_objetivo * 1000

st.sidebar.markdown(f"**Equivalente:** `{kg_equivalentes:,} Kg`")

fcr_actual = st.sidebar.slider("FCR Actual (Línea Base)", 1.2, 2.5, 1.7)
costo_alimento = st.sidebar.number_input("Costo Alimento (S/ por Kg)", value=4.85)

st.sidebar.info("AQUAMARKET S.A.C. | RUC: 20601363628")

# 4. Motor de Cálculo
fcr_objetivo = fcr_actual * 0.85
ahorro_total_kg = kg_equivalentes * (fcr_actual - fcr_objetivo)
utilidad_recuperada = ahorro_total_kg * costo_alimento

# 5. Visualización de Resultados
col1, col2 = st.columns(2)
with col1:
    st.metric(label="RESCATE DE CAPITAL (S/.)", value=f"S/ {utilidad_recuperada:,.0f}")
with col2:
    st.metric(label="OPTIMIZACIÓN FCR", value=f"-{((1 - (fcr_objetivo/fcr_actual))*100):.1f}%")

st.markdown(f"""
    > **DIAGNÓSTICO EJECUTIVO:**  
    > Para una producción de **{tm_objetivo} TM** ({kg_equivalentes:,} Kg), su operación presenta un lucro cesante técnico de **S/ {utilidad_recuperada:,.2f}** por ciclo. 
    > La implementación de **Aqua-Scale** estabilizará su FCR en **{fcr_objetivo:.2f}**.
""")

# 6. Gráfico de ROI
st.write("### 📈 Curva de Recuperación de Utilidades (90 días)")
chart_data = pd.DataFrame({
    'Fase': ['Inicio', 'Audit', 'Control', 'Scale'],
    'Soles Recatados': [0, utilidad_recuperada*0.15, utilidad_recuperada*0.50, utilidad_recuperada]
})
st.line_chart(chart_data.set_index('Fase'))

st.write("---")
st.caption("© 2024 BE2SCALE - División de Ingeniería de Aquamarket S.A.C. | RUC: 20601363628")

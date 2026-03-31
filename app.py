import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import math

# 1. Configuración de Marca y Estilo Pro
st.set_page_config(page_title="BE2SCALE | Optimizer", layout="centered", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #FFFFFF; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #00897B; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #112240; border-radius: 4px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00897B; }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado Institucional
st.title("📊 BE2SCALE")
st.markdown("### **Bio-Economic Optimizer v1.6**")
st.write("---")

# 3. Sidebar: Parámetros Compartidos (Lo que alimenta a toda la App)
st.sidebar.header("🏢 DATOS DE LA OPERACIÓN")
entidad_nombre = st.sidebar.text_input("Municipalidad/Empresa", value="Municipalidad de Ayavirí")
tm_objetivo = st.sidebar.number_input("Biomasa Objetivo (TM)", value=20, step=1, format="%d")
kg_equivalentes = tm_objetivo * 1000

st.sidebar.header("🏔️ VARIABLES DE CAMPO")
altitud = st.sidebar.number_input("Altitud (m.s.n.m.)", value=3500, step=100)
temp_agua = st.sidebar.slider("Temperatura del Agua (°C)", 5.0, 20.0, 12.0)
costo_alimento = st.sidebar.number_input("Costo Alimento (S/ por Kg)", value=4.85)

st.sidebar.info("AQUAMARKET S.A.C. | RUC: 20601363628")

# --- CREACIÓN DE PESTAÑAS ---
tab1, tab2 = st.tabs(["💰 Análisis Económico", "🧬 Ingeniería Bio-Térmica"])

with tab1:
    st.subheader(f"Simulación de Eficiencia: {entidad_nombre}")
    
    # Sliders de FCR
    fcr_actual = st.sidebar.slider("FCR Actual (Línea Base)", 1.2, 2.5, 1.70)
    fcr_objetivo = st.sidebar.slider("FCR Objetivo (Meta BE2SCALE)", 0.9, 2.0, 1.45)

    # Cálculos Financieros
    gasto_actual = kg_equivalentes * fcr_actual * costo_alimento
    gasto_meta = kg_equivalentes * fcr_objetivo * costo_alimento
    ahorro = gasto_actual - gasto_meta
    mejora_pct = ((fcr_actual - fcr_objetivo) / fcr_actual) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.error("PRESUPUESTO ACTUAL")
        st.subheader(f"S/ {gasto_actual:,.0f}")
    with col2:
        st.success("PRESUPUESTO OPTIMIZADO")
        st.subheader(f"S/ {gasto_meta:,.0f}")

    st.metric(label="CAPITAL RESCATADO (AHORRO)", value=f"S/ {ahorro:,.0f}", delta=f"{mejora_pct:.1f}% Eficiencia")
    
    st.info(f"Diagnóstico: Al optimizar el FCR de {fcr_actual} a {fcr_objetivo}, rescatamos S/ {ahorro:,.2f} de presupuesto operativo.")

with tab2:
    st.subheader("Análisis de Saturación de Oxígeno (O2)")
    
    # Lógica Termodinámica (Física de Altitud)
    # 1. Presión Atmosférica (Ley de Henry ajustada)
    p_atm = 760 * math.exp(-altitud / 8000)
    # 2. Solubilidad teórica O2 (Benson & Krause)
    o2_base = 14.603 - 0.4025 * temp_agua + 0.0077 * (temp_agua**2)
    # 3. Oxígeno Real Disponible (mg/L)
    o2_real = o2_base * (p_atm / 760)

    # Semáforo Visual
    if o2_real < 5.5:
        st.error(f"🔴 ESTADO CRÍTICO: {o2_real:.2f} mg/L")
        nota = "Peligro de Hipoxia. El pez no metaboliza el alimento. FCR incontrolable."
    elif 5.5 <= o2_real < 7.0:
        st.warning(f"🟡 ESTADO DE ALERTA: {o2_real:.2f} mg/L")
        nota = "Crecimiento Lento. El metabolismo está estresado por la altitud/temperatura."
    else:
        st.success(f"🟢 ESTADO ÓPTIMO: {o2_real:.2f} mg/L")
        nota = "Condiciones ideales para conversión alimenticia eficiente."

    st.markdown(f"> **Veredicto Técnico:** {nota}")
    
    # Velocímetro Visual (Barra de progreso)
    st.progress(min(o2_real/12.0, 1.0))
    st.caption(f"Disponibilidad de O2 calculada para {altitud} msnm")

# --- LÓGICA DEL PDF (Se mantiene al final) ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BE2SCALE - REPORTE DE INGENIERÍA", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Entidad: {entidad_nombre.upper()} | Fecha: {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Ahorro Proyectado: S/ {ahorro:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Oxígeno Disponible calculado: {o2_real:.2f} mg/L", ln=True)
    pdf.ln(20)
    pdf.cell(200, 10, txt="Ing. William Bernuy Espinoza - Aquamarket S.A.C.", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.write("---")
if st.sidebar.button("Generar Reporte PDF"):
    pdf_data = create_pdf()
    st.sidebar.download_button("📩 Descargar PDF", data=pdf_data, file_name="Reporte_BE2SCALE.pdf")

st.caption("© 2024 BE2SCALE | Ingeniería de Precisión para el Perú.")

import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# 1. Configuración de Marca
st.set_page_config(page_title="BE2SCALE | Optimizer", layout="centered", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #FFFFFF; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #00897B; }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado
st.title("📊 BE2SCALE")
st.markdown("### **Bio-Economic Optimizer v1.4**")
st.write("---")

# 3. Panel de Control
st.sidebar.header("🏢 DATOS DE LA OPERACIÓN")
entidad_nombre = st.sidebar.text_input("Nombre de la Municipalidad/Empresa", value="Municipalidad de Ayavirí")
tm_objetivo = st.sidebar.number_input("Biomasa Objetivo (TM)", value=20, step=1, format="%d")
kg_equivalentes = tm_objetivo * 1000

st.sidebar.header("⚙️ PARÁMETROS TÉCNICOS")
fcr_actual = st.sidebar.slider("FCR Actual (Línea Base)", 1.2, 2.5, 1.7)
costo_alimento = st.sidebar.number_input("Costo Alimento (S/ por Kg)", value=4.85)

# 4. Motor de Cálculo Financiero
# Escenario Actual (Sin BE2SCALE)
alimento_total_actual = kg_equivalentes * fcr_actual
gasto_total_actual = alimento_total_actual * costo_alimento

# Escenario Optimizado (Meta BE2SCALE - 15% mejora)
fcr_objetivo = fcr_actual * 0.85
alimento_total_meta = kg_equivalentes * fcr_objetivo
gasto_total_meta = alimento_total_meta * costo_alimento

# El Rescate
utilidad_recuperada = gasto_total_actual - gasto_total_meta
fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

# 5. Visualización de Resultados Estratégicos
st.subheader(f"Análisis Presupuestal: {entidad_nombre}")

# Fila 1: Los Totales (El "Golpe de Realidad")
col1, col2 = st.columns(2)
with col1:
    st.error(f"GASTO ACTUAL ESTIMADO")
    st.subheader(f"S/ {gasto_total_actual:,.0f}")
    st.caption(f"Basado en FCR {fcr_actual}")

with col2:
    st.success(f"GASTO OPTIMIZADO BE2SCALE")
    st.subheader(f"S/ {gasto_total_meta:,.0f}")
    st.caption(f"Meta FCR {fcr_objetivo:.2f}")

st.write("---")

# Fila 2: El Beneficio Neto
c1, c2 = st.columns(2)
with c1:
    st.metric(label="CAPITAL RESCATADO (AHORRO)", value=f"S/ {utilidad_recuperada:,.0f}", delta=f"-15% Gasto")
with c2:
    st.metric(label="ALIMENTO AHORRADO", value=f"{alimento_total_actual - alimento_total_meta:,.0f} Kg")

diagnostico_texto = f"Al optimizar el FCR de {fcr_actual} a {fcr_objetivo:.2f}, la {entidad_nombre} reduce su presupuesto operativo de S/ {gasto_total_actual:,.2f} a S/ {gasto_total_meta:,.2f}, liberando S/ {utilidad_recuperada:,.2f} de capital para reinversión."

st.info(diagnostico_texto)

# 6. Generación de PDF con desglose financiero
def create_pdf(nombre, tm, fcr_a, fcr_o, gasto_a, gasto_o, ahorro, fecha):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(200, 10, txt="BE2SCALE - ESTUDIO DE RENTABILIDAD", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Fecha: {fecha} | RUC: 20601363628", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"ENTIDAD: {nombre.upper()}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="RESUMEN FINANCIERO DEL PROYECTO:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, txt=f"1. Gasto Proyectado (Sin Optimización): S/ {gasto_a:,.2f}", ln=True)
    pdf.cell(200, 8, txt=f"2. Gasto Optimizado (Metodología BE2SCALE): S/ {gasto_o:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_fill_color(224, 255, 224)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 15, txt=f"TOTAL CAPITAL RESCATADO: S/ {ahorro:,.2f}", border=1, ln=True, align='C', fill=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, txt=f"CONCLUSIÓN: {diagnostico_texto}")
    
    pdf.ln(30)
    pdf.cell(200, 10, txt="Ing. William Bernuy Espinoza - Director Estratégico", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 7. Botón de Descarga
pdf_data = create_pdf(entidad_nombre, tm_objetivo, fcr_actual, fcr_objetivo, gasto_total_actual, gasto_total_meta, utilidad_recuperada, fecha_actual)
st.download_button(
    label=f"📩 DESCARGAR ANALISIS PRESUPUESTAL PDF",
    data=pdf_data,
    file_name=f"Analisis_Presupuestal_BE2SCALE_{entidad_nombre.replace(' ', '_')}.pdf",
    mime="application/pdf",
)

st.caption("AQUAMARKET S.A.C. | Ingeniería de Rentabilidad Acuícola")

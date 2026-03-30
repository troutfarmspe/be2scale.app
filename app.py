import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# 1. Configuración de Marca
st.set_page_config(page_title="BE2SCALE | Optimizer", layout="centered", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #FFFFFF; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #00897B; }
    .stSlider { color: #00897B; }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado
st.title("📊 BE2SCALE")
st.markdown("### **Bio-Economic Optimizer v1.5**")
st.write("---")

# 3. Panel de Control (Doble Deslizador)
st.sidebar.header("🏢 DATOS DE LA OPERACIÓN")
entidad_nombre = st.sidebar.text_input("Municipalidad/Empresa", value="Municipalidad de Ayavirí")
tm_objetivo = st.sidebar.number_input("Biomasa Objetivo (TM)", value=20, step=1, format="%d")
kg_equivalentes = tm_objetivo * 1000

st.sidebar.header("⚙️ INGENIERÍA DE ALIMENTACIÓN")
fcr_actual = st.sidebar.slider("FCR Actual (Línea Base)", 1.2, 2.5, 1.70, help="El FCR que la municipalidad registra actualmente.")
fcr_objetivo = st.sidebar.slider("FCR Objetivo (Meta BE2SCALE)", 0.9, 2.0, 1.45, help="La meta técnica basada en potencial genético y optimización.")
costo_alimento = st.sidebar.number_input("Costo Alimento (S/ por Kg)", value=4.85)

st.sidebar.info("AQUAMARKET S.A.C. | RUC: 20601363628")

# 4. Motor de Cálculo (Diferencial Técnico)
# Escenario Actual
gasto_total_actual = kg_equivalentes * fcr_actual * costo_alimento

# Escenario Meta (Seleccionado por el Consultor)
gasto_total_meta = kg_equivalentes * fcr_objetivo * costo_alimento

# El Rescate de Capital
utilidad_recuperada = gasto_total_actual - gasto_total_meta
mejora_porcentual = ((fcr_actual - fcr_objetivo) / fcr_actual) * 100
fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

# 5. Visualización Estratégica
st.subheader(f"Simulación de Eficiencia: {entidad_nombre}")

col1, col2 = st.columns(2)
with col1:
    st.error(f"PRESUPUESTO ACTUAL")
    st.subheader(f"S/ {gasto_total_actual:,.0f}")
    st.caption(f"Con FCR de {fcr_actual}")

with col2:
    st.success(f"PRESUPUESTO OPTIMIZADO")
    st.subheader(f"S/ {gasto_total_meta:,.0f}")
    st.caption(f"Con FCR Meta de {fcr_objetivo}")

st.write("---")

# Fila 2: Indicadores de Rescate
c1, c2 = st.columns(2)
with c1:
    st.metric(label="CAPITAL RESCATADO", value=f"S/ {utilidad_recuperada:,.0f}", delta=f"{mejora_porcentual:.1f}% Eficiencia")
with c2:
    st.metric(label="AHORRO EN INSUMO", value=f"{(kg_equivalentes*(fcr_actual-fcr_objetivo)):,.0f} Kg")

# 6. Explicación Técnica para el Alcalde
st.markdown(f"### **¿Cómo logramos bajar de {fcr_actual} a {fcr_objetivo}?**")
st.info(f"""
La reducción de **{fcr_actual - fcr_objetivo:.2f} puntos de FCR** se logra mediante:
1. **Sincronización Metabólica:** Ajuste de raciones según curvas de temperatura real.
2. **Hidrodinámica de Pozas:** Reducción del pellet perdido en zonas muertas.
3. **Optimización de Oxígeno:** Mejora de la tasa de absorción de nutrientes.
""")

# 7. Generación de PDF
def create_pdf(nombre, tm, fcr_a, fcr_o, gasto_a, gasto_o, ahorro, fecha):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(200, 10, txt="BE2SCALE - REPORTE DE INGENIERÍA ECONÓMICA", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Fecha: {fecha} | RUC: 20601363628", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"ENTIDAD: {nombre.upper()}", ln=True)
    
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"ANÁLISIS DE BRECHA DE RENTABILIDAD:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, txt=f"- Gasto Actual con FCR {fcr_a}: S/ {gasto_a:,.2f}", ln=True)
    pdf.cell(200, 8, txt=f"- Gasto Proyectado con FCR {fcr_o}: S/ {gasto_o:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_fill_color(224, 255, 224)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 15, txt=f"AHORRO DIRECTO RESCATADO: S/ {ahorro:,.2f}", border=1, ln=True, align='C', fill=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, txt=f"CONCLUSIÓN: La optimización de {fcr_a - fcr_o:.2f} puntos en el Factor de Conversión representa un beneficio neto de S/ {ahorro:,.2f} para la {nombre}, financiado por la reducción de desperdicios biológicos.")
    
    pdf.ln(30)
    pdf.cell(200, 10, txt="Ing. William Bernuy Espinoza - Director Estratégico", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# Botón de Descarga
pdf_data = create_pdf(entidad_nombre, tm_objetivo, fcr_actual, fcr_objetivo, gasto_total_actual, gasto_total_meta, utilidad_recuperada, fecha_actual)
st.download_button(
    label=f"📩 DESCARGAR INFORME TÉCNICO",
    data=pdf_data,
    file_name=f"Informe_Tecnico_BE2SCALE_{entidad_nombre.replace(' ', '_')}.pdf",
    mime="application/pdf",
)

st.caption("BE2SCALE v1.5 | Rigor en Datos, Éxito en Resultados.")

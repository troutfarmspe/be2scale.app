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
st.markdown("### **Bio-Economic Optimizer v1.7**")
st.write("---")

# 3. Sidebar: Parámetros Compartidos
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
    fcr_actual = st.sidebar.slider("FCR Actual (Línea Base)", 1.2, 2.5, 1.70)
    fcr_objetivo = st.sidebar.slider("FCR Objetivo (Meta BE2SCALE)", 0.9, 2.0, 1.45)

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
    st.info(f"Diagnóstico: La optimización técnica libera S/ {ahorro:,.2f} de presupuesto operativo.")

with tab2:
    st.subheader("Análisis de Saturación de Oxígeno (O2)")
    p_atm = 760 * math.exp(-altitud / 8000)
    o2_base = 14.603 - 0.4025 * temp_agua + 0.0077 * (temp_agua**2)
    o2_real = o2_base * (p_atm / 760)

    if o2_real < 5.5:
        color_status = "CRÍTICO"
        nota = "Peligro de Hipoxia severa. El metabolismo biológico está bloqueado."
    elif 5.5 <= o2_real < 7.0:
        color_status = "ALERTA"
        nota = "Estrés metabólico detectado. El FCR aumentará por baja asimilación."
    else:
        color_status = "ÓPTIMO"
        nota = "Condiciones ideales para conversión alimenticia de alta precisión."

    st.markdown(f"### Estatus: **{color_status}**")
    st.progress(min(o2_real/12.0, 1.0))
    st.write(f"**Oxígeno Disponible:** {o2_real:.2f} mg/L a {altitud} msnm.")
    st.write(f"> **Veredicto:** {nota}")

# --- FUNCIÓN DE REPORTE AVANZADO (PDF) ---
def create_advanced_pdf(nombre, tm, fcr_a, fcr_o, g_a, g_o, ahorro, o2, alt, temp, status, nota):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Corporativo
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(0, 51, 102) # Azul Marino
    pdf.cell(190, 15, txt="INFORME DE INGENIERÍA Y RENTABILIDAD", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 5, txt="BE2SCALE - División de Consultoría Estratégica Aquamarket S.A.C.", ln=True, align='C')
    pdf.set_font("Arial", size=9)
    pdf.cell(190, 5, txt=f"Emitido: {datetime.datetime.now().strftime('%d/%m/%Y')} | RUC: 20601363628", ln=True, align='C')
    pdf.ln(10)

    # Bloque 1: Resumen de Entidad
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, txt=f" ENTIDAD: {nombre.upper()}", border=1, ln=True, fill=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, txt=f" Biomasa Proyectada: {tm} TM", border=1)
    pdf.cell(95, 8, txt=f" Altitud: {alt} m.s.n.m.", border=1, ln=True)
    pdf.ln(5)

    # Bloque 2: Diagnóstico Bio-Térmico (Ciencia)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200, 0, 0) if o2 < 5.5 else pdf.set_text_color(0, 100, 0)
    pdf.cell(190, 10, txt=f" DIAGNÓSTICO BIO-TÉRMICO (Status: {status})", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(190, 6, txt=f"Basado en la Ley de Henry y la cinética térmica a {temp} C, la saturación máxima de Oxígeno Disuelto es de {o2:.2f} mg/L. {nota}")
    pdf.ln(5)

    # Bloque 3: Análisis Económico (Cuadro Comparativo)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, txt=" RESUMEN DE OPTIMIZACIÓN FINANCIERA", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(63, 10, txt="Escenario", border=1, align='C')
    pdf.cell(63, 10, txt="FCR", border=1, align='C')
    pdf.cell(64, 10, txt="Inversión Alimento", border=1, ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(63, 10, txt="Línea Base (Actual)", border=1, align='C')
    pdf.cell(63, 10, txt=f"{fcr_a}", border=1, align='C')
    pdf.cell(64, 10, txt=f"S/ {g_a:,.2f}", border=1, ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(63, 10, txt="Meta BE2SCALE", border=1, align='C')
    pdf.cell(63, 10, txt=f"{fcr_o:.2f}", border=1, align='C')
    pdf.cell(64, 10, txt=f"S/ {g_o:,.2f}", border=1, ln=True, align='C')
    pdf.ln(5)

    # Bloque 4: El Rescate (Monto Final)
    pdf.set_fill_color(0, 137, 123) # Verde BE2SCALE
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 15, txt=f" CAPITAL RESCATADO POR CICLO: S/ {ahorro:,.2f} ", border=1, ln=True, align='C', fill=True)
    
    # Bloque 5: Metodología
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 8, txt="METODOLOGÍA DE INTERVENCIÓN BE2SCALE:", ln=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(190, 5, txt="1. Ajuste Dinámico de Raciones: Sincronización metabólica según T de agua.\n2. Tech-Audit: Optimización de infraestructura de aireación y flujo hidráulico.\n3. Monitoreo Predictivo: Control de datos para evitar desperdicio de pellet en fondo.")

    # Firma
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 5, txt="_______________________________________", ln=True, align='R')
    pdf.cell(190, 5, txt="Ing. William Bernuy Espinoza", ln=True, align='R')
    pdf.set_font("Arial", size=9)
    pdf.cell(190, 5, txt="Director Estratégico BE2SCALE", ln=True, align='R')

    return pdf.output(dest='S').encode('latin-1')

# Botón de Descarga en Sidebar
st.sidebar.write("---")
if st.sidebar.button("📄 GENERAR INFORME AVANZADO"):
    pdf_bytes = create_advanced_pdf(entidad_nombre, tm_objetivo, fcr_actual, fcr_objetivo, gasto_actual, gasto_meta, ahorro, o2_real, altitud, temp_agua, color_status, nota)
    st.sidebar.download_button(label="⬇️ DESCARGAR REPORTE", data=pdf_bytes, file_name=f"Informe_BE2SCALE_{entidad_nombre}.pdf", mime="application/pdf")

st.caption("BE2SCALE v1.7 | Rigor Científico para la Acuicultura Peruana")

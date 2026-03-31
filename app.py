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

# 2. Encabezado
st.title("📊 BE2SCALE")
st.markdown("### **Bio-Economic Optimizer v1.8**")
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

# --- LÓGICA TERMODINÁMICA (Para ambas pestañas) ---
p_atm = 760 * math.exp(-altitud / 8000)
o2_base = 14.603 - 0.4025 * temp_agua + 0.0077 * (temp_agua**2)
o2_real = o2_base * (p_atm / 760)

# Definición de Semáforo
if o2_real < 5.5:
    color_hex = "#FF4B4B" # Rojo
    status_o2 = "CRÍTICO (HIPOXIA)"
    nota_o2 = "Riesgo inminente. El metabolismo está bloqueado. El FCR se dispara."
elif 5.5 <= o2_real < 7.0:
    color_hex = "#FFA500" # Naranja/Amarillo
    status_o2 = "ALERTA (ESTRÉS)"
    nota_o2 = "Eficiencia reducida. El crecimiento es lento y el desperdicio es alto."
else:
    color_hex = "#00897B" # Verde BE2SCALE
    status_o2 = "ÓPTIMO (PRECISIÓN)"
    nota_o2 = "Condiciones ideales para conversión alimenticia de alta velocidad."

# --- CREACIÓN DE PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["💰 Análisis Económico", "🧬 Ingeniería Bio-Térmica", "📐 Capacidad de Carga", "⚖️ Cumplimiento Normativo"])

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
    st.subheader("Disponibilidad de Oxígeno Real (O2)")
    
    # Visualización de Semáforo Dinámico
    st.markdown(f"""
        <div style="background-color:#112240; padding:30px; border-radius:15px; border-left: 12px solid {color_hex};">
            <h3 style="color:white; margin:0;">ESTADO: {status_o2}</h3>
            <h1 style="color:{color_hex}; margin:10px 0;">{o2_real:.2f} mg/L</h1>
            <p style="color:#CCCCCC; font-size:1.1em;">{nota_o2}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.write(f"**Cálculo Termodinámico:** {altitud} msnm / {temp_agua} °C")
    st.progress(min(o2_real/12.0, 1.0))

with tab3:
    st.subheader("📐 Capacidad de Carga Científica")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        tipo_tanque = st.selectbox("Estructura de Cultivo", ["Rectangular (Raceway)", "Circular (Concreto/Geomembrana)", "Jaula Flotante"])
        volumen = st.number_input("Volumen Total (m³)", value=100, step=10)
    with col_t2:
        recambio_hora = st.slider("Recambios de agua por hora (R)", 0.5, 4.0, 1.0, help="Veces que se renueva el volumen total en 1 hora.")

with tab4:
    st.subheader("⚖️ Marco Normativo y Cumplimiento (PRODUCE)")
    st.write("Verificación de estándares según la normativa técnica peruana vigente.")

    st.markdown("""
    <div style="background-color:#112240; padding:15px; border-radius:10px; border-left: 5px solid #FFA500;">
        <p style="color:white; margin:0; font-weight:bold;">NTP 032.103:2024 - ACUICULTURA</p>
        <p style="color:gray; font-size:0.9em;">Método para la determinación del Factor de Conversión Alimenticia (FCA) en Trucha Arcoíris.</p>
    </div>
    """, unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        cumple_registro = st.checkbox("¿Cuenta con Registro Diario de Alimentación?")
        cumple_biometria = st.checkbox("¿Realiza Biometrías Mensuales?")
    with col_l2:
        cumple_muestreo = st.checkbox("¿Aplica muestreo representativo (5-10%)?")
        cumple_sanipes = st.checkbox("¿Cuenta con Protocolo Sanitario vigente?")

    if cumple_registro and cumple_biometria and cumple_muestreo:
        st.success("✅ Los datos ingresados cumplen con el rigor metodológico de la NTP 032.103:2024.")
    else:
        st.warning("⚠️ Atención: Para que este reporte tenga validez ante PRODUCE, debe regularizar sus protocolos de muestreo y registro.")

    st.info("**Nota para AMYPE:** El cumplimiento de estas normas es requisito para la renovación de derechos acuícolas y el acceso a créditos de FONDEPES.")

    # --- LÓGICA DE INGENIERÍA AQUA-SCALE ---
    # 1. Consumo de O2 estimado para Trucha (0.2 - 0.4 g O2 / kg pez / hora)
    consumo_o2_kg = 0.25 
    # 2. Oxígeno disponible para el pez (O2 Real - O2 salida seguridad [5 mg/L])
    o2_disponible = max(o2_real - 5.0, 0.1)
    
    # 3. Fórmula de Capacidad de Carga (Basada en Flujo y Oxígeno)
    # Capacidad (kg) = (Flujo L/h * O2 disponible mg/L) / Consumo O2 mg/kg/h
    flujo_l_h = volumen * 1000 * recambio_hora
    biomasa_max = (flujo_l_h * o2_disponible) / (consumo_o2_kg * 1000)
    
    # Ajuste por tipo de estructura (Eficiencia de mezcla)
    if tipo_tanque == "Jaula Flotante": biomasa_max *= 0.7  # Menor control de flujo
    if tipo_tanque == "Circular (Concreto/Geomembrana)": biomasa_max *= 1.1 # Mejor autolimpieza/mezcla
    
    densidad_max = biomasa_max / volumen

    # Visualización Senior
    st.markdown(f"""
        <div style="background-color:#112240; padding:20px; border-radius:10px; border-top: 5px solid #00897B;">
            <p style="color:gray; margin:0;">DENSIDAD TÉCNICA RECOMENDADA</p>
            <h2 style="color:#00897B; margin:0;">{densidad_max:.2f} kg/m³</h2>
            <hr>
            <p style="color:gray; margin:0;">BIOMASA MÁXIMA SOPORTADA</p>
            <h1 style="color:white; margin:0;">{biomasa_max:,.0f} Kg de Trucha</h1>
            <p style="color:#FFA500; font-size:0.9em;">*Cálculo basado en {recambio_hora} recambio(s)/hora y {o2_real:.2f} mg/L de O₂ de entrada.</p>
        </div>
    """, unsafe_allow_html=True)

    st.warning(f"**Nota de Consultoría:** Si desea subir de {densidad_max:.1f} kg/m³, es imperativo implementar **Aireación Mecánica** o inyección de Oxígeno líquido.")


# --- FUNCIÓN DE REPORTE PDF AVANZADO ---
def create_final_pdf(tipo, vol, dens_max, bio_max):
    pdf = FPDF()
    pdf.add_page()
    
    # Título y Marca
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(190, 15, txt="INFORME TÉCNICO DE RENTABILIDAD", ln=True, align='C')
    pdf.set_font("Arial", size=9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(190, 5, txt=f"BE2SCALE - AQUAMARKET S.A.C. | RUC: 20601363628 | {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, txt=f" CLIENTE: {entidad_nombre.upper()}", border=1, ln=True, fill=False)
    
    # 1. Diagnóstico Bio-Térmico
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, txt="1. DIAGNÓSTICO BIOMÉTRICO (SATURACIÓN O2):", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(190, 6, txt=f"A una altitud de {altitud} msnm y temperatura de {temp_agua}C, el oxígeno disponible es de {o2_real:.2f} mg/L. Estatus: {status_o2}. {nota_o2}")

    # 2. CAPACIDAD DE CARGA DE INFRAESTRUCTURA (Nuevo Bloque)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, txt=f"2. EVALUACIÓN DE INFRAESTRUCTURA ({tipo.upper()}):", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, txt=f" Volumen de Cultivo: {vol} m3", border=1)
    pdf.cell(95, 8, txt=f" Densidad Máxima sugerida: {dens_max:.2f} kg/m3", border=1, ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 8, txt=f" Límite Biológico del Sistema: {bio_max:,.0f} Kg de Trucha", border=1, ln=True, align='C')
    pdf.ln(5)

    # 3. Análisis Financiero
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, txt="2. OPTIMIZACIÓN DEL GASTO OPERATIVO:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 10, txt=f"Gasto Actual (FCR {fcr_actual}):", border=1)
    pdf.cell(95, 10, txt=f"S/ {gasto_actual:,.2f}", border=1, ln=True)
    pdf.cell(95, 10, txt=f"Meta BE2SCALE (FCR {fcr_objetivo:.2f}):", border=1)
    pdf.cell(95, 10, txt=f"S/ {gasto_meta:,.2f}", border=1, ln=True)
    
    pdf.ln(5)
    pdf.set_fill_color(0, 137, 123)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 15, txt=f"CAPITAL RESCATADO POR CICLO: S/ {ahorro:,.2f}", border=1, ln=True, align='C', fill=True)
    
    # Firmas de Conformidad
    pdf.ln(25)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, txt="__________________________", ln=0, align='C')
    pdf.cell(95, 10, txt="__________________________", ln=1, align='C')
    pdf.cell(95, 5, txt="Ing. William Bernuy E.", ln=0, align='C')
    pdf.cell(95, 5, txt="Conformidad del Cliente", ln=1, align='C')
    pdf.set_font("Arial", size=8)
    pdf.cell(95, 5, txt="Director Estratégico BE2SCALE", ln=0, align='C')
    pdf.cell(95, 5, txt=f"{entidad_nombre}", ln=1, align='C')

    return pdf.output(dest='S').encode('latin-1')

# Botón en Sidebar
st.sidebar.write("---")
if st.sidebar.button("📄 GENERAR REPORTE PDF FINAL"):
    # Asegúrate que estas variables (tipo_tanque, volumen, densidad_max, biomasa_max) 
    # coincidan con las de tu Tab 3
    pdf_bytes = create_final_pdf(tipo_tanque, volumen, densidad_max, biomasa_max)
    st.sidebar.download_button(label="⬇️ DESCARGAR AHORA", data=pdf_bytes, file_name=f"Informe_BE2SCALE_{entidad_nombre}.pdf", mime="application/pdf")


st.caption("BE2SCALE v1.8 | Ingeniería de Precisión para el Perú.")

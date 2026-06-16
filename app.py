import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN DE LA PÁGINA (UI/UX Móvil y Tema Oscuro)
st.set_page_config(
    page_title="Gestión Financiera Inteligente",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para forzar un diseño premium, limpio y responsivo
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 480px; padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #3b82f6; color: white; font-weight: bold; }
    
    /* Contenedores de tarjetas de información */
    div.data-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div.cuenta-item {
        background-color: #0f172a;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 6px;
        border: 1px solid #334155;
    }
    .flex-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
    }
    .text-muted { color: #94a3b8; font-size: 0.85em; }
    .text-success { color: #10b981; font-weight: bold; }
    .text-warning { color: #f59e0b; font-weight: bold; }
    .text-danger { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE ESTADO (Persistencia de la Inyección Inteligente)
if 'ingresos_extras' not in st.session_state:
    st.session_state.ingresos_extras = 0.0

# Base de datos semilla estructurada según el modelo relacional del Brief
INGRESO_FIJO_Q = 5000.00

gastos_fijos = [
    {"concepto": "Renta y Servicios (Provisión)", "monto": 2500.00, "dia_vencimiento": 5, "metodo": "Transferencia"},
    {"concepto": "Supermercado y Comida", "monto": 1200.00, "dia_vencimiento": 18, "metodo": "Efectivo/Débito"}
]

deudas = [
    {"nombre": "Tarjeta Santander", "saldo_total": 15000.00, "tasa_interes_anual": 21.76, "pago_minimo": 800.00, "fecha_limite_dia": 25, "es_msi": False},
    {"nombre": "Compra Mercado Libre", "saldo_total": 3400.00, "tasa_interes_anual": 44.00, "pago_minimo": 450.00, "fecha_limite_dia": 9, "es_msi": False},
    {"nombre": "Plan Telcel (MSI)", "saldo_total": 2400.00, "tasa_interes_anual": 0.00, "pago_minimo": 400.00, "fecha_limite_dia": 12, "es_msi": True}
]

# 3. MOTOR DE INTELIGENCIA Y ALGORITMOS (Lógica de Negocio Avanzada)
def procesar_fase_a_detallada(quincena_actual):
    """Calcula la jerarquía estricta y extrae los conceptos específicos por quincena"""
    alertas = []
    
    # Prioridad 1: Gastos Fijos que caen en este bloque de días
    gastos_aplicables = []
    for g in gastos_fijos:
        if (quincena_actual == 1 and g["dia_vencimiento"] <= 15) or (quincena_actual == 2 and g["dia_vencimiento"] > 15):
            gastos_aplicables.append(g)
            
    # Prioridad 2: Pagos Mínimos Obligatorios del periodo actual + amortizaciones preventivas
    deudas_aplicables = []
    for d in deudas:
        # Regla de amortización quincenal obligatoria (Ej: vence el 9, se provisiona en la Q2 del mes anterior)
        if quincena_actual == 2 and d["fecha_limite_dia"] <= 15:
            alertas.append(f"⚠️ **Amortización Preventiva:** '{d['nombre']}' vence el día {d['fecha_limite_dia']} de la siguiente quincena. Se bloquea desde este ingreso quincenal para proteger tu historial crediticio.")
            deudas_aplicables.append(d)
        elif quincena_actual == 1 and (15 < d["fecha_limite_dia"] <= 31):
            pass # Le corresponde a la segunda quincena
        elif (quincena_actual == 1 and d["fecha_limite_dia"] <= 15) or (quincena_actual == 2 and d["fecha_limite_dia"] > 15):
            deudas_aplicables.append(d)
            
    return gastos_aplicables, deudas_aplicables, alertas

def calcular_fase_b_avalancha():
    if st.session_state.ingresos_extras <= 0:
        return None
    
    # Filtramos deudas reales con tasa de interés que tengan saldo
    deudas_con_interes = [d for d in deudas if not d["es_msi"] and d["saldo_total"] > 0]
    if not deudas_con_interes:
        return "¡Felicidades! Todas tus cuentas con interés están liquidadas. Puedes usar el dinero para ahorro o inversión."
        
    # Algoritmo Avalancha: Buscar la mayor tasa anual
    deuda_objetivo = max(deudas_con_interes, key=lambda x: x["tasa_interes_anual"])
    monto_inyectar = min(st.session_state.ingresos_extras, deuda_objetivo["saldo_total"])
    
    return {
        "deuda": deuda_objetivo["nombre"],
        "tasa": deuda_objetivo["tasa_interes_anual"],
        "monto": monto_inyectar
    }

# 4. INTERFAZ DE USUARIO (VISTAS COMPLETAS)
st.title("📱 Finanzas Inteligentes")
st.caption("Presupuesto Base Cero Dinámico & Algoritmo Avalancha")

# Control de tiempo real simulado
quincena = st.select_slider("📍 Evaluar Periodo Quincenal", options=[1, 2], format_func=lambda x: f"Quincena {x} del Mes")

st.markdown("### 🎛️ Panel de Control")

# Módulo de Ingreso Rápido
with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.write(f"**Ingreso Fijo Garantizado:** `${INGRESO_FIJO_Q:,.2f} MXN`")
    
    extra_input = st.number_input("Inyección Inteligente (Comisiones / Extras)", min_value=0.0, step=100.0, key="input_dinamico_extras")
    
    if st.button("🚀 Registrar Ingreso Extra"):
        st.session_state.ingresos_extras = extra_input
        st.success(f"¡Inyección de ${extra_input:,.2f} MXN registrada en el motor de decisiones!")
    st.markdown('</div>', unsafe_allow_html=True)

# Procesamiento de datos mediante el motor inteligente
gastos_lista, deudas_lista, alertas_motor = procesar_fase_a_detallada(quincena)
total_g_fijos = sum(g["monto"] for g in gastos_lista)
total_minimos = sum(d["pago_minimo"] for d in deudas_lista)
dinero_libre = INGRESO_FIJO_Q - total_g_fijos - total_minimos
recomendacion_avalancha = calcular_fase_b_avalancha()

# --- SEMÁFORO FINANCIERO CON DESGLOSE DE CUENTAS ---
st.markdown("### 🧠 Tabla Inteligente (Semáforo)")

# Desplegar avisos preventivos del motor
for alerta in alertas_motor:
    st.warning(alerta)

# 1. Bloque de Gastos Fijos Detallados
with st.container():
    st.markdown(f"""
    <div class="data-card" style="border-left-color: #3b82f6;">
        <div class="flex-header">
            <span>🏠 Prioridad 1: Gastos Fijos</span>
            <span class="text-warning">${total_g_fijos:,.2f} MXN</span>
        </div>
        <p class="text-muted">Retener de forma obligatoria para subsistencia diaria:</p>
    """, unsafe_allow_html=True)
    
    for g in gastos_lista:
        st.markdown(f"""
        <div class="cuenta-item">
            <div class="flex-header">
                <span>• {g['concepto']}</span>
                <span>${g['monto']:,.2f}</span>
            </div>
            <div class="text-muted">Vence el día {g['dia_vencimiento']} | Pago: {g['metodo']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Bloque de Mínimos Obligatorios Detallados (¿A qué cuentas va?)
with st.container():
    st.markdown(f"""
    <div class="data-card" style="border-left-color: #ef4444;">
        <div class="flex-header">
            <span>🛡️ Prioridad 2: Pagos Mínimos</span>
            <span class="text-danger">${total_minimos:,.2f} MXN</span>
        </div>
        <p class="text-muted">Asignación obligatoria a cuentas para proteger historial crediticio:</p>
    """, unsafe_allow_html=True)
    
    for d in deudas_lista:
        tipo_deuda = "Plan MSI" if d["es_msi"] else f"Tasa Anual: {d['tasa_interes_anual']}%"
        st.markdown(f"""
        <div class="cuenta-item">
            <div class="flex-header">
                <span>💳 {d['nombre']}</span>
                <span>${d['pago_minimo']:,.2f}</span>
            </div>
            <div class="text-muted">Vence el día {d['fecha_limite_dia']} | {tipo_deuda}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Bloque de Remanente Libre
with st.container():
    color_libre = "#10b981" if dinero_libre >= 0 else "#ef4444"
    st.markdown(f"""
    <div class="data-card" style="border-left-color: {color_libre};">
        <div class="flex-header">
            <span>🟢 Remanente Libre Disponible</span>
            <span style="color: {color_libre};">${dinero_libre:,.2f} MXN</span>
        </div>
        <p class="text-muted">Dinero remanente para consumo variable o despensa diaria una vez cubiertos los blindajes.</p>
    </div>
    """, unsafe_allow_html=True)

# Modo Destrucción de Deuda Activo (Fase B - Inyecciones variables)
if recomendacion_avalancha:
    if isinstance(recomendacion_avalancha, dict):
        st.markdown(f"""
        <div style="background-color:#10b981; padding:16px; border-radius:12px; color:white; margin-bottom:15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        💥 <b>MODO DESTRUCCIÓN DE DEUDA ACTIVADO</b><br>
        Se detectó una comisión o ingreso extra libre de <b>${st.session_state.ingresos_extras:,.2f} MXN</b>.<br><br>
        <b>Recomendación del Motor Avalancha:</b><br>
        Destina el 100% de esta inyección (<b>${recomendacion_avalancha['monto']:,.2f} MXN</b>) de forma directa como pago extra a la cuenta: <b>{recomendacion_avalancha['deuda']}</b>.<br>
        <i>Razón inteligente: Mitiga el costo del dinero al atacar tu cuenta con la tasa anual más agresiva ({recomendacion_avalancha['tasa']}%).</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(recomendacion_avalancha)

# --- VISTA B: TABLA DE DISTRIBUCIÓN MENSUAL ---
st.markdown("### 📊 Distribución del Mes Actual")
tab1, tab2 = st.tabs(["Quincena 1 (Día 15)", "Quincena 2 (Día 30/31)"])

with tab1:
    g1, d1, _ = procesar_fase_a_detallada(1)
    df_q1 = pd.DataFrame({
        "Concepto / Cuenta": [x["concepto"] for x in g1] + [x["nombre"] for x in d1],
        "Categoría": ["Gasto Fijo"]*len(g1) + ["Mínimo Obligatorio"]*len(d1),
        "Monto a Retener": [x["monto"] for x in g1] + [x["pago_minimo"] for x in d1]
    })
    st.dataframe(df_q1, hide_index=True, use_container_width=True)

with tab2:
    g2, d2, _ = procesar_fase_a_detallada(2)
    df_q2 = pd.DataFrame({
        "Concepto / Cuenta": [x["concepto"] for x in g2] + [x["nombre"] for x in d2],
        "Categoría": ["Gasto Fijo"]*len(g2) + ["Mínimo Obligatorio"]*len(d2),
        "Monto a Retener": [x["monto"] for x in g2] + [x["pago_minimo"] for x in d2]
    })
    st.dataframe(df_q2, hide_index=True, use_container_width=True)

# --- VISTA C: MÓDULO DE GESTIÓN DE DEUDAS Y PROYECCIONES (Solucionado) ---
st.markdown("### 📉 Proyección de Línea de Tiempo")
df_deudas_base = pd.DataFrame(deudas)

# Control deslizante para estimar futuros abonos mensuales adicionales recurrentes
abono_proyectado = st.slider("Simular abono extra mensual futuro", 0, 5000, int(st.session_state.ingresos_extras), step=250)

proyecciones = []
for d in deudas:
    if d["es_msi"]:
        # Los meses sin intereses bajan linealmente con el pago mínimo establecido
        meses_fin = np.ceil(d["saldo_total"] / d["pago_minimo"]) if d["pago_minimo"] > 0 else 12
    else:
        # Buscamos de forma segura cuál es la deuda con la tasa más alta en el DataFrame para inyectarle el extra simulado
        tasa_maxima = df_deudas_base[df_deudas_base['es_msi'] == False]['tasa_interes_anual'].max()
        es_la_mayor_tasa = (d["tasa_interes_anual"] == tasa_maxima)
        
        capacidad_pago = d["pago_minimo"] + (abono_proyectado if es_la_mayor_tasa else 0)
        meses_fin = np.ceil(d["saldo_total"] / capacidad_pago) if capacidad_pago > 0 else 0
        
    proyecciones.append({"Deuda / Cuenta": d["nombre"], "Meses Restantes": int(meses_fin)})

df_proyeccion = pd.DataFrame(proyecciones)

# Gráfica visual clara de barras de cara al usuario
st.bar_chart(df_proyeccion.set_index("Deuda / Cuenta"))
st.dataframe(df_proyeccion, hide_index=True, use_container_width=True)

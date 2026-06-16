import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN DE LA PÁGINA (UI/UX Premium & Mobile-First)
st.set_page_config(
    page_title="Smart Finance Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados para el Semáforo Financiero y tarjetas interactivas
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 480px; padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #3b82f6; color: white; font-weight: bold; }
    
    div.data-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 16px;
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
    .flex-header { display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
    .text-muted { color: #94a3b8; font-size: 0.85em; }
    .text-success { color: #10b981; font-weight: bold; }
    .text-warning { color: #f59e0b; font-weight: bold; }
    .text-danger { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE PERSISTENCIA EN MEMORIA (Base de Datos Dinámica del Usuario)
if 'ingresos_extras' not in st.session_state:
    st.session_state.ingresos_extras = 0.0

# Inicialización de Gastos Fijos Reales si no existen en la sesión
if 'gastos_fijos_db' not in st.session_state:
    st.session_state.gastos_fijos_db = [
        {"concepto": "Gasolina (apoyo mamá)", "monto": 800.00, "dia_vencimiento": 5},
        {"concepto": "Gym", "monto": 499.00, "dia_vencimiento": 10},
        {"concepto": "Internet", "monto": 399.00, "dia_vencimiento": 12},
        {"concepto": "Melimas", "monto": 399.00, "dia_vencimiento": 15},
        {"concepto": "Celular (Cargo Nu)", "monto": 289.00, "dia_vencimiento": 19},
        {"concepto": "Transporte", "monto": 240.00, "dia_vencimiento": 20},
        {"concepto": "CFE (Promedio)", "monto": 200.00, "dia_vencimiento": 25},
        {"concepto": "Amazon Prime + Music", "monto": 99.00, "dia_vencimiento": 4},
        {"concepto": "Spotify / plan dúo", "monto": 97.00, "dia_vencimiento": 19}
    ]

# Inicialización de Deudas Reales (Corte a Junio 2026) si no existen en la sesión
if 'deudas_db' not in st.session_state:
    st.session_state.deudas_db = [
        {"nombre": "Préstamo", "saldo_total": 48630.87, "tasa_interes_anual": 21.12, "pago_minimo": 3500.00, "fecha_limite_dia": 9, "es_msi": False},
        {"nombre": "Tarjeta Santander", "saldo_total": 40284.29, "tasa_interes_anual": 21.76, "pago_minimo": 1500.00, "fecha_limite_dia": 1, "es_msi": False}, # Mínimo estimado prudente
        {"nombre": "ADO Nu (Último mes!)", "saldo_total": 734.00, "tasa_interes_anual": 0.00, "pago_minimo": 734.00, "fecha_limite_dia": 19, "es_msi": True},
        {"nombre": "Fijo Nu", "saldo_total": 1081.62, "tasa_interes_anual": 0.00, "pago_minimo": 540.81, "fecha_limite_dia": 19, "es_msi": True},
        {"nombre": "Fijo Nu 2", "saldo_total": 2630.97, "tasa_interes_anual": 0.00, "pago_minimo": 438.49, "fecha_limite_dia": 19, "es_msi": True},
        {"nombre": "Compra Mercado", "saldo_total": 839.34, "tasa_interes_anual": 44.00, "pago_minimo": 279.78, "fecha_limite_dia": 16, "es_msi": False}
    ]

INGRESO_FIJO_Q = 5000.00

# 3. MOTOR DE INTELIGENCIA Y ALGORITMOS (Presupuesto Base Cero Dinámico)
def procesar_fase_a_detallada(quincena_actual):
    alertas = []
    
    # Dividir gastos fijos mensuales equitativamente o por quincena según su vencimiento diario
    gastos_aplicables = []
    for g in st.session_state.gastos_fijos_db:
        if (quincena_actual == 1 and g["dia_vencimiento"] <= 15) or (quincena_actual == 2 and g["dia_vencimiento"] > 15):
            gastos_aplicables.append(g)
            
    # Distribución estricta de mínimos obligatorios
    deudas_aplicables = []
    for d in st.session_state.deudas_db:
        # Regla de amortización quincenal preventiva del Brief:
        # Si estamos en Q2 (días 16-30) y una deuda vence del 1 al 15 del mes entrante (ej. Santander el 1 o Préstamo el 9)
        # El motor debe alertar y retenerlo obligatoriamente desde la Q2 actual.
        if quincena_actual == 2 and d["fecha_limite_dia"] <= 15:
            alertas.append(f"⚠️ **Amortización Preventiva:** '{d['nombre']}' vence el día {d['fecha_limite_dia']}. Se fondea con esta Q2 para evitar recargos al inicio del próximo mes.")
            deudas_aplicables.append(d)
        elif quincena_actual == 1 and (15 < d["fecha_limite_dia"] <= 31):
            pass # Corresponde de forma natural a Q2
        elif (quincena_actual == 1 and d["fecha_limite_dia"] <= 15) or (quincena_actual == 2 and d["fecha_limite_dia"] > 15):
            deudas_aplicables.append(d)
            
    return gastos_aplicables, deudas_aplicables, alertas

def calcular_fase_b_avalancha():
    if st.session_state.ingresos_extras <= 0:
        return None
    
    # Filtrar deudas con interés reales que sigan teniendo saldo pendiente
    con_interes = [d for d in st.session_state.deudas_db if not d["es_msi"] and d["saldo_total"] > 0]
    if not con_interes:
        return "⚡ ¡Felicidades! No tienes deudas con interés activo para aplicar Avalancha."
        
    # Algoritmo Avalancha: Atacar la tasa de interés anual más agresiva
    deuda_objetivo = max(con_interes, key=lambda x: x["tasa_interes_anual"])
    monto_inyectar = min(st.session_state.ingresos_extras, deuda_objetivo["saldo_total"])
    
    return {
        "deuda": deuda_objetivo["nombre"],
        "tasa": deuda_objetivo["tasa_interes_anual"],
        "monto": monto_inyectar
    }

# 4. INTERFAZ DE USUARIO (UI / UX MÓVIL)
st.title("📱 Smart Finance App")
st.caption("Ecosistema Personalizado de Gestión Financiera Inteligente")

# --- NUEVO MÓDULO: REGISTRO Y EDICIÓN COMPLETA DE DEUDAS (Petición del usuario) ---
with st.expander("🛠️ Administrar Mis Deudas y Gastos (Modificar Cuentas)"):
    st.markdown("#### Agregar Nueva Deuda o Compra")
    with st.form("nueva_deuda_form"):
        n_nombre = st.text_input("Nombre de la cuenta / concepto")
        n_saldo = st.number_input("Saldo Total Actual ($)", min_value=0.0, step=100.0)
        n_tasa = st.number_input("Tasa de Interés Anual (%)", min_value=0.0, step=1.0)
        n_minimo = st.number_input("Pago Mínimo Quincenal/Mensual ($)", min_value=0.0, step=50.0)
        n_dia = st.number_input("Día Límite de Pago (1-31)", min_value=1, max_value=31, value=15)
        n_msi = st.checkbox("¿Es Plan Fijo / Meses Sin Intereses (0% Tasa)?")
        
        if st.form_submit_button("💾 Registrar en Base de Datos"):
            if n_nombre:
                st.session_state.deudas_db.append({
                    "nombre": n_nombre, "saldo_total": n_saldo, "tasa_interes_anual": n_tasa,
                    "pago_minimo": n_minimo, "fecha_limite_dia": n_dia, "es_msi": n_msi
                })
                st.success(f"'{n_nombre}' guardada exitosamente.")
            else:
                st.error("Por favor ingresa un nombre para la deuda.")

    st.markdown("---")
    st.markdown("#### Modificar Datos Actuales Directamente")
    # Permitir edición interactiva en una tabla editable nativa de Streamlit
    df_deudas_editable = pd.DataFrame(st.session_state.deudas_db)
    edited_df = st.data_editor(df_deudas_editable, num_rows="dynamic", hide_index=True, use_container_width=True)
    if st.button("🔄 Actualizar Todo"):
        st.session_state.deudas_db = edited_df.to_dict(orient="records")
        st.success("¡Base de datos financiera sincronizada e integrada con éxito!")

# Control de simulación quincenal
quincena = st.select_slider("📍 Periodo Quincenal a Evaluar", options=[1, 2], format_func=lambda x: f"Quincena {x} del Mes")

st.markdown("### 🎛️ Panel de Ingresos")
with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.write(f"**Tu Ingreso Fijo Base (Quincenal):** `${INGRESO_FIJO_Q:,.2f} MXN`")
    
    extra_input = st.number_input("Inyección Inteligente (Comisión / Extra Variable)", min_value=0.0, step=100.0, key="val_extra")
    if st.button("🚀 Activar Inyección"):
        st.session_state.ingresos_extras = extra_input
        st.success("Ingreso variable inyectado al motor de aceleración de pagos.")
    st.markdown('</div>', unsafe_allow_html=True)

# Ejecución de cálculos basados en tu información viva
gastos_lista, deudas_lista, alertas_motor = procesar_fase_a_detallada(quincena)
total_g_fijos = sum(g["monto"] for g in gastos_lista)
total_minimos = sum(d["pago_minimo"] for d in deudas_lista)
dinero_libre = INGRESO_FIJO_Q - total_g_fijos - total_minimos
recomendacion_avalancha = calcular_fase_b_avalancha()

# --- SEMÁFORO FINANCIERO DINÁMICO CON TUS CUENTAS ---
st.markdown("### 🧠 Semáforo Financiero Inteligente")

for alerta in alertas_motor:
    st.warning(alerta)

# 1. Bloque de Tus Gastos de Vida Reales
with st.container():
    st.markdown(f"""
    <div class="data-card" style="border-left-color: #3b82f6;">
        <div class="flex-header">
            <span>🏠 Prioridad 1: Subtotal Vida</span>
            <span class="text-warning">${total_g_fijos:,.2f} MXN</span>
        </div>
        <p class="text-muted">Gastos de operación indispensables filtrados para este periodo:</p>
    """, unsafe_allow_html=True)
    for g in gastos_lista:
        st.markdown(f"""
        <div class="cuenta-item">
            <div class="flex-header">
                <span>• {g['concepto']}</span>
                <span>${g['monto']:,.2f}</span>
            </div>
            <div class="text-muted">Vence el día {g['dia_vencimiento']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Bloque de Tus Pagos Mínimos Obligatorios Reales
with st.container():
    st.markdown(f"""
    <div class="data-card" style="border-left-color: #ef4444;">
        <div class="flex-header">
            <span>🛡️ Prioridad 2: Blindaje de Crédito</span>
            <span class="text-danger">${total_minimos:,.2f} MXN</span>
        </div>
        <p class="text-muted">Montos mínimos que debes transferir ya a estas cuentas específicas:</p>
    """, unsafe_allow_html=True)
    for d in deudas_lista:
        detalles = "Plan Fijo 0%" if d["es_msi"] else f"Tasa: {d['tasa_interes_anual']}%"
        st.markdown(f"""
        <div class="cuenta-item">
            <div class="flex-header">
                <span>💳 {d['nombre']}</span>
                <span>${d['pago_minimo']:,.2f}</span>
            </div>
            <div class="text-muted">Vence el día {d['fecha_limite_dia']} | {detalles} | Saldo: ${d['saldo_total']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Liquidez Libre
with st.container():
    color_box = "#10b981" if dinero_libre >= 0 else "#ef4444"
    st.markdown(f"""
    <div class="data-card" style="border-left-color: {color_box};">
        <div class="flex-header">
            <span>🟢 Flujo Libre de la Quincena</span>
            <span style="color: {color_box};">${dinero_libre:,.2f} MXN</span>
        </div>
        <p class="text-muted">Remanente libre para consumo diario discrecional tras proteger supervivencia y deudas.</p>
    </div>
    """, unsafe_allow_html=True)

# Fase B: Ejecución del algoritmo de aceleración Avalancha con tus comisiones
if recomendacion_avalancha:
    if isinstance(recomendacion_avalancha, dict):
        st.markdown(f"""
        <div style="background-color:#10b981; padding:16px; border-radius:12px; color:white; margin-bottom:15px;">
        💥 <b>MODO DESTRUCCIÓN DE DEUDA ACTIVADO</b><br>
        Inyección extra detectada: <b>${st.session_state.ingresos_extras:,.2f} MXN</b>.<br><br>
        <b>Estrategia de Optimización Matemática (Avalancha):</b><br>
        Transfiere el 100% de este dinero extra (<b>${recomendacion_avalancha['monto']:,.2f} MXN</b>) como un abono directo a capital a la cuenta: <b>{recomendacion_avalancha['deuda']}</b>.<br>
        <i>Razón del motor: Al ser tu cuenta con la tasa más alta ({recomendacion_avalancha['tasa']}% Anual), liquidarla primero te ahorra la mayor cantidad de dinero en intereses futuros.</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(recomendacion_avalancha)

# --- VISTA B: DESGLOSE COMPLETO DEL MES ---
st.markdown("### 📊 Proyección Operativa Mensual")
t1, t2 = st.tabs(["Quincena 1 (Día 15)", "Quincena 2 (Día 30/31)"])

with t1:
    g1, d1, _ = procesar_fase_a_detallada(1)
    df_q1 = pd.DataFrame({
        "Cuenta / Concepto": [x["concepto"] for x in g1] + [x["nombre"] for x in d1],
        "Tipo": ["Gasto de Vida"]*len(g1) + ["Mínimo Obligatorio"]*len(d1),
        "Monto Requerido": [x["monto"] for x in g1] + [x["pago_minimo"] for x in d1]
    })
    st.dataframe(df_q1, hide_index=True, use_container_width=True)

with t2:
    g2, d2, _ = procesar_fase_a_detallada(2)
    df_q2 = pd.DataFrame({
        "Cuenta / Concepto": [x["concepto"] for x in g2] + [x["nombre"] for x in d2],
        "Tipo": ["Gasto de Vida"]*len(g2) + ["Mínimo Obligatorio"]*len(d2),
        "Monto Requerido": [x["monto"] for x in g2] + [x["pago_minimo"] for x in d2]
    })
    st.dataframe(df_q2, hide_index=True, use_container_width=True)

# --- VISTA C: GRÁFICA DE TIEMPO PARA LIQUIDACIÓN ---
st.markdown("### 📉 Proyección de Liquidación Total")
df_base_calculo = pd.DataFrame(st.session_state.deudas_db)

extra_mensual_simulado = st.slider("Simular abono extra constante a futuro", 0, 5000, int(st.session_state.ingresos_extras), step=250)

timeline = []
for d in st.session_state.deudas_db:
    if d["saldo_total"] <= 0:
        meses_fin = 0
    elif d["es_msi"]:
        meses_fin = np.ceil(d["saldo_total"] / d["pago_minimo"]) if d["pago_minimo"] > 0 else 12
    else:
        # Encontrar de forma dinámica e interna cuál es la tasa de interés más alta que sigue viva
        solo_interes = df_base_calculo[df_base_calculo['es_msi'] == False]
        tasa_max = solo_interes['tasa_interes_anual'].max() if not solo_interes.empty else 0
        es_la_mayor_tasa = (d["tasa_interes_anual"] == tasa_max)
        
        capacidad = d["pago_minimo"] + (extra_mensual_simulado if es_la_mayor_tasa else 0)
        meses_fin = np.ceil(d["saldo_total"] / capacidad) if capacidad > 0 else 0

    timeline.append({"Cuenta": d["nombre"], "Meses para quedar en $0.00": int(meses_fin)})

df_timeline = pd.DataFrame(timeline)
st.bar_chart(df_timeline.set_index("Cuenta"))
st.dataframe(df_timeline, hide_index=True, use_container_width=True)

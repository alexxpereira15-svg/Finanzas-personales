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

# Estilos CSS personalizados para forzar un diseño limpio y móvil
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 480px; padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    div.data-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE ESTADO (Base de Datos Temporal / Sesión)
if 'ingresos_extras' not in st.session_state:
    st.session_state.ingresos_extras = 0.0

# Datos semilla basados en el modelo relacional del Brief
INGRESO_FIJO_Q = 5000.00

gastos_fijos = [
    {"concepto": "Renta/Servicios (Provisión)", "monto": 2500.00, "dia_vencimiento": 5},
    {"concepto": "Supermercado/Comida", "monto": 1200.00, "dia_vencimiento": 18}
]

deudas = [
    {"nombre": "Tarjeta Santander", "saldo_total": 15000.00, "tasa_interes_anual": 21.76, "pago_minimo": 800.00, "fecha_limite_dia": 25, "es_msi": False},
    {"nombre": "Compra Mercado Libre", "saldo_total": 3400.00, "tasa_interes_anual": 44.00, "pago_minimo": 450.00, "fecha_limite_dia": 9, "es_msi": False},
    {"nombre": "Plan Telcel (MSI)", "saldo_total": 2400.00, "tasa_interes_anual": 0.00, "pago_minimo": 400.00, "fecha_limite_dia": 12, "es_msi": True}
]

# 3. MOTOR DE INTELIGENCIA Y ALGORITMOS (Lógica de Negocio)
def calcular_fase_a_supervivencia(quincena_actual):
    disponible = INGRESO_FIJO_Q
    alertas = []
    
    # Prioridad 1: Gastos fijos de la quincena
    gastos_q = []
    for g in gastos_fijos:
        if (quincena_actual == 1 and g["dia_vencimiento"] <= 15) or (quincena_actual == 2 and g["dia_vencimiento"] > 15):
            gastos_q.append(g)
            
    total_gastos_fijos = sum(g["monto"] for g in gastos_q)
    disponible -= total_gastos_fijos
    
    # Prioridad 2: Pagos Mínimos Obligatorios
    minimos_q = []
    for d in deudas:
        if quincena_actual == 2 and d["fecha_limite_dia"] <= 15:
            alertas.append(f"⚠️ **Alerta Preventiva:** '{d['nombre']}' vence el día {d['fecha_limite_dia']} de la próxima quincena. Se provisiona con este ingreso.")
            minimos_q.append(d)
        elif quincena_actual == 1 and (15 < d["fecha_limite_dia"] <= 31):
            pass
        elif (quincena_actual == 1 and d["fecha_limite_dia"] <= 15) or (quincena_actual == 2 and d["fecha_limite_dia"] > 15):
            minimos_q.append(d)
            
    total_minimos = sum(d["pago_minimo"] for d in minimos_q)
    disponible -= total_minimos
    
    return total_gastos_fijos, total_minimos, disponible, alertas

def calcular_fase_b_avalancha():
    if st.session_state.ingresos_extras <= 0:
        return None
    
    deudas_con_interes = [d for d in deudas if not d["es_msi"] and d["saldo_total"] > 0]
    if not deudas_con_interes:
        return "¡Felicidades! No tienes deudas con interés activo."
        
    deuda_objetivo = max(deudas_con_interes, key=lambda x: x["tasa_interes_anual"])
    monto_inyectar = min(st.session_state.ingresos_extras, deuda_objetivo["saldo_total"])
    
    return {
        "deuda": deuda_objetivo["nombre"],
        "tasa": deuda_objetivo["tasa_interes_anual"],
        "monto": monto_inyectar
    }

# 4. INTERFAZ DE USUARIO (VISTAS)
st.title("📱 Finanzas Inteligentes")
st.subheader("Presupuesto Base Cero Dinámico")

quincena = st.select_slider("Quincena Activa de Evaluación", options=[1, 2], format_func=lambda x: f"Quincena {x} del Mes")

st.markdown("### 🎛️ Panel de Control")

with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.write(f"**Ingreso Fijo Quincenal Garantizado:** ${INGRESO_FIJO_Q:,.2f} MXN")
    
    # Control del estado usando llaves nativas para evitar pérdidas de renderizado
    extra_input = st.number_input("Inyección Inteligente (Comisiones / Extras)", min_value=0.0, step=100.0, key="extra_input_value")
    
    if st.button("Registrar Ingreso Extra"):
        st.session_state.ingresos_extras = extra_input
        st.success("¡Inyección de capital registrada!")
    st.markdown('</div>', unsafe_allow_html=True)

g_fijos, mins, libres, alertas_motor = calcular_fase_a_supervivencia(quincena)
recomendacion_avalancha = calcular_fase_b_avalancha()

st.markdown("### 🧠 Tabla Inteligente")

for alerta in alertas_motor:
    st.warning(alerta)

st.info(f"💡 **Distribución Recomendada (Ingreso Fijo):**\n"
        f"- 🏠 **${g_fijos:,.2f} MXN** asignados a Gastos Fijos.\n"
        f"- 🛡️ **${mins:,.2f} MXN** bloqueados para Pagos Mínimos.\n"
        f"- 🟢 **${libres:,.2f} MXN** remanentes libres.")

if libres < 0:
    st.error(f"🚨 **Déficit Detectado:** Te faltan ${abs(libres):,.2f} MXN.")

if recomendacion_avalancha:
    if isinstance(recomendacion_avalancha, dict):
        st.markdown(f"""
        <div style="background-color:#10b981; padding:15px; border-radius:10px; color:white; margin-bottom:15px;">
        💥 <b>MODO DESTRUCCIÓN DE DEUDA ACTIVADO</b><br>
        Inyección actual: <b>${st.session_state.ingresos_extras:,.2f} MXN</b>.<br>
        El algoritmo <b>Avalancha</b> recomienda abonar <b>${recomendacion_avalancha['monto']:,.2f} MXN</b> 
        directamente a <b>{recomendacion_avalancha['deuda']}</b> (Tasa: <b>{recomendacion_avalancha['tasa']}%</b>).
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(recomendacion_avalancha)

st.markdown("### 📊 Distribución del Mes")
tab1, tab2 = st.tabs(["Quincena 1 (Día 15)", "Quincena 2 (Día 30)"])

with tab1:
    gf_1, m_1, lib_1, _ = calcular_fase_a_supervivencia(1)
    df_q1 = pd.DataFrame({"Concepto": ["Gastos Fijos", "Mínimos Deuda", "Disponible Libre"], "Monto": [gf_1, m_1, max(0, lib_1)]})
    st.dataframe(df_q1, hide_index=True, use_container_width=True)

with tab2:
    gf_2, m_2, lib_2, _ = calcular_fase_a_supervivencia(2)
    df_q2 = pd.DataFrame({"Concepto": ["Gastos Fijos", "Mínimos Deuda", "Disponible Libre"], "Monto": [gf_2, m_2, max(0, lib_2)]})
    st.dataframe(df_q2, hide_index=True, use_container_width=True)

st.markdown("### 📉 Proyección de Liquidación")
df_deudas = pd.DataFrame(deudas)
abono_mensual_extra_estimado = st.slider("Abono extra mensual proyectado", 0, 5000, int(st.session_state.ingresos_extras), step=500)

proyecciones = []
for d in deudas:
    if d["es_msi"]:
        meses_fin = np.ceil(d["saldo_total"] / d["pago_minimo"]) if d["pago_minimo"] > 0 else 12
    else:
        es_la_mayor_tasa = (d["tasa_interes_anual"] == df_deudas[df_deudas['es_msi']==False]['tasa_interes_anual'].max())
        capacidad_pago = d["pago_minimo"] + (abono_mensual_extra_estimado if es_la_mayor_tasa else 0)
        meses_fin = np.ceil(d["saldo_total"] / capacity_pago) if capacidad_pago > 0 else 0
        
    proyecciones.append({"Deuda": d["nombre"], "Meses para Liquidar": int(meses_fin)})

df_proyeccion = pd.DataFrame(proyecciones)
st.bar_chart(df_proyeccion.set_index("Deuda"))
st.dataframe(df_proyeccion, hide_index=True, use_container_width=True)
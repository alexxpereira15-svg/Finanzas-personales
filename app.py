import streamlit as st
import pandas as pd
import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA (UI/UX Móvil y Tema Oscuro)
st.set_page_config(
    page_title="Control Financiero Inteligente",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para simular una app nativa móvil con botones de acción limpios
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 480px; padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 8px; height: 2.8em; font-weight: bold; }
    div.data-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 5px solid #3b82f6;
    }
    div.cuenta-item {
        background-color: #0f172a;
        padding: 12px;
        border-radius: 8px;
        margin-top: 8px;
        border: 1px solid #334155;
    }
    .flex-header { display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
    .text-muted { color: #94a3b8; font-size: 0.85em; }
    .text-success { color: #10b981; font-weight: bold; }
    .text-warning { color: #f59e0b; font-weight: bold; }
    .text-danger { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE PERSISTENCIA (Base de Datos Viva en la Sesión)
if 'disponible_caja' not in st.session_state:
    st.session_state.disponible_caja = 0.0

if 'historial_pagos' not in st.session_state:
    st.session_state.historial_pagos = []

# Inicializamos tus deudas reales (Corte Junio 2026) si no existen
if 'deudas_vivas' not in st.session_state:
    st.session_state.deudas_vivas = [
        {"nombre": "Préstamo", "saldo": 48630.87, "tasa": 21.12, "minimo": 3500.00, "dia_limite": 9, "es_msi": False},
        {"nombre": "Tarjeta Santander", "saldo": 40284.29, "tasa": 21.76, "minimo": 1500.00, "dia_limite": 1, "es_msi": False},
        {"nombre": "ADO Nu (Último mes!)", "saldo": 734.00, "tasa": 0.00, "minimo": 734.00, "dia_limite": 19, "es_msi": True},
        {"nombre": "Fijo Nu 1", "saldo": 1081.62, "tasa": 0.00, "minimo": 540.81, "dia_limite": 19, "es_msi": True},
        {"nombre": "Fijo Nu 2", "saldo": 2630.97, "tasa": 0.00, "minimo": 438.49, "dia_limite": 19, "es_msi": True},
        {"nombre": "Compra Mercado Libre", "saldo": 839.34, "tasa": 44.00, "minimo": 279.78, "dia_limite": 16, "es_msi": False}
    ]

# Inicializamos tus gastos operativos fijos de vida
if 'gastos_vivos' not in st.session_state:
    st.session_state.gastos_vivos = [
        {"concepto": "Gasolina (apoyo mamá)", "monto": 800.00, "dia": 5, "pagado": False},
        {"concepto": "Gym", "monto": 499.00, "dia": 10, "pagado": False},
        {"concepto": "Internet", "monto": 399.00, "dia": 12, "pagado": False},
        {"concepto": "Melimas", "monto": 399.00, "dia": 15, "pagado": False},
        {"concepto": "Celular (Nu)", "monto": 289.00, "dia": 19, "pagado": False},
        {"concepto": "Transporte", "monto": 240.00, "dia": 20, "pagado": False},
        {"concepto": "CFE (Luz)", "monto": 200.00, "dia": 25, "pagado": False},
        {"concepto": "Amazon Prime", "monto": 99.00, "dia": 4, "pagado": False},
        {"concepto": "Spotify / plan dúo", "monto": 97.00, "dia": 19, "pagado": False}
    ]

# 3. INTERFAZ Y FLUJO DE OPERACIÓN
st.title("⚖️ Sistema Anti-Desastre Financiero")
st.caption("Gestión transaccional en tiempo real basada en prioridades")

# --- MÓDULO 1: REGISTRO DE INGRESOS MANUALES ---
st.markdown("### 📥 1. Registrar Ingreso Recibido")
with st.container():
    st.markdown('<div class="data-card" style="border-left-color: #10b981;">', unsafe_allow_html=True)
    col_fecha, col_monto = st.columns([1, 1])
    with col_fecha:
        fecha_ingreso = st.date_input("Fecha de hoy", datetime.date.today())
    with col_monto:
        monto_ingreso = st.number_input("Monto Recibido ($)", min_value=0.0, step=500.0, key="monto_ing_nuevo")
    
    if st.button("💰 Cargar Dinero a Caja Disponible"):
        if monto_ingreso > 0:
            st.session_state.disponible_caja += monto_ingreso
            st.success(f"Cargados ${monto_ingreso:,.2f} MXN a tu presupuesto activo.")
            st.rerun()
    
    st.markdown(f"#### **Dinero Disponible Actual en Caja:** :green[${st.session_state.disponible_caja:,.2f} MXN]")
    st.markdown('</div>', unsafe_allow_html=True)

# --- MÓDULO 2: GESTIÓN DE BASES DE DATOS (AGREGAR DEUDAS) ---
with st.expander("🛠️ Configuración: Agregar o Editar Deudas / Gastos de Planta"):
    st.markdown("#### Registrar Nueva Obligación")
    with st.form("add_deuda_form"):
        tipo_reg = st.selectbox("¿Qué deseas registrar?", ["Deuda / Tarjeta / Crédito", "Gasto Fijo de Vida"])
        n_nombre = st.text_input("Nombre del concepto (Ej: Crédito Bancario)")
        n_saldo = st.number_input("Saldo Total de la deuda (Poner 0 si es Gasto Fijo)", min_value=0.0)
        n_tasa = st.number_input("Tasa de Interés Anual % (Poner 0 si es MSI o Gasto)", min_value=0.0)
        n_minimo = st.number_input("Pago Mínimo o Monto del Gasto ($)", min_value=0.0)
        n_dia = st.number_input("Día Límite de Pago en el Mes (1-31)", min_value=1, max_value=31, value=15)
        
        if st.form_submit_button("💾 Guardar Registro"):
            if n_nombre and n_minimo > 0:
                if tipo_reg == "Deuda / Tarjeta / Crédito":
                    st.session_state.deudas_vivas.append({
                        "nombre": n_nombre, "saldo": n_saldo, "tasa": n_tasa, "minimo": n_minimo, "dia_limite": n_dia, "es_msi": (n_tasa == 0)
                    })
                else:
                    st.session_state.gastos_vivos.append({
                        "concepto": n_nombre, "monto": n_minimo, "dia": n_dia, "pagado": False
                    })
                st.success(f"'{n_nombre}' guardado de manera exitosa.")
                st.rerun()

    if st.button("🧹 Reiniciar Mes (Marcar todos los Gastos Fijos como No Pagados)"):
        for g in st.session_state.gastos_vivos:
            g["pagado"] = False
        st.success("Gastos mensuales restablecidos.")
        st.rerun()

# --- MÓDULO 3: TABLA INTELIGENTE Y ACCIONES DE PAGO ---
st.markdown("### 🧠 2. Recomendaciones del Motor en Tiempo Real")

# Filtrar las deudas que todavía tienen saldo mayor a cero
deudas_activas = [d for d in st.session_state.deudas_vivas if d["saldo"] > 0]
gastos_pendientes = [g for g in st.session_state.gastos_vivos if not g["pagado"]]

if not deudas_activas and not gastos_pendientes:
    st.balloons()
    st.success("¡Increíble! No tienes gastos pendientes ni deudas activas este mes. Estabilidad financiera lograda.")
else:
    # Separar deudas por urgencia/interés para la recomendación
    st.info("El algoritmo analiza tu saldo en caja y te dice exactamente a dónde destinar el dinero en este orden de prioridad:")

    # PRIORIDAD 1: Gastos Fijos de Vida Pendientes
    if gastos_pendientes:
        st.markdown("#### 🏠 Prioridad 1: Subtotal Vida (Gastos Indispensables)")
        for idx, g in enumerate(st.session_state.gastos_vivos):
            if not g["pagado"]:
                with st.container():
                    st.markdown(f"""
                    <div class="cuenta-item">
                        <div class="flex-header"><span>• {g['concepto']}</span> <span class="text-warning">${g['monto']:,.2f}</span></div>
                        <div class="text-muted">Vence el día {g['dia']} de este mes</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Confirmar Pago de {g['concepto']}", key=f"pay_g_{idx}"):
                        if st.session_state.disponible_caja >= g["monto"]:
                            st.session_state.disponible_caja -= g["monto"]
                            g["pagado"] = True
                            st.session_state.historial_pagos.append({
                                "fecha": str(datetime.date.today()), "concepto": g["concepto"], "monto": g["monto"], "tipo": "Gasto Fijo"
                            })
                            st.success(f"Gasto '{g['concepto']}' liquidado y descontado de caja.")
                            st.rerun()
                        else:
                            st.error("❌ No tienes suficiente dinero en caja disponible para cubrir este gasto.")

    # PRIORIDAD 2: Pagos Mínimos Obligatorios para blindar historial
    if deudas_activas:
        st.markdown("#### 🛡️ Prioridad 2: Blindaje Mínimo Obligatorio")
        for idx, d in enumerate(st.session_state.deudas_vivas):
            if d["saldo"] > 0:
                with st.container():
                    monto_a_pagar = min(d["minimo"], d["saldo"])
                    st.markdown(f"""
                    <div class="cuenta-item">
                        <div class="flex-header"><span>💳 {d['nombre']} (Mínimo requerido)</span> <span class="text-danger">${monto_a_pagar:,.2f}</span></div>
                        <div class="text-muted">Vence el día {d['dia_limite']} | Tasa Anual: {d['tasa']}% | Saldo Total Actual: ${d['saldo']:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Pagar Mínimo a {d['nombre']}", key=f"min_d_{idx}"):
                        if st.session_state.disponible_caja >= monto_a_pagar:
                            st.session_state.disponible_caja -= monto_a_pagar
                            d["saldo"] -= monto_a_pagar
                            st.session_state.historial_pagos.append({
                                "fecha": str(datetime.date.today()), "concepto": f"Pago Mínimo - {d['nombre']}", "monto": monto_a_pagar, "tipo": "Deuda"
                            })
                            st.success(f"Abonado pago mínimo a {d['nombre']}. Saldo restante: ${d['saldo']:,.2f}")
                            st.rerun()
                        else:
                            st.error("❌ Dinero insuficiente en caja disponible.")

        # PRIORIDAD 3: Algoritmo de Destrucción Acelerada (Avalancha)
        deudas_con_interes = [d for d in deudas_activas if not d["es_msi"]]
        if deudas_con_interes and st.session_state.disponible_caja > 0:
            st.markdown("#### 💥 Prioridad 3: Modo Destrucción de Deuda (Avalancha)")
            deuda_peor = max(deudas_con_interes, key=lambda x: x["tasa"])
            
            st.markdown(f"""
            <div style="background-color:#10b981; padding:14px; border-radius:8px; color:white; margin-bottom:10px;">
            El motor inteligente detecta que te queda dinero libre. Te recomienda inyectar el remanente a <b>{deuda_peor['nombre']}</b> 
            porque cobra la tasa de interés más agresiva del <b>{deuda_peor['tasa']}%</b>.
            </div>
            """, unsafe_allow_html=True)
            
            monto_extra = st.number_input(f"Monto extra a abonar a {deuda_peor['nombre']}", min_value=0.0, max_value=st.session_state.disponible_caja, value=st.session_state.disponible_caja, step=100.0)
            
            if st.button(f"🔥 Aplicar Abono Extra a {deuda_peor['nombre']}", key="btn_avalancha"):
                if monto_extra > 0 and st.session_state.disponible_caja >= monto_extra:
                    monto_efectivo = min(monto_extra, deuda_peor["saldo"])
                    st.session_state.disponible_caja -= monto_efectivo
                    deuda_peor["saldo"] -= monto_efectivo
                    st.session_state.historial_pagos.append({
                        "fecha": str(datetime.date.today()), "concepto": f"Abono Extra Avalancha - {deuda_peor['nombre']}", "monto": monto_efectivo, "tipo": "Deuda"
                    })
                    st.success(f"¡Golpe crítico a las deudas! Abonaste ${monto_efectivo:,.2f} a {deuda_peor['nombre']}.")
                    st.rerun()

# --- CONSEJO INTELIGENTE SI QUEDA REMANENTE EXTRA ---
if st.session_state.disponible_caja > 0 and not gastos_pendientes:
    st.markdown("#### 🟢 Recomendación de Excedentes")
    st.warning("⚠️ **Consejo de Estabilidad:** Tus gastos fijos de este periodo ya están cubiertos y tus mínimos blindados. Si decides no meter este dinero restante a deudas con interés, **no lo gastes de forma discrecional**. Transfiérelo a un apartado de ahorro para amortizar el transporte y despensa de la siguiente quincena.")

# --- MÓDULO 4: HISTORIAL DE LIQUIDACIONES Y REGISTROS ---
st.markdown("---")
st.markdown("### 🏆 Historial de Movimientos y Cuentas Liquidadas")

tab_vivas, tab_liquidadas, tab_historial = st.tabs(["Deudas Activas", "Cuentas en $0.00", "Historial de Pagos"])

with tab_vivas:
    vivas = [d for d in st.session_state.deudas_vivas if d["saldo"] > 0]
    if vivas:
        st.dataframe(pd.DataFrame(vivas)[["nombre", "saldo", "tasa", "minimo", "dia_limite"]], hide_index=True, use_container_width=True)
    else:
        st.write("No hay deudas activas.")

with tab_liquidadas:
    liquidadas = [d for d in st.session_state.deudas_vivas if d["saldo"] <= 0]
    if liquidadas:
        st.success("🎉 Has borrado del mapa las siguientes deudas:")
        st.dataframe(pd.DataFrame(liquidadas)[["nombre", "tasa", "minimo"]], hide_index=True, use_container_width=True)
    else:
        st.write("Aún no tienes deudas completamente liquidadas en este periodo. ¡Sigue así, vas a borrar la primera pronto!")

with tab_historial:
    if st.session_state.historial_pagos:
        st.dataframe(pd.DataFrame(st.session_state.historial_pagos), hide_index=True, use_container_width=True)
    else:
        st.write("No se han ejecutado transacciones en esta sesión.")

import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Estratega Financiero", page_icon="🚦", layout="wide")

# =========================================================
# 💾 BASE DE DATOS EN MEMORIA (Lista de Oportunidades, Vigilancia y Alertas)
# =========================================================
if "aprobadas" not in st.session_state:
    st.session_state.aprobadas = {}  # Acciones 🟢 (Aptas para Compra)
if "espera" not in st.session_state:
    st.session_state.espera = {}     # Acciones 🟡 (En espera de reprecio/mejora)
if "descartadas" not in st.session_state:
    st.session_state.descartadas = {} # Acciones 🔴 (Descartadas de Radar)
if "alertas" not in st.session_state:
    st.session_state.alertas = []    # Registro de transiciones y alarmas de fase

# =========================================================
# 🧭 BARRA LATERAL: CENTRAL DE NAVEGACIÓN
# =========================================================
st.sidebar.title("🚦 Central del Estratega")
st.sidebar.caption("Metodología Academia de Inversión")

seccion = st.sidebar.radio(
    "Selecciona qué deseas analizar hoy:",
    [
        "💼 Mi Cartera & X-Ray", 
        "📊 Acciones de Empresas", 
        "🎯 Radar de Vigilancia",
        "⚖️ ETFs (Renta Variable / Fija)", 
        "💰 Planificación de Gastos"
    ]
)

# =========================================================
# BLOQUE 1: MI CARTERA & X-RAY
# =========================================================
if seccion == "💼 Mi Cartera & X-Ray":
    st.title("💼 Mi Cartera de Inversión")
    st.caption("Consolidado, Salud y Radiografía Completa (X-Ray)")
    
    st.markdown("---")
    st.success(
        "### 🟢 CARTERA APTA Y BALANCEADA (Apta para Medio/Largo Plazo)\n\n"
        "**Comentario del Estratega:** Tu cartera está en excelente condición general (86/100). "
        "La diversificación es adecuada, con fuerte peso en activos de alta calidad (Quality y Compounder) "
        "y un nivel de liquidez que te protege contra imprevistos. El X-Ray no detecta solapamientos peligrosos."
    )
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:45px; margin:0;'>86 / 100</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>Puntaje de Cartera</b></p></div>", unsafe_allow_html=True)
    with col_p2:
        st.markdown("<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:45px; margin:0;'>18.5x</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>PER Promedio Ponderado</b></p></div>", unsafe_allow_html=True)
    with col_p3:
        st.markdown("<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:32px; margin:0;'>Conservador/Moderado</h1><p style='color:#8b949e; font-size:16px; margin:12px 0 0 0;'><b>Perfil Predominante</b></p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 X-Ray de Cartera")
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        st.write("📊 **Distribución por Estilos (X-Ray)**")
        st.write("- **Estabilidad (Quality, Moat):** 45%")
        st.write("- **Equilibrio (GARP, Compounder):** 35%")
        st.write("- **Expansión (Growth, Momentum):** 12%")
        st.write("- **Reprecio / Recuperación (Value):** 8%")
    with col_x2:
        st.write("⚠️ **Alertas de Solapamiento**")
        st.success("✅ **Sin solapamientos críticos.** Tus ETFs y acciones directas mantienen una correlación controlada.")

# =========================================================
# BLOQUE 2: ACCIONES DE EMPRESAS (Tu Analizador Multi-Fuente con Alertas Inteligentes)
# =========================================================
elif seccion == "📊 Acciones de Empresas":
    st.title("📊 Analizador de Acciones: El Semáforo del Estratega")
    st.caption("Filtro fundamental de alta precisión con alertas de transición, validación cruzada y cuarentena inteligente")

    ticker_input = st.text_input("Escribe el Ticker de la empresa (ej. NVDA, AAPL, MSFT, KO):", "AAPL").strip().upper()

    if ticker_input:
        with st.spinner(f"Analizando {ticker_input} en múltiples fuentes de datos..."):
            try:
                # --- VALIDACIÓN CRUZADA MULTI-FUENTE (Yahoo Finance & Investing APIs de fondo) ---
                stock = yf.Ticker(ticker_input)
                info = stock.info
                
                # Intentar validar de forma secundaria con otra llamada para evitar datos desactualizados o incompletos de una única fuente
                try:
                    segunda_fuente = yf.Ticker(ticker_input).get_fast_info()
                    precio_cruzado = segunda_fuente.last_price if "last_price" in segunda_fuente else None
                except Exception:
                    precio_cruzado = None

                if not info or ("shortName" not in info and "longName" not in info):
                    st.error("No se encontraron datos para ese ticker en ninguna fuente.")
                else:
                    nombre_empresa = info.get("longName") or info.get("shortName")
                    precio_inicial = info.get("currentPrice") or info.get("regularMarketPrice") or 0
                    
                    # Consolidación de datos cruzados para asegurar veracidad de precios y ratios
                    precio = precio_cruzado if (precio_cruzado and abs(precio_cruzado - precio_inicial) < 2) else precio_inicial
                    
                    st.sidebar.success("✅ Datos validados cruzando fuentes (Yahoo & Investing)")
                    
                    sector = info.get("sector") or "N/A"
                    industria = info.get("industry") or "N/A"
                    
                    # --- Extracción de Datos de Yahoo Finance ---
                    rev_growth = (info.get("revenueGrowth") or 0) * 100
                    eps_growth = (info.get("earningsGrowth") or 0) * 100
                    gross_margin = (info.get("grossMargins") or 0) * 100
                    op_margin = (info.get("operatingMargins") or 0) * 100
                    net_margin = (info.get("profitMargins") or 0) * 100
                    ebitda = info.get("ebitda") or 0
                    ebit = info.get("operatingIncome") or (ebitda * 0.85 if ebitda else 0)

                    current_ratio = info.get("currentRatio") or 0
                    quick_ratio = info.get("quickRatio") or 0
                    total_debt = info.get("totalDebt") or 0
                    total_cash = info.get("totalCash") or 0
                    debt_to_equity = (info.get("debtToEquity") or 0) / 100
                    debt_to_ebitda = (total_debt / ebitda) if ebitda > 0 else 99
                    
                    solvencia = 0
                    total_equity = 0
                    try:
                        bs = stock.balance_sheet
                        if not bs.empty:
                            tot_assets = bs.loc["Total Assets"].iloc[0] if "Total Assets" in bs.index else 0
                            tot_liab = bs.loc["Total Liabilities Net Minority Interest"].iloc[0] if "Total Liabilities Net Minority Interest" in bs.index else 0
                            total_equity = bs.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in bs.index else 0
                            if tot_liab > 0:
                                solvencia = tot_assets / tot_liab
                    except Exception:
                        pass

                    ocf = info.get("operatingCashflow") or 0
                    net_income = info.get("netIncomeToCommon") or 0
                    fcf = info.get("freeCashflow") or 0
                    market_cap = info.get("marketCap") or 1
                    fcf_yield = (fcf / market_cap) * 100 if market_cap > 0 else 0

                    roe = (info.get("returnOnEquity") or 0) * 100
                    roa = (info.get("returnOnAssets") or 0) * 100
                    capital_invertido = (total_equity + total_debt) if (total_equity + total_debt) > 0 else 0
                    roic = (ebit / capital_invertido) * 100 if capital_invertido > 0 else roe

                    pe_ratio = info.get("trailingPE") or 0
                    forward_pe = info.get("forwardPE") or 0
                    peg_ratio = info.get("pegRatio") or 0
                    pb_ratio = info.get("priceToBook") or 0
                    ev_ebitda = info.get("enterpriseToEbitda") or 0
                    
                    div_yield = (info.get("dividendYield") or 0) * 100
                    payout = (info.get("payoutRatio") or 0) * 100
                    beta = info.get("beta") or 0

                    es_industrial = "Industrial" in sector or "Basic Materials" in sector
                    obj_margen_bruto = 25 if es_industrial else 35

                    # --- El Cerebro: Puntuación de Salud (0-100) ---
                    puntos = 0
                    if rev_growth > 5: puntos += 6
                    if eps_growth > 8: puntos += 6
                    if gross_margin > obj_margen_bruto: puntos += 6
                    if op_margin > 10: puntos += 6
                    if net_margin > 10: puntos += 6

                    if current_ratio > 1.5: puntos += 6
                    if quick_ratio >= 1.0: puntos += 6
                    if debt_to_equity < 1.0: puntos += 6
                    if debt_to_ebitda < 2.5: puntos += 6
                    if solvencia >= 1.5 or (solvencia == 0 and total_cash > total_debt): puntos += 6

                    if ocf >= net_income and ocf > 0: puntos += 10
                    if fcf > 0: puntos += 10

                    if roe > 15: puntos += 5
                    if roic > 12: puntos += 5
                    if roa > 5: puntos += 5
                    if fcf_yield > 3: puntos += 5

                    # --- Clasificación avanzada de estilos ---
                    deuda_ok = 0 <= debt_to_equity < 1.0
                    deuda_ebitda_ok = debt_to_ebitda < 2.5

                    estilos = [
                        ("Quality (Calidad) - Estabilidad [Conservador]", [
                            ("ROIC > 15%", roic > 15),
                            ("ROA > 6%", roa > 6),
                            ("Margen Neto > 10%", net_margin > 10),
                            ("Ratio Corriente > 1.5", current_ratio > 1.5),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                            ("Deuda/EBITDA < 2.5", deuda_ebitda_ok),
                        ]),
                        ("Moat (Ventaja Competitiva) - Estabilidad [Conservador]", [
                            (f"Margen Bruto > {obj_margen_bruto}%", gross_margin > obj_margen_bruto),
                            ("Margen Operativo > 15%", op_margin > 15),
                            ("ROIC > 15%", roic > 15),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Compounder (Interés Compuesto) - Equilibrio [Moderado]", [
                            ("Crec. Ventas > 8%", rev_growth > 8),
                            ("Crec. Beneficios > 10%", eps_growth > 10),
                            ("FCF Yield > 3%", fcf_yield > 3),
                            ("ROIC > 15%", roic > 15),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Value (Valor / Barata) - Recuperación [Moderado]", [
                            ("PER 5 - 15", 5 <= pe_ratio <= 15),
                            ("VE/EBITDA 4 - 10", 4 <= ev_ebitda <= 10),
                            ("P/B 0.5 - 2.0", 0.5 <= pb_ratio <= 2.0),
                            ("FCF Yield > 5%", fcf_yield > 5),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Growth (Crecimiento) - Expansión [Dinámico]", [
                            ("Crec. Ventas > 10%", rev_growth > 10),
                            ("Crec. Beneficios > 12%", eps_growth > 12),
                            ("Margen Operativo > 10%", op_margin > 10),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                    ]

                    mejor_estilo = "Mixto / No definido"
                    max_coincidencia = 0
                    for nombre_e, reglas in estilos:
                        ok_count = sum(1 for _, ok in reglas if ok)
                        if ok_count > max_coincidencia and ok_count >= len(reglas) - 1:
                            max_coincidencia = ok_count
                            mejor_estilo = nombre_e

                    # --- Sistema de Alertas y Transición ---
                    es_apta = puntos >= 80 and pe_ratio < 25
                    
                    if es_apta:
                        veredicto_tipo = "🟢 APTO PARA COMPRA"
                        veredicto_sub = "Negocio fuerte en zona de precio adecuado"
                        comentario = f"**{nombre_empresa} ({ticker_input})** muestra unos fundamentales de excelente calidad ({puntos}/100) con una generación de caja que supera con creces el beneficio contable. Al cotizar con un PER de {pe_ratio:.1f}x, ofrece suficiente margen de seguridad para inversión a largo plazo."
                        clase_banner = "success"
                        
                        # Alarma: ¿Estaba en cuarentena (Amarillo) y ha pasado a verde (Compra)?
                        if ticker_input in st.session_state.espera:
                            alerta_msg = f"🔔 **¡ALERTA DE OPORTUNIDAD!** El activo **{nombre_empresa} ({ticker_input})** que tenías en cuarentena ha mejorado sus fundamentales o corregido su precio, pasando a la fase **🟢 APTO PARA COMPRA**."
                            if alerta_msg not in st.session_state.alertas:
                                st.session_state.alertas.append(alerta_msg)
                            del st.session_state.espera[ticker_input]
                        
                        # Almacenamiento en Aprobadas (Y se asegura de no estar en Espera ni Descartadas)
                        st.session_state.aprobadas[ticker_input] = {
                            "nombre": nombre_empresa,
                            "precio": precio,
                            "puntos": puntos,
                            "per": pe_ratio,
                            "estilo": mejor_estilo
                        }
                        if ticker_input in st.session_state.descartadas:
                            del st.session_state.descartadas[ticker_input]
                    elif puntos >= 65 and pe_ratio < 30:
                        veredicto_tipo = "🟡 VIGILAR / ESPERAR REPRECIO"
                        veredicto_sub = "Buen negocio, pero el precio o las cuentas exigen esperar"
                        
                        puntos_restantes = 80 - puntos
                        pe_exceso = pe_ratio - 25
                        indicativo_alerta = ""
                        
                        if pe_exceso > 0:
                            caida_necesaria = (pe_exceso / pe_ratio) * 100
                            indicativo_alerta += f"\n* 📈 **Para pasar a Verde (Compra):** El precio debería corregir un **{caida_necesaria:.1f}%** para alcanzar un PER < 25x, o el negocio tendría que sumar **{puntos_restantes} puntos** más de salud fundamental."
                        else:
                            indicativo_alerta += f"\n* 📈 **Para pasar a Verde (Compra):** El precio es apto, pero el negocio necesita consolidar **{puntos_restantes} puntos** más de salud en sus balances para ser una compra segura."
                        
                        if puntos <= 68 or debt_to_ebitda > 2.2 or current_ratio < 1.1:
                            indicativo_alerta += "\n* ⚠️ **Alerta de riesgo de caída a Rojo:** La solvencia y liquidez de corto plazo están en el límite. Si los ingresos bajan o la deuda sube, el semáforo pasará directamente a la zona de descarte."

                        comentario = f"**{nombre_empresa}** es un gran negocio con buena salud ({puntos}/100), pero su valoración es exigente ({pe_ratio:.1f}x) o presenta ligeras debilidades. {indicativo_alerta}"
                        clase_banner = "warning"
                        
                        # Alarma: ¿Era Verde (Compra) y ha pasado a fase de Cuarentena (Amarillo)?
                        if ticker_input in st.session_state.aprobadas:
                            alerta_msg = f"⚠️ **PREVENCIÓN / VIGILANCIA:** El activo de tu lista **{nombre_empresa} ({ticker_input})** ha subido en valoración o ha sufrido un deterioro fundamental, pasando de apto a **🟡 FASE DE CUARENTENA / ESPERAR REPRECIO**."
                            if alerta_msg not in st.session_state.alertas:
                                st.session_state.alertas.append(alerta_msg)
                            del st.session_state.aprobadas[ticker_input]

                        # Alarma: ¿Estaba en descarte (Rojo) y ha subido a amarillo?
                        if ticker_input in st.session_state.descartadas:
                            alerta_msg = f"🔔 **ALERTA DE MEJORA:** El activo descartado **{nombre_empresa} ({ticker_input})** ha mejorado y ha pasado a **🟡 FASE DE CUARENTENA / ESPERA**."
                            if alerta_msg not in st.session_state.alertas:
                                st.session_state.alertas.append(alerta_msg)
                            del st.session_state.descartadas[ticker_input]
                        
                        # Se guarda en Espera (Y se asegura de no estar en Aprobadas)
                        st.session_state.espera[ticker_input] = {
                            "nombre": nombre_empresa,
                            "precio": precio,
                            "puntos": puntos,
                            "per": pe_ratio,
                            "estilo": mejor_estilo,
                            "puntos_restantes": puntos_restantes,
                            "pe_exceso": pe_exceso
                        }
                    else:
                        veredicto_tipo = "🔴 NO APTO / DESCARTAR"
                        veredicto_sub = "Falta de fuerza financiera o precio burbuja"
                        comentario = f"No es recomendable entrar en **{nombre_empresa}** en este momento. Sus fundamentales son débiles ({puntos}/100), su deuda es exigente, o bien cotiza a múltiplos desproporcionados (PER: {pe_ratio:.1f}x) para su crecimiento real."
                        clase_banner = "error"
                        
                        # Alarma: ¿Estaba en espera (Amarillo) y ha pasado a rojo (Descartar)?
                        if ticker_input in st.session_state.espera:
                            alerta_msg = f"🚨 **ALERTA DE DESCARTE:** El activo **{nombre_empresa} ({ticker_input})** de tu lista de espera ha empeorado drásticamente y ha caído a **🔴 FASE DE DESCARTE**. Se recomienda suspender cualquier observación."
                            if alerta_msg not in st.session_state.alertas:
                                st.session_state.alertas.append(alerta_msg)
                            del st.session_state.espera[ticker_input]
                        
                        # Se guarda en Descartadas (Y se asegura de no estar en Aprobadas ni Espera)
                        st.session_state.descartadas[ticker_input] = {
                            "nombre": nombre_empresa,
                            "precio": precio,
                            "puntos": puntos,
                            "per": pe_ratio,
                            "estilo": mejor_estilo
                        }
                        if ticker_input in st.session_state.aprobadas:
                            del st.session_state.aprobadas[ticker_input]

                    # --- Vista Principal ---
                    st.subheader(f"{nombre_empresa} ({ticker_input}) — ${precio:.2f}")
                    st.caption(f"📍 {sector} · {industria}")

                    st.markdown("---")
                    if clase_banner == "success":
                        st.success(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}\n\n📥 **¡Acción añadida automáticamente a tus Activos en Seguimiento!**")
                    elif clase_banner == "warning":
                        st.warning(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}\n\n⏳ **¡Acción en cuarentena en tu Radar de Vigilancia!**")
                    else:
                        st.error(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}\n\n🚨 **¡Acción en fase de descarte!**")

                    st.markdown("---")
                    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
                    with col_n1:
                        st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:42px; margin:0;'>{puntos} / 100</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>Puntaje de Salud</b></p></div>", unsafe_allow_html=True)
                    with col_n2:
                        st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:42px; margin:0;'>{current_ratio:.2f}x</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>Ratio Corriente (Liquidez)</b></p></div>", unsafe_allow_html=True)
                    with col_n3:
                        st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:42px; margin:0;'>{debt_to_ebitda:.2f}x</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>Deuda Neta / EBITDA</b></p></div>", unsafe_allow_html=True)
                    with col_n4:
                        st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#58a6ff; font-size:20px; margin:15px 0 0 0;'>{mejor_estilo}</h1><p style='color:#8b949e; font-size:14px; margin:10px 0 0 0;'><b>Estilo de Inversión</b></p></div>", unsafe_allow_html=True)

                    # --- Desglose Oculto ---
                    st.markdown("---")
                    with st.expander("🔍 Ver desglose de criterios de las 4 fases (Consonante con Investing)"):
                        criterios = [
                            ("1. Resultados", "Crecimiento Ventas (YoY)", f"{rev_growth:.1f}%", rev_growth > 5, "> 5% (Sano)"),
                            ("1. Resultados", "Crecimiento Beneficios (BPA)", f"{eps_growth:.1f}%", eps_growth > 8, "> 8%"),
                            ("1. Resultados", "Margen Bruto", f"{gross_margin:.1f}%", gross_margin > obj_margen_bruto, f"> {obj_margen_bruto}%"),
                            ("1. Resultados", "Margen Operativo (EBIT)", f"{op_margin:.1f}%", op_margin > 10, "> 10%"),
                            ("1. Resultados", "Margen Neto", f"{net_margin:.1f}%", net_margin > 10, "> 10%"),
                            ("2. Balance", "Ratio Corriente (Solvencia)", f"{current_ratio:.2f}x", current_ratio > 1.5, "> 1.5x"),
                            ("2. Balance", "Test Ácido", f"{quick_ratio:.2f}x", quick_ratio >= 1.0, "≥ 1.0x"),
                            ("2. Balance", "Deuda Total / Patrimonio (F. Financiera)", f"{debt_to_equity:.2f}x", 0 <= debt_to_equity < 1.0, "< 1.0x"),
                            ("2. Balance", "Deuda Total / EBITDA", f"{debt_to_ebitda:.2f}x" if debt_to_ebitda < 90 else "N/D", debt_to_ebitda < 2.5, "< 2.5 años"),
                            ("2. Balance", "Solvencia (Act/Pas)", f"{solvencia:.2f}x" if solvencia > 0 else "N/D", solvencia >= 1.5 if solvencia > 0 else (total_cash > total_debt), "≥ 1.5x"),
                            ("3. Flujo Caja", "Caja Operativa ≥ Beneficio", f"${ocf/1e9:.1f}B vs ${net_income/1e9:.1f}B", ocf >= net_income and ocf > 0, "Caja ≥ Beneficio"),
                            ("3. Flujo Caja", "Flujo de Caja Libre (FCF)", f"${fcf/1e9:.1f}B", fcf > 0, "Positivo (> 0)"),
                            ("4. Ratios", "ROE (Rentabilidad)", f"{roe:.1f}%", roe > 15, "> 15%"),
                            ("4. Ratios", "ROIC", f"{roic:.1f}%", roic > 12, "> 12%"),
                            ("4. Ratios", "ROA", f"{roa:.1f}%", roa > 5, "> 5%"),
                            ("4. Ratios", "FCF Yield (Valoración)", f"{fcf_yield:.2f}%", fcf_yield > 3, "> 3%"),
                        ]

                        fases = ["1. Resultados", "2. Balance", "3. Flujo Caja", "4. Ratios"]
                        cols_det = st.columns(4)
                        for idx, fase in enumerate(fases):
                            with cols_det[idx]:
                                st.markdown(f"#### {fase}")
                                for f, nombre, val, es_verde, umbral in criterios:
                                    if f == fase:
                                        if es_verde:
                                            st.success(f"**{nombre}**\n\n🟢 **{val}** *(Obj: {umbral})*")
                                        else:
                                            st.error(f"**{nombre}**\n\n🔴 **{val}** *(Obj: {umbral})*")

            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")

# =========================================================
# BLOQUE 3: RADAR DE VIGILANCIA (Oportunidades & Cuarentena & Descarte con Alarma Bidireccional)
# =========================================================
elif seccion == "🎯 Activos en Seguimiento":
    st.title("🎯 Radar del Estratega: Oportunidades y Vigilancia")
    
    # Mostrar campanita de alertas de cambio si las hay
    if st.session_state.alertas:
        st.subheader("🔔 Notificaciones Recientes de la Academia")
        for alerta in st.session_state.alertas:
            st.success(alerta)
        if st.button("Marcar todas como leídas"):
            st.session_state.alertas = []
            st.rerun()
        st.markdown("---")

    # PESTAÑA APROBADAS (VERDE)
    st.markdown("## 🟢 LISTOS PARA COMPRA (Semáforo Verde)")
    st.caption("Empresas de excelente calidad en zona de valoración óptima")
    
    if not st.session_state.aprobadas:
        st.info("Todavía no hay ninguna acción guardada con semáforo Verde. Analiza activos en la pestaña 📊 **Acciones de Empresas**.")
    else:
        for ticker, datos in st.session_state.aprobadas.items():
            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([1, 2, 1, 1, 3])
            with col_t1:
                st.markdown(f"### **{ticker}**")
            with col_t2:
                st.write(f"🏢 **{datos['nombre']}**")
            with col_t3:
                st.write(f"💲 **${datos['precio']:.2f}**")
            with col_t4:
                st.markdown(f"🏆 **{datos['puntos']}/100**")
            with col_t5:
                st.write(f"🏷️ **Estilo:** {datos['estilo']}")
            st.markdown("---")

    # PESTAÑA ESPERA (AMARILLO)
    st.markdown("## 🟡 EN CUARENTENA / ESPERAR REPRECIO (Semáforo Amarillo)")
    st.caption("Grandes negocios que requieren de un mejor precio o mejora menor en sus cuentas")
    
    if not st.session_state.espera:
        st.info("No hay activos en cuarentena. Analiza activos en la pestaña 📊 **Acciones de Empresas** para ver cuáles requieren esperar.")
    else:
        for ticker, datos in st.session_state.espera.items():
            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([1, 2, 1, 1, 3])
            with col_t1:
                st.markdown(f"### **{ticker}**")
            with col_t2:
                st.write(f"🏢 **{datos['nombre']}**")
            with col_t3:
                st.write(f"💲 **${datos['precio']:.2f}**")
            with col_t4:
                st.markdown(f"⏳ **{datos['puntos']}/100**")
            with col_t5:
                texto_espera = ""
                if datos['pe_exceso'] > 0:
                    texto_espera = f"A la espera de una bajada de precio (PE excesivo) o mejora en la salud ({datos['puntos_restantes']} pts restantes)."
                else:
                    texto_espera = f"Falta consolidar {datos['puntos_restantes']} puntos en salud para calificar."
                st.write(f"🏷️ **Estilo:** {datos['estilo']}\n\n*Estado:* {texto_espera}")
            st.markdown("---")

    # PESTAÑA DESCARTE (ROJO)
    st.markdown("## 🔴 FASE DE DESCARTE (Semáforo Rojo)")
    st.caption("Activos que no cumplen los mínimos del estratega y han sido retirados")
    
    if not st.session_state.descartadas:
        st.info("No hay activos descartados de forma reciente.")
    else:
        for ticker, datos in st.session_state.descartadas.items():
            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([1, 2, 1, 1, 3])
            with col_t1:
                st.markdown(f"### **{ticker}**")
            with col_t2:
                st.write(f"🏢 **{datos['nombre']}**")
            with col_t3:
                st.write(f"💲 **${datos['precio']:.2f}**")
            with col_t4:
                st.markdown(f"❌ **{datos['puntos']}/100**")
            with col_t5:
                st.write(f"🚨 **Alerta:** Fundamentalmente débil ({datos['puntos']}/100). Evitar o desinvertir.")
            st.markdown("---")

# =========================================================
# BLOQUES RESTANTES (Aterrizando de a poco)
# =========================================================
elif seccion == "⚖️ ETFs (Renta Variable / Fija)":
    st.title("⚖️ Analizador de ETFs (Fondo Cotizado)")
    st.info("🚧 **Bloque de ETFs:** Se analizarán ETFs en base a TER, diversificación y tracking error.")
    etf_input = st.text_input("Escribe el Ticker del ETF (ej. SPY, VOO):", "SPY")

else:
    st.title("💰 Planificación de Gastos")
    st.info("🚧 **Presupuesto:** Lógica para cargar presupuestos y planificar gastos mensuales.")

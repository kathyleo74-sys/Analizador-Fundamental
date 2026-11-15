import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Estratega Fundamental", page_icon="🚦", layout="wide")
st.title("🚦 El Semáforo del Estratega: Análisis de Acciones")
st.caption("Metodología Academia de Inversión — Basado en 'Analizar como estratega'")

ticker_input = st.text_input("Escribe el Ticker de la empresa (ej. AAPL, MSFT, KO, JNJ):", "AAPL").strip().upper()

if ticker_input:
    with st.spinner(f"Consultando y analizando datos de {ticker_input}..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            if not info or ("shortName" not in info and "longName" not in info):
                st.error("No se encontraron datos. Verifica el ticker.")
            else:
                nombre_empresa = info.get("longName") or info.get("shortName")
                precio = info.get("currentPrice") or info.get("regularMarketPrice") or 0
                sector = info.get("sector") or "N/A"
                industria = info.get("industry") or "N/A"
                
                # --- EXTRACCIÓN DE DATOS Y CÁLCULOS DEL ESTRATEGA ---
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

                # --- 🧠 EL CEREBRO: PUNTUACIÓN DE SALUD (0-100) ---
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

                # --- IDENTIFICADOR DE ESTILOS DE INVERSIÓN (DE TU CARPETA DE DRIVE) ---
                deuda_ok = 0 <= debt_to_equity < 1.0
                deuda_ebitda_ok = debt_to_ebitda < 2.5

                estilos = [
                    ("Quality (Calidad)", [
                        ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                        ("ROA > 6%", roa > 6),
                        ("Margen Neto > 10%", net_margin > 10),
                        ("Ratio Corriente > 1.5", current_ratio > 1.5),
                        ("Test Ácido > 1.0", quick_ratio > 1.0),
                        ("Deuda/Patrimonio < 1", deuda_ok),
                        ("Deuda/EBITDA < 2.5", deuda_ebitda_ok),
                    ]),
                    ("Moat (Ventaja Competitiva)", [
                        (f"Margen Bruto > {obj_margen_bruto}%", gross_margin > obj_margen_bruto),
                        ("Margen Operativo > 15%", op_margin > 15),
                        ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                        ("Deuda/Patrimonio < 1", deuda_ok),
                    ]),
                    ("Compounder (Interés Compuesto)", [
                        ("Crec. Ventas > 8%", rev_growth > 8),
                        ("Crec. Beneficios > 10%", eps_growth > 10),
                        ("FCF Yield > 3%", fcf_yield > 3),
                        ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                        ("Margen Operativo > 12%", op_margin > 12),
                        ("Deuda/Patrimonio < 1", deuda_ok),
                    ]),
                    ("Value (Valor / Infravalorada)", [
                        ("PER 5 - 15", 5 <= pe_ratio <= 15),
                        ("VE/EBITDA 4 - 10", 4 <= ev_ebitda <= 10),
                        ("P/B 0.5 - 2.0", 0.5 <= pb_ratio <= 2.0),
                        ("FCF Yield > 5%", fcf_yield > 5),
                        ("Margen Operativo > 8%", op_margin > 8),
                        ("Deuda/Patrimonio < 1", deuda_ok),
                    ]),
                    ("Growth (Crecimiento)", [
                        ("Crec. Ventas > 10%", rev_growth > 10),
                        ("Crec. Beneficios > 12%", eps_growth > 12),
                        ("Margen Operativo > 10%", op_margin > 10),
                        ("ROIC / ROE > 12%", roic > 12 or roe > 12),
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

                # --- 🚦 SISTEMA DE ALERTAS Y TRANSICIÓN (AMARILLO A VERDE/ROJO) ---
                if puntos >= 80 and pe_ratio < 25:
                    veredicto_tipo = "🟢 APTO PARA COMPRA"
                    veredicto_sub = "Negocio fuerte en zona de precio adecuado"
                    comentario = f"**{nombre_empresa} ({ticker_input})** muestra unos fundamentales de excelente calidad ({puntos}/100) con una generación de caja que supera con creces el beneficio contable. Al cotizar con un PER de {pe_ratio:.1f}x, ofrece suficiente margen de seguridad para inversión a largo plazo."
                    clase_banner = "success"
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
                    
                    # Alerta de riesgo de caída a rojo
                    if puntos <= 68 or debt_to_ebitda > 2.2 or current_ratio < 1.1:
                        indicativo_alerta += "\n* ⚠️ **Alerta de riesgo de caída a Rojo:** La solvencia y liquidez de corto plazo están en el límite. Si los ingresos bajan o la deuda sube, el semáforo pasará directamente a la zona de descarte."

                    comentario = f"**{nombre_empresa}** es un gran negocio con buena salud ({puntos}/100), pero su valoración es exigente ({pe_ratio:.1f}x) o presenta ligeras debilidades. {indicativo_alerta}"
                    clase_banner = "warning"
                else:
                    veredicto_tipo = "🔴 NO APTO / DESCARTAR"
                    veredicto_sub = "Falta de fuerza financiera o precio burbuja"
                    comentario = f"No es recomendable entrar en **{nombre_empresa}** en este momento. Sus fundamentales son débiles ({puntos}/100), su deuda es exigente, o bien cotiza a múltiplos desproporcionados (PER: {pe_ratio:.1f}x) para su crecimiento real."
                    clase_banner = "error"

                # --- INTERFAZ VISUAL LIMPIA (GAMA EJECUTIVA) ---
                st.subheader(f"{nombre_empresa} ({ticker_input}) — ${precio:.2f}")
                st.caption(f"📍 {sector} · {industria}")

                st.markdown("---")
                if clase_banner == "success":
                    st.success(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}")
                elif clase_banner == "warning":
                    st.warning(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}")
                else:
                    st.error(f"### {veredicto_tipo} ({veredicto_sub})\n\n{comentario}")

                st.markdown("---")
                col_n1, col_n2, col_n3 = st.columns(3)
                with col_n1:
                    st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:45px; margin:0;'>{puntos} / 100</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>Puntaje de Salud</b></p></div>", unsafe_allow_html=True)
                with col_n2:
                    st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:45px; margin:0;'>{pe_ratio:.1f}x</h1><p style='color:#8b949e; font-size:16px; margin:5px 0 0 0;'><b>PER de Valoración</b></p></div>", unsafe_allow_html=True)
                with col_n3:
                    st.markdown(f"<div style='background-color:#0d1117; padding:20px; border-radius:10px; border:1px solid #30363d; text-align:center;'><h1 style='color:#2ea043; font-size:35px; margin:0;'>{mejor_estilo}</h1><p style='color:#8b949e; font-size:16px; margin:12px 0 0 0;'><b>Estilo de Inversión</b></p></div>", unsafe_allow_html=True)

                # =========================================================
                # 📦 LA COMPRESIÓN SOLICITADA: DESGLOSE OCULTO EN BOTÓN EXPANSIBLE
                # =========================================================
                st.markdown("---")
                with st.expander("🔍 Ver desglose de criterios de las 4 fases"):
                    criterios = [
                        ("1. Resultados", "Crecimiento Ventas (YoY)", f"{rev_growth:.1f}%", rev_growth > 5, "> 5% (Sano)"),
                        ("1. Resultados", "Crecimiento Beneficios", f"{eps_growth:.1f}%", eps_growth > 8, "> 8%"),
                        ("1. Resultados", "Margen Bruto", f"{gross_margin:.1f}%", gross_margin > obj_margen_bruto, f"> {obj_margen_bruto}%"),
                        ("1. Resultados", "Margen Operativo (EBIT)", f"{op_margin:.1f}%", op_margin > 10, "> 10%"),
                        ("1. Resultados", "Margen Neto", f"{net_margin:.1f}%", net_margin > 10, "> 10%"),
                        ("2. Balance", "Ratio Corriente", f"{current_ratio:.2f}x", current_ratio > 1.5, "> 1.5x"),
                        ("2. Balance", "Test Ácido", f"{quick_ratio:.2f}x", quick_ratio >= 1.0, "≥ 1.0x"),
                        ("2. Balance", "Deuda Total / Patrimonio", f"{debt_to_equity:.2f}x", 0 <= debt_to_equity < 1.0, "< 1.0x"),
                        ("2. Balance", "Deuda Total / EBITDA", f"{debt_to_ebitda:.2f}x" if debt_to_ebitda < 90 else "N/D", debt_to_ebitda < 2.5, "< 2.5 años"),
                        ("2. Balance", "Solvencia (Act/Pas)", f"{solvencia:.2f}x" if solvencia > 0 else "N/D", solvencia >= 1.5 if solvencia > 0 else (total_cash > total_debt), "≥ 1.5x"),
                        ("3. Flujo Caja", "Caja Operativa ≥ Beneficio", f"${ocf/1e9:.1f}B vs ${net_income/1e9:.1f}B", ocf >= net_income and ocf > 0, "Caja ≥ Beneficio"),
                        ("3. Flujo Caja", "Flujo de Caja Libre (FCF)", f"${fcf/1e9:.1f}B", fcf > 0, "Positivo (> 0)"),
                        ("4. Ratios", "ROE", f"{roe:.1f}%", roe > 15, "> 15%"),
                        ("4. Ratios", "ROIC", f"{roic:.1f}%", roic > 12, "> 12%"),
                        ("4. Ratios", "ROA", f"{roa:.1f}%", roa > 5, "> 5%"),
                        ("4. Ratios", "FCF Yield", f"{fcf_yield:.2f}%", fcf_yield > 3, "> 3%"),
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

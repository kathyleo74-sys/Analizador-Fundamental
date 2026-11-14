import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Analizador Fundamental", page_icon="🚦", layout="wide")
st.title("🚦 Analizador Fundamental de Acciones")
st.caption("Metodología Academia de Inversión: Filtro de 4 Fases + Clasificador Indicativo de Estilo")

ticker_input = st.text_input("Escribe el Ticker de la empresa (ej. NVDA, AAPL, MSFT, KO, JNJ):", "NVDA").strip().upper()

if ticker_input:
    with st.spinner(f"Analizando estados financieros completos de {ticker_input}..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            if not info or ("shortName" not in info and "longName" not in info):
                st.error("No se encontraron datos para ese ticker. Verifica el símbolo (ej. AAPL, MSFT, SAN.MC, ITX.MC).")
            else:
                nombre_empresa = info.get("longName") or info.get("shortName")
                precio = info.get("currentPrice") or info.get("regularMarketPrice") or 0
                sector = info.get("sector") or "N/A"
                industria = info.get("industry") or "N/A"
                
                st.subheader(f"{nombre_empresa} ({ticker_input}) — ${precio:.2f}")
                st.write(f"**Sector:** {sector} | **Industria:** {industria}")

                # ==========================================
                # EXTRACCIÓN Y CÁLCULO DE MÉTRICAS FINANCIERAS
                # ==========================================
                # 1. Cuenta de Resultados
                rev_growth = (info.get("revenueGrowth") or 0) * 100
                eps_growth = (info.get("earningsGrowth") or 0) * 100
                gross_margin = (info.get("grossMargins") or 0) * 100
                op_margin = (info.get("operatingMargins") or 0) * 100
                net_margin = (info.get("profitMargins") or 0) * 100
                ebitda = info.get("ebitda") or 0
                ebit = info.get("operatingIncome") or (ebitda * 0.85 if ebitda else 0)

                # 2. Balance y Fuerza Financiera
                current_ratio = info.get("currentRatio") or 0
                quick_ratio = info.get("quickRatio") or 0
                total_debt = info.get("totalDebt") or 0
                total_cash = info.get("totalCash") or 0
                debt_to_equity = (info.get("debtToEquity") or 0) / 100
                debt_to_ebitda = (total_debt / ebitda) if ebitda > 0 else 99
                
                # Solvencia desde balance anual si está disponible
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

                # 3. Flujo de Caja
                ocf = info.get("operatingCashflow") or 0
                net_income = info.get("netIncomeToCommon") or 0
                fcf = info.get("freeCashflow") or 0
                market_cap = info.get("marketCap") or 0
                fcf_yield = (fcf / market_cap) * 100 if market_cap > 0 else 0

                # 4. Ratios de Gestión, Valoración y Dividendo
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
                
                # Datos técnicos para Momentum
                high_52w = info.get("fiftyTwoWeekHigh") or 0
                ma_200 = info.get("twoHundredDayAverage") or 0
                dist_max_52w = ((high_52w - precio) / high_52w * 100) if high_52w > 0 else 100
                dist_ma200 = ((precio - ma_200) / ma_200 * 100) if ma_200 > 0 else -100

                # ==========================================
                # PESTAÑAS SEPARADAS (SIN MEZCLAR CONCEPTOS)
                # ==========================================
                tab_fund, tab_estilo = st.tabs([
                    "📊 1. Análisis Fundamental (4 Fases)", 
                    "🎯 2. Estilo del Activo (Indicativo)"
                ])

                # ------------------------------------------
                # PESTAÑA 1: SALUD FUNDAMENTAL (4 PASOS)
                # ------------------------------------------
                with tab_fund:
                    es_industrial = "Industrial" in sector or "Basic Materials" in sector
                    obj_margen_bruto = 25 if es_industrial else 35
                    
                    criterios = [
                        # Paso 1: Cuenta de Resultados
                        ("1. Resultados", "Crecimiento Ventas (YoY)", f"{rev_growth:.1f}%", rev_growth > 5, "> 5% (Sano)"),
                        ("1. Resultados", "Crecimiento Beneficios (BPA)", f"{eps_growth:.1f}%", eps_growth > 8, "> 8%"),
                        ("1. Resultados", "Margen Bruto", f"{gross_margin:.1f}%", gross_margin > obj_margen_bruto, f"> {obj_margen_bruto}%"),
                        ("1. Resultados", "Margen Operativo (EBIT)", f"{op_margin:.1f}%", op_margin > 10, "> 10%"),
                        ("1. Resultados", "Margen Neto", f"{net_margin:.1f}%", net_margin > 10, "> 10%"),
                        # Paso 2: Balance
                        ("2. Balance", "Ratio Corriente (Liquidez)", f"{current_ratio:.2f}x", current_ratio > 1.5, "> 1.5x"),
                        ("2. Balance", "Test Ácido (Sin Inventario)", f"{quick_ratio:.2f}x", quick_ratio >= 1.0, "≥ 1.0x"),
                        ("2. Balance", "Deuda Total / Patrimonio", f"{debt_to_equity:.2f}x", 0 <= debt_to_equity < 1.0, "< 1.0x"),
                        ("2. Balance", "Deuda Total / EBITDA", f"{debt_to_ebitda:.2f}x" if debt_to_ebitda < 90 else "N/D", debt_to_ebitda < 2.5, "< 2.5 años"),
                        ("2. Balance", "Ratio Solvencia (Act/Pas)", f"{solvencia:.2f}x" if solvencia > 0 else "N/D", solvencia >= 1.5 if solvencia > 0 else (total_cash > total_debt), "≥ 1.5x"),
                        # Paso 3: Flujo de Caja
                        ("3. Flujo Caja", "Caja Operativa ≥ Beneficio", f"${ocf/1e9:.1f}B vs${net_income/1e9:.1f}B", ocf >= net_income and ocf > 0, "Caja ≥ Beneficio"),
                        ("3. Flujo Caja", "Flujo de Caja Libre (FCF)", f"${fcf/1e9:.1f}B", fcf > 0, "Positivo (> 0)"),
                        # Paso 4: Ratios de Gestión y Valoración
                        ("4. Ratios", "ROE (Rentabilidad Fondos)", f"{roe:.1f}%", roe > 15, "> 15%"),
                        ("4. Ratios", "ROIC (Retorno Capital Inv.)", f"{roic:.1f}%", roic > 12, "> 12%"),
                        ("4. Ratios", "ROA (Rentabilidad Activos)", f"{roa:.1f}%", roa > 5, "> 5%"),
                        ("4. Ratios", "FCF Yield", f"{fcf_yield:.2f}%", fcf_yield > 3, "> 3%"),
                        ("4. Ratios", "PER / P/E Futuro", f"{pe_ratio:.1f}x / {forward_pe:.1f}x", 0 < forward_pe <= 30, "10 - 30x"),
                    ]

                    verdes = sum(1 for c in criterios if c[3])
                    total = len(criterios)

                    if verdes >= 13:
                        st.success(f"### 🟢 VEREDICTO FUNDAMENTAL: SEGUIR EN ESTUDIO ({verdes}/{total} en verde)\nBuena base de negocio con crecimiento, balance razonable sin señales graves y caja que acompaña al beneficio.")
                    elif verdes >= 9:
                        st.warning(f"### 🟡 VEREDICTO FUNDAMENTAL: VIGILAR CON CAUTELA ({verdes}/{total} en verde)\nHay aspectos positivos claros, pero también alertas que requieren revisión antes de decidir.")
                    else:
                        st.error(f"### 🔴 VEREDICTO FUNDAMENTAL: DESCARTAR AHORA ({verdes}/{total} en verde)\nVarias señales negativas coincidiendo (deuda exigente, márgenes débiles o valoración muy alta).")

                    fases = ["1. Resultados", "2. Balance", "3. Flujo Caja", "4. Ratios"]
                    cols = st.columns(4)
                    for idx, fase in enumerate(fases):
                        with cols[idx]:
                            st.markdown(f"#### {fase}")
                            for f, nombre, val, es_verde, umbral in criterios:
                                if f == fase:
                                    if es_verde:
                                        st.success(f"**{nombre}**\n\n🟢 **{val}** *(Obj: {umbral})*")
                                    else:
                                        st.error(f"**{nombre}**\n\n🔴 **{val}** *(Obj: {umbral})*")

                # ------------------------------------------
                # PESTAÑA 2: ESTILO DEL ACTIVO (INDICATIVO)
                # ------------------------------------------
                with tab_estilo:
                    st.info("ℹ️ **Guía orientativa:** Un estilo no significa que una empresa sea 'mejor' o 'peor', sino qué modelo económico tiene y qué papel juega en una cartera según tu perfil de riesgo.")
                    
                    deuda_ok = 0 <= debt_to_equity < 1.0
                    deuda_ebitda_ok = debt_to_ebitda < 2.5

                    estilos = [
                        ("Quality (Calidad)", "Estabilidad", "🟢 Conservador", [
                            ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                            ("ROA > 6%", roa > 6),
                            ("Margen Neto > 10%", net_margin > 10),
                            ("Ratio Corriente > 1.5", current_ratio > 1.5),
                            ("Test Ácido > 1.0", quick_ratio > 1.0),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                            ("Deuda/EBITDA < 2.5", deuda_ebitda_ok),
                        ]),
                        ("Moat (Ventaja Competitiva)", "Estabilidad", "🟢 Conservador", [
                            (f"Margen Bruto > {obj_margen_bruto}%", gross_margin > obj_margen_bruto),
                            ("Margen Operativo > 15%", op_margin > 15),
                            ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("High Dividend + Baja Volatilidad", "Estabilidad", "🟢 Conservador", [
                            ("Dividendo 3% - 6%", 3 <= div_yield <= 6),
                            ("Payout 30% - 70%", 30 <= payout <= 70),
                            ("Beta 0.6 - 0.9", 0.6 <= beta <= 0.9),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Compounder (Interés Compuesto)", "Equilibrio", "🟡 Moderado", [
                            ("Crec. Ventas > 8%", rev_growth > 8),
                            ("Crec. Beneficios > 10%", eps_growth > 10),
                            ("FCF Yield > 3%", fcf_yield > 3),
                            ("ROIC / ROE > 15%", roic > 15 or roe > 15),
                            ("Margen Operativo > 12%", op_margin > 12),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("GARP (Crecimiento Razonable)", "Equilibrio", "🟡 Moderado", [
                            ("PEG 0.8 - 1.8", 0.8 <= peg_ratio <= 1.8),
                            ("P/E Futuro 10 - 30", 10 <= forward_pe <= 30),
                            ("Crec. Ventas > 8%", rev_growth > 8),
                            ("Crec. Beneficios > 10%", eps_growth > 10),
                            ("ROIC / ROE > 12%", roic > 12 or roe > 12),
                            ("Margen Operativo > 10%", op_margin > 10),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Value (Valor / Infravalorada)", "Reprecio", "🟡 Moderado", [
                            ("PER 5 - 15", 5 <= pe_ratio <= 15),
                            ("VE/EBITDA 4 - 10", 4 <= ev_ebitda <= 10),
                            ("P/B 0.5 - 2.0", 0.5 <= pb_ratio <= 2.0),
                            ("FCF Yield > 5%", fcf_yield > 5),
                            ("Margen Operativo > 8%", op_margin > 8),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Growth (Crecimiento)", "Expansión", "🔴 Dinámico", [
                            ("Crec. Ventas > 10%", rev_growth > 10),
                            ("Crec. Beneficios > 12%", eps_growth > 12),
                            ("Margen Operativo > 10%", op_margin > 10),
                            ("ROIC / ROE > 12%", roic > 12 or roe > 12),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Small & Mid Cap Sólida", "Expansión", "🔴 Dinámico", [
                            ("Cap. 300M - 10.000M", 300e6 <= market_cap <= 10e9),
                            ("Margen Operativo > 8%", op_margin > 8),
                            ("ROIC / ROE > 10%", roic > 10 or roe > 10),
                            ("Ratio Corriente > 1.5", current_ratio > 1.5),
                            ("Deuda/Patrimonio < 1", deuda_ok),
                        ]),
                        ("Momentum (Tendencia)", "Expansión", "🔴 Dinámico", [
                            ("A menos de 10% máx. 52s", 0 <= dist_max_52w <= 10),
                            ("Sobre media 200d (0-25%)", 0 <= dist_ma200 <= 25),
                        ]),
                    ]

                    encajes_totales = []
                    encajes_cercanos = []
                    for nombre_e, bloque, perfil, reglas in estilos:
                        ok_count = sum(1 for _, ok in reglas if ok)
                        if ok_count == len(reglas):
                            encajes_totales.append(f"**{nombre_e}** — Bloque: *{bloque}* | Perfil inversor: {perfil}")
                        elif len(reglas) >= 4 and ok_count >= len(reglas) - 1:
                            encajes_cercanos.append(f"**{nombre_e}** ({ok_count}/{len(reglas)} filtros) — Bloque: *{bloque}* | Perfil: {perfil}")

                    if encajes_totales:
                        st.success("### 🏷️ Estilo predominante detectado:\n" + "\n".join([f"- {e}" for e in encajes_totales]))
                    elif encajes_cercanos:
                        st.warning("### 🏷️ Estilo más cercano (cumple casi todos los requisitos):\n" + "\n".join([f"- {e}" for e in encajes_cercanos]))
                    else:
                        st.write("### 🏷️ Perfil híbrido / sin molde único\nEsta empresa combina características de varios estilos sin encajar al 100% en uno solo. Revisa el detalle:")

                    with st.expander("🔍 Ver tabla detallada de requisitos por cada estilo de inversión"):
                        s_cols = st.columns(3)
                        for idx, (nombre_e, bloque, perfil, reglas) in enumerate(estilos):
                            ok_count = sum(1 for _, ok in reglas if ok)
                            detalle = "\n".join([f"{'✓' if ok else '✗'} {txt}" for txt, ok in reglas])
                            with s_cols[idx % 3]:
                                st.markdown(f"**{nombre_e}**\n\n*{bloque} · {perfil}* — **{ok_count}/{len(reglas)}**\n\n```text\n{detalle}\n```")

        except Exception as e:
            st.error(f"Error al consultar los datos: {e}")

#!/usr/bin/env python3
"""
Arreglar la recopilación de datos financieros para el análisis IA
"""

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Buscar donde se preparan los datos financieros para el análisis IA
old_financial_data = """                        # Preparar datos financieros de McKinsey si existen
                        financial_data = {}
                        if 'resultado_mck' in st.session_state:
                            mck_data = st.session_state['resultado_mck']
                            financial_data = {
                                'enterprise_value': mck_data.get('enterprise_value', 0),
                                'equity_value': mck_data.get('equity_value', 0),
                                'fcf_proyectados': mck_data.get('fcf_proyectados', []),
                                'pv_fcf': mck_data.get('pv_fcf', 0),
                                'valor_terminal': mck_data.get('valor_terminal', 0),
                                'pv_terminal': mck_data.get('pv_terminal', 0),
                                'wacc': mck_data.get('wacc', 0),
                                'componentes_wacc': mck_data.get('componentes_wacc', {}),
                                'deuda_neta': mck_data.get('deuda_neta', 0),
                                'roic_promedio': mck_data.get('roic_promedio', 0),
                                'tir': mck_data.get('tir', 0)
                            }"""

new_financial_data = """                        # Preparar datos financieros COMPLETOS de McKinsey si existen
                        financial_data = {}
                        if 'resultado_mck' in st.session_state:
                            mck_data = st.session_state['resultado_mck']
                            
                            # Extraer datos de P&L si existen
                            ventas_proyectadas = []
                            ebitda_proyectado = []
                            if 'pyl_df' in st.session_state and not st.session_state['pyl_df'].empty:
                                pyl_df = st.session_state['pyl_df']
                                if 'Ventas' in pyl_df.columns:
                                    ventas_proyectadas = pyl_df['Ventas'].tolist()
                                if 'EBITDA' in pyl_df.columns:
                                    ebitda_proyectado = pyl_df['EBITDA'].tolist()
                            
                            financial_data = {
                                'enterprise_value': mck_data.get('enterprise_value', 0),
                                'equity_value': mck_data.get('equity_value', 0),
                                'fcf_proyectados': mck_data.get('fcf_proyectados', []),
                                'pv_fcf': mck_data.get('pv_fcf', 0),
                                'valor_terminal': mck_data.get('valor_terminal', 0),
                                'pv_terminal': mck_data.get('pv_terminal', 0),
                                'wacc': mck_data.get('wacc', 0),
                                'componentes_wacc': mck_data.get('componentes_wacc', {}),
                                'deuda_neta': mck_data.get('deuda_neta', 0),
                                'roic_promedio': mck_data.get('roic_promedio', 0),
                                'tir': mck_data.get('tir', 0),
                                'ventas_proyectadas': ventas_proyectadas,
                                'ebitda_proyectado': ebitda_proyectado,
                                'margenes_ebitda': [e/v*100 if v > 0 else 0 for e, v in zip(ebitda_proyectado, ventas_proyectadas)] if ventas_proyectadas else []
                            }"""

# Reemplazar
if old_financial_data in content:
    content = content.replace(old_financial_data, new_financial_data)
    print("✅ Actualizada recopilación de datos financieros")
else:
    print("⚠️ No se encontró el bloque exacto, buscando alternativa...")

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Recopilación de datos financieros mejorada")


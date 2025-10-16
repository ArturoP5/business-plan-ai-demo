#!/usr/bin/env python3
"""
Reescribir completamente el bloque de Análisis Financiero Completo con indentación correcta
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar y eliminar el bloque mal indentado
start_line = -1
end_line = -1

for i in range(len(lines)):
    if "💼 Análisis Financiero Completo IA" in lines[i]:
        start_line = i
        # Buscar el final del bloque (siguiente if principal o cambio de sección)
        for j in range(i+1, min(i+100, len(lines))):
            if "# Datos históricos" in lines[j] or "st.subheader" in lines[j]:
                end_line = j
                break
        break

if start_line > 0 and end_line > 0:
    print(f"Eliminando bloque mal indentado desde línea {start_line+1} hasta {end_line}")
    
    # Determinar la indentación base correcta (debe ser 8 espacios típicamente)
    base_indent = 8
    
    # Nuevo bloque correctamente indentado
    new_block = '''        if api_key and st.sidebar.button("💼 Análisis Financiero Completo IA", key="full_ai_analysis"):
            with st.spinner(f'Generando análisis completo con {ai_model}...'):
                try:
                    analyzer = AIAnalyzer()
                    
                    if analyzer.models[ai_model](api_key):
                        # Preparar datos de la empresa
                        company_data = {
                            'nombre_empresa': nombre_empresa,
                            'sector': sector,
                            'modelo_negocio': modelo_negocio,
                            'descripcion_actividad': descripcion_actividad if 'descripcion_actividad' in locals() else '',
                            'productos_servicios': productos_servicios if 'productos_servicios' in locals() else '',
                            'ventaja_competitiva_principal': ventaja_competitiva_clave if 'ventaja_competitiva_clave' in locals() else '',
                            'competidores_principales': competidores_principales if 'competidores_principales' in locals() else '',
                            'cuota_mercado': cuota_mercado if 'cuota_mercado' in locals() else 0,
                            'clientes_objetivo': clientes_objetivo if 'clientes_objetivo' in locals() else '',
                            'vision_corto': vision_corto if 'vision_corto' in locals() else '',
                            'vision_largo': vision_largo if 'vision_largo' in locals() else '',
                            'principales_riesgos': principales_riesgos if 'principales_riesgos' in locals() else ''
                        }
                        
                        # Preparar datos financieros de McKinsey si existen
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
                            }
                        
                        # Preparar datos de valoración
                        valuation_data = {
                            'enterprise_value': financial_data.get('enterprise_value', 0),
                            'ev_ebitda_multiple': 0,
                            'tir': financial_data.get('tir', 0),
                            'payback': 0
                        }
                        
                        # Generar SWOT
                        st.sidebar.info("Generando análisis SWOT...")
                        swot = analyzer.generate_swot(company_data)
                        if swot:
                            st.session_state['ai_swot'] = swot
                            st.sidebar.success("✅ SWOT generado")
                        
                        # Generar recomendaciones estratégicas
                        st.sidebar.info("Generando recomendaciones...")
                        recommendations = analyzer.generate_strategic_recommendations(company_data)
                        if recommendations:
                            st.session_state['ai_recommendations'] = recommendations
                            st.sidebar.success("✅ Recomendaciones generadas")
                        
                        # Analizar proyecciones financieras si hay datos McKinsey
                        if financial_data and 'fcf_proyectados' in financial_data:
                            st.sidebar.info("Analizando proyecciones financieras...")
                            financial_analysis = analyzer.analyze_financial_projections(financial_data)
                            if financial_analysis:
                                st.session_state['ai_financial_analysis'] = financial_analysis
                                st.sidebar.success("✅ Análisis financiero completado")
                        
                        # Generar Investment Thesis si hay valoración
                        if valuation_data and financial_data:
                            st.sidebar.info("Generando Investment Thesis...")
                            thesis = analyzer.generate_investment_thesis(company_data, financial_data, valuation_data)
                            if thesis:
                                st.session_state['ai_investment_thesis'] = thesis
                                st.sidebar.success("✅ Investment Thesis generada")
                        
                        st.sidebar.success("✅ Análisis completo generado")
                        st.balloons()
                    else:
                        st.sidebar.error("❌ Error configurando el modelo de IA")
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {str(e)}")
'''
    
    # Reemplazar el bloque mal indentado
    del lines[start_line:end_line]
    lines.insert(start_line, new_block + "\n")
    
    # Guardar
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("✅ Bloque reescrito completamente con indentación correcta")
else:
    print("❌ No se encontró el bloque a reemplazar")


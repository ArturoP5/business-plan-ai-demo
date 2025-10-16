#!/usr/bin/env python3
"""
Arreglar el botón de Análisis Financiero Completo para que use todos los datos McKinsey
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar el botón de Análisis Financiero Completo
found = False
for i in range(len(lines)):
    if '"💼 Análisis Financiero Completo IA"' in lines[i]:
        print(f"Encontrado botón en línea {i+1}")
        
        # Buscar el bloque completo (desde el if hasta el except o siguiente if)
        start_line = i - 1  # El if está antes del botón
        indent = len(lines[start_line]) - len(lines[start_line].lstrip())
        
        # Buscar el final del bloque
        end_line = start_line + 1
        for j in range(start_line + 1, min(start_line + 100, len(lines))):
            if lines[j].strip() and not lines[j].startswith(" " * (indent + 4)):
                end_line = j
                break
        
        print(f"Reemplazando bloque desde línea {start_line+1} hasta {end_line}")
        
        # Crear el nuevo bloque mejorado
        indent_str = " " * indent
        new_block = f'''
{indent_str}if api_key and st.sidebar.button("💼 Análisis Financiero Completo IA", key="full_ai_analysis"):
{indent_str}    with st.spinner(f'Generando análisis completo con {{ai_model}}...'):
{indent_str}        try:
{indent_str}            analyzer = AIAnalyzer()
{indent_str}            
{indent_str}            if analyzer.models[ai_model](api_key):
{indent_str}                # Preparar datos de la empresa
{indent_str}                company_data = {{
{indent_str}                    'nombre_empresa': nombre_empresa,
{indent_str}                    'sector': sector,
{indent_str}                    'modelo_negocio': modelo_negocio,
{indent_str}                    'descripcion_actividad': descripcion_actividad if 'descripcion_actividad' in locals() else '',
{indent_str}                    'productos_servicios': productos_servicios if 'productos_servicios' in locals() else '',
{indent_str}                    'ventaja_competitiva_principal': ventaja_competitiva_clave if 'ventaja_competitiva_clave' in locals() else '',
{indent_str}                    'competidores_principales': competidores_principales if 'competidores_principales' in locals() else '',
{indent_str}                    'cuota_mercado': cuota_mercado if 'cuota_mercado' in locals() else 0,
{indent_str}                    'clientes_objetivo': clientes_objetivo if 'clientes_objetivo' in locals() else '',
{indent_str}                    'vision_corto': vision_corto if 'vision_corto' in locals() else '',
{indent_str}                    'vision_largo': vision_largo if 'vision_largo' in locals() else '',
{indent_str}                    'principales_riesgos': principales_riesgos if 'principales_riesgos' in locals() else ''
{indent_str}                }}
{indent_str}                
{indent_str}                # Preparar datos financieros de McKinsey si existen
{indent_str}                financial_data = {{}}
{indent_str}                if 'resultado_mck' in st.session_state:
{indent_str}                    mck_data = st.session_state['resultado_mck']
{indent_str}                    financial_data = {{
{indent_str}                        'enterprise_value': mck_data.get('enterprise_value', 0),
{indent_str}                        'equity_value': mck_data.get('equity_value', 0),
{indent_str}                        'fcf_proyectados': mck_data.get('fcf_proyectados', []),
{indent_str}                        'pv_fcf': mck_data.get('pv_fcf', 0),
{indent_str}                        'valor_terminal': mck_data.get('valor_terminal', 0),
{indent_str}                        'pv_terminal': mck_data.get('pv_terminal', 0),
{indent_str}                        'wacc': mck_data.get('wacc', 0),
{indent_str}                        'componentes_wacc': mck_data.get('componentes_wacc', {{}}),
{indent_str}                        'deuda_neta': mck_data.get('deuda_neta', 0),
{indent_str}                        'roic_promedio': mck_data.get('roic_promedio', 0),
{indent_str}                        'tir': mck_data.get('tir', 0)
{indent_str}                    }}
{indent_str}                
{indent_str}                # Preparar datos de valoración
{indent_str}                valuation_data = {{
{indent_str}                    'enterprise_value': financial_data.get('enterprise_value', 0),
{indent_str}                    'ev_ebitda_multiple': 0,  # Calcular si es necesario
{indent_str}                    'tir': financial_data.get('tir', 0),
{indent_str}                    'payback': 0  # Calcular si es necesario
{indent_str}                }}
{indent_str}                
{indent_str}                # Generar SWOT
{indent_str}                st.sidebar.info("Generando análisis SWOT...")
{indent_str}                swot = analyzer.generate_swot(company_data)
{indent_str}                if swot:
{indent_str}                    st.session_state['ai_swot'] = swot
{indent_str}                    st.sidebar.success("✅ SWOT generado")
{indent_str}                
{indent_str}                # Generar recomendaciones estratégicas
{indent_str}                st.sidebar.info("Generando recomendaciones...")
{indent_str}                recommendations = analyzer.generate_strategic_recommendations(company_data)
{indent_str}                if recommendations:
{indent_str}                    st.session_state['ai_recommendations'] = recommendations
{indent_str}                    st.sidebar.success("✅ Recomendaciones generadas")
{indent_str}                
{indent_str}                # Analizar proyecciones financieras si hay datos McKinsey
{indent_str}                if financial_data and 'fcf_proyectados' in financial_data:
{indent_str}                    st.sidebar.info("Analizando proyecciones financieras...")
{indent_str}                    financial_analysis = analyzer.analyze_financial_projections(financial_data)
{indent_str}                    if financial_analysis:
{indent_str}                        st.session_state['ai_financial_analysis'] = financial_analysis
{indent_str}                        st.sidebar.success("✅ Análisis financiero completado")
{indent_str}                
{indent_str}                # Generar Investment Thesis si hay valoración
{indent_str}                if valuation_data and financial_data:
{indent_str}                    st.sidebar.info("Generando Investment Thesis...")
{indent_str}                    thesis = analyzer.generate_investment_thesis(company_data, financial_data, valuation_data)
{indent_str}                    if thesis:
{indent_str}                        st.session_state['ai_investment_thesis'] = thesis
{indent_str}                        st.sidebar.success("✅ Investment Thesis generada")
{indent_str}                
{indent_str}                st.sidebar.success("✅ Análisis completo generado")
{indent_str}                st.balloons()
{indent_str}            else:
{indent_str}                st.sidebar.error("❌ Error configurando el modelo de IA")
{indent_str}        except Exception as e:
{indent_str}            st.sidebar.error(f"❌ Error: {{str(e)}}")
'''
        
        # Reemplazar el bloque
        del lines[start_line:end_line]
        lines.insert(start_line, new_block)
        found = True
        break

if found:
    # Guardar el archivo
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("✅ Botón de Análisis Financiero Completo actualizado")
else:
    print("❌ No se encontró el botón de Análisis Financiero Completo")


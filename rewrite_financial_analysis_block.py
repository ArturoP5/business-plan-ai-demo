#!/usr/bin/env python3
"""
Reescribir completamente el bloque de análisis financiero para evitar errores de indentación
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar y eliminar el bloque problemático actual
start_line = -1
end_line = -1

for i in range(len(lines)):
    if "💼 Análisis Financiero Completo IA" in lines[i]:
        start_line = i
        # Buscar el final del bloque (próximo if al mismo nivel o menos indentación)
        base_indent = len(lines[i]) - len(lines[i].lstrip())
        
        for j in range(i+1, len(lines)):
            line_indent = len(lines[j]) - len(lines[j].lstrip())
            # Si encontramos algo con menor o igual indentación que no sea espacio en blanco
            if lines[j].strip() and line_indent <= base_indent:
                end_line = j
                break
        
        if end_line == -1:
            end_line = min(i + 100, len(lines))
        
        print(f"Eliminando bloque problemático desde línea {start_line+1} hasta {end_line}")
        break

if start_line > 0:
    # Eliminar el bloque viejo
    del lines[start_line:end_line]
    
    # Insertar el bloque nuevo correctamente formateado
    # Necesitamos la indentación correcta
    # Buscar la indentación del botón anterior (Generar Análisis IA)
    base_indent = 8  # Por defecto 8 espacios
    for i in range(max(0, start_line-20), start_line):
        if "🎯 Generar Análisis IA" in lines[i]:
            base_indent = len(lines[i]) - len(lines[i].lstrip())
            break
    
    # Crear el bloque correcto con la indentación apropiada
    indent = " " * base_indent
    new_block = f'''
{indent}if api_key and st.sidebar.button("💼 Análisis Financiero Completo IA", key="full_ai_analysis"):
{indent}    with st.spinner(f'Generando análisis completo con {{ai_model}}...'):
{indent}        try:
{indent}            analyzer = AIAnalyzer()
{indent}            
{indent}            if analyzer.models[ai_model](api_key):
{indent}                # Preparar datos de la empresa
{indent}                company_data = {{
{indent}                    'nombre_empresa': nombre_empresa,
{indent}                    'sector': sector,
{indent}                    'modelo_negocio': modelo_negocio,
{indent}                    'descripcion_actividad': descripcion_actividad if 'descripcion_actividad' in locals() else '',
{indent}                    'productos_servicios': productos_servicios if 'productos_servicios' in locals() else '',
{indent}                    'ventaja_competitiva_principal': ventaja_competitiva_clave if 'ventaja_competitiva_clave' in locals() else '',
{indent}                    'competidores_principales': competidores_principales if 'competidores_principales' in locals() else '',
{indent}                    'cuota_mercado': cuota_mercado if 'cuota_mercado' in locals() else 0,
{indent}                    'clientes_objetivo': clientes_objetivo if 'clientes_objetivo' in locals() else '',
{indent}                    'vision_corto': vision_corto if 'vision_corto' in locals() else '',
{indent}                    'vision_largo': vision_largo if 'vision_largo' in locals() else '',
{indent}                    'principales_riesgos': principales_riesgos if 'principales_riesgos' in locals() else ''
{indent}                }}
{indent}                
{indent}                # Generar SWOT
{indent}                st.sidebar.info("Generando análisis SWOT...")
{indent}                swot = analyzer.generate_swot(company_data)
{indent}                if swot:
{indent}                    st.session_state['ai_swot'] = swot
{indent}                    st.sidebar.success("✅ SWOT generado")
{indent}                
{indent}                # Si hay proyecciones, analizar financieros
{indent}                if 'proyecciones' in st.session_state:
{indent}                    st.sidebar.info("Analizando proyecciones financieras...")
{indent}                    financial_data = {{
{indent}                        'ventas_proyectadas': st.session_state.get('ventas_proyectadas', []),
{indent}                        'ebitda_proyectado': st.session_state.get('ebitda_proyectado', []),
{indent}                        'margenes_ebitda': st.session_state.get('margenes_ebitda', [])
{indent}                    }}
{indent}                    
{indent}                    financial_analysis = analyzer.analyze_financial_projections(financial_data)
{indent}                    if financial_analysis:
{indent}                        st.session_state['ai_financial_analysis'] = financial_analysis
{indent}                        st.sidebar.success("✅ Análisis financiero completado")
{indent}                
{indent}                st.sidebar.success("✅ Análisis completo generado")
{indent}                st.balloons()
{indent}            else:
{indent}                st.sidebar.error("❌ Error configurando el modelo de IA")
{indent}        except Exception as e:
{indent}            st.sidebar.error(f"❌ Error: {{str(e)}}")
'''
    
    # Insertar el nuevo bloque
    lines.insert(start_line, new_block)
    
    # Guardar
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("✅ Bloque de análisis financiero completamente reescrito")
    print(f"✅ Insertado en línea {start_line+1} con indentación de {base_indent} espacios")
else:
    print("❌ No se encontró el bloque a reemplazar")


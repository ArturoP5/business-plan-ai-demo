#!/usr/bin/env python3
"""
Agrega correctamente el botón de PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar el botón en la línea correcta (5275)
button_found = False
for i in range(5270, 5280):
    if i < len(lines) and '📊 Generar Informe de Valoración' in lines[i]:
        button_found = True
        
        # Insertar columnas ANTES del if del botón
        indent = '                '
        columns_code = f'''{indent}# Opciones de generación de informe
{indent}col1, col2 = st.columns(2)
{indent}
{indent}with col1:
'''
        lines.insert(i, columns_code)
        
        # Ahora buscar donde cerrar col1 y agregar col2 con el segundo botón
        # Buscar el except del primer botón (aproximadamente 30 líneas después)
        for j in range(i+25, i+40):
            if j < len(lines) and 'except Exception as e:' in lines[j] and 'pdf' in lines[j+1].lower():
                # Buscar el final del except
                for k in range(j+1, j+5):
                    if k < len(lines) and 'st.error' in lines[k]:
                        # Insertar el segundo botón después del error
                        second_button = f'''
{indent}with col2:
{indent}    if st.button("🤖 Generar Informe con IA", type="secondary", use_container_width=True):
{indent}        try:
{indent}            from utils.pdf_ai_generator_completo import generate_complete_ai_pdf
{indent}            from utils.ai_integration_completo import AIAnalyzerCompleto
{indent}            
{indent}            ia_selected = st.session_state.get('ia_selected')
{indent}            
{indent}            if not ia_selected:
{indent}                st.error("❌ Configura una IA en el sidebar primero")
{indent}            else:
{indent}                with st.spinner("Generando análisis con IA..."):
{indent}                    # Obtener API key
{indent}                    api_key = st.session_state.get(f'{"{ia_selected}_api_key"}')
{indent}                    
{indent}                    if api_key:
{indent}                        # Preparar datos
{indent}                        datos = st.session_state.datos_guardados
{indent}                        analyzer = AIAnalyzerCompleto()
{indent}                        
{indent}                        # Configurar modelo
{indent}                        if ia_selected == 'gemini':
{indent}                            analyzer.setup_gemini(api_key)
{indent}                            model_name = "Gemini Pro"
{indent}                        elif ia_selected == 'openai':
{indent}                            analyzer.setup_gpt4(api_key)
{indent}                            model_name = "GPT-4"
{indent}                        else:
{indent}                            analyzer.setup_claude(api_key)
{indent}                            model_name = "Claude 3"
{indent}                        
{indent}                        # Generar análisis
{indent}                        company_data = datos.get('datos_empresa', {"{}"})
{indent}                        financial_data = {"{"}
{indent}                            'enterprise_value': datos.get('resultado_mckinsey', {"{}"}).get('enterprise_value', 0),
{indent}                            'wacc': datos.get('resultado_mckinsey', {"{}"}).get('wacc', 0),
{indent}                            'tir': datos.get('resultado_mckinsey', {"{}"}).get('tir_proyecto', 0),
{indent}                            'payback': datos.get('resultado_mckinsey', {"{}"}).get('payback_years', 0)
{indent}                        {"}"}
{indent}                        
{indent}                        ai_analysis = analyzer.generate_complete_analysis(company_data, financial_data)
{indent}                        
{indent}                        # Generar PDF
{indent}                        pdf_buffer = generate_complete_ai_pdf(datos, ai_analysis)
{indent}                        
{indent}                        # Descarga
{indent}                        from datetime import datetime
{indent}                        nombre = company_data.get('nombre_empresa', 'Empresa')
{indent}                        fecha = datetime.now().strftime('%Y%m%d')
{indent}                        
{indent}                        st.download_button(
{indent}                            "📥 Descargar Informe IA",
{indent}                            data=pdf_buffer.getvalue(),
{indent}                            file_name=f"Informe_IA_{{nombre}}_{{fecha}}.pdf",
{indent}                            mime="application/pdf",
{indent}                            key="download_ai"
{indent}                        )
{indent}                        st.success(f"✅ Informe generado con {{model_name}}")
{indent}                    else:
{indent}                        st.error("❌ API key no encontrada")
{indent}                        
{indent}        except Exception as e:
{indent}            st.error(f"Error con IA: {{str(e)}}")
'''
                        lines.insert(k+1, second_button)
                        print(f"✅ Segundo botón agregado después de línea {k+1}")
                        break
                break
        
        if button_found:
            print(f"✅ Columnas agregadas en línea {i}")
        break

if not button_found:
    print("❌ No se encontró el botón en las líneas esperadas")
else:
    # Guardar
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("\n✅ Modificación completada exitosamente")

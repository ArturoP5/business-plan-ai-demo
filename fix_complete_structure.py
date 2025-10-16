#!/usr/bin/env python3
"""
Arregla completamente la estructura de los botones
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y reemplazar toda la sección problemática
for i in range(5270, 5320):
    if '# Opciones de generación de informe' in lines[i]:
        # Encontramos el inicio, ahora buscar donde termina el except
        end_index = i
        for j in range(i, i+50):
            if 'st.error(f"Error generando informe:' in lines[j]:
                end_index = j + 1
                break
        
        # Reemplazar toda la sección con la versión correcta
        correct_structure = """                # Opciones de generación de informe
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 Generar Informe de Valoración", type="primary", use_container_width=True):
                        try:
                            from utils.pdf_mckinsey_generator import generar_pdf_mckinsey
                            with st.spinner("Preparando informe ejecutivo..."):
                                datos = st.session_state.datos_guardados
                                resultado_mck = datos.get("resultado_mckinsey", {})
                            
                                if resultado_mck:
                                    pdf_bytes = generar_pdf_mckinsey(
                                        datos_empresa=datos["datos_empresa"],
                                        resultado_mckinsey=resultado_mck,
                                        pyl_df=datos["pyl"],
                                        balance_df=datos.get("balance"),
                                        analisis_ia=datos.get("analisis_ia", {}),
                                        fcf_df=datos.get("cash_flow"),
                                    )
                                    
                                    st.download_button(
                                        label="📥 Descargar Informe DCF",
                                        data=pdf_bytes,
                                        file_name=f"Valoracion_DCF_{datos['datos_empresa']['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                    st.success("✅ Informe generado exitosamente")
                                else:
                                    st.warning("⚠️ Genera primero la valoración en el tab 'Valoración'")
                        except Exception as e:
                            st.error(f"Error generando informe: {str(e)}")
                
                with col2:
                    if st.button("🤖 Generar Informe con IA", type="secondary", use_container_width=True):
                        try:
                            from utils.pdf_ai_generator_completo import generate_complete_ai_pdf
                            from utils.ai_integration_completo import AIAnalyzerCompleto
                            
                            ia_selected = st.session_state.get('ia_selected')
                            
                            if not ia_selected:
                                st.error("❌ Configura una IA en el sidebar primero")
                                st.info("Ve a: Sidebar → Configuración de IA → Selecciona modelo y agrega API key")
                            else:
                                with st.spinner(f"🤖 Generando análisis completo con IA..."):
                                    api_key = st.session_state.get(f'{ia_selected}_api_key')
                                    
                                    if api_key:
                                        # Preparar datos
                                        datos = st.session_state.datos_guardados
                                        analyzer = AIAnalyzerCompleto()
                                        
                                        # Configurar modelo
                                        model_name = ""
                                        if ia_selected == 'gemini':
                                            if analyzer.setup_gemini(api_key):
                                                model_name = "Gemini Pro"
                                        elif ia_selected == 'openai':
                                            if analyzer.setup_gpt4(api_key):
                                                model_name = "GPT-4"
                                        else:
                                            if analyzer.setup_claude(api_key):
                                                model_name = "Claude 3"
                                        
                                        if model_name:
                                            # Generar análisis
                                            company_data = datos.get('datos_empresa', {})
                                            financial_data = {
                                                'enterprise_value': datos.get('resultado_mckinsey', {}).get('enterprise_value', 0),
                                                'wacc': datos.get('resultado_mckinsey', {}).get('wacc', 0),
                                                'tir': datos.get('resultado_mckinsey', {}).get('tir_proyecto', 0),
                                                'payback': datos.get('resultado_mckinsey', {}).get('payback_years', 0)
                                            }
                                            
                                            st.info(f"Generando análisis con {model_name}...")
                                            ai_analysis = analyzer.generate_complete_analysis(company_data, financial_data)
                                            
                                            # Generar PDF
                                            datos['ia_model'] = model_name
                                            pdf_buffer = generate_complete_ai_pdf(datos, ai_analysis)
                                            
                                            # Descarga
                                            nombre = company_data.get('nombre_empresa', 'Empresa').replace(' ', '_')
                                            fecha = datetime.now().strftime('%Y%m%d')
                                            
                                            st.download_button(
                                                "📥 Descargar Informe Completo IA",
                                                data=pdf_buffer.getvalue(),
                                                file_name=f"Informe_IA_{nombre}_{fecha}.pdf",
                                                mime="application/pdf",
                                                key="download_ai_pdf",
                                                use_container_width=True
                                            )
                                            st.success(f"✅ Informe con IA generado ({model_name})")
                                            
                                            # Mostrar contenido
                                            with st.expander("📋 Contenido del informe"):
                                                st.markdown('''
                                                **Análisis con IA:**
                                                - Resumen Ejecutivo
                                                - SWOT personalizado
                                                - Benchmarking sectorial
                                                - Matriz de riesgos
                                                - KPIs recomendados
                                                - Plan de acción
                                                
                                                **Anexos Financieros:**
                                                - P&L proyectado
                                                - FCF proyectado
                                                - Balance proyectado
                                                ''')
                                        else:
                                            st.error("Error configurando el modelo de IA")
                                    else:
                                        st.error("❌ API key no encontrada")
                        except Exception as e:
                            st.error(f"Error con IA: {str(e)}")
                            import traceback
                            st.text(traceback.format_exc())
"""
        
        # Reemplazar las líneas
        lines[i:end_index] = [correct_structure]
        print(f"✅ Estructura completa reemplazada (líneas {i+1} a {end_index+1})")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Estructura de botones arreglada completamente")
print("  - Botón 1: Informe tradicional")
print("  - Botón 2: Informe con IA")

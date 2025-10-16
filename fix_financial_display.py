#!/usr/bin/env python3
"""
Arreglar la visualización del análisis financiero completo
"""

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Buscar la pestaña 9 (Análisis IA)
tab9_pos = content.find("with tab9:")

if tab9_pos > 0:
    # Buscar donde se muestra el SWOT
    swot_display = content.find("'ai_swot' in st.session_state:", tab9_pos)
    
    if swot_display > 0:
        # Buscar el final de la sección de SWOT para agregar el análisis financiero
        # Buscar donde termina la visualización del SWOT (siguiente if o línea vacía)
        next_section = content.find("\n    if ", swot_display + 500)
        
        if next_section < 0:
            next_section = content.find("\n\n", swot_display + 500)
        
        if next_section > 0:
            # Insertar código para mostrar análisis financiero
            financial_display = """
        # Mostrar Análisis Financiero si existe
        if 'ai_financial_analysis' in st.session_state:
            st.markdown("---")
            st.subheader("📊 Análisis Financiero Generado por IA")
            
            financial = st.session_state['ai_financial_analysis']
            
            if 'analisis_ventas' in financial:
                st.markdown("### 📈 Análisis de Ventas")
                st.write(financial['analisis_ventas'])
            
            if 'analisis_rentabilidad' in financial:
                st.markdown("### 💰 Análisis de Rentabilidad")
                st.write(financial['analisis_rentabilidad'])
            
            if 'analisis_flujos' in financial:
                st.markdown("### 💵 Análisis de Flujos de Caja")
                st.write(financial['analisis_flujos'])
            
            if 'fortalezas_financieras' in financial:
                st.markdown("### ✅ Fortalezas Financieras")
                for f in financial['fortalezas_financieras']:
                    st.write(f"• {f}")
            
            if 'riesgos_financieros' in financial:
                st.markdown("### ⚠️ Riesgos Financieros")
                for r in financial['riesgos_financieros']:
                    st.write(f"• {r}")
        
        # Mostrar Investment Thesis si existe
        if 'ai_investment_thesis' in st.session_state:
            st.markdown("---")
            st.subheader("💼 Investment Thesis - IA")
            
            thesis = st.session_state['ai_investment_thesis']
            
            if 'resumen_ejecutivo' in thesis:
                st.markdown("### 📋 Resumen Ejecutivo")
                st.write(thesis['resumen_ejecutivo'])
            
            if 'puntos_clave_inversion' in thesis:
                st.markdown("### 🎯 Puntos Clave de Inversión")
                for i, punto in enumerate(thesis['puntos_clave_inversion'], 1):
                    st.write(f"{i}. {punto}")
            
            if 'recomendacion' in thesis:
                color = "green" if thesis['recomendacion'] == 'COMPRAR' else "red"
                st.markdown(f"### Recomendación: :{color}[**{thesis['recomendacion']}**]")
"""
            
            content = content[:next_section] + financial_display + content[next_section:]
            
            # Guardar
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(content)
            
            print("✅ Agregada visualización de análisis financiero completo")
        else:
            print("⚠️ No se encontró dónde insertar el análisis financiero")
    else:
        print("⚠️ No se encontró la sección de visualización del SWOT")
else:
    print("⚠️ No se encontró tab9")


#!/usr/bin/env python3
"""
Insertar directamente la visualización del análisis financiero
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Tab9 está en línea 6069, SWOT en 6072
# Vamos a buscar después del SWOT para insertar el análisis financiero
insert_after_line = -1

for i in range(6070, min(6200, len(lines))):
    # Buscar donde termina la visualización del SWOT
    if "'ai_recommendations' in st.session_state" in lines[i]:
        # Insertar antes de las recomendaciones
        insert_after_line = i
        break
    elif "else:" in lines[i] and i > 6100:
        # O insertar antes del else
        insert_after_line = i
        break

if insert_after_line == -1:
    # Si no encontramos esos puntos, insertar después de línea 6140 aprox
    insert_after_line = 6140

print(f"Insertando visualización después de línea {insert_after_line}")

# Código a insertar
financial_display_code = '''    
    # Mostrar Análisis Financiero Completo
    if 'ai_financial_analysis' in st.session_state:
        st.markdown("---")
        st.subheader("💼 Análisis Financiero Completo - IA")
        
        financial = st.session_state['ai_financial_analysis']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'analisis_ventas' in financial:
                st.markdown("#### 📈 Análisis de Ventas")
                st.write(financial['analisis_ventas'])
            
            if 'analisis_rentabilidad' in financial:
                st.markdown("#### 💰 Rentabilidad")
                st.write(financial['analisis_rentabilidad'])
        
        with col2:
            if 'analisis_flujos' in financial:
                st.markdown("#### 💵 Flujos de Caja")
                st.write(financial['analisis_flujos'])
            
            if 'analisis_balance' in financial:
                st.markdown("#### 📊 Balance")
                st.write(financial['analisis_balance'])
        
        if 'fortalezas_financieras' in financial:
            st.markdown("### ✅ Fortalezas Financieras")
            for f in financial.get('fortalezas_financieras', []):
                st.write(f"• {f}")
        
        if 'riesgos_financieros' in financial:
            st.markdown("### ⚠️ Riesgos Financieros")
            for r in financial.get('riesgos_financieros', []):
                st.write(f"• {r}")
        
        if 'conclusiones' in financial:
            st.markdown("### 📝 Conclusiones")
            st.info(financial['conclusiones'])
    
    # Mostrar Investment Thesis
    if 'ai_investment_thesis' in st.session_state:
        st.markdown("---")
        st.subheader("🎯 Investment Thesis - IA")
        
        thesis = st.session_state['ai_investment_thesis']
        
        if 'resumen_ejecutivo' in thesis:
            st.markdown("#### 📋 Resumen Ejecutivo")
            st.write(thesis['resumen_ejecutivo'])
        
        if 'puntos_clave_inversion' in thesis:
            st.markdown("#### 🔑 Puntos Clave de Inversión")
            for i, punto in enumerate(thesis.get('puntos_clave_inversion', []), 1):
                st.write(f"{i}. {punto}")
        
        if 'recomendacion' in thesis:
            rec = thesis['recomendacion']
            if 'COMPRAR' in str(rec).upper():
                st.success(f"**Recomendación: {rec}**")
            elif 'VENDER' in str(rec).upper():
                st.error(f"**Recomendación: {rec}**")
            else:
                st.warning(f"**Recomendación: {rec}**")
'''

# Insertar el código
lines.insert(insert_after_line, financial_display_code)

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Visualización del análisis financiero agregada exitosamente")


#!/usr/bin/env python3
"""
Arreglar definitivamente la integración del análisis IA en el PDF
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la sección de tab7 (Documentos)
tab7_start = -1
for i, line in enumerate(lines):
    if "with tab7:" in line:
        tab7_start = i
        print(f"Encontrado tab7 en línea {i+1}")
        break

if tab7_start > 0:
    # Buscar dentro de tab7 donde se genera el PDF
    for i in range(tab7_start, min(tab7_start + 200, len(lines))):
        if "generar_pdf" in lines[i].lower() or "pdf" in lines[i].lower() and "button" in lines[i].lower():
            print(f"Encontrada generación PDF en línea {i+1}: {lines[i].strip()[:60]}...")
            
            # Insertar código para recopilar análisis IA antes de generar el PDF
            if "ai_analysis" not in lines[i-5:i+5]:  # Verificar que no esté ya
                insert_code = """
        # Recopilar análisis IA si existe
        ai_analysis = {}
        if 'ai_swot' in st.session_state:
            ai_analysis['swot'] = st.session_state['ai_swot']
        if 'ai_financial_analysis' in st.session_state:
            ai_analysis['analisis_financiero'] = st.session_state['ai_financial_analysis']
        if 'ai_investment_thesis' in st.session_state:
            ai_analysis['investment_thesis'] = st.session_state['ai_investment_thesis']
        
"""
                # Insertar antes del botón
                lines.insert(i, insert_code)
                print(f"✅ Agregado código para recopilar análisis IA")
                break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Integración IA-PDF arreglada en tab7")


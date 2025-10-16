#!/usr/bin/env python3
"""
Arreglar la integración del análisis IA en el PDF
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde se genera el PDF
pdf_generation_found = False
for i, line in enumerate(lines):
    if "Generar PDF" in line and "st.button" in line:
        print(f"Encontrado botón generar PDF en línea {i+1}")
        
        # Buscar la función que genera el PDF
        for j in range(i, min(i+100, len(lines))):
            if "generar_pdf_profesional" in lines[j] or "PDFMcKinsey" in lines[j]:
                print(f"Encontrada generación PDF en línea {j+1}")
                
                # Verificar si ya incluye ai_analysis
                if "ai_analysis" not in lines[j]:
                    # Necesitamos agregar la recolección de datos IA antes
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
                    # Insertar antes de la generación
                    lines[j] = insert_code + lines[j]
                    
                    # Ahora buscar la llamada exacta a generar_pdf_profesional
                    for k in range(j, min(j+30, len(lines))):
                        if "generar_pdf_profesional(" in lines[k]:
                            # Agregar ai_analysis como parámetro
                            if "ai_analysis" not in lines[k]:
                                # Buscar el cierre del paréntesis
                                if ")" in lines[k]:
                                    lines[k] = lines[k].replace(")", ", ai_analysis=ai_analysis)")
                                    print(f"Agregado ai_analysis al PDF en línea {k+1}")
                            break
                    
                pdf_generation_found = True
                break
        break

# Guardar cambios
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

if pdf_generation_found:
    print("✅ Integración IA-PDF arreglada")
else:
    print("⚠️ No se encontró la generación del PDF")


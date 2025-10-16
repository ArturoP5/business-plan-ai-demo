#!/usr/bin/env python3
"""
Asegurar que el generador PDF acepte y use el análisis IA
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Verificar si generar_pdf_profesional acepta ai_analysis
if "def generar_pdf_profesional" in content:
    # Buscar la definición de la función
    start = content.find("def generar_pdf_profesional")
    end = content.find("):", start)
    
    function_def = content[start:end+2]
    print(f"Definición actual: {function_def[:100]}...")
    
    if "ai_analysis" not in function_def:
        # Agregar ai_analysis como parámetro
        new_def = function_def.replace("):", ", ai_analysis=None):")
        content = content.replace(function_def, new_def)
        print("✅ Agregado parámetro ai_analysis")
    
    # Buscar donde se genera el SWOT para agregar el análisis IA después
    if "# SWOT Analysis" in content or "add_swot" in content:
        # Buscar el lugar correcto para insertar el análisis IA
        swot_pos = content.find("# SWOT Analysis")
        if swot_pos == -1:
            swot_pos = content.find("pdf.add_page()")  # Agregar después de cualquier add_page
        
        if swot_pos > 0:
            # Insertar llamada al análisis IA
            insert_code = """
    # Agregar análisis IA si está disponible
    if ai_analysis and len(ai_analysis) > 0:
        pdf_gen.add_ai_analysis_section(pdf, ai_analysis)
"""
            # Buscar el siguiente add_page después del SWOT
            next_page = content.find("pdf.add_page()", swot_pos + 100)
            if next_page > 0:
                content = content[:next_page] + insert_code + content[next_page:]
                print("✅ Agregada sección de análisis IA al PDF")

# Guardar cambios
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Generador PDF actualizado para incluir análisis IA")


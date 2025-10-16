#!/usr/bin/env python3
"""
Asegurar que ai_analysis se pase correctamente a generar_pdf_mckinsey
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la llamada a generar_pdf_mckinsey (alrededor de línea 5338)
for i in range(5330, min(5350, len(lines))):
    if "generar_pdf_mckinsey(" in lines[i]:
        print(f"Encontrada llamada a generar_pdf_mckinsey en línea {i+1}")
        
        # Verificar si ya incluye ai_analysis
        if "ai_analysis" not in lines[i]:
            # Buscar el cierre del paréntesis
            paren_line = i
            while paren_line < len(lines) and ")" not in lines[paren_line]:
                paren_line += 1
            
            if paren_line < len(lines):
                # Agregar ai_analysis como parámetro
                lines[paren_line] = lines[paren_line].replace(")", ", ai_analysis=ai_analysis)")
                print(f"✅ Agregado ai_analysis a la llamada en línea {paren_line+1}")
        else:
            print("✅ ai_analysis ya está incluido")
        break

# También necesitamos actualizar la función generar_pdf_mckinsey para que acepte el parámetro
with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    pdf_content = f.read()

# Buscar la definición de generar_pdf_mckinsey
if "def generar_pdf_mckinsey" in pdf_content:
    import re
    # Buscar la definición completa
    pattern = r'def generar_pdf_mckinsey\([^)]*\)'
    match = re.search(pattern, pdf_content)
    
    if match:
        old_def = match.group()
        print(f"\nDefinición actual: {old_def}")
        
        if "ai_analysis" not in old_def:
            # Agregar ai_analysis como parámetro
            new_def = old_def.replace(")", ", ai_analysis=None)")
            pdf_content = pdf_content.replace(old_def, new_def)
            print(f"Nueva definición: {new_def}")
            
            # Ahora agregar el código para usar ai_analysis dentro de la función
            # Buscar donde agregar la sección de IA (después del SWOT)
            swot_section = pdf_content.find("# Página 9: SWOT")
            if swot_section == -1:
                swot_section = pdf_content.find("SWOT")
            
            if swot_section > 0:
                # Buscar el siguiente pdf.add_page() después del SWOT
                next_page = pdf_content.find("pdf.add_page()", swot_section + 100)
                if next_page > 0:
                    # Insertar el análisis IA
                    ia_code = """
    # Agregar análisis IA si está disponible
    if ai_analysis and len(ai_analysis) > 0:
        # Página de Análisis IA
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "ANÁLISIS CON INTELIGENCIA ARTIFICIAL", 0, 1, 'C')
        pdf.ln(5)
        
        # SWOT IA
        if 'swot' in ai_analysis and ai_analysis['swot']:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Análisis SWOT - Perspectiva IA", 0, 1)
            pdf.set_font("Arial", "", 10)
            
            swot_data = ai_analysis['swot']
            
            # Fortalezas
            if 'fortalezas' in swot_data:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Fortalezas:", 0, 1)
                pdf.set_font("Arial", "", 10)
                for f in swot_data['fortalezas'][:4]:
                    pdf.cell(0, 5, f"• {f[:80]}", 0, 1)
                pdf.ln(3)
            
            # Debilidades
            if 'debilidades' in swot_data:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Debilidades:", 0, 1)
                pdf.set_font("Arial", "", 10)
                for d in swot_data['debilidades'][:4]:
                    pdf.cell(0, 5, f"• {d[:80]}", 0, 1)
                pdf.ln(3)
            
            # Oportunidades
            if 'oportunidades' in swot_data:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Oportunidades:", 0, 1)
                pdf.set_font("Arial", "", 10)
                for o in swot_data['oportunidades'][:4]:
                    pdf.cell(0, 5, f"• {o[:80]}", 0, 1)
                pdf.ln(3)
            
            # Amenazas
            if 'amenazas' in swot_data:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Amenazas:", 0, 1)
                pdf.set_font("Arial", "", 10)
                for a in swot_data['amenazas'][:4]:
                    pdf.cell(0, 5, f"• {a[:80]}", 0, 1)
"""
                    pdf_content = pdf_content[:next_page] + ia_code + pdf_content[next_page:]
                    print("✅ Agregada sección de análisis IA al generador PDF")
            
            # Guardar el archivo actualizado
            with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
                f.write(pdf_content)

# Guardar app.py actualizado
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Integración completa IA-PDF finalizada")


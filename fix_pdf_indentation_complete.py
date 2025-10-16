#!/usr/bin/env python3
"""
Arreglar la indentación de la sección de análisis IA en el PDF
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar y arreglar las líneas problemáticas (1654-1670)
for i in range(1653, min(1670, len(lines))):
    # La línea pdf.add_page() debe tener indentación
    if i == 1653 and "pdf.add_page()" in lines[i]:
        # Esta línea necesita indentación (probablemente 4 o 8 espacios)
        lines[i] = "    " + lines[i].lstrip()
        print(f"Corregida línea {i+1}: pdf.add_page()")
    
    # Las líneas siguientes ya tienen indentación pero incorrecta
    elif i >= 1654 and i <= 1659:
        # Quitar espacios extra al inicio
        lines[i] = "    " + lines[i].lstrip()
        print(f"Corregida línea {i+1}")

# Guardar
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Indentación corregida en la sección de análisis IA")


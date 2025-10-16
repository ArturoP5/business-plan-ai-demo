#!/usr/bin/env python3
"""
Arreglar el error de indentación en pdf_mckinsey_generator.py línea 1657
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar alrededor de la línea 1657
if len(lines) > 1657:
    print(f"Línea 1656: {lines[1655].rstrip()}")
    print(f"Línea 1657: {lines[1656].rstrip()}")
    print(f"Línea 1658: {lines[1657].rstrip()}")
    
    # Verificar y corregir la indentación
    for i in range(1655, min(1660, len(lines))):
        if lines[i].strip() and not lines[i][0].isspace() and i > 0:
            # Esta línea no está indentada pero debería estarlo
            # Ver la indentación de la línea anterior
            prev_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
            if prev_indent > 0:
                lines[i] = " " * prev_indent + lines[i]
                print(f"Corregida indentación en línea {i+1}")

# Guardar
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Indentación corregida en PDF generator")


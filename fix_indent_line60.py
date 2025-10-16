#!/usr/bin/env python3
"""
Arreglar error de indentación en línea 60
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"📝 Analizando línea 60 y contexto...")

# Mostrar contexto alrededor de línea 60
if len(lines) > 60:
    for i in range(max(0, 55), min(65, len(lines))):
        indent = len(lines[i]) - len(lines[i].lstrip())
        print(f"L{i+1:3d} (indent={indent:2d}): {lines[i].rstrip()[:80]}")

# La línea 60 (índice 59) probablemente tiene indentación incorrecta
if len(lines) > 59:
    line60 = lines[59]
    current_indent = len(line60) - len(line60.lstrip())
    
    # Determinar la indentación correcta basándose en el contexto
    # Si está dentro de una función, típicamente sería 4 espacios
    # Si está dentro de un bloque, sería 8 espacios
    
    # Ver la línea anterior
    if len(lines) > 58:
        prev_indent = len(lines[58]) - len(lines[58].lstrip())
        
        # Si la línea anterior termina con : necesita indent adicional
        if lines[58].rstrip().endswith(':'):
            correct_indent = prev_indent + 4
        else:
            correct_indent = prev_indent
        
        if current_indent != correct_indent:
            print(f"\n❌ Error: Línea 60 tiene {current_indent} espacios, debería tener {correct_indent}")
            # Corregir la indentación
            lines[59] = ' ' * correct_indent + lines[59].lstrip()
            print(f"✅ Corregida indentación de línea 60")
            
            # Guardar
            with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
                f.writelines(lines)
            print("✅ Archivo guardado")
        else:
            print(f"✓ La indentación parece correcta ({current_indent} espacios)")


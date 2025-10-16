#!/usr/bin/env python3
"""
Arreglar la indentación del código de análisis IA en tab7
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la línea 5331 donde está el try
if len(lines) > 5334:
    print(f"Línea 5331: {lines[5330].rstrip()}")
    print(f"Línea 5334: {lines[5333].rstrip()}")
    
    # Verificar si hay un try antes
    if "try:" in lines[5330]:
        # El código después del try debe estar indentado
        base_indent = len(lines[5330]) - len(lines[5330].lstrip())
        needed_indent = base_indent + 4
        
        print(f"Indentación del try: {base_indent} espacios")
        print(f"Indentación necesaria para el contenido: {needed_indent} espacios")
        
        # Arreglar la indentación de las líneas del análisis IA (5334 en adelante)
        for i in range(5333, min(5345, len(lines))):
            if lines[i].strip():  # Si la línea no está vacía
                current_indent = len(lines[i]) - len(lines[i].lstrip())
                if current_indent < needed_indent:
                    lines[i] = " " * needed_indent + lines[i].lstrip()
                    print(f"Corregida línea {i+1}")
        
        # Guardar
        with open("app.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print("\n✅ Indentación corregida en tab7")
    else:
        print("⚠️ No se encontró 'try:' en la línea esperada")
else:
    print("⚠️ El archivo no tiene suficientes líneas")


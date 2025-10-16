#!/usr/bin/env python3
"""
Arreglar error de indentación en línea 1778
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Verificar línea 1778 (índice 1777)
if len(lines) > 1777:
    print(f"Línea 1777: {repr(lines[1776])[:80]}")
    print(f"Línea 1778: {repr(lines[1777])[:80]}")
    print(f"Línea 1779: {repr(lines[1778])[:80]}")
    
    # Contar espacios en las líneas anteriores para determinar la indentación correcta
    for i in range(1775, 1780):
        if i < len(lines):
            line = lines[i]
            spaces = len(line) - len(line.lstrip())
            print(f"Línea {i+1}: {spaces} espacios de indentación")
    
    # Buscar la indentación correcta basándose en el contexto
    # El if con el botón debe estar al mismo nivel que otros if en esa sección
    correct_indent = 8  # Típicamente 8 espacios para este nivel
    
    # Arreglar la línea 1778
    if "💼 Análisis Financiero Completo IA" in lines[1777]:
        lines[1777] = " " * correct_indent + lines[1777].lstrip()
        print(f"\n✅ Corregida indentación de línea 1778 a {correct_indent} espacios")
    
    # Guardar
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)


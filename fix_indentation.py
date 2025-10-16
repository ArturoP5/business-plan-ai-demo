#!/usr/bin/env python3
"""
Arregla la indentación de default_costos_var
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Arreglar la línea 1376 (índice 1375)
if "default_costos_var = 40" in lines[1375]:
    # Quitar espacios extras al inicio
    lines[1375] = "        default_costos_var = 40\n"
    print("✅ Indentación corregida en línea 1376")

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

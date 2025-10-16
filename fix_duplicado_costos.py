#!/usr/bin/env python3
"""
Elimina la línea duplicada de default_costos_var
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Eliminar la segunda asignación (línea 1376)
if lines[1375].strip() == "default_costos_var = 40":
    del lines[1375]  # Eliminar el duplicado
    print("✅ Eliminada línea duplicada 1376")

with open('app.py', 'w') as f:
    f.writelines(lines)

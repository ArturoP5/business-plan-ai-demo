#!/usr/bin/env python3
"""
Arregla las comas faltantes después de principales_riesgos
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar líneas con principales_riesgos que no terminan en coma
for i in range(len(lines)):
    if "'principales_riesgos':" in lines[i] and lines[i].rstrip().endswith("'"):
        # Agregar coma al final
        lines[i] = lines[i].rstrip() + ',\n'
        print(f"✅ Agregada coma en línea {i+1}")

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Comas faltantes corregidas")

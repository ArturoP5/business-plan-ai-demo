#!/usr/bin/env python3
"""
Arregla los tipos del slider - todos deben ser float para usar step=0.1
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar y arreglar las líneas del slider de costos_variables
for i in range(len(lines)):
    # Línea con min_value=10
    if "min_value=10," in lines[i] and i > 1745 and i < 1755:
        lines[i] = "        min_value=10.0,\n"
        print(f"✅ Línea {i+1}: Cambiado min_value de 10 a 10.0")
    
    # Línea con max_value=98
    if "max_value=98," in lines[i] and i > 1745 and i < 1755:
        lines[i] = "        max_value=98.0,\n"
        print(f"✅ Línea {i+1}: Cambiado max_value de 98 a 98.0")

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Tipos corregidos. Ahora todos son float para compatibilidad con step=0.1")

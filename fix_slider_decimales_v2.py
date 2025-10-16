#!/usr/bin/env python3
"""
Convierte el slider de costos variables para aceptar decimales
Versión corregida con el rango correcto
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

changes = 0

# Buscar en el rango correcto (1756-1763)
for i in range(1755, 1764):
    if i < len(lines):
        # Cambiar min_value=10 a 10.0
        if "min_value=10," in lines[i]:
            lines[i] = lines[i].replace("min_value=10,", "min_value=10.0,")
            print(f"✅ Línea {i+1}: min_value → 10.0")
            changes += 1
        
        # Cambiar max_value=98 a 98.0
        if "max_value=98," in lines[i]:
            lines[i] = lines[i].replace("max_value=98,", "max_value=98.0,")
            print(f"✅ Línea {i+1}: max_value → 98.0")
            changes += 1
        
        # Cambiar step=1 a step=0.1
        if "step=1," in lines[i]:
            lines[i] = lines[i].replace("step=1,", "step=0.1,")
            print(f"✅ Línea {i+1}: step → 0.1")
            changes += 1

if changes == 3:
    with open('app.py', 'w') as f:
        f.writelines(lines)
    print("\n✅ Slider convertido para aceptar decimales (0.1% de precisión)")
else:
    print(f"⚠️ Solo se encontraron {changes} de 3 cambios esperados")

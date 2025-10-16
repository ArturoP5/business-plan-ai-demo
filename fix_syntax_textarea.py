#!/usr/bin/env python3
"""
Arregla el error de sintaxis en productos_servicios text_area
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y arreglar el text_area de productos_servicios (alrededor de línea 1567-1570)
for i in range(1565, 1575):
    if i < len(lines) and '"Productos/Servicios Principales",' in lines[i]:
        # Si hay duplicado, eliminar esta línea
        if i+1 < len(lines) and '"Productos/Servicios Principales",' in lines[i+1]:
            del lines[i+1]
            print(f"✅ Eliminado título duplicado en línea {i+2}")
            break
        # O si la línea anterior ya tiene el título
        if i-1 >= 0 and '"Productos/Servicios Principales",' in lines[i-1]:
            del lines[i]
            print(f"✅ Eliminado título duplicado en línea {i+1}")
            break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Error de sintaxis corregido")

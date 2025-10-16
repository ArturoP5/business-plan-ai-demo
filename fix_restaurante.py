#!/usr/bin/env python3
"""
Agrega campos faltantes al Restaurante La Terraza SL
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar el restaurante
for i in range(len(lines)):
    if "'nombre_empresa': 'Restaurante La Terraza SL'" in lines[i]:
        # Insertar los campos
        indent = '                '
        lines.insert(i+1, f"{indent}'descripcion_actividad': 'Restaurante de alta cocina mediterránea con terraza panorámica. Especializado en productos locales de temporada y carta de vinos premium. Eventos corporativos y celebraciones privadas.',\n")
        lines.insert(i+2, f"{indent}'productos_servicios': 'Menú degustación (80€), carta tradicional renovada, eventos privados, catering premium, escuela de cocina, wine tasting',\n")
        print("✅ Agregados campos a Restaurante La Terraza SL")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

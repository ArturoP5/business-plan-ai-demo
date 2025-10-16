#!/usr/bin/env python3
"""
Arregla la carga de costos_variables desde Excel
Elimina duplicados y carga correctamente el dato
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Primero eliminar las líneas duplicadas (1375-1376)
# y reemplazar con la carga correcta desde Excel

# Encontrar la sección exacta
for i in range(len(lines)):
    if i == 1374 and "default_ventas = datos_excel['pyl_historico']['ventas']" in lines[i]:
        # Reemplazar las dos líneas siguientes (los duplicados) con la carga correcta
        new_line = "        default_costos_var = int(datos_excel['pyl_historico'].get('costos_variables_pct', 40)) if 'costos_variables_pct' in datos_excel['pyl_historico'] else 40\n"
        
        # Reemplazar líneas 1375 y 1376
        lines[1375] = new_line
        del lines[1376]  # Eliminar el duplicado
        
        print("✅ Eliminados duplicados")
        print("✅ Implementada carga desde Excel:")
        print("  - Busca 'costos_variables_pct' en el Excel")
        print("  - Si existe, lo usa (como entero)")
        print("  - Si no existe, usa 40 por defecto")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

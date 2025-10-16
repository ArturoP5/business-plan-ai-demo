#!/usr/bin/env python3
"""
Implementa carga correcta de costos_variables desde Excel
Maneja tanto valor único como lista de valores
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea actual (1375 después de eliminar duplicado)
for i, line in enumerate(lines):
    if i == 1374 and "default_costos_var = 40" in line:
        # Reemplazar con código que maneja Excel correctamente
        new_code = """        # Cargar costos variables del Excel (puede ser valor único o lista)
        if 'costos_variables_pct' in datos_excel['pyl_historico']:
            costos_data = datos_excel['pyl_historico']['costos_variables_pct']
            if isinstance(costos_data, list):
                # Si es lista, tomar el último año (más reciente)
                default_costos_var = float(costos_data[-1]) if costos_data else 40.0
            else:
                # Si es valor único
                default_costos_var = float(costos_data) if costos_data else 40.0
        else:
            default_costos_var = 40.0
"""
        lines[i] = new_code
        print("✅ Implementada carga correcta desde Excel")
        print("  - Si es lista: toma el último año")
        print("  - Si es valor único: lo usa directamente")
        print("  - Siempre convierte a float para decimales")
        break

with open('app.py', 'w') as f:
    f.writelines(lines)

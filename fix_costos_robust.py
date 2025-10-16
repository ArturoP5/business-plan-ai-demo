#!/usr/bin/env python3
"""
Fix robusto para manejar costos_variables como lista o float
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Reemplazar la línea 1375 con una versión más robusta
old_line = lines[1374]
new_line = """        # Manejar costos_variables que puede venir como lista o número único
        costos_var_data = datos_excel["pyl_historico"].get("costos_variables_pct", 40)
        if isinstance(costos_var_data, list):
            # Si es lista, tomar el promedio
            default_costos_var = float(sum(costos_var_data) / len(costos_var_data))
        elif isinstance(costos_var_data, (int, float)) and not pd.isna(costos_var_data):
            default_costos_var = float(costos_var_data)
        else:
            default_costos_var = 40.0
"""

lines[1374] = new_line

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Fix aplicado:")
print("  - Maneja costos como lista (toma promedio)")
print("  - Maneja costos como número único")
print("  - Siempre retorna float para compatibilidad con slider")

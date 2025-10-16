#!/usr/bin/env python3
"""
Permite decimales en el slider de costos variables
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0

# Fix 1: Línea 1375 - No convertir a int cuando viene del Excel
for i, line in enumerate(lines):
    if 'default_costos_var = int(datos_excel["pyl_historico"]["costos_variables_pct"])' in line:
        new_line = line.replace('int(datos_excel["pyl_historico"]["costos_variables_pct"])', 
                               'float(datos_excel["pyl_historico"]["costos_variables_pct"])')
        lines[i] = new_line
        print(f"✅ Línea {i+1}: Cambiado int() a float() para preservar decimales del Excel")
        changes += 1
        break

# Fix 2: Línea ~1750 - Cambiar step de 1 a 0.5
for i, line in enumerate(lines):
    if 'step=1,' in line and 'costos_variables_slider' in line:
        lines[i] = line.replace('step=1,', 'step=0.5,')
        print(f"✅ Línea {i+1}: Cambiado step de 1 a 0.5 para permitir decimales")
        changes += 1
        break

if changes == 2:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"\n✅ Ambos cambios aplicados. Ahora puedes usar 40.5%, 41%, etc.")
else:
    print(f"⚠️ Solo se aplicaron {changes} cambios de 2 esperados")

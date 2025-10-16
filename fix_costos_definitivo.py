#!/usr/bin/env python3
"""
Fix definitivo para costos variables desde Excel
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea exacta donde está default_ventas
for i in range(len(lines)):
    if "default_ventas = datos_excel['pyl_historico']['ventas']" in lines[i]:
        print(f"Encontrada línea de ventas en {i+1}")
        
        # La siguiente línea debería ser costos_var
        # Reemplazar las DOS líneas duplicadas con UNA correcta
        if i+1 < len(lines) and "default_costos_var = 40" in lines[i+1]:
            # Reemplazar con carga desde Excel
            lines[i+1] = "        default_costos_var = int(datos_excel['pyl_historico'].get('costos_variables_pct', 40))\n"
            
            # Si hay duplicado en la siguiente línea, eliminarlo
            if i+2 < len(lines) and "default_costos_var = 40" in lines[i+2]:
                del lines[i+2]
                print("✅ Eliminado duplicado")
            
            print("✅ Implementada carga desde Excel")
            break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\nAhora default_costos_var cargará desde Excel['pyl_historico']['costos_variables_pct']")

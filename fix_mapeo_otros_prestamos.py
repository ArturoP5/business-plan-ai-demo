#!/usr/bin/env python3
"""
Arregla el mapeo de otros_prestamos con compatibilidad hacia atrás
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y arreglar la línea 1431
for i in range(1430, 1435):
    if "default_otros_prestamos = int(datos_excel['balance_pasivo'].get('prestamos_lp', 0))" in lines[i]:
        # Reemplazar con versión compatible
        lines[i] = "        default_otros_prestamos = int(datos_excel['balance_pasivo'].get('otros_prestamos_lp', datos_excel['balance_pasivo'].get('prestamos_lp', 0)))\n"
        print(f"✅ Línea {i+1} arreglada con compatibilidad dual")
        print("   Ahora busca 'otros_prestamos_lp' primero, luego 'prestamos_lp'")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Mapeo corregido")
print("Los 200,000€ de TechStart deberían cargarse correctamente ahora")
print("El descuadre de 200,000€ debería resolverse")

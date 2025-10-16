#!/usr/bin/env python3
"""
Fix para mapear prestamos_lp del Excel a otros_prestamos_lp en el código
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar la línea 1404 y cambiar el mapeo
for i, line in enumerate(lines):
    if "default_otros_prestamos = int(datos_excel['balance_pasivo'].get('otros_prestamos_lp', 0))" in line:
        # Cambiar para que busque 'prestamos_lp' en lugar de 'otros_prestamos_lp'
        new_line = "        default_otros_prestamos = int(datos_excel['balance_pasivo'].get('prestamos_lp', 0))\n"
        lines[i] = new_line
        print(f"✅ Línea {i+1}: Cambiado mapeo de 'otros_prestamos_lp' a 'prestamos_lp'")
        break

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Ahora el código leerá 'prestamos_lp' del Excel (120000 en tu caso)")
